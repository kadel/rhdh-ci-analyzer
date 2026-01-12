#!/usr/bin/env python3
"""
CI Failure Classification: Infrastructure vs Playwright Tests

This script classifies CI failures to determine if they are caused by:
- Infrastructure/Environment issues (tests never started)
- Playwright test failures (tests ran but some failed)

Usage:
    ./classify-failures.py [ci-logs-directory]
    ./classify-failures.py -s <run-directory>  # Single run detailed analysis
    ./classify-failures.py --ai                 # Use AI to analyze infrastructure failures

AI Analysis Requirements:
    pip install google-genai
    export GEMINI_API_KEY="your-api-key"
    
    Uses Google Gen AI SDK: https://googleapis.github.io/python-genai/
"""

import argparse
import gzip
import json
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Tuple, List, Dict

# Prow base URL for job links
PROW_BASE_URL = "https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh"
# GitHub PR base URL
GITHUB_PR_BASE_URL = "https://github.com/redhat-developer/rhdh/pull"


class Color:
    """ANSI color codes for terminal output."""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color


class Classification(Enum):
    """CI run classification types."""
    INFRA_FAILURE = "Infrastructure Failure"
    TEST_FAILURE = "Test Failure"
    TEST_SUCCESS = "Test Success"
    JOB_ABORTED = "Job Aborted"
    UNKNOWN = "Unknown"


@dataclass
class TestCaseFailure:
    """Information about a single test case failure."""
    test_name: str  # Full test name (e.g., "Test timestamp column on Catalog › Import an existing Git...")
    spec_file: str  # e.g., "e2e/catalog-timestamp.spec.ts"
    failure_message: str  # Short failure message
    error_type: str  # e.g., "TimeoutError", "Error"
    pr_number: str = ""
    run_id: str = ""
    suite_type: str = ""  # "showcase" or "showcase-rbac"


@dataclass
class JUnitStats:
    """Statistics from junit-results.xml."""
    tests: int = 0
    failures: int = 0
    skipped: int = 0
    errors: int = 0
    time: float = 0.0
    failed_tests: List[TestCaseFailure] = field(default_factory=list)


class InfraFailureCategory(Enum):
    """Specific infrastructure failure categories."""
    CLONE_FAILURE = "Repository Clone Failure"
    DOCKER_IMAGE_TIMEOUT = "Docker Image Timeout"
    OPERATOR_INSTALL_TIMEOUT = "Operator Install Timeout"
    POD_NOT_READY = "Pod/Deployment Not Ready"
    MISSING_CRD = "Missing CRD"
    HELM_INSTALL_FAILED = "Helm Install Failed"
    CLUSTER_CONNECTIVITY = "Cluster Connectivity"
    RESOURCE_QUOTA_EXCEEDED = "Resource Quota Exceeded"
    SCRIPT_ERROR = "Script Error"
    UNKNOWN = "Unknown Infrastructure Error"


@dataclass
class BuildLogAnalysis:
    """Analysis results from build-log.txt content."""
    playwright_tests_started: bool = False
    test_count: int = 0
    worker_count: int = 0
    has_error: bool = False
    error_message: str = ""
    has_timeout: bool = False
    timeout_message: str = ""
    has_interrupt: bool = False
    interrupt_message: str = ""
    infra_failure_category: Optional[InfraFailureCategory] = None
    infra_failure_detail: str = ""


@dataclass
class AIRootCauseAnalysis:
    """AI-generated root cause analysis for infrastructure failures."""
    root_cause_category: str = ""  # Short category name (e.g., "Operator Installation Timeout")
    root_cause_detail: str = ""    # Detailed explanation
    suggested_fix: str = ""        # Suggested fix or investigation steps
    confidence: str = ""           # high/medium/low
    relevant_log_lines: List[str] = field(default_factory=list)


@dataclass
class JobStatus:
    """Status information from finished.json and prowjob.json."""
    result: str = ""  # e.g., "ABORTED", "SUCCESS", "FAILURE"
    state: str = ""   # e.g., "aborted", "success", "failure" 
    description: str = ""  # e.g., "Aborted by trigger plugin."
    is_aborted: bool = False


@dataclass
class RunAnalysis:
    """Analysis results for a single CI run."""
    pr_number: str
    run_id: str
    run_path: Path
    job_name: str = ""  # e.g., "pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm"
    
    job_status: Optional[JobStatus] = None
    
    has_showcase: bool = False
    has_showcase_rbac: bool = False
    has_junit_showcase: bool = False
    has_junit_rbac: bool = False
    
    webm_count_showcase: int = 0
    webm_count_rbac: int = 0
    png_count_showcase: int = 0
    png_count_rbac: int = 0
    
    junit_showcase: Optional[JUnitStats] = None
    junit_rbac: Optional[JUnitStats] = None
    
    overall_result: Optional[int] = None
    build_log_path: Optional[Path] = None
    build_log_analysis: Optional[BuildLogAnalysis] = None
    build_log_content: Optional[str] = None  # Store for AI analysis
    ai_analysis: Optional[AIRootCauseAnalysis] = None
    
    classification: Classification = Classification.UNKNOWN
    reason: str = ""
    
    def get_prow_url(self) -> str:
        """Generate Prow URL for this run."""
        return f"{PROW_BASE_URL}/{self.pr_number}/{self.job_name}/{self.run_id}"

    def get_github_pr_url(self) -> str:
        """Generate GitHub PR URL."""
        return f"{GITHUB_PR_BASE_URL}/{self.pr_number}"


@dataclass
class Summary:
    """Summary statistics for all analyzed runs."""
    total: int = 0
    infra_failures: int = 0
    test_failures: int = 0
    test_successes: int = 0
    job_aborted: int = 0
    unknown: int = 0
    infra_failure_runs: list = field(default_factory=list)
    test_failure_runs: list = field(default_factory=list)
    aborted_runs: list = field(default_factory=list)
    all_test_failures: List[TestCaseFailure] = field(default_factory=list)  # All individual test failures
    analyzed_prs: set = field(default_factory=set)  # Unique PR numbers analyzed


# Gzip magic bytes
GZIP_MAGIC = b"\x1f\x8b"


def is_gzipped(filepath: Path) -> bool:
    """Check if a file is gzip compressed by reading magic bytes."""
    try:
        with open(filepath, "rb") as f:
            magic = f.read(2)
            return magic == GZIP_MAGIC
    except (IOError, OSError):
        return False


def read_file_text(filepath: Path) -> Optional[str]:
    """Read a text file, automatically detecting and handling gzip compression."""
    if not filepath.exists():
        return None

    try:
        if is_gzipped(filepath):
            with gzip.open(filepath, "rt", encoding="utf-8", errors="replace") as f:
                return f.read()
        else:
            return filepath.read_text(encoding="utf-8", errors="replace")
    except (IOError, OSError):
        return None


def read_file_bytes(filepath: Path) -> Optional[bytes]:
    """Read a file as bytes, automatically detecting and handling gzip compression."""
    if not filepath.exists():
        return None

    try:
        if is_gzipped(filepath):
            with gzip.open(filepath, "rb") as f:
                return f.read()
        else:
            return filepath.read_bytes()
    except (IOError, OSError):
        return None


def count_files(directory: Path, extension: str) -> int:
    """Count files with a specific extension in a directory tree."""
    if not directory.exists():
        return 0
    return len(list(directory.rglob(f"*{extension}")))


def parse_junit(junit_path: Path, pr_number: str = "", run_id: str = "", suite_type: str = "") -> Optional[JUnitStats]:
    """Parse junit-results.xml and extract statistics including individual failures."""
    if not junit_path.exists():
        return None

    try:
        # Read file content (handles gzip automatically)
        content = read_file_text(junit_path)
        if not content:
            return None
        root = ET.fromstring(content)

        stats = JUnitStats(
            tests=int(root.get('tests', 0)),
            failures=int(root.get('failures', 0)),
            skipped=int(root.get('skipped', 0)),
            errors=int(root.get('errors', 0)),
            time=float(root.get('time', 0.0))
        )

        # Extract individual test case failures
        for testsuite in root.findall('.//testsuite'):
            spec_file = testsuite.get('name', 'unknown')

            for testcase in testsuite.findall('testcase'):
                failure = testcase.find('failure')
                if failure is not None:
                    test_name = testcase.get('name', 'unknown')
                    failure_message = failure.get('message', '')

                    # Extract error type from failure text
                    failure_text = failure.text or ""
                    error_type = "Unknown"
                    if "TimeoutError" in failure_text or "Timeout" in failure_message:
                        error_type = "TimeoutError"
                    elif "Error:" in failure_text:
                        error_match = re.search(r'(Error|AssertionError|TypeError|ReferenceError):', failure_text)
                        if error_match:
                            error_type = error_match.group(1)
                    elif "expect(" in failure_text:
                        error_type = "AssertionError"

                    stats.failed_tests.append(TestCaseFailure(
                        test_name=test_name,
                        spec_file=spec_file,
                        failure_message=failure_message[:200] if failure_message else "",
                        error_type=error_type,
                        pr_number=pr_number,
                        run_id=run_id,
                        suite_type=suite_type
                    ))

        return stats
    except (ET.ParseError, ValueError):
        return None


def read_overall_result(result_path: Path) -> Optional[int]:
    """Read OVERALL_RESULT.txt and return the status code."""
    content = read_file_text(result_path)
    if not content:
        return None

    try:
        return int(content.strip())
    except ValueError:
        return None


def read_build_log(log_path: Path) -> Optional[str]:
    """Read build log content, handling gzip compression if needed."""
    return read_file_text(log_path)


def read_json_file(json_path: Path) -> Optional[dict]:
    """Read a JSON file, handling gzip compression if needed."""
    content = read_file_text(json_path)
    if not content:
        return None

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return None


def get_job_status(run_path: Path) -> JobStatus:
    """Extract job status from finished.json and prowjob.json."""
    status = JobStatus()
    
    # Check finished.json (primary source for result)
    finished_json_path = run_path / "finished.json"
    finished_data = read_json_file(finished_json_path)
    if finished_data:
        status.result = finished_data.get("result", "").upper()
    
    # Check prowjob.json (has more detailed state info)
    prowjob_json_path = run_path / "prowjob.json"
    prowjob_data = read_json_file(prowjob_json_path)
    if prowjob_data:
        prow_status = prowjob_data.get("status", {})
        status.state = prow_status.get("state", "")
        status.description = prow_status.get("description", "")
    
    # Determine if job was aborted
    status.is_aborted = (
        status.result == "ABORTED" or
        status.state == "aborted" or
        "abort" in status.description.lower()
    )
    
    return status


def init_gemini_client():
    """Initialize the Google Gen AI client for Gemini."""
    try:
        from google import genai
    except ImportError:
        print(f"{Color.RED}Error: google-genai package not installed.{Color.NC}")
        print(f"Install it with: pip install google-genai")
        sys.exit(1)
    
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print(f"{Color.RED}Error: GEMINI_API_KEY or GOOGLE_API_KEY environment variable not set.{Color.NC}")
        sys.exit(1)
    
    # Create client using the new google-genai library
    # See: https://googleapis.github.io/python-genai/
    return genai.Client(api_key=api_key)


def analyze_with_ai(client, build_log_content: str) -> AIRootCauseAnalysis:
    """Use Gemini AI to analyze a build log and determine root cause.
    
    Uses the google-genai library: https://googleapis.github.io/python-genai/
    """
    # Truncate log if too long (keep start and end)
    max_chars = 30000
    if len(build_log_content) > max_chars:
        # Keep first 5000 chars (setup/clone) and last 25000 chars (error/timeout)
        head_chars = 5000
        tail_chars = 25000
        build_log_content = build_log_content[:head_chars] + "\n... [middle truncated] ...\n" + build_log_content[-tail_chars:]
    
    prompt = f"""You are an expert SRE analyzing CI build logs for Red Hat Developer Hub (RHDH) on OpenShift.
The Playwright E2E tests never started, indicating an infrastructure or environment setup failure.

Your goal is to identify the precise ROOT CAUSE.

Key Failure Categories to consider (but be specific):
- ImagePullBackOff / Docker Image Timeout (RHDH or CLI images)
- Operator Installation Timeout (e.g. CrunchyDB, Prometheus)
- PVC/Storage Provisioning Failed
- Cluster Connectivity / Network Issues
- Resource Quota Exceeded (CPU/Memory)
- Helm Chart Installation Failed
- Missing CRDs (Custom Resource Definitions)
- Script/Setup Logic Errors
- Git Clone/Fetch Failures

Analyze the log, find the specific error lines, and determine the root cause.

Respond in this exact JSON format (no markdown):
{{
  "root_cause_category": "<short, specific category, e.g., 'CrunchyDB Operator Timeout'>",
  "root_cause_detail": "<concise explanation of the failure context>",
  "relevant_log_lines": ["<exact log line 1>", "<exact log line 2>"],
  "suggested_fix": "<actionable remediation step>",
  "confidence": "<high|medium|low>"
}}

BUILD LOG (truncated):
{build_log_content}
"""
    
    try:
        # Use the new google-genai client API
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        text = response.text.strip()
        
        # Remove markdown code blocks if present
        if text.startswith("```"):
            text = re.sub(r'^```(?:json)?\n?', '', text)
            text = re.sub(r'\n?```$', '', text)
        
        data = json.loads(text)
        return AIRootCauseAnalysis(
            root_cause_category=data.get("root_cause_category", "Unknown"),
            root_cause_detail=data.get("root_cause_detail", ""),
            suggested_fix=data.get("suggested_fix", ""),
            confidence=data.get("confidence", "low"),
            relevant_log_lines=data.get("relevant_log_lines", [])
        )
    except Exception as e:
        return AIRootCauseAnalysis(
            root_cause_category="AI Analysis Failed",
            root_cause_detail=str(e)[:100],
            confidence="low"
        )


def analyze_build_log(log_content: str) -> BuildLogAnalysis:
    """Analyze build log content and extract classification indicators."""
    analysis = BuildLogAnalysis()
    
    # Check for Playwright test execution
    # Pattern: "Running X tests using Y workers"
    running_match = re.search(r'Running (\d+) tests? using (\d+) workers?', log_content)
    if running_match:
        analysis.playwright_tests_started = True
        analysis.test_count = int(running_match.group(1))
        analysis.worker_count = int(running_match.group(2))
    
    # Check for timeout errors (infrastructure failure indicators)
    timeout_patterns = [
        r'Timed out (?:after \d+ seconds\. )?(?:waiting for [^.]+|[^.]+)',
        r'Error: Timed out waiting for [^.]+',
        r'timeout: \d+[ms]* exceeded',
    ]
    for pattern in timeout_patterns:
        timeout_match = re.search(pattern, log_content, re.IGNORECASE)
        if timeout_match:
            analysis.has_timeout = True
            analysis.timeout_message = timeout_match.group(0)[:100]  # Truncate
            break
    
    # Check for error indicators
    error_patterns = [
        r'❌ Exited with an error',
        r'Error: [A-Z][^.\n]{10,100}',  # Error followed by meaningful message
        r'FATAL: [^\n]+',
        r'error: cannot [^\n]+',
    ]
    for pattern in error_patterns:
        error_match = re.search(pattern, log_content)
        if error_match:
            analysis.has_error = True
            analysis.error_message = error_match.group(0)[:100]  # Truncate
            break
    
    # Check for interrupt/abort signals (job was manually cancelled)
    interrupt_patterns = [
        r'Entrypoint received interrupt: terminated',
        r'Received signal\.[^\n]*interrupt',
        r'"msg":\s*"Received signal\."[^}]*"signal":\s*2',  # SIGINT in JSON logs
        r'Process did not exit before \d+s grace period',
        r'context canceled',
        r'context deadline exceeded',
    ]
    for pattern in interrupt_patterns:
        interrupt_match = re.search(pattern, log_content, re.IGNORECASE)
        if interrupt_match:
            analysis.has_interrupt = True
            analysis.interrupt_message = interrupt_match.group(0)[:100]
            break
    
    # Detect specific infrastructure failure categories (if tests didn't start)
    if not analysis.playwright_tests_started:
        _detect_infra_failure_category(analysis, log_content)
    
    return analysis


def _detect_infra_failure_category(analysis: BuildLogAnalysis, log_content: str) -> None:
    """Detect specific infrastructure failure category from build log.

    Categories based on OpenShift CI artifacts documentation:
    https://docs.ci.openshift.org/docs/how-tos/artifacts/
    """

    # 1. Repository Clone Failure (check clone-log.txt indicators in build log)
    clone_failure_patterns = [
        r'failed to clone[^\n]*',
        r'error: RPC failed[^\n]*',
        r'fatal: could not read from remote repository[^\n]*',
        r'Cloning into .* failed[^\n]*',
        r'clonerefs.*error[^\n]*',
        r'failed to fetch[^\n]*repository[^\n]*',
    ]
    for pattern in clone_failure_patterns:
        if match := re.search(pattern, log_content, re.IGNORECASE):
            analysis.infra_failure_category = InfraFailureCategory.CLONE_FAILURE
            analysis.infra_failure_detail = match.group(0)[:80]
            return

    # 2. Docker Image Timeout - most common
    if match := re.search(r'Timed out waiting for Docker image ([^\s.]+)', log_content):
        analysis.infra_failure_category = InfraFailureCategory.DOCKER_IMAGE_TIMEOUT
        analysis.infra_failure_detail = f"Image: {match.group(1)}"
        return

    # 3. Operator Installation Timeout
    if match := re.search(r"Operator '([^']+)' did not reach '([^']+)'", log_content):
        analysis.infra_failure_category = InfraFailureCategory.OPERATOR_INSTALL_TIMEOUT
        analysis.infra_failure_detail = f"{match.group(1)} (expected: {match.group(2)})"
        return
    
    # 3. Pod/Deployment Not Ready
    if match := re.search(r"(Pod|Deployment) '([^']+)' is not ready", log_content, re.IGNORECASE):
        analysis.infra_failure_category = InfraFailureCategory.POD_NOT_READY
        analysis.infra_failure_detail = f"{match.group(1)}: {match.group(2)}"
        return
    
    # Also check for pod timeout patterns
    if match := re.search(r'(pod|deployment)[^\n]*(not ready|timeout|timed out)[^\n]*', log_content, re.IGNORECASE):
        analysis.infra_failure_category = InfraFailureCategory.POD_NOT_READY
        analysis.infra_failure_detail = match.group(0)[:80]
        return
    
    # 4. Missing CRD
    if match := re.search(r'resource mapping not found.*no matches for kind "([^"]+)"', log_content, re.DOTALL):
        analysis.infra_failure_category = InfraFailureCategory.MISSING_CRD
        analysis.infra_failure_detail = f"Kind: {match.group(1)}"
        return
    
    if match := re.search(r'ensure CRDs are installed first', log_content):
        analysis.infra_failure_category = InfraFailureCategory.MISSING_CRD
        # Try to find which CRD
        if crd_match := re.search(r'no matches for kind "([^"]+)"', log_content):
            analysis.infra_failure_detail = f"Kind: {crd_match.group(1)}"
        return
    
    # 5. Helm Install Failed
    if match := re.search(r'Error: (INSTALLATION FAILED|UPGRADE FAILED)[^\n]*', log_content):
        analysis.infra_failure_category = InfraFailureCategory.HELM_INSTALL_FAILED
        analysis.infra_failure_detail = match.group(0)[:80]
        return
    
    # 6. Cluster Connectivity Issues
    connectivity_patterns = [
        r'Unable to connect to the server[^\n]*',
        r'connection refused[^\n]*',
        r'no route to host[^\n]*',
        r'dial tcp[^\n]*connection refused',
        r'i/o timeout[^\n]*',
    ]
    for pattern in connectivity_patterns:
        if match := re.search(pattern, log_content, re.IGNORECASE):
            analysis.infra_failure_category = InfraFailureCategory.CLUSTER_CONNECTIVITY
            analysis.infra_failure_detail = match.group(0)[:80]
            return

    # 7. Resource Quota Exceeded (from pods.json/events.json indicators in build log)
    quota_patterns = [
        r'exceeded quota[^\n]*',
        r'forbidden: exceeded[^\n]*',
        r'resource quota[^\n]*exceeded[^\n]*',
        r'insufficient[^\n]*(cpu|memory|quota)[^\n]*',
        r'FailedScheduling[^\n]*Insufficient[^\n]*',
    ]
    for pattern in quota_patterns:
        if match := re.search(pattern, log_content, re.IGNORECASE):
            analysis.infra_failure_category = InfraFailureCategory.RESOURCE_QUOTA_EXCEEDED
            analysis.infra_failure_detail = match.group(0)[:80]
            return

    # 8. Script Error (generic ❌)
    if match := re.search(r'❌ ([^\n]+)', log_content):
        analysis.infra_failure_category = InfraFailureCategory.SCRIPT_ERROR
        analysis.infra_failure_detail = match.group(1)[:80]
        return
    
    # If we have a timeout or error but couldn't categorize specifically
    if analysis.has_timeout or analysis.has_error:
        analysis.infra_failure_category = InfraFailureCategory.UNKNOWN
        analysis.infra_failure_detail = analysis.timeout_message or analysis.error_message


def analyze_run(run_path: Path, pr_number: str, run_id: str, job_name: str = "", ai_client=None) -> RunAnalysis:
    """Analyze a single CI run and classify it."""
    analysis = RunAnalysis(
        pr_number=pr_number,
        run_id=run_id,
        run_path=run_path,
        job_name=job_name
    )
    
    # Get job status from finished.json and prowjob.json
    analysis.job_status = get_job_status(run_path)
    
    # Define artifact paths
    artifacts_base = run_path / "artifacts" / "e2e-ocp-helm" / "redhat-developer-rhdh-ocp-helm" / "artifacts"
    showcase_dir = artifacts_base / "showcase"
    showcase_rbac_dir = artifacts_base / "showcase-rbac"
    
    # Check showcase directories
    analysis.has_showcase = showcase_dir.exists()
    analysis.has_showcase_rbac = showcase_rbac_dir.exists()
    
    # Check junit results
    junit_showcase_path = showcase_dir / "junit-results.xml"
    junit_rbac_path = showcase_rbac_dir / "junit-results.xml"
    
    analysis.has_junit_showcase = junit_showcase_path.exists()
    analysis.has_junit_rbac = junit_rbac_path.exists()

    # Parse junit files with context for failure tracking
    analysis.junit_showcase = parse_junit(junit_showcase_path, pr_number, run_id, "showcase")
    analysis.junit_rbac = parse_junit(junit_rbac_path, pr_number, run_id, "showcase-rbac")
    
    # Count artifacts
    if analysis.has_showcase:
        analysis.webm_count_showcase = count_files(showcase_dir, ".webm")
        analysis.png_count_showcase = count_files(showcase_dir, ".png")
    
    if analysis.has_showcase_rbac:
        analysis.webm_count_rbac = count_files(showcase_rbac_dir, ".webm")
        analysis.png_count_rbac = count_files(showcase_rbac_dir, ".png")
    
    # Read overall result
    overall_result_path = artifacts_base / "reporting" / "OVERALL_RESULT.txt"
    analysis.overall_result = read_overall_result(overall_result_path)
    
    # Find build log path (check multiple locations)
    build_log_candidates = [
        run_path / "artifacts" / "e2e-ocp-helm" / "redhat-developer-rhdh-ocp-helm" / "build-log.txt",
        run_path / "build-log.txt",
    ]
    for log_path in build_log_candidates:
        if log_path.exists():
            analysis.build_log_path = log_path
            break
    
    # Analyze build log content
    if analysis.build_log_path:
        log_content = read_build_log(analysis.build_log_path)
        if log_content:
            analysis.build_log_content = log_content  # Store for AI analysis
            analysis.build_log_analysis = analyze_build_log(log_content)
    
    # Classify based on job status, build log content, and artifacts
    log_analysis = analysis.build_log_analysis
    job_status = analysis.job_status
    
    # Check for aborted job first (highest priority - job was manually cancelled)
    if job_status and job_status.is_aborted:
        analysis.classification = Classification.JOB_ABORTED
        if job_status.description:
            analysis.reason = f"Job aborted: {job_status.description}"
        else:
            analysis.reason = f"Job aborted (result={job_status.result}, state={job_status.state})"
        return analysis
    
    # Check for interrupt signals in build log (may not have prowjob.json)
    if log_analysis and log_analysis.has_interrupt and not log_analysis.playwright_tests_started:
        analysis.classification = Classification.JOB_ABORTED
        analysis.reason = f"Job interrupted: {log_analysis.interrupt_message}"
        return analysis
    
    if log_analysis and log_analysis.playwright_tests_started:
        # Playwright tests were started
        if analysis.overall_result == 0:
            analysis.classification = Classification.TEST_SUCCESS
            analysis.reason = f"Playwright tests ran and passed ({log_analysis.test_count} tests, {log_analysis.worker_count} workers)"
        else:
            analysis.classification = Classification.TEST_FAILURE
            analysis.reason = f"Playwright tests ran but some failed ({log_analysis.test_count} tests, {log_analysis.worker_count} workers)"
    elif log_analysis and (log_analysis.has_timeout or log_analysis.has_error or log_analysis.infra_failure_category):
        # Error or timeout before tests started
        analysis.classification = Classification.INFRA_FAILURE
        if ai_client and analysis.build_log_content:
            # Use AI to analyze the infrastructure failure
            ai_result = analyze_with_ai(ai_client, analysis.build_log_content)
            analysis.ai_analysis = ai_result
            analysis.reason = f"{ai_result.root_cause_category}: {ai_result.root_cause_detail}" if ai_result.root_cause_detail else ai_result.root_cause_category
        elif log_analysis.infra_failure_category:
            cat = log_analysis.infra_failure_category.value
            detail = log_analysis.infra_failure_detail
            analysis.reason = f"{cat}: {detail}" if detail else cat
        elif log_analysis.has_timeout:
            analysis.reason = f"Setup timeout: {log_analysis.timeout_message}"
        else:
            analysis.reason = f"Setup error: {log_analysis.error_message}"
    elif log_analysis:
        # Build log exists but no clear indicators - likely infra failure
        analysis.classification = Classification.INFRA_FAILURE
        if ai_client and analysis.build_log_content:
            # Use AI to analyze the infrastructure failure
            ai_result = analyze_with_ai(ai_client, analysis.build_log_content)
            analysis.ai_analysis = ai_result
            analysis.reason = f"{ai_result.root_cause_category}: {ai_result.root_cause_detail}" if ai_result.root_cause_detail else ai_result.root_cause_category
        else:
            analysis.reason = "Tests never started - check build log for details"
    else:
        # No build log - use artifact-based classification as fallback
        total_webm = analysis.webm_count_showcase + analysis.webm_count_rbac
        has_test_artifacts = analysis.has_showcase or analysis.has_showcase_rbac
        has_junit = analysis.has_junit_showcase or analysis.has_junit_rbac
        
        if has_test_artifacts and has_junit:
            if analysis.overall_result == 0:
                analysis.classification = Classification.TEST_SUCCESS
                analysis.reason = f"Playwright tests ran and passed (webm: {total_webm})"
            else:
                analysis.classification = Classification.TEST_FAILURE
                analysis.reason = f"Playwright tests ran but some failed (webm: {total_webm})"
        elif total_webm > 0:
            analysis.classification = Classification.TEST_FAILURE
            analysis.reason = f"Playwright tests partially ran (webm: {total_webm})"
        else:
            analysis.classification = Classification.INFRA_FAILURE
            analysis.reason = "No build log or Playwright artifacts found"
    
    return analysis


def print_header():
    """Print the script header."""
    print(f"{Color.BOLD}╔══════════════════════════════════════════════════════════════════╗{Color.NC}")
    print(f"{Color.BOLD}║       CI Failure Classification: Infrastructure vs Tests         ║{Color.NC}")
    print(f"{Color.BOLD}╚══════════════════════════════════════════════════════════════════╝{Color.NC}")
    print()


def print_run_result(analysis: RunAnalysis):
    """Print the classification result for a single run."""
    short_run = analysis.run_id
    pr_label = f"PR #{analysis.pr_number}"
    
    if analysis.classification == Classification.INFRA_FAILURE:
        icon = f"{Color.RED}✗{Color.NC}"
        label = f"{Color.RED}INFRASTRUCTURE{Color.NC}"
    elif analysis.classification == Classification.TEST_FAILURE:
        icon = f"{Color.YELLOW}⚠{Color.NC}"
        label = f"{Color.YELLOW}TEST FAILURE{Color.NC}"
    elif analysis.classification == Classification.TEST_SUCCESS:
        icon = f"{Color.GREEN}✓{Color.NC}"
        label = f"{Color.GREEN}TEST SUCCESS{Color.NC}"
    elif analysis.classification == Classification.JOB_ABORTED:
        icon = f"{Color.CYAN}⊘{Color.NC}"
        label = f"{Color.CYAN}ABORTED{Color.NC}"
    else:
        icon = f"{Color.BLUE}?{Color.NC}"
        label = f"{Color.BLUE}UNKNOWN{Color.NC}"
    
    print(f"  {icon} {pr_label} [{short_run}]: {label} - {analysis.reason}")
    
    # Show build log path for infrastructure failures
    if analysis.classification == Classification.INFRA_FAILURE and analysis.build_log_path:
        print(f"      {Color.CYAN}→ Build log: {analysis.build_log_path}{Color.NC}")


def print_summary(summary: Summary, ai_analyze: bool = False):
    """Print the summary statistics."""
    print()
    print(f"{Color.BOLD}════════════════════════════════════════════════════════════════════{Color.NC}")
    print(f"{Color.BOLD}Summary{Color.NC}")
    print(f"{Color.BOLD}════════════════════════════════════════════════════════════════════{Color.NC}")
    print()
    print(f"PRs analyzed: {Color.BOLD}{len(summary.analyzed_prs)}{Color.NC} | Total CI runs: {Color.BOLD}{summary.total}{Color.NC}")
    print()

    infra_pct = (summary.infra_failures * 100 // summary.total) if summary.total > 0 else 0
    test_fail_pct = (summary.test_failures * 100 // summary.total) if summary.total > 0 else 0
    test_succ_pct = (summary.test_successes * 100 // summary.total) if summary.total > 0 else 0
    aborted_pct = (summary.job_aborted * 100 // summary.total) if summary.total > 0 else 0

    print(f"  {Color.RED}■{Color.NC} Infrastructure failures: {Color.BOLD}{summary.infra_failures}{Color.NC} ({infra_pct}%)")
    print(f"  {Color.YELLOW}■{Color.NC} Test failures:          {Color.BOLD}{summary.test_failures}{Color.NC} ({test_fail_pct}%)")
    print(f"  {Color.GREEN}■{Color.NC} Test successes:         {Color.BOLD}{summary.test_successes}{Color.NC} ({test_succ_pct}%)")
    print(f"  {Color.CYAN}■{Color.NC} Jobs aborted:           {Color.BOLD}{summary.job_aborted}{Color.NC} ({aborted_pct}%)")

    if summary.unknown > 0:
        print(f"  {Color.BLUE}■{Color.NC} Unknown:                {Color.BOLD}{summary.unknown}{Color.NC}")

    print()

    # Show aborted jobs detail
    if summary.aborted_runs:
        print(f"{Color.BOLD}Aborted Jobs:{Color.NC}")
        for analysis in summary.aborted_runs:
            print(f"  PR #{analysis.pr_number} [{analysis.run_id}]: {analysis.reason}")
        print()

    # Show infrastructure failures grouped by category
    if summary.infra_failure_runs:
        if ai_analyze:
            print(f"{Color.BOLD}Infrastructure Failures by Root Cause (AI Analysis):{Color.NC}")
        else:
            print(f"{Color.BOLD}Infrastructure Failures by Category:{Color.NC}")

        # Group by category (use AI category if available, otherwise regex category)
        by_category: Dict[str, list] = defaultdict(list)
        for analysis in summary.infra_failure_runs:
            if ai_analyze and analysis.ai_analysis:
                cat = analysis.ai_analysis.root_cause_category
            elif analysis.build_log_analysis and analysis.build_log_analysis.infra_failure_category:
                cat = analysis.build_log_analysis.infra_failure_category.value
            else:
                cat = "Unknown"
            by_category[cat].append(analysis)

        # Print by category (sorted by count)
        for cat, runs in sorted(by_category.items(), key=lambda x: -len(x[1])):
            # Show confidence for AI analysis
            confidence_str = ""
            if ai_analyze and runs and runs[0].ai_analysis and runs[0].ai_analysis.confidence:
                confidence_str = f" [{runs[0].ai_analysis.confidence}]"
            print(f"\n  {Color.YELLOW}{cat}{Color.NC}{confidence_str} ({len(runs)} failures):")
            for analysis in runs[:5]:  # Show max 5 per category
                detail = ""
                if ai_analyze and analysis.ai_analysis and analysis.ai_analysis.root_cause_detail:
                    detail = f" - {analysis.ai_analysis.root_cause_detail[:60]}"
                elif analysis.build_log_analysis and analysis.build_log_analysis.infra_failure_detail:
                    detail = f" - {analysis.build_log_analysis.infra_failure_detail[:60]}"
                print(f"    PR #{analysis.pr_number}{detail}")
            if len(runs) > 5:
                print(f"    ... and {len(runs) - 5} more")
        print()

    # Show most common Playwright test failures
    if summary.all_test_failures:
        print_test_failure_summary(summary.all_test_failures)


def print_test_failure_summary(failures: List[TestCaseFailure]):
    """Print summary of most common Playwright test failures."""
    print(f"{Color.BOLD}════════════════════════════════════════════════════════════════════{Color.NC}")
    print(f"{Color.BOLD}Most Common Playwright Test Failures{Color.NC}")
    print(f"{Color.BOLD}════════════════════════════════════════════════════════════════════{Color.NC}")
    print()

    total_failures = len(failures)
    print(f"Total test case failures: {Color.BOLD}{total_failures}{Color.NC}")
    print()

    # Group failures by test name
    by_test_name: Dict[str, List[TestCaseFailure]] = defaultdict(list)
    for f in failures:
        by_test_name[f.test_name].append(f)

    # Sort by frequency (most common first)
    sorted_tests = sorted(by_test_name.items(), key=lambda x: -len(x[1]))

    # Print top 15 most common failures
    print(f"{Color.BOLD}Top Failing Test Cases:{Color.NC}")
    print(f"{'Rank':<5} {'Count':<7} {'Test Name':<70}")
    print("-" * 85)

    for rank, (test_name, test_failures) in enumerate(sorted_tests[:15], 1):
        count = len(test_failures)
        # Truncate long test names
        display_name = test_name[:67] + "..." if len(test_name) > 70 else test_name
        print(f"{rank:<5} {count:<7} {display_name}")

    if len(sorted_tests) > 15:
        print(f"      ... and {len(sorted_tests) - 15} more unique failing tests")

    print()

    # Group by spec file
    by_spec: Dict[str, List[TestCaseFailure]] = defaultdict(list)
    for f in failures:
        by_spec[f.spec_file].append(f)

    sorted_specs = sorted(by_spec.items(), key=lambda x: -len(x[1]))

    print(f"{Color.BOLD}Most Problematic Spec Files:{Color.NC}")
    print(f"{'Rank':<5} {'Count':<7} {'Spec File':<60}")
    print("-" * 75)

    for rank, (spec_file, spec_failures) in enumerate(sorted_specs[:10], 1):
        count = len(spec_failures)
        display_file = spec_file[:57] + "..." if len(spec_file) > 60 else spec_file
        print(f"{rank:<5} {count:<7} {display_file}")

    print()

    # Group by error type
    by_error_type: Dict[str, int] = defaultdict(int)
    for f in failures:
        by_error_type[f.error_type] += 1

    sorted_errors = sorted(by_error_type.items(), key=lambda x: -x[1])

    print(f"{Color.BOLD}Failures by Error Type:{Color.NC}")
    for error_type, count in sorted_errors:
        pct = count * 100 // total_failures if total_failures > 0 else 0
        print(f"  {Color.YELLOW}{error_type}{Color.NC}: {count} ({pct}%)")

    print()


def analyze_single_run_detailed(run_path: Path):
    """Analyze a single run and print detailed information."""
    print(f"{Color.CYAN}Analyzing single run: {run_path}{Color.NC}")
    print()
    
    # Create a dummy analysis to get paths
    analysis = analyze_run(run_path, "N/A", "N/A")
    
    artifacts_base = run_path / "artifacts" / "e2e-ocp-helm" / "redhat-developer-rhdh-ocp-helm" / "artifacts"
    showcase_dir = artifacts_base / "showcase"
    showcase_rbac_dir = artifacts_base / "showcase-rbac"
    
    print(f"{Color.BOLD}Checking indicators:{Color.NC}")
    
    # Check showcase directory
    if analysis.has_showcase:
        print(f"  {Color.GREEN}✓{Color.NC} showcase/ directory exists")
        print(f"    → {analysis.webm_count_showcase} video recordings (.webm)")
        print(f"    → {analysis.png_count_showcase} screenshots (.png)")
    else:
        print(f"  {Color.RED}✗{Color.NC} showcase/ directory NOT found")
    
    # Check showcase-rbac directory
    if analysis.has_showcase_rbac:
        print(f"  {Color.GREEN}✓{Color.NC} showcase-rbac/ directory exists")
        print(f"    → {analysis.webm_count_rbac} video recordings (.webm)")
        print(f"    → {analysis.png_count_rbac} screenshots (.png)")
    else:
        print(f"  {Color.RED}✗{Color.NC} showcase-rbac/ directory NOT found")
    
    # Check junit results - showcase
    if analysis.junit_showcase:
        print(f"  {Color.GREEN}✓{Color.NC} junit-results.xml exists (showcase)")
        stats = analysis.junit_showcase
        print(f"    → Tests: {stats.tests}, Failures: {stats.failures}, Skipped: {stats.skipped}")
    else:
        print(f"  {Color.RED}✗{Color.NC} junit-results.xml NOT found (showcase)")
    
    # Check junit results - rbac
    if analysis.junit_rbac:
        print(f"  {Color.GREEN}✓{Color.NC} junit-results.xml exists (showcase-rbac)")
        stats = analysis.junit_rbac
        print(f"    → Tests: {stats.tests}, Failures: {stats.failures}, Skipped: {stats.skipped}")
    else:
        print(f"  {Color.RED}✗{Color.NC} junit-results.xml NOT found (showcase-rbac)")
    
    # Check overall result
    if analysis.overall_result is not None:
        if analysis.overall_result == 0:
            print(f"  {Color.GREEN}✓{Color.NC} OVERALL_RESULT: SUCCESS (0)")
        else:
            print(f"  {Color.RED}✗{Color.NC} OVERALL_RESULT: FAILURE ({analysis.overall_result})")
    else:
        print(f"  {Color.BLUE}?{Color.NC} OVERALL_RESULT.txt NOT found")
    
    # Check job status (from finished.json / prowjob.json)
    if analysis.job_status:
        status = analysis.job_status
        if status.is_aborted:
            print(f"  {Color.CYAN}⊘{Color.NC} JOB STATUS: ABORTED")
            if status.result:
                print(f"    → result: {status.result}")
            if status.state:
                print(f"    → state: {status.state}")
            if status.description:
                print(f"    → description: {status.description}")
        else:
            print(f"  {Color.GREEN}✓{Color.NC} JOB STATUS: result={status.result}, state={status.state}")
    else:
        print(f"  {Color.BLUE}?{Color.NC} Job status files NOT found")
    
    # Check build log analysis
    print()
    print(f"{Color.BOLD}Build Log Analysis:{Color.NC}")
    if analysis.build_log_path:
        print(f"  {Color.GREEN}✓{Color.NC} Build log found: {analysis.build_log_path}")
        if analysis.build_log_analysis:
            log_analysis = analysis.build_log_analysis
            if log_analysis.playwright_tests_started:
                print(f"  {Color.GREEN}✓{Color.NC} Playwright tests started: {log_analysis.test_count} tests using {log_analysis.worker_count} workers")
            else:
                print(f"  {Color.RED}✗{Color.NC} Playwright tests NOT started")
            
            if log_analysis.has_timeout:
                print(f"  {Color.RED}✗{Color.NC} Timeout detected: {log_analysis.timeout_message}")
            
            if log_analysis.has_error:
                print(f"  {Color.RED}✗{Color.NC} Error detected: {log_analysis.error_message}")
            
            if log_analysis.has_interrupt:
                print(f"  {Color.CYAN}⊘{Color.NC} Interrupt detected: {log_analysis.interrupt_message}")
            
            if log_analysis.infra_failure_category:
                cat = log_analysis.infra_failure_category.value
                print(f"  {Color.RED}✗{Color.NC} Infrastructure failure: {Color.YELLOW}{cat}{Color.NC}")
                if log_analysis.infra_failure_detail:
                    print(f"    → {log_analysis.infra_failure_detail}")
        else:
            print(f"  {Color.YELLOW}⚠{Color.NC} Could not parse build log")
    else:
        print(f"  {Color.RED}✗{Color.NC} Build log NOT found")
    
    print()
    print(f"{Color.BOLD}Classification:{Color.NC}")
    
    if analysis.classification == Classification.JOB_ABORTED:
        print(f"  {Color.CYAN}→ JOB WAS ABORTED/CANCELLED{Color.NC}")
        print(f"    The job was {Color.CYAN}manually interrupted{Color.NC} before completion")
        print(f"    Common causes: new commit pushed, manual /cancel, PR closed/updated")
        print(f"    {Color.BOLD}Reason:{Color.NC} {analysis.reason}")
    elif analysis.classification in (Classification.TEST_SUCCESS, Classification.TEST_FAILURE):
        print(f"  {Color.GREEN}→ PLAYWRIGHT TESTS EXECUTED{Color.NC}")
        print(f"    The failure (if any) is related to {Color.YELLOW}test scenarios{Color.NC}")
    else:
        print(f"  {Color.RED}→ INFRASTRUCTURE/ENVIRONMENT FAILURE{Color.NC}")
        print(f"    Playwright tests {Color.RED}never started{Color.NC} - check cluster setup, deployment, or CI pipeline")
        if analysis.build_log_analysis and analysis.build_log_analysis.infra_failure_category:
            cat = analysis.build_log_analysis.infra_failure_category.value
            print(f"    {Color.BOLD}Category:{Color.NC} {Color.YELLOW}{cat}{Color.NC}")
            if analysis.build_log_analysis.infra_failure_detail:
                print(f"    {Color.BOLD}Detail:{Color.NC} {analysis.build_log_analysis.infra_failure_detail}")
        print(f"    {Color.BOLD}Reason:{Color.NC} {analysis.reason}")
        if analysis.build_log_path:
            print()
            print(f"{Color.BOLD}Build log:{Color.NC}")
            print(f"  {Color.CYAN}{analysis.build_log_path}{Color.NC}")


def _slugify(text: str) -> str:
    """Convert text to a markdown anchor slug."""
    # Lowercase, replace spaces with hyphens, remove special characters
    slug = text.lower().replace(" ", "-")
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    return slug


def generate_summary_markdown_report(summary: Summary, ai_analyze: bool = False) -> str:
    """Generate a markdown report from the summary."""
    lines = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines.append("# CI Failure Classification Report")
    lines.append("")
    lines.append(f"**Generated:** {timestamp}")
    if ai_analyze:
        lines.append("")
        lines.append("*Infrastructure failures analyzed using AI*")
    lines.append("")

    # Summary statistics
    lines.append("## Summary")
    lines.append("")
    lines.append(f"**PRs analyzed:** {len(summary.analyzed_prs)} | **Total CI runs:** {summary.total}")
    lines.append("")
    lines.append("| Classification | Count | Percentage |")
    lines.append("|----------------|-------|------------|")

    if summary.total > 0:
        lines.append(f"| [Infrastructure Failures](#infrastructure-failures-by-category) | {summary.infra_failures} | {summary.infra_failures * 100 // summary.total}% |")
        lines.append(f"| [Test Failures](#most-common-playwright-test-failures) | {summary.test_failures} | {summary.test_failures * 100 // summary.total}% |")
        lines.append(f"| Test Successes | {summary.test_successes} | {summary.test_successes * 100 // summary.total}% |")
        lines.append(f"| [Jobs Aborted](#aborted-jobs) | {summary.job_aborted} | {summary.job_aborted * 100 // summary.total}% |")
        if summary.unknown > 0:
            lines.append(f"| Unknown | {summary.unknown} | {summary.unknown * 100 // summary.total}% |")
    lines.append("")

    # Pre-compute groupings for summary tables
    by_category: Dict[str, List[RunAnalysis]] = defaultdict(list)
    if summary.infra_failure_runs:
        for analysis in summary.infra_failure_runs:
            if ai_analyze and analysis.ai_analysis:
                cat = analysis.ai_analysis.root_cause_category
            elif analysis.build_log_analysis and analysis.build_log_analysis.infra_failure_category:
                cat = analysis.build_log_analysis.infra_failure_category.value
            else:
                cat = "Unknown"
            by_category[cat].append(analysis)

    by_test_name: Dict[str, List[TestCaseFailure]] = defaultdict(list)
    if summary.all_test_failures:
        for f in summary.all_test_failures:
            by_test_name[f.test_name].append(f)
    sorted_tests = sorted(by_test_name.items(), key=lambda x: -len(x[1]))

    # Summary: Top 10 Infrastructure Failure Categories
    if by_category:
        if ai_analyze:
            lines.append("### Top Infrastructure Failure Root Causes (AI Analysis)")
            lines.append("")
            lines.append("| Rank | Root Cause | Count | Confidence | Details |")
            lines.append("|------|------------|-------|------------|---------|")
        else:
            lines.append("### Top Infrastructure Failure Categories")
            lines.append("")
            lines.append("| Rank | Category | Count | Details |")
            lines.append("|------|----------|-------|---------|")
        total_infra = len(summary.infra_failure_runs)
        for rank, (cat, runs) in enumerate(sorted(by_category.items(), key=lambda x: -len(x[1]))[:10], 1):
            pct = len(runs) * 100 // total_infra if total_infra > 0 else 0
            anchor = _slugify(cat)
            if ai_analyze:
                confidence = runs[0].ai_analysis.confidence if runs and runs[0].ai_analysis else "N/A"
                lines.append(f"| {rank} | [{cat}](#{anchor}) | {len(runs)} ({pct}%) | {confidence} | [Details](#{anchor}) |")
            else:
                lines.append(f"| {rank} | [{cat}](#{anchor}) | {len(runs)} ({pct}%) | [Details](#{anchor}) |")
        lines.append("")

    # Summary: Top 10 Failing Test Cases
    if sorted_tests:
        lines.append("### Top 10 Failing Test Cases")
        lines.append("")
        lines.append("| Rank | Count | Test Name | Details |")
        lines.append("|------|-------|-----------|---------|")
        for rank, (test_name, test_failures) in enumerate(sorted_tests[:10], 1):
            count = len(test_failures)
            safe_name = test_name.replace("|", "\\|")[:60]
            if len(test_name) > 60:
                safe_name += "..."
            lines.append(f"| {rank} | {count} | {safe_name} | [Details](#detailed-breakdown-of-top-10-failing-tests) |")
        lines.append("")

    # Infrastructure failures by category (detailed)
    if summary.infra_failure_runs:
        if ai_analyze:
            lines.append("## Infrastructure Failures by Root Cause")
        else:
            lines.append("## Infrastructure Failures by Category")
        lines.append("")

        # Summary table with anchors
        if ai_analyze:
            lines.append("| Root Cause | Count | Percentage | Confidence |")
            lines.append("|------------|-------|------------|------------|")
        else:
            lines.append("| Category | Count | Percentage |")
            lines.append("|----------|-------|------------|")
        total_infra = len(summary.infra_failure_runs)
        for cat, runs in sorted(by_category.items(), key=lambda x: -len(x[1])):
            pct = len(runs) * 100 // total_infra if total_infra > 0 else 0
            anchor = _slugify(cat)
            if ai_analyze:
                confidence = runs[0].ai_analysis.confidence if runs and runs[0].ai_analysis else "N/A"
                lines.append(f"| [{cat}](#{anchor}) | {len(runs)} | {pct}% | {confidence} |")
            else:
                lines.append(f"| [{cat}](#{anchor}) | {len(runs)} | {pct}% |")
        lines.append("")

        # Details per category
        for cat, runs in sorted(by_category.items(), key=lambda x: -len(x[1])):
            lines.append(f"### {cat}")
            lines.append("")
            # Show AI analysis details if available
            if ai_analyze and runs and runs[0].ai_analysis:
                ai = runs[0].ai_analysis
                if ai.confidence:
                    lines.append(f"**Confidence:** {ai.confidence}")
                    lines.append("")
                if ai.root_cause_detail:
                    lines.append(f"**Detail:** {ai.root_cause_detail}")
                    lines.append("")
                if ai.suggested_fix:
                    lines.append(f"**Suggested Fix:** {ai.suggested_fix}")
                    lines.append("")
            lines.append(f"**{len(runs)} failures**")
            lines.append("")
            for run in runs:
                prow_url = run.get_prow_url()
                github_url = run.get_github_pr_url()
                detail = ""
                if ai_analyze and run.ai_analysis and run.ai_analysis.root_cause_detail:
                    detail = f" - {run.ai_analysis.root_cause_detail[:60]}"
                elif run.build_log_analysis and run.build_log_analysis.infra_failure_detail:
                    detail = f" - {run.build_log_analysis.infra_failure_detail[:60]}"
                lines.append(f"- [PR #{run.pr_number}]({github_url}) ([job logs]({prow_url})){detail}")
            lines.append("")

    # Aborted jobs
    if summary.aborted_runs:
        lines.append("## Aborted Jobs")
        lines.append("")
        lines.append(f"**{len(summary.aborted_runs)} jobs aborted**")
        lines.append("")
        for run in summary.aborted_runs:
            prow_url = run.get_prow_url()
            github_url = run.get_github_pr_url()
            lines.append(f"- [PR #{run.pr_number}]({github_url}) ([job logs]({prow_url})) - {run.reason}")
        lines.append("")

    # Test failures (CI runs with test failures)
    if summary.test_failure_runs:
        lines.append("## Test Failures")
        lines.append("")
        lines.append(f"**{len(summary.test_failure_runs)} CI runs with test failures** ([see detailed test analysis](#most-common-playwright-test-failures))")
        lines.append("")
        for run in summary.test_failure_runs[:20]:  # Limit to 20
            prow_url = run.get_prow_url()
            github_url = run.get_github_pr_url()
            lines.append(f"- [PR #{run.pr_number}]({github_url}) ([job logs]({prow_url})) - {run.reason}")
        if len(summary.test_failure_runs) > 20:
            lines.append(f"- ... and {len(summary.test_failure_runs) - 20} more")
        lines.append("")

    # Most Common Playwright Test Failures
    if summary.all_test_failures:
        lines.extend(generate_test_failure_markdown(summary.all_test_failures))

    return "\n".join(lines)


def generate_test_failure_markdown(failures: List[TestCaseFailure]) -> List[str]:
    """Generate markdown section for Playwright test failures."""
    lines = []

    lines.append("## Most Common Playwright Test Failures")
    lines.append("")
    lines.append(f"**Total test case failures:** {len(failures)}")
    lines.append("")

    # Group failures by test name
    by_test_name: Dict[str, List[TestCaseFailure]] = defaultdict(list)
    for f in failures:
        by_test_name[f.test_name].append(f)

    sorted_tests = sorted(by_test_name.items(), key=lambda x: -len(x[1]))

    # Top failing test cases table
    lines.append("### Top Failing Test Cases")
    lines.append("")
    lines.append("| Rank | Count | Test Name | Affected PRs |")
    lines.append("|------|-------|-----------|--------------|")

    for rank, (test_name, test_failures) in enumerate(sorted_tests[:20], 1):
        count = len(test_failures)
        # Get unique PRs affected
        prs = sorted(set(f.pr_number for f in test_failures))
        prs_str = ", ".join(prs[:5])
        if len(prs) > 5:
            prs_str += f" (+{len(prs) - 5})"
        # Escape pipe characters in test name for markdown table
        safe_name = test_name.replace("|", "\\|")[:80]
        lines.append(f"| {rank} | {count} | {safe_name} | {prs_str} |")

    lines.append("")

    # Most problematic spec files
    by_spec: Dict[str, List[TestCaseFailure]] = defaultdict(list)
    for f in failures:
        by_spec[f.spec_file].append(f)

    sorted_specs = sorted(by_spec.items(), key=lambda x: -len(x[1]))

    lines.append("### Most Problematic Spec Files")
    lines.append("")
    lines.append("| Rank | Failures | Spec File |")
    lines.append("|------|----------|-----------|")

    for rank, (spec_file, spec_failures) in enumerate(sorted_specs[:15], 1):
        count = len(spec_failures)
        lines.append(f"| {rank} | {count} | `{spec_file}` |")

    lines.append("")

    # Failures by error type
    by_error_type: Dict[str, int] = defaultdict(int)
    for f in failures:
        by_error_type[f.error_type] += 1

    sorted_errors = sorted(by_error_type.items(), key=lambda x: -x[1])
    total_failures = len(failures)

    lines.append("### Failures by Error Type")
    lines.append("")
    lines.append("| Error Type | Count | Percentage |")
    lines.append("|------------|-------|------------|")

    for error_type, count in sorted_errors:
        pct = count * 100 // total_failures if total_failures > 0 else 0
        lines.append(f"| {error_type} | {count} | {pct}% |")

    lines.append("")

    # Detailed breakdown of top 10 failing tests
    lines.append("### Detailed Breakdown of Top 10 Failing Tests")
    lines.append("")

    for rank, (test_name, test_failures) in enumerate(sorted_tests[:10], 1):
        count = len(test_failures)
        spec_file = test_failures[0].spec_file if test_failures else "unknown"
        error_type = test_failures[0].error_type if test_failures else "unknown"

        lines.append(f"#### {rank}. {test_name}")
        lines.append("")
        lines.append(f"- **Spec File:** `{spec_file}`")
        lines.append(f"- **Failure Count:** {count}")
        lines.append(f"- **Error Type:** {error_type}")

        # Show failure message if available
        if test_failures and test_failures[0].failure_message:
            msg = test_failures[0].failure_message[:150]
            lines.append(f"- **Sample Error:** `{msg}`")

        # List affected PRs
        prs = sorted(set(f.pr_number for f in test_failures))
        lines.append(f"- **Affected PRs:** {', '.join(prs)}")
        lines.append("")

    return lines


def analyze_directory(logs_dir: Path, ai_analyze: bool = False, output_file: Optional[str] = None, pr_limit: Optional[int] = None) -> Summary:
    """Analyze all CI runs in a directory."""
    print_header()
    print(f"{Color.CYAN}Scanning directory: {logs_dir}{Color.NC}")
    if pr_limit:
        print(f"{Color.CYAN}Limiting to {pr_limit} most recent PRs{Color.NC}")
    if ai_analyze:
        print(f"{Color.CYAN}Using AI for infrastructure failure analysis{Color.NC}")
    print()

    # Initialize AI client early if needed
    ai_client = None
    if ai_analyze:
        ai_client = init_gemini_client()

    summary = Summary()

    # Find all PR directories and sort by PR number (descending for most recent first)
    pr_dirs = [d for d in logs_dir.iterdir() if d.is_dir() and d.name.isdigit()]
    pr_dirs = sorted(pr_dirs, key=lambda x: int(x.name), reverse=True)

    # Apply limit if specified
    if pr_limit:
        pr_dirs = pr_dirs[:pr_limit]

    # Process PRs (re-sort ascending for output order)
    for pr_dir in sorted(pr_dirs, key=lambda x: int(x.name)):
        pr_number = pr_dir.name
        summary.analyzed_prs.add(pr_number)

        # Find job directories
        for job_dir in pr_dir.iterdir():
            if not job_dir.is_dir() or not job_dir.name.startswith("pull-ci-"):
                continue
            
            # Find run directories
            for run_dir in job_dir.iterdir():
                if not run_dir.is_dir():
                    continue
                
                run_id = run_dir.name
                if not run_id.isdigit():
                    continue
                
                analysis = analyze_run(run_dir, pr_number, run_id, job_name=job_dir.name, ai_client=ai_client)
                print_run_result(analysis)

                # Update summary
                summary.total += 1
                if analysis.classification == Classification.INFRA_FAILURE:
                    summary.infra_failures += 1
                    summary.infra_failure_runs.append(analysis)
                elif analysis.classification == Classification.TEST_FAILURE:
                    summary.test_failures += 1
                    summary.test_failure_runs.append(analysis)
                elif analysis.classification == Classification.TEST_SUCCESS:
                    summary.test_successes += 1
                elif analysis.classification == Classification.JOB_ABORTED:
                    summary.job_aborted += 1
                    summary.aborted_runs.append(analysis)
                else:
                    summary.unknown += 1

                # Collect individual test failures from junit reports
                if analysis.junit_showcase and analysis.junit_showcase.failed_tests:
                    summary.all_test_failures.extend(analysis.junit_showcase.failed_tests)
                if analysis.junit_rbac and analysis.junit_rbac.failed_tests:
                    summary.all_test_failures.extend(analysis.junit_rbac.failed_tests)
    
    print_summary(summary, ai_analyze=ai_analyze)

    # Generate markdown report
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    timestamp_suffix = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if output_file:
        # Use provided filename but add to reports dir with timestamp
        base_name = Path(output_file).stem
        report_file = reports_dir / f"{base_name}_{timestamp_suffix}.md"
    else:
        report_file = reports_dir / f"ci-failure-report_{timestamp_suffix}.md"

    markdown_content = generate_summary_markdown_report(summary, ai_analyze=ai_analyze)
    report_file.write_text(markdown_content)
    print()
    print(f"{Color.GREEN}✓ Report saved to: {Color.BOLD}{report_file}{Color.NC}")

    return summary


def main():
    parser = argparse.ArgumentParser(
        description="Classify CI failures as Infrastructure vs Playwright test failures.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Analyze ./ci-logs (report saved to reports/)
  %(prog)s ./my-logs                          # Analyze custom directory
  %(prog)s -n 10                              # Analyze only 10 most recent PRs
  %(prog)s -s ./ci-logs/3843/pull-ci.../run-id/  # Single run analysis
  %(prog)s -o my-report                        # Custom base name (reports/my-report_YYYY-MM-DD_HH-MM-SS.md)
  %(prog)s --ai                                # Use AI to analyze infrastructure failures

Environment Variables:
  GEMINI_API_KEY or GOOGLE_API_KEY    Required for --ai mode
        """
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='./ci-logs',
        help='Path to CI logs directory or single run (default: ./ci-logs-full)'
    )
    parser.add_argument(
        '-s', '--single',
        action='store_true',
        help='Analyze a single run directory in detail'
    )
    parser.add_argument(
        '--ai',
        action='store_true',
        help='Use Gemini AI to analyze infrastructure failures and determine root causes'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Base name for report file (saved to reports/ with timestamp suffix)'
    )
    parser.add_argument(
        '-n', '--limit',
        type=int,
        default=None,
        help='Limit analysis to N most recent PRs (by PR number)'
    )

    args = parser.parse_args()
    path = Path(args.path)
    
    if not path.exists():
        print(f"Error: Path not found: {path}", file=sys.stderr)
        sys.exit(1)
    
    if args.single:
        analyze_single_run_detailed(path)
    else:
        analyze_directory(
            path,
            ai_analyze=args.ai,
            output_file=args.output,
            pr_limit=args.limit
        )


if __name__ == "__main__":
    main()

