# RHDH CI Failure Analysis Toolkit

Tools for analyzing CI failures in Red Hat Developer Hub (RHDH) Playwright E2E tests. Helps distinguish between **infrastructure failures** (tests never started) and **actual test failures** (tests ran but failed).

## Why This Exists

RHDH runs Playwright E2E tests on OpenShift via Prow CI. When a CI job fails, it's not always clear if:
- The test environment failed to set up (Docker image timeout, operator install failure, etc.)
- The Playwright tests actually ran and found bugs

This toolkit downloads CI logs, classifies failures, identifies the most common failing tests, and generates reports to help prioritize fixes.

## Quick Start

```bash
# Install dependencies
uv sync

# Download recent CI logs (requires gcloud auth)
gcloud auth application-default login
uv run download-ci-logs.py ./ci-logs

# Decompress build logs
uv run extract_gzipped_logs.py

# Analyze and generate report
uv run classify-failures.py ./ci-logs
```

This generates `ci-failure-report.md` with:
- Classification breakdown (infrastructure vs test failures)
- Top infrastructure failure categories
- Most common failing Playwright tests
- Links to GitHub PRs and Prow job logs

## Tools

### classify-failures.py

The main analysis tool. Classifies CI runs and generates reports.

```bash
# Analyze all PRs in ci-logs directory
uv run classify-failures.py ./ci-logs

# Analyze only the 20 most recent PRs
uv run classify-failures.py -n 20

# Detailed analysis of a single run
uv run classify-failures.py -s ./ci-logs/3843/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/1234567890/

# Use Gemini AI to analyze infrastructure failures (requires GEMINI_API_KEY)
export GEMINI_API_KEY="your-key"
uv run classify-failures.py --ai
```

**Output:**
- Console summary with color-coded classifications
- `ci-failure-report.md` with detailed breakdown

### download-ci-logs.py

Downloads CI logs from the GCS bucket used by Prow.

```bash
uv run download-ci-logs.py ./ci-logs
```

Downloads logs for recent PRs from:
- `pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm`
- `pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm`

### download-junit-reports.py

Downloads only the junit-results.xml files (faster than full logs).

```bash
uv run download-junit-reports.py ./ci-logs
```

### extract_gzipped_logs.py

Decompresses gzipped build-log.txt files in place.

```bash
uv run extract_gzipped_logs.py
```

## Classification Categories

### Infrastructure Failures
Tests never started due to environment issues:

| Category | Description |
|----------|-------------|
| Docker Image Timeout | PR image not available in registry |
| Operator Install Timeout | Operator (e.g., Crunchy Postgres) failed to install |
| Pod/Deployment Not Ready | Pods didn't reach ready state |
| Missing CRD | Required CRD not installed |
| Helm Install Failed | Helm chart installation failed |
| Cluster Connectivity | Network/connection issues |
| Script Error | Setup script failed |

### Test Failures
Playwright tests ran but some failed. The report shows:
- Most common failing test cases
- Most problematic spec files
- Failure breakdown by error type (TimeoutError vs AssertionError)

### Job Aborted
Job was cancelled (new commit pushed, manual cancel, PR closed).

## Report Structure

The generated `ci-failure-report.md` includes:

1. **Summary** - Overall classification breakdown with links
2. **Top Infrastructure Failure Categories** - Quick overview table
3. **Top 10 Failing Test Cases** - Most frequently failing tests
4. **Infrastructure Failures by Category** - Detailed breakdown with affected PRs
5. **Most Common Playwright Test Failures** - Full test failure analysis
6. **Detailed Breakdown** - Individual test failure details with error messages

## Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) for dependency management
- `gcloud` CLI for downloading logs
- `GEMINI_API_KEY` for AI analysis (optional)

## CI Log Structure (Prow Artifacts)

Every Prow job generates an artifacts directory containing execution information and results. These files enable investigation of job steps and outcomes. See [OpenShift CI Artifacts Documentation](https://docs.ci.openshift.org/docs/how-tos/artifacts/) for complete details.

```
ci-logs/
  <pr-number>/
    pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/
      <run-id>/
        # Root-level Prow artifacts
        build-log.txt          # Text version of build logs (key for classification)
        clone-log.txt          # Repository cloning output from clonerefs
        clone-records.json     # Clone metadata
        started.json           # Job start marker with timestamp and PR info
        finished.json          # Job end marker (result: SUCCESS/FAILURE/ABORTED)
        prowjob.json           # Complete ProwJob object definition
        podinfo.json           # Pod and Event object dumps
        sidecar-logs.json      # Sidecar container output managing uploads

        # ci-operator artifacts
        artifacts/
          build-logs/          # Individual build logs as text files (e.g., src.log)
          build-resources/     # JSON dumps of K8s objects:
                               #   builds.json, pods.json, events.json, imagestreams.json
          ci-operator.log      # Debug output in JSON format (superset of build-log)
          ci-operator-step-graph.json  # K8s/OpenShift objects created per step
          junit_operator.xml   # Operator-level JUnit results

          # RHDH E2E test step artifacts
          e2e-ocp-helm/
            redhat-developer-rhdh-ocp-helm/
              build-log.txt    # Test step specific build log
              artifacts/
                showcase/
                  junit-results.xml    # Playwright test results
                  *.webm               # Test video recordings
                  *.png                # Screenshots on failure
                  test-results/        # Detailed test output
                showcase-rbac/
                  junit-results.xml    # RBAC test results
```

### Key Files for Troubleshooting

| File | Use Case |
|------|----------|
| `build-log.txt` | Primary source for classification - look for "Running X tests using Y workers" |
| `finished.json` | Check job result (SUCCESS/FAILURE/ABORTED) |
| `prowjob.json` | Get abort reasons from `status.state` and `status.description` |
| `clone-log.txt` | Debug repository cloning failures |
| `artifacts/build-resources/pods.json` | Investigate pod scheduling/timeout issues |
| `artifacts/build-resources/events.json` | Check Kubernetes events for errors |
| `junit-results.xml` | Parse individual test failures and error messages |

## Example Output

```
╔══════════════════════════════════════════════════════════════════╗
║       CI Failure Classification: Infrastructure vs Tests         ║
╚══════════════════════════════════════════════════════════════════╝

  ✗ PR #3904 [1999461923778727936]: INFRASTRUCTURE - Operator Install Timeout
  ⚠ PR #3905 [1999462000000000000]: TEST FAILURE - Playwright tests ran (45 tests)
  ✓ PR #3906 [1999462100000000000]: TEST SUCCESS - All tests passed
  ⊘ PR #3907 [1999462200000000000]: ABORTED - Job aborted by trigger plugin

════════════════════════════════════════════════════════════════════
Summary
════════════════════════════════════════════════════════════════════

PRs analyzed: 150 | Total CI runs: 809

  ■ Infrastructure failures: 116 (14%)
  ■ Test failures:          172 (21%)
  ■ Test successes:         192 (23%)
  ■ Jobs aborted:           329 (40%)
```
