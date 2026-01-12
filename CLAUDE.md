# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CI failure analysis toolkit for Red Hat Developer Hub (RHDH) Playwright E2E tests running on OpenShift. The tools classify failures as infrastructure issues vs actual test failures and generate reports.

## Commands

```bash
# Run the main classifier (uses uv for dependency management)
uv run classify-failures.py ./ci-logs

# Analyze only N most recent PRs
uv run classify-failures.py ./ci-logs -n 20

# Single run detailed analysis
uv run classify-failures.py -s ./ci-logs/<pr>/<job>/<run-id>/

# Custom report base name (saved to reports/ with timestamp)
uv run classify-failures.py -o my-report

# With AI root cause analysis (requires GEMINI_API_KEY)
uv run classify-failures.py --ai

# Download CI logs from GCS (requires gcloud auth)
uv run download-ci-logs.py ./ci-logs

# Download with options
uv run download-ci-logs.py ./ci-logs --max-prs 100 --max-workers 20

# Download only junit reports (faster)
uv run download-junit-reports.py ./ci-logs

# Extract gzipped build logs
uv run extract_gzipped_logs.py

# Archive (gzip) all uncompressed log files
uv run archive-logs.py ./ci-logs

# Dry run to see what would be compressed
uv run archive-logs.py ./ci-logs --dry-run

# Include binary files (skipped by default)
uv run archive-logs.py ./ci-logs --include-binary
```

## Architecture

### Data Flow
1. `download-ci-logs.py` fetches logs from GCS bucket `test-platform-results`
2. `classify-failures.py` analyzes logs and generates reports in `reports/` directory with timestamp suffix
   - Automatically detects and reads gzipped files (checks magic bytes, not extension)
3. `archive-logs.py` compresses logs to save disk space (optional)

Note: `extract_gzipped_logs.py` is optional - `classify-failures.py` handles gzipped files automatically.

### CI Log Structure (Prow Artifacts)

Every Prow job generates an artifacts directory. See [OpenShift CI Artifacts Docs](https://docs.ci.openshift.org/docs/how-tos/artifacts/).

```
ci-logs/
  <pr-number>/
    <job-name>/                    # e.g., pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm
      <run-id>/
        # Root-level Prow artifacts:
        build-log.txt              # Text version of build logs (key for classification)
        clone-log.txt              # Repository cloning output from clonerefs
        clone-records.json         # Clone metadata
        started.json               # Job start marker (timestamp, PR info)
        finished.json              # Job end marker (result: SUCCESS/FAILURE/ABORTED)
        prowjob.json               # Complete ProwJob object (state, description)
        podinfo.json               # Pod and Event object dumps
        sidecar-logs.json          # Sidecar container output

        # ci-operator artifacts:
        artifacts/
          build-logs/              # Individual build logs (e.g., src.log)
          build-resources/         # K8s object dumps (pods.json, events.json, builds.json)
          ci-operator.log          # Debug output in JSON format
          ci-operator-step-graph.json
          junit_operator.xml       # Operator-level JUnit results

          # Test step artifacts (RHDH specific):
          e2e-ocp-helm/redhat-developer-rhdh-ocp-helm/
            build-log.txt          # Test step build log
            artifacts/
              reporting/
                OVERALL_RESULT.txt # Exit code (0 = success, non-zero = failure)
              showcase/
                junit-results.xml  # Playwright test results
                *.webm             # Test video recordings
                *.png              # Screenshots
              showcase-rbac/
                junit-results.xml
```

### Key Files for Classification
- `build-log.txt` (root or test step): Look for "Running X tests using Y workers" to detect if Playwright started
- `finished.json`: Check `result` field (SUCCESS/FAILURE/ABORTED)
- `prowjob.json`: Check `status.state` and `status.description` for abort reasons
- `junit-results.xml`: Parse for individual test failures
- `OVERALL_RESULT.txt`: Exit code (0 = tests passed)

### Classification Logic (classify-failures.py)
- **Infrastructure Failure**: Tests never started (Docker image timeout, operator install failure, pod not ready, missing CRD, helm failure, clone failure, resource quota exceeded)
- **Test Failure**: Playwright tests ran but some failed (detected by "Running X tests using Y workers" in build log)
- **Job Aborted**: Job was cancelled (detected from prowjob.json or interrupt signals in logs)
- **Test Success**: Tests ran and passed (OVERALL_RESULT.txt = 0)

### Infrastructure Failure Categories
- `CLONE_FAILURE`: Repository cloning failed
- `DOCKER_IMAGE_TIMEOUT`: PR/CLI image not available in registry
- `OPERATOR_INSTALL_TIMEOUT`: Operator (e.g., Crunchy Postgres) failed to install
- `POD_NOT_READY`: Pods didn't reach ready state
- `MISSING_CRD`: Required CustomResourceDefinition not installed
- `HELM_INSTALL_FAILED`: Helm chart installation failed
- `CLUSTER_CONNECTIVITY`: Network/connection issues
- `RESOURCE_QUOTA_EXCEEDED`: CPU/memory/quota limits exceeded
- `SCRIPT_ERROR`: Setup script failed
- `UNKNOWN`: Unknown infrastructure error

### Key Data Classes
- `RunAnalysis`: Complete analysis of a single CI run
- `BuildLogAnalysis`: Parsed indicators from build-log.txt
- `JUnitStats`: Test statistics including individual `TestCaseFailure` items
- `JobStatus`: Status from finished.json and prowjob.json
- `AIRootCauseAnalysis`: AI-generated root cause analysis (when --ai flag used)
- `Summary`: Aggregated statistics across all analyzed runs

## Dependencies

- `google-genai`: Required for `--ai` mode in classify-failures.py (Gemini AI)
- `google-cloud-storage`: Required for download scripts (download-ci-logs.py, download-junit-reports.py)

Install with: `uv sync` (uses pyproject.toml and uv.lock)

## Environment Variables

- `GEMINI_API_KEY` or `GOOGLE_API_KEY`: Required for `--ai` mode (Gemini root cause analysis)
- GCS bucket is public, so no auth required for downloads

## Script Reference

### classify-failures.py
Main classification and reporting tool. Reports are saved to `reports/` directory with timestamp suffix.

Automatically detects and reads gzipped files by checking magic bytes (`\x1f\x8b`), not file extension. Works with all log file types: build-log.txt, JSON files, junit-results.xml, OVERALL_RESULT.txt.

```
Arguments:
  path              Path to CI logs directory (default: ./ci-logs)
  -s, --single      Analyze a single run directory in detail
  -n, --limit N     Limit analysis to N most recent PRs
  -o, --output NAME Base name for report (saved to reports/<name>_YYYY-MM-DD_HH-MM-SS.md)
  --ai              Use Gemini AI for root cause analysis
```

### download-ci-logs.py
Downloads CI logs from GCS bucket.

```
Arguments:
  output_dir        Output directory (default: ./ci-logs)
  --max-prs N       Maximum PRs to process (default: 200)
  --max-workers N   Parallel download workers (default: 10)
  --job-names       Job names to download (default: main and release-1.8 e2e-ocp-helm)
```

### download-junit-reports.py
Downloads only junit-results.xml files (faster than full logs).

```
Arguments:
  output_dir        Output directory (default: ./ci-logs)
  max_workers       Parallel download workers (positional, default: 10)
```

Note: Only downloads from main branch job (`pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm`).

### extract_gzipped_logs.py
Decompresses gzipped build-log.txt files in place. **Optional** - `classify-failures.py` reads gzipped files automatically.

```
Arguments: None (scans ./ci-logs directory)
```

### archive-logs.py
Compresses all uncompressed files in ci-logs directory. Checks file content (gzip magic bytes) not just extension. Skips binary formats by default.

```
Arguments:
  directory         Directory to archive (default: ./ci-logs)
  -n, --dry-run     Show what would be compressed without compressing
  --include-binary  Include binary formats that don't compress well (.webm, .png, .jpg, etc.)
```
