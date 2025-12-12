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

# With AI root cause analysis (requires GEMINI_API_KEY)
uv run classify-failures.py --ai

# Download CI logs from GCS (requires gcloud auth)
uv run download-ci-logs.py ./ci-logs

# Download only junit reports
uv run download-junit-reports.py ./ci-logs

# Extract gzipped build logs
uv run extract_gzipped_logs.py
```

## Architecture

### Data Flow
1. `download-ci-logs.py` fetches logs from GCS bucket `test-platform-results`
2. `extract_gzipped_logs.py` decompresses gzipped build-log.txt files
3. `classify-failures.py` analyzes logs and generates `ci-failure-report.md`

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

### Classification Logic (classify-failures.py)
- **Infrastructure Failure**: Tests never started (Docker image timeout, operator install failure, pod not ready, missing CRD, helm failure)
- **Test Failure**: Playwright tests ran but some failed (detected by "Running X tests using Y workers" in build log)
- **Job Aborted**: Job was cancelled (detected from prowjob.json or interrupt signals in logs)
- **Test Success**: Tests ran and passed (OVERALL_RESULT.txt = 0)

### Key Data Classes
- `RunAnalysis`: Complete analysis of a single CI run
- `BuildLogAnalysis`: Parsed indicators from build-log.txt
- `JUnitStats`: Test statistics including individual `TestCaseFailure` items
- `Summary`: Aggregated statistics across all analyzed runs

## Environment Variables

- `GEMINI_API_KEY` or `GOOGLE_API_KEY`: Required for `--ai` mode (Gemini root cause analysis)
- GCS access requires `gcloud auth application-default login`
