# CI Failure Classification Report

**Generated:** 2026-01-12 14:23:02

*Infrastructure failures analyzed using AI*

## Summary

**PRs analyzed:** 50 | **Total CI runs:** 285

| Classification | Count | Percentage |
|----------------|-------|------------|
| [Infrastructure Failures](#infrastructure-failures-by-category) | 45 | 15% |
| [Test Failures](#most-common-playwright-test-failures) | 69 | 24% |
| Test Successes | 50 | 17% |
| [Jobs Aborted](#aborted-jobs) | 121 | 42% |

### Top Infrastructure Failure Root Causes (AI Analysis)

| Rank | Root Cause | Count | Confidence | Details |
|------|------------|-------|------------|---------|
| 1 | [Docker Image Timeout](#docker-image-timeout) | 16 (35%) | high | [Details](#docker-image-timeout) |
| 2 | [Cluster Connectivity / Network Issues](#cluster-connectivity--network-issues) | 7 (15%) | high | [Details](#cluster-connectivity--network-issues) |
| 3 | [AI Analysis Failed](#ai-analysis-failed) | 3 (6%) | low | [Details](#ai-analysis-failed) |
| 4 | [Skipped E2E Tests](#skipped-e2e-tests) | 2 (4%) | high | [Details](#skipped-e2e-tests) |
| 5 | [Script/Setup Logic Errors](#scriptsetup-logic-errors) | 1 (2%) | high | [Details](#scriptsetup-logic-errors) |
| 6 | [Secret Creation Failure](#secret-creation-failure) | 1 (2%) | high | [Details](#secret-creation-failure) |
| 7 | [Invalid Base64 Data in Secret](#invalid-base64-data-in-secret) | 1 (2%) | high | [Details](#invalid-base64-data-in-secret) |
| 8 | [Tekton Pipeline Operator Timeout](#tekton-pipeline-operator-timeout) | 1 (2%) | high | [Details](#tekton-pipeline-operator-timeout) |
| 9 | [Postgres Database Creation Failure](#postgres-database-creation-failure) | 1 (2%) | high | [Details](#postgres-database-creation-failure) |
| 10 | [Postgres Database Connection Timeout](#postgres-database-connection-timeout) | 1 (2%) | high | [Details](#postgres-database-connection-timeout) |

### Top 10 Failing Test Cases

| Rank | Count | Test Name | Details |
|------|-------|-----------|---------|
| 1 | 18 | Test Adoption Insights › Test Adoption Insights plugin: load... | [Details](#detailed-breakdown-of-top-10-failing-tests) |
| 2 | 16 | Test Kubernetes Plugin › Verify that a user with permissions... | [Details](#detailed-breakdown-of-top-10-failing-tests) |
| 3 | 13 | Test RBAC › Test RBAC plugin as an admin user › Edit users a... | [Details](#detailed-breakdown-of-top-10-failing-tests) |
| 4 | 12 | Test Kubernetes Plugin › Verify that a user without permissi... | [Details](#detailed-breakdown-of-top-10-failing-tests) |
| 5 | 9 | Test Topology Plugin with RBAC › Verify a user without permi... | [Details](#detailed-breakdown-of-top-10-failing-tests) |
| 6 | 9 | Test Topology Plugin with RBAC › Verify a user with permissi... | [Details](#detailed-breakdown-of-top-10-failing-tests) |
| 7 | 9 | Test Topology Plugin with RBAC › Verify a user with permissi... | [Details](#detailed-breakdown-of-top-10-failing-tests) |
| 8 | 9 | Test global floating action button plugin › Check if Git and... | [Details](#detailed-breakdown-of-top-10-failing-tests) |
| 9 | 8 | Test Orchestrator RBAC › Test Orchestrator RBAC: Global Work... | [Details](#detailed-breakdown-of-top-10-failing-tests) |
| 10 | 7 | Mark notification tests › Mark notification as read | [Details](#detailed-breakdown-of-top-10-failing-tests) |

## Infrastructure Failures by Root Cause

| Root Cause | Count | Percentage | Confidence |
|------------|-------|------------|------------|
| [Docker Image Timeout](#docker-image-timeout) | 16 | 35% | high |
| [Cluster Connectivity / Network Issues](#cluster-connectivity--network-issues) | 7 | 15% | high |
| [AI Analysis Failed](#ai-analysis-failed) | 3 | 6% | low |
| [Skipped E2E Tests](#skipped-e2e-tests) | 2 | 4% | high |
| [Script/Setup Logic Errors](#scriptsetup-logic-errors) | 1 | 2% | high |
| [Secret Creation Failure](#secret-creation-failure) | 1 | 2% | high |
| [Invalid Base64 Data in Secret](#invalid-base64-data-in-secret) | 1 | 2% | high |
| [Tekton Pipeline Operator Timeout](#tekton-pipeline-operator-timeout) | 1 | 2% | high |
| [Postgres Database Creation Failure](#postgres-database-creation-failure) | 1 | 2% | high |
| [Postgres Database Connection Timeout](#postgres-database-connection-timeout) | 1 | 2% | high |
| [ImagePullBackOff / Docker Image Timeout](#imagepullbackoff--docker-image-timeout) | 1 | 2% | high |
| [ImagePullBackOff / Docker Image Timeout (CLI images)](#imagepullbackoff--docker-image-timeout-cli-images) | 1 | 2% | high |
| [ImagePullBackOff / Docker Image Timeout (RHDH images)](#imagepullbackoff--docker-image-timeout-rhdh-images) | 1 | 2% | high |
| [Cluster Connectivity / DNS Resolution Failure](#cluster-connectivity--dns-resolution-failure) | 1 | 2% | high |
| [Tekton Pipeline Webhook Timeout](#tekton-pipeline-webhook-timeout) | 1 | 2% | high |
| [Tekton Pipeline Webhook Endpoint Failure](#tekton-pipeline-webhook-endpoint-failure) | 1 | 2% | high |
| [Tekton Pipeline Webhook Endpoint Timeout](#tekton-pipeline-webhook-endpoint-timeout) | 1 | 2% | high |
| [Init Container CrashLoopBackOff](#init-container-crashloopbackoff) | 1 | 2% | high |
| [Pod Init Container CrashLoopBackOff](#pod-init-container-crashloopbackoff) | 1 | 2% | high |
| [Backstage Deployment Timeout](#backstage-deployment-timeout) | 1 | 2% | high |
| [Tekton Webhook Failure](#tekton-webhook-failure) | 1 | 2% | high |

### Docker Image Timeout

**Confidence:** high

**Detail:** The CI pipeline timed out while waiting for the RHDH Docker image `rhdh-community/rhdh:pr-3924-2eddee83` to become available. This suggests a problem with the image build or registry access.

**Suggested Fix:** Investigate the image build process for `rhdh-community/rhdh:pr-3924-2eddee83`. Check the image registry to ensure the image was successfully pushed. Verify that the CI environment has the necessary credentials and network access to pull the image from the registry.

**16 failures**

- [PR #3924](https://github.com/redhat-developer/rhdh/pull/3924) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3924/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009203802871173120)) - The CI pipeline timed out while waiting for the RHDH Docker 
- [PR #3924](https://github.com/redhat-developer/rhdh/pull/3924) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3924/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2003024433005989888)) - The build timed out while waiting for the newly built RHDH i
- [PR #3924](https://github.com/redhat-developer/rhdh/pull/3924) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3924/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001224806988517376)) - The CI pipeline timed out while waiting for the `rhdh-commun
- [PR #3924](https://github.com/redhat-developer/rhdh/pull/3924) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3924/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001244851139514368)) - The build timed out while waiting for the rhdh-community/rhd
- [PR #3924](https://github.com/redhat-developer/rhdh/pull/3924) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3924/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2003408715239133184)) - The pipeline timed out while waiting for the Docker image `r
- [PR #3924](https://github.com/redhat-developer/rhdh/pull/3924) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3924/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009546533753589760)) - The CI build timed out while waiting for the Docker image `r
- [PR #3924](https://github.com/redhat-developer/rhdh/pull/3924) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3924/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009232537615863808)) - The CI pipeline timed out while waiting for the rhdh-communi
- [PR #3940](https://github.com/redhat-developer/rhdh/pull/3940) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3940/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2002053080366977024)) - The build timed out while waiting for the RHDH Docker image 
- [PR #3943](https://github.com/redhat-developer/rhdh/pull/3943) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3943/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2002945139886002176)) - The build timed out while waiting for the `rhdh-community/rh
- [PR #3943](https://github.com/redhat-developer/rhdh/pull/3943) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3943/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2005482095085883392)) - The CI job timed out while waiting for the Docker image `rhd
- [PR #3958](https://github.com/redhat-developer/rhdh/pull/3958) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3958/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009448603923255296)) - The CI pipeline timed out while waiting for the Docker image
- [PR #3958](https://github.com/redhat-developer/rhdh/pull/3958) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3958/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009651041867403264)) - The CI job timed out while waiting for the Docker image `rhd
- [PR #3958](https://github.com/redhat-developer/rhdh/pull/3958) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3958/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2010555582162931712)) - The CI pipeline timed out while waiting for the Docker image
- [PR #3958](https://github.com/redhat-developer/rhdh/pull/3958) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3958/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008259474380296192)) - The CI pipeline timed out waiting for the Docker image `rhdh
- [PR #3963](https://github.com/redhat-developer/rhdh/pull/3963) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3963/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008588560650735616)) - The CI pipeline timed out while waiting for the Docker image
- [PR #3979](https://github.com/redhat-developer/rhdh/pull/3979) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3979/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2009448607744266240)) - The CI pipeline timed out while waiting for the Docker image

### Cluster Connectivity / Network Issues

**Confidence:** high

**Detail:** The build log shows a `curl: (6) Could not resolve host: quay.io` error. This indicates that the OpenShift cluster where the CI job is running cannot resolve the hostname `quay.io`, which is necessary to pull container images. This network connectivity issue prevented Playwright E2E tests from even starting since they couldn't pull necessary container images or access other resources hosted on quay.io.

**Suggested Fix:** Investigate the cluster's DNS configuration and network policies to ensure that it can resolve external hostnames, specifically `quay.io`. Check if there are any egress network policies blocking access to external registries.

**7 failures**

- [PR #3921](https://github.com/redhat-developer/rhdh/pull/3921) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3921/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008547142272028672)) - The build log shows a `curl: (6) Could not resolve host: qua
- [PR #3927](https://github.com/redhat-developer/rhdh/pull/3927) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3927/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001603622214832128)) - The initial `oc login` command failed due to a DNS lookup ti
- [PR #3928](https://github.com/redhat-developer/rhdh/pull/3928) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3928/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001627260154548224)) - The build log shows a 'Could not resolve host: quay.io' erro
- [PR #3929](https://github.com/redhat-developer/rhdh/pull/3929) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3929/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2001700156948353024)) - The build log shows that the test environment is unable to c
- [PR #3942](https://github.com/redhat-developer/rhdh/pull/3942) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3942/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2002142036471320576)) - The build log shows a DNS resolution failure when trying to 
- [PR #3951](https://github.com/redhat-developer/rhdh/pull/3951) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3951/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009537786599706624)) - The build failed to authenticate to the OpenShift cluster be
- [PR #3960](https://github.com/redhat-developer/rhdh/pull/3960) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3960/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008619915115761664)) - The 'e2e-ocp-helm-openshift-configure-cincinnati' step faile

### AI Analysis Failed

**Confidence:** low

**Detail:** Expecting value: line 1 column 1 (char 0)

**3 failures**

- [PR #3947](https://github.com/redhat-developer/rhdh/pull/3947) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3947/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009351766612643840)) - Expecting value: line 1 column 1 (char 0)
- [PR #3949](https://github.com/redhat-developer/rhdh/pull/3949) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3949/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009600380844904448)) - Expecting value: line 1 column 1 (char 0)
- [PR #3982](https://github.com/redhat-developer/rhdh/pull/3982) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3982/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2010516621637980160)) - Invalid control character at: line 5 column 6 (char 388)

### Skipped E2E Tests

**Confidence:** high

**Detail:** The PR title contains '[skip-e2e]' which instructs the CI pipeline to skip E2E test execution. The pipeline detected this and exited with code 0, indicating a successful skip.

**Suggested Fix:** Remove '[skip-e2e]' from the PR title if E2E tests are intended to be run. If skipping was intentional, no action is needed.

**2 failures**

- [PR #3975](https://github.com/redhat-developer/rhdh/pull/3975) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3975/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009384069380444160)) - The PR title contains '[skip-e2e]' which instructs the CI pi
- [PR #3976](https://github.com/redhat-developer/rhdh/pull/3976) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3976/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2009385425059188736)) - The PR title contains the '[skip-e2e]' tag, which caused the

### Script/Setup Logic Errors

**Confidence:** high

**Detail:** The shell script attempting to parse PR title information using `jq` failed because the PR title either did not exist or was malformed/empty, resulting in an invalid JSON response for `jq` to parse. This likely halts the subsequent execution of the E2E tests.

**Suggested Fix:** Implement error handling in the shell script to gracefully handle cases where the PR title is empty or invalid. Ensure the script checks for the existence and validity of the PR title before attempting to parse it with `jq`. Consider providing a default or skipping the parsing if the title is problematic.

**1 failures**

- [PR #3916](https://github.com/redhat-developer/rhdh/pull/3916) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3916/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008062301764063232)) - The shell script attempting to parse PR title information us

### Secret Creation Failure

**Confidence:** high

**Detail:** The pipeline failed because it could not create a secret named `rhdh-k8s-plugin-secret` in the `showcase` namespace. The error message indicates that the secret data contains invalid base64 encoding, causing the Kubernetes API server to reject the request.

**Suggested Fix:** Examine the YAML file being applied that defines the `rhdh-k8s-plugin-secret`. Verify that the `data` field contains valid base64 encoded strings. If the secret is generated dynamically, ensure the encoding process is correct. Investigate the source of the secret data and the encoding mechanism used.

**1 failures**

- [PR #3921](https://github.com/redhat-developer/rhdh/pull/3921) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3921/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001631163533234176)) - The pipeline failed because it could not create a secret nam

### Invalid Base64 Data in Secret

**Confidence:** high

**Detail:** The build failed because the script attempted to create a Kubernetes Secret with invalid base64 encoded data. The error `Error from server (BadRequest): error when creating "STDIN": Secret in version "v1" cannot be handled as a Secret: illegal base64 data at input byte 164` indicates the data provided for the secret was not properly base64 encoded, preventing the secret's creation. This likely originates from the YAML files applied to the `showcase` namespace.

**Suggested Fix:** Examine the YAML files being applied to the `showcase` namespace, specifically the `rhdh-k8s-plugin-secret`. Ensure that any data intended to be stored in the secret is properly base64 encoded before being included in the YAML. Investigate the script that generates or modifies this secret to verify its correctness.

**1 failures**

- [PR #3921](https://github.com/redhat-developer/rhdh/pull/3921) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3921/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001644222913974272)) - The build failed because the script attempted to create a Ku

### Tekton Pipeline Operator Timeout

**Confidence:** high

**Detail:** The Tekton Pipelines operator installation timed out while waiting for the `tekton-pipelines-webhook` endpoint to be created and also timed out waiting for the Tekton Pipeline CRD to be registered. This suggests a problem with the Tekton Pipelines operator deployment itself or with the cluster's ability to reconcile the operator and related resources.

**Suggested Fix:** Investigate the Tekton Pipelines operator deployment in the `openshift-operators` namespace. Check the operator pod logs for errors. Verify cluster network connectivity and resource availability for the operator. Also check for any pre-existing Tekton Pipelines installations that might be interfering.

**1 failures**

- [PR #3923](https://github.com/redhat-developer/rhdh/pull/3923) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3923/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2001415217069690880)) - The Tekton Pipelines operator installation timed out while w

### Postgres Database Creation Failure

**Confidence:** high

**Detail:** The 'rhdh-rbac-create-sonataflow-database' job in the 'showcase-rbac' namespace failed to create the 'sonataflow' database. The init container 'wait-for-db' timed out while waiting for the database to become available, causing the subsequent 'psql' container to fail when attempting to create the database. This is likely due to the Crunchy Postgres operator failing to provision the database in a timely manner. The logs show that the operator installation timed out earlier in the process.

**Suggested Fix:** Investigate why the Crunchy Postgres operator timed out. Check operator logs for errors related to provisioning the database. Increase the timeout value for the operator installation and the 'rhdh-rbac-create-sonataflow-database' job, but this is only a temporary fix. The underlying issue should be investigated and resolved.

**1 failures**

- [PR #3927](https://github.com/redhat-developer/rhdh/pull/3927) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3927/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008413705104003072)) - The 'rhdh-rbac-create-sonataflow-database' job in the 'showc

### Postgres Database Connection Timeout

**Confidence:** high

**Detail:** The job `rhdh-rbac-create-sonataflow-database` failed because the init container `wait-for-db` timed out while trying to connect to the PostgreSQL database. This indicates a problem with the external Crunchy Postgres database connectivity or the database not being ready within the timeout period.

**Suggested Fix:** Investigate the PostgreSQL database setup and connectivity. Verify that the database is running, accessible from within the cluster, and that the credentials in the `postgres-cred` secret are correct. Consider increasing the timeout for the `wait-for-db` init container if the database initialization takes longer than expected, or investigate why the DB might be slow to start.

**1 failures**

- [PR #3928](https://github.com/redhat-developer/rhdh/pull/3928) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3928/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001815505987440640)) - The job `rhdh-rbac-create-sonataflow-database` failed becaus

### ImagePullBackOff / Docker Image Timeout

**Confidence:** high

**Detail:** The log indicates that the `quay.io/redhat-appstudio/e2e-tests:multiarch` image failed to be pulled, resulting in an ImagePullBackOff error. This is likely due to a timeout or network issue preventing the image from being retrieved from the registry within the allowed time.

**Suggested Fix:** Investigate network connectivity to quay.io from the OpenShift cluster. Consider increasing the image pull timeout or pre-pulling the image to ensure it's available before the test starts. Also, verify the image name and tag are correct.

**1 failures**

- [PR #3947](https://github.com/redhat-developer/rhdh/pull/3947) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3947/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009890758408015872)) - The log indicates that the `quay.io/redhat-appstudio/e2e-tes

### ImagePullBackOff / Docker Image Timeout (CLI images)

**Confidence:** high

**Detail:** The CI build failed because the command line interface (CLI) tools image could not be pulled from the registry. Specifically, the `cli` init container failed to start due to an `ImagePullBackOff` error. This suggests that the image either does not exist at the specified tag, the registry is unavailable, or there are network connectivity issues preventing the image from being pulled. It is likely a temporary issue.

**Suggested Fix:** Retry the CI build. If the issue persists, investigate the availability of the `quay.io/redhat-appstudio/cli:latest` image and network connectivity to the Quay.io registry from the build environment. Consider using a specific, immutable tag instead of `latest` to improve reliability and prevent unexpected changes.

**1 failures**

- [PR #3947](https://github.com/redhat-developer/rhdh/pull/3947) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3947/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009710919168299008)) - The CI build failed because the command line interface (CLI)

### ImagePullBackOff / Docker Image Timeout (RHDH images)

**Confidence:** high

**Detail:** The build log shows numerous ImagePullBackOff errors when attempting to pull RHDH-related images (e.g., backend, frontend, postgres) from the `quay.io/redhat-appstudio` registry. This indicates a failure to retrieve the necessary container images, likely due to network issues, registry unavailability, or incorrect image names/tags.

**Suggested Fix:** 1. Verify network connectivity to quay.io from the OpenShift cluster. 2. Check the quay.io registry status for any outages or performance issues. 3. Confirm that the image names and tags used in the deployment configuration are correct and exist in the registry. 4. Consider increasing the image pull timeout in the kubelet configuration if network latency is high.

**1 failures**

- [PR #3947](https://github.com/redhat-developer/rhdh/pull/3947) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3947/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009505903337803776)) - The build log shows numerous ImagePullBackOff errors when at

### Cluster Connectivity / DNS Resolution Failure

**Confidence:** high

**Detail:** The `e2e-ocp-helm-gather-must-gather` step failed because it could not resolve the cluster's API server address (`api.rhdh-4-18-XXXXXXXXX-57znn.XXXXXXX.devcluster.openshift.com`) using the cluster's DNS server (`172.30.0.10:53`). Additionally, the step `e2e-ocp-helm-openshift-configure-cincinnati` timed out trying to reach the Kubernetes API. This indicates a fundamental networking problem preventing communication with the cluster's API server, likely a DNS configuration error within the cluster or a broader connectivity issue.

**Suggested Fix:** Investigate the cluster's DNS configuration. Verify that `172.30.0.10` is correctly configured as the DNS server within the cluster and that it can resolve the API server's hostname. Check for any firewall rules or network policies that might be blocking DNS resolution or connectivity to the API server. Ensure the cluster's core DNS pods are running and healthy.

**1 failures**

- [PR #3947](https://github.com/redhat-developer/rhdh/pull/3947) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3947/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2005968429386829824)) - The `e2e-ocp-helm-gather-must-gather` step failed because it

### Tekton Pipeline Webhook Timeout

**Confidence:** high

**Detail:** The Tekton Pipeline webhook endpoint failed to become available after the Tekton Pipelines operator was installed. This caused an error during the creation of a PipelineRun resource, specifically, the webhook timed out when attempting to mutate/validate the resource. The message 'no endpoints available for service "tekton-pipelines-webhook"' indicates a connectivity or readiness issue with the webhook service.

**Suggested Fix:** Investigate the Tekton Pipelines operator installation process. Verify the health and readiness of the tekton-pipelines-webhook service and pods in the openshift-pipelines namespace. Check for any errors or resource constraints preventing the webhook from becoming available. Increase the timeout for webhook endpoint creation or retry the Tekton operator installation.

**1 failures**

- [PR #3949](https://github.com/redhat-developer/rhdh/pull/3949) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3949/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2007746819299217408)) - The Tekton Pipeline webhook endpoint failed to become availa

### Tekton Pipeline Webhook Endpoint Failure

**Confidence:** high

**Detail:** The Tekton Pipelines webhook service, tekton-pipelines-webhook, did not have any available endpoints. This caused a failure when creating the hello-world-pipeline.yaml resource because the webhook could not be reached during the defaulting process.

**Suggested Fix:** Investigate the tekton-pipelines-webhook pod/service. Check the logs for the webhook pod to see why it's not becoming ready, check the tekton pipeline operator logs as well to determine if the controller is encountering any issues.

**1 failures**

- [PR #3949](https://github.com/redhat-developer/rhdh/pull/3949) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3949/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2007756457042251776)) - The Tekton Pipelines webhook service, tekton-pipelines-webho

### Tekton Pipeline Webhook Endpoint Timeout

**Confidence:** high

**Detail:** The Tekton Pipelines operator was installed, but the tekton-pipelines-webhook service endpoint failed to become available within the allotted time, leading to a timeout. Subsequent attempts to create resources, specifically a PipelineRun, failed because the webhook service was unavailable.

**Suggested Fix:** Investigate the tekton-pipelines-webhook deployment and service to determine why endpoints are not becoming available. Check pod logs for errors, service configuration, and network policies that might be preventing connectivity. Consider increasing the timeout for webhook endpoint creation if the deployment consistently takes longer than expected, or implement retry logic in the deployment scripts.

**1 failures**

- [PR #3949](https://github.com/redhat-developer/rhdh/pull/3949) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3949/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2007760441173872640)) - The Tekton Pipelines operator was installed, but the tekton-

### Init Container CrashLoopBackOff

**Confidence:** high

**Detail:** The `rhdh-rbac-developer-hub` pod is failing due to the `install-dynamic-plugins` init container repeatedly crashing. This prevents the main backstage-backend container from starting, resulting in Backstage being unavailable (HTTP 503) and the E2E tests from running. The Backoff suggests a persistent issue, not a transient one.

**Suggested Fix:** Investigate the logs of the `install-dynamic-plugins` init container in the `rhdh-rbac-developer-hub` pod to determine the cause of the crashes. Common causes include missing dependencies, incorrect file permissions, or errors in the plugin installation scripts. Once the root cause of the init container failure is identified, fix the underlying issue.

**1 failures**

- [PR #3960](https://github.com/redhat-developer/rhdh/pull/3960) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3960/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008305406362783744)) - The `rhdh-rbac-developer-hub` pod is failing due to the `ins

### Pod Init Container CrashLoopBackOff

**Confidence:** high

**Detail:** The `rhdh-rbac-developer-hub` pod's init container, `install-dynamic-plugins`, is failing and causing a `CrashLoopBackOff` which prevents backstage from becoming available. This is likely due to a script or configuration error within the init container itself.

**Suggested Fix:** Examine the logs of the `install-dynamic-plugins` init container in the `rhdh-rbac-developer-hub` pod to identify the specific error causing the crashloop. Debug the script and configuration responsible for installing dynamic plugins within that init container.

**1 failures**

- [PR #3960](https://github.com/redhat-developer/rhdh/pull/3960) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3960/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008594338870726656)) - The `rhdh-rbac-developer-hub` pod's init container, `install

### Backstage Deployment Timeout

**Confidence:** high

**Detail:** The Playwright E2E tests failed to start because the Backstage instance was not available after multiple attempts. The logs show a continuous loop of attempting to reach Backstage, indicated by the "Backstage not yet available (HTTP Status: 503)" messages. Additionally, the rhdh-rbac-developer-hub pod is in Init:CrashLoopBackOff state, indicating an issue during the initialization of the Backstage instance, preventing it from becoming available.

**Suggested Fix:** Investigate the rhdh-rbac-developer-hub pod's init container logs to determine the cause of the Init:CrashLoopBackOff. Check resource limits, image availability, and any configuration issues that might be preventing the Backstage instance from initializing properly. Examine the 'install-dynamic-plugins' container for errors.

**1 failures**

- [PR #3960](https://github.com/redhat-developer/rhdh/pull/3960) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3960/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008956497110765568)) - The Playwright E2E tests failed to start because the Backsta

### Tekton Webhook Failure

**Confidence:** high

**Detail:** The Tekton Operator Proxy Webhook service has no available endpoints, causing a failure when creating the ACM OperatorGroup. This likely indicates an issue with the Tekton Pipelines operator deployment or configuration, preventing the webhook service from functioning correctly and blocking subsequent operator installations.

**Suggested Fix:** Investigate the Tekton Pipelines operator deployment. Check the logs for the tekton-operator-proxy-webhook pod to identify the cause of the missing endpoints. Ensure the Tekton Pipelines operator is properly installed and configured before attempting to install other operators that depend on it.

**1 failures**

- [PR #3974](https://github.com/redhat-developer/rhdh/pull/3974) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3974/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2009379408053276672)) - The Tekton Operator Proxy Webhook service has no available e

## Aborted Jobs

**121 jobs aborted**

- [PR #3917](https://github.com/redhat-developer/rhdh/pull/3917) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3917/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001233721285414912)) - Job aborted: subhashkhileri successfully aborted 185cac64-622e-4c32-b139-341368805a0c.
- [PR #3917](https://github.com/redhat-developer/rhdh/pull/3917) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3917/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2000879161865932800)) - Job aborted: Aborted by trigger plugin.
- [PR #3917](https://github.com/redhat-developer/rhdh/pull/3917) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3917/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001234079759994880)) - Job aborted: subhashkhileri successfully aborted fcfc593d-2241-4597-8f95-0a0bea16be6b.
- [PR #3921](https://github.com/redhat-developer/rhdh/pull/3921) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3921/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2000948000783863808)) - Job aborted: Aborted by trigger plugin.
- [PR #3921](https://github.com/redhat-developer/rhdh/pull/3921) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3921/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2000950747428032512)) - Job aborted: Aborted by trigger plugin.
- [PR #3921](https://github.com/redhat-developer/rhdh/pull/3921) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3921/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2000947460486205440)) - Job aborted: Aborted by trigger plugin.
- [PR #3921](https://github.com/redhat-developer/rhdh/pull/3921) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3921/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009633619999461376)) - Job aborted: Job triggered.
- [PR #3921](https://github.com/redhat-developer/rhdh/pull/3921) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3921/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009216320691769344)) - Job aborted: Aborted by trigger plugin.
- [PR #3923](https://github.com/redhat-developer/rhdh/pull/3923) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3923/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2001386034415276032)) - Job aborted: Aborted by trigger plugin.
- [PR #3923](https://github.com/redhat-developer/rhdh/pull/3923) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3923/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2001381134872612864)) - Job aborted: Aborted by trigger plugin.
- [PR #3923](https://github.com/redhat-developer/rhdh/pull/3923) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3923/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2001294230772781056)) - Job aborted: Aborted by trigger plugin.
- [PR #3923](https://github.com/redhat-developer/rhdh/pull/3923) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3923/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2001382555135250432)) - Job aborted: Aborted by trigger plugin.
- [PR #3923](https://github.com/redhat-developer/rhdh/pull/3923) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3923/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2001352333543346176)) - Job aborted: Job triggered.
- [PR #3923](https://github.com/redhat-developer/rhdh/pull/3923) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3923/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2001393502495182848)) - Job aborted: Aborted by trigger plugin.
- [PR #3923](https://github.com/redhat-developer/rhdh/pull/3923) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3923/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2001408446024388608)) - Job aborted: Aborted by trigger plugin.
- [PR #3923](https://github.com/redhat-developer/rhdh/pull/3923) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3923/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2001100701366751232)) - Job aborted: Job triggered.
- [PR #3923](https://github.com/redhat-developer/rhdh/pull/3923) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3923/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2001656708568453120)) - Job aborted: Aborted by trigger plugin.
- [PR #3923](https://github.com/redhat-developer/rhdh/pull/3923) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3923/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2001365966327386112)) - Job aborted: Job triggered.
- [PR #3923](https://github.com/redhat-developer/rhdh/pull/3923) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3923/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2001651710132490240)) - Job aborted: Aborted by trigger plugin.
- [PR #3923](https://github.com/redhat-developer/rhdh/pull/3923) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3923/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2001101399563177984)) - Job aborted: Aborted by trigger plugin.
- [PR #3924](https://github.com/redhat-developer/rhdh/pull/3924) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3924/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009199850989555712)) - Job aborted: Aborted by trigger plugin.
- [PR #3924](https://github.com/redhat-developer/rhdh/pull/3924) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3924/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009192449116737536)) - Job aborted: Aborted by trigger plugin.
- [PR #3925](https://github.com/redhat-developer/rhdh/pull/3925) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3925/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001319278778781696)) - Job aborted: Aborted by trigger plugin.
- [PR #3928](https://github.com/redhat-developer/rhdh/pull/3928) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3928/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001607536242855936)) - Job aborted: Aborted by trigger plugin.
- [PR #3928](https://github.com/redhat-developer/rhdh/pull/3928) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3928/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001604757810057216)) - Job aborted: Aborted by trigger plugin.
- [PR #3928](https://github.com/redhat-developer/rhdh/pull/3928) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3928/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001608150653865984)) - Job aborted: Job triggered.
- [PR #3929](https://github.com/redhat-developer/rhdh/pull/3929) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3929/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2001691575104573440)) - Job aborted: Job triggered.
- [PR #3929](https://github.com/redhat-developer/rhdh/pull/3929) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3929/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2001680700314488832)) - Job aborted: Aborted by trigger plugin.
- [PR #3929](https://github.com/redhat-developer/rhdh/pull/3929) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3929/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2008246358066073600)) - Job aborted: Job triggered.
- [PR #3929](https://github.com/redhat-developer/rhdh/pull/3929) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3929/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2001681840905129984)) - Job aborted: Aborted by trigger plugin.
- [PR #3929](https://github.com/redhat-developer/rhdh/pull/3929) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3929/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2002052544888573952)) - Job aborted: Aborted by trigger plugin.
- [PR #3929](https://github.com/redhat-developer/rhdh/pull/3929) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3929/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2002052658193502208)) - Job aborted: Job triggered.
- [PR #3930](https://github.com/redhat-developer/rhdh/pull/3930) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3930/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001699222285455360)) - Job aborted: Job triggered.
- [PR #3931](https://github.com/redhat-developer/rhdh/pull/3931) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3931/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2001734072140828672)) - Job aborted: Job triggered.
- [PR #3932](https://github.com/redhat-developer/rhdh/pull/3932) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3932/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2001747429942104064)) - Job aborted: Job triggered.
- [PR #3934](https://github.com/redhat-developer/rhdh/pull/3934) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3934/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001878577871589376)) - Job aborted: Aborted by trigger plugin.
- [PR #3934](https://github.com/redhat-developer/rhdh/pull/3934) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3934/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001884357446340608)) - Job aborted: Aborted by trigger plugin.
- [PR #3934](https://github.com/redhat-developer/rhdh/pull/3934) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3934/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001879481169481728)) - Job aborted: Aborted by trigger plugin.
- [PR #3935](https://github.com/redhat-developer/rhdh/pull/3935) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3935/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001889323900735488)) - Job aborted: Aborted by trigger plugin.
- [PR #3935](https://github.com/redhat-developer/rhdh/pull/3935) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3935/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001891884452024320)) - Job aborted: Job triggered.
- [PR #3935](https://github.com/redhat-developer/rhdh/pull/3935) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3935/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001887926891319296)) - Job aborted: Aborted by trigger plugin.
- [PR #3935](https://github.com/redhat-developer/rhdh/pull/3935) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3935/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001887341416812544)) - Job aborted: Aborted by trigger plugin.
- [PR #3938](https://github.com/redhat-developer/rhdh/pull/3938) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3938/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2002034465764806656)) - Job aborted: Job triggered.
- [PR #3940](https://github.com/redhat-developer/rhdh/pull/3940) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3940/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2002052565071564800)) - Job aborted: Aborted by trigger plugin.
- [PR #3940](https://github.com/redhat-developer/rhdh/pull/3940) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3940/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2002028890863702016)) - Job aborted: Job triggered.
- [PR #3940](https://github.com/redhat-developer/rhdh/pull/3940) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3940/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2002042521974214656)) - Job aborted: Aborted by trigger plugin.
- [PR #3941](https://github.com/redhat-developer/rhdh/pull/3941) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3941/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2002098625227788288)) - Job aborted: Job triggered.
- [PR #3942](https://github.com/redhat-developer/rhdh/pull/3942) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3942/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2002128855850029056)) - Job aborted: Job triggered.
- [PR #3945](https://github.com/redhat-developer/rhdh/pull/3945) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3945/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2003129032358498304)) - Job aborted: Aborted by trigger plugin.
- [PR #3945](https://github.com/redhat-developer/rhdh/pull/3945) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3945/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2003133141740425216)) - Job aborted: Aborted by trigger plugin.
- [PR #3945](https://github.com/redhat-developer/rhdh/pull/3945) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3945/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2003128348766638080)) - Job aborted: Aborted by trigger plugin.
- [PR #3946](https://github.com/redhat-developer/rhdh/pull/3946) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3946/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2003379253369901056)) - Job aborted: Job triggered.
- [PR #3946](https://github.com/redhat-developer/rhdh/pull/3946) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3946/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2003378676518883328)) - Job aborted: Aborted by trigger plugin.
- [PR #3947](https://github.com/redhat-developer/rhdh/pull/3947) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3947/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009695363618836480)) - Job aborted: Aborted by trigger plugin.
- [PR #3947](https://github.com/redhat-developer/rhdh/pull/3947) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3947/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2005919530953478144)) - Job aborted: Job triggered.
- [PR #3947](https://github.com/redhat-developer/rhdh/pull/3947) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3947/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009697053524889600)) - Job aborted: Job triggered.
- [PR #3947](https://github.com/redhat-developer/rhdh/pull/3947) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3947/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2006035112633831424)) - Job aborted: Job triggered.
- [PR #3947](https://github.com/redhat-developer/rhdh/pull/3947) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3947/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009336481331548160)) - Job aborted: Aborted by trigger plugin.
- [PR #3947](https://github.com/redhat-developer/rhdh/pull/3947) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3947/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009336384170496000)) - Job aborted: Aborted by trigger plugin.
- [PR #3947](https://github.com/redhat-developer/rhdh/pull/3947) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3947/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009696151741140992)) - Job aborted: Aborted by trigger plugin.
- [PR #3947](https://github.com/redhat-developer/rhdh/pull/3947) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3947/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2005954727325470720)) - Job aborted: Job triggered.
- [PR #3947](https://github.com/redhat-developer/rhdh/pull/3947) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3947/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009337347862171648)) - Job aborted: Job triggered.
- [PR #3949](https://github.com/redhat-developer/rhdh/pull/3949) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3949/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2007807218312810496)) - Job aborted: Job triggered.
- [PR #3951](https://github.com/redhat-developer/rhdh/pull/3951) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3951/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009157293765038080)) - Job aborted: Aborted by trigger plugin.
- [PR #3951](https://github.com/redhat-developer/rhdh/pull/3951) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3951/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009516556194680832)) - Job aborted: Aborted by trigger plugin.
- [PR #3951](https://github.com/redhat-developer/rhdh/pull/3951) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3951/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008795947865214976)) - Job aborted: Job triggered.
- [PR #3951](https://github.com/redhat-developer/rhdh/pull/3951) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3951/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009522933327728640)) - Job aborted: Job triggered.
- [PR #3951](https://github.com/redhat-developer/rhdh/pull/3951) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3951/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009503484969226240)) - Job aborted: Job triggered.
- [PR #3951](https://github.com/redhat-developer/rhdh/pull/3951) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3951/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009162000034172928)) - Job aborted: Job triggered.
- [PR #3951](https://github.com/redhat-developer/rhdh/pull/3951) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3951/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008899035741556736)) - Job aborted: Job triggered.
- [PR #3955](https://github.com/redhat-developer/rhdh/pull/3955) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3955/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2008254826739142656)) - Job aborted: Aborted by trigger plugin.
- [PR #3955](https://github.com/redhat-developer/rhdh/pull/3955) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3955/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2008254860188717056)) - Job aborted: Job triggered.
- [PR #3955](https://github.com/redhat-developer/rhdh/pull/3955) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3955/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2008255070625337344)) - Job aborted: Aborted by trigger plugin.
- [PR #3955](https://github.com/redhat-developer/rhdh/pull/3955) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3955/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2008254732832870400)) - Job aborted: Aborted by trigger plugin.
- [PR #3955](https://github.com/redhat-developer/rhdh/pull/3955) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3955/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2008254782145302528)) - Job aborted: Aborted by trigger plugin.
- [PR #3957](https://github.com/redhat-developer/rhdh/pull/3957) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3957/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2008258528480858112)) - Job aborted: Aborted by trigger plugin.
- [PR #3960](https://github.com/redhat-developer/rhdh/pull/3960) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3960/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008288762773114880)) - Job aborted: Aborted by trigger plugin.
- [PR #3960](https://github.com/redhat-developer/rhdh/pull/3960) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3960/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008609380009775104)) - Job aborted: Job triggered.
- [PR #3960](https://github.com/redhat-developer/rhdh/pull/3960) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3960/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008584238600818688)) - Job aborted: Job triggered.
- [PR #3960](https://github.com/redhat-developer/rhdh/pull/3960) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3960/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008294675470880768)) - Job aborted: Job triggered.
- [PR #3960](https://github.com/redhat-developer/rhdh/pull/3960) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3960/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008583964708573184)) - Job aborted: Aborted by trigger plugin.
- [PR #3960](https://github.com/redhat-developer/rhdh/pull/3960) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3960/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008284907863805952)) - Job aborted: Aborted by trigger plugin.
- [PR #3960](https://github.com/redhat-developer/rhdh/pull/3960) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3960/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008573462569816064)) - Job aborted: Job triggered.
- [PR #3960](https://github.com/redhat-developer/rhdh/pull/3960) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3960/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008942414651199488)) - Job aborted: Aborted by trigger plugin.
- [PR #3963](https://github.com/redhat-developer/rhdh/pull/3963) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3963/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008588408225533952)) - Job aborted: Job triggered.
- [PR #3966](https://github.com/redhat-developer/rhdh/pull/3966) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3966/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008886224034467840)) - Job aborted: Aborted by trigger plugin.
- [PR #3966](https://github.com/redhat-developer/rhdh/pull/3966) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3966/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008892550693261312)) - Job aborted: Job triggered.
- [PR #3966](https://github.com/redhat-developer/rhdh/pull/3966) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3966/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008829056899878912)) - Job aborted: Job triggered.
- [PR #3968](https://github.com/redhat-developer/rhdh/pull/3968) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3968/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009314197086670848)) - Job aborted: Job triggered.
- [PR #3969](https://github.com/redhat-developer/rhdh/pull/3969) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3969/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2009320000678006784)) - Job aborted: Job triggered.
- [PR #3970](https://github.com/redhat-developer/rhdh/pull/3970) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3970/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009539978605891584)) - Job aborted: Job triggered.
- [PR #3970](https://github.com/redhat-developer/rhdh/pull/3970) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3970/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009618902174142464)) - Job aborted: Job triggered.
- [PR #3970](https://github.com/redhat-developer/rhdh/pull/3970) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3970/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009553753698471936)) - Job aborted: Aborted by trigger plugin.
- [PR #3970](https://github.com/redhat-developer/rhdh/pull/3970) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3970/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009563845873373184)) - Job aborted: Job triggered.
- [PR #3970](https://github.com/redhat-developer/rhdh/pull/3970) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3970/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009390896642002944)) - Job aborted: Job triggered.
- [PR #3972](https://github.com/redhat-developer/rhdh/pull/3972) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3972/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2010024202349842432)) - Job aborted: Job triggered.
- [PR #3973](https://github.com/redhat-developer/rhdh/pull/3973) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3973/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009605594574491648)) - Job aborted: Aborted by trigger plugin.
- [PR #3973](https://github.com/redhat-developer/rhdh/pull/3973) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3973/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009685842250960896)) - Job aborted: Aborted by trigger plugin.
- [PR #3973](https://github.com/redhat-developer/rhdh/pull/3973) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3973/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009687709437661184)) - Job aborted: Job triggered.
- [PR #3973](https://github.com/redhat-developer/rhdh/pull/3973) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3973/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009607305577893888)) - Job aborted: Job triggered.
- [PR #3974](https://github.com/redhat-developer/rhdh/pull/3974) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3974/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2009351899735658496)) - Job aborted: Aborted by trigger plugin.
- [PR #3974](https://github.com/redhat-developer/rhdh/pull/3974) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3974/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2009352055088484352)) - Job aborted: Job triggered.
- [PR #3975](https://github.com/redhat-developer/rhdh/pull/3975) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3975/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009383890652762112)) - Job aborted: Job triggered.
- [PR #3975](https://github.com/redhat-developer/rhdh/pull/3975) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3975/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009383820054237184)) - Job aborted: Aborted by trigger plugin.
- [PR #3975](https://github.com/redhat-developer/rhdh/pull/3975) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3975/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009383791528775680)) - Job aborted: Aborted by trigger plugin.
- [PR #3975](https://github.com/redhat-developer/rhdh/pull/3975) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3975/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009383855139590144)) - Job aborted: Aborted by trigger plugin.
- [PR #3976](https://github.com/redhat-developer/rhdh/pull/3976) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3976/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2009383958906671104)) - Job aborted: Aborted by trigger plugin.
- [PR #3976](https://github.com/redhat-developer/rhdh/pull/3976) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3976/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2009384017060696064)) - Job aborted: Aborted by trigger plugin.
- [PR #3976](https://github.com/redhat-developer/rhdh/pull/3976) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3976/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2009384050086645760)) - Job aborted: Job triggered.
- [PR #3976](https://github.com/redhat-developer/rhdh/pull/3976) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3976/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2009383989604782080)) - Job aborted: Aborted by trigger plugin.
- [PR #3978](https://github.com/redhat-developer/rhdh/pull/3978) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3978/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009387692365713408)) - Job aborted: Job triggered.
- [PR #3981](https://github.com/redhat-developer/rhdh/pull/3981) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3981/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009566596527296512)) - Job aborted: Job triggered.
- [PR #3982](https://github.com/redhat-developer/rhdh/pull/3982) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3982/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009730254859407360)) - Job aborted: Job triggered.
- [PR #3982](https://github.com/redhat-developer/rhdh/pull/3982) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3982/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2010014875543146496)) - Job aborted: Aborted by trigger plugin.
- [PR #3982](https://github.com/redhat-developer/rhdh/pull/3982) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3982/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2010014735759577088)) - Job aborted: Job triggered.
- [PR #3982](https://github.com/redhat-developer/rhdh/pull/3982) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3982/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009730415912292352)) - Job aborted: Aborted by trigger plugin.
- [PR #3982](https://github.com/redhat-developer/rhdh/pull/3982) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3982/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2010015405069832192)) - Job aborted: Job triggered.
- [PR #3982](https://github.com/redhat-developer/rhdh/pull/3982) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3982/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009730719760257024)) - Job aborted: Job triggered.
- [PR #3982](https://github.com/redhat-developer/rhdh/pull/3982) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3982/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2010502823271206912)) - Job aborted: Job triggered.
- [PR #3984](https://github.com/redhat-developer/rhdh/pull/3984) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3984/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009987753898414080)) - Job aborted: Aborted by trigger plugin.
- [PR #3984](https://github.com/redhat-developer/rhdh/pull/3984) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3984/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009991025866575872)) - Job aborted: Job triggered.

## Test Failures

**69 CI runs with test failures** ([see detailed test analysis](#most-common-playwright-test-failures))

- [PR #3917](https://github.com/redhat-developer/rhdh/pull/3917) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3917/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001247942169595904)) - Playwright tests ran but some failed (128 tests, 3 workers)
- [PR #3919](https://github.com/redhat-developer/rhdh/pull/3919) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3919/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2000938859113746432)) - Playwright tests ran but some failed (128 tests, 3 workers)
- [PR #3920](https://github.com/redhat-developer/rhdh/pull/3920) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3920/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2000993191729303552)) - Playwright tests ran but some failed (128 tests, 3 workers)
- [PR #3920](https://github.com/redhat-developer/rhdh/pull/3920) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3920/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2001006710361165824)) - Playwright tests ran but some failed (128 tests, 3 workers)
- [PR #3921](https://github.com/redhat-developer/rhdh/pull/3921) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3921/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009699183119831040)) - Playwright tests ran but some failed (128 tests, 3 workers)
- [PR #3921](https://github.com/redhat-developer/rhdh/pull/3921) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3921/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2000965931152445440)) - Playwright tests ran but some failed (128 tests, 3 workers)
- [PR #3921](https://github.com/redhat-developer/rhdh/pull/3921) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3921/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2000952053215531008)) - Playwright tests ran but some failed (128 tests, 3 workers)
- [PR #3921](https://github.com/redhat-developer/rhdh/pull/3921) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3921/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009646407065014272)) - Playwright tests ran but some failed (128 tests, 3 workers)
- [PR #3921](https://github.com/redhat-developer/rhdh/pull/3921) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3921/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2000980701146517504)) - Playwright tests ran but some failed (128 tests, 3 workers)
- [PR #3921](https://github.com/redhat-developer/rhdh/pull/3921) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3921/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008767932309442560)) - Playwright tests ran but some failed (128 tests, 3 workers)
- [PR #3921](https://github.com/redhat-developer/rhdh/pull/3921) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3921/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008484583137349632)) - Playwright tests ran but some failed (128 tests, 3 workers)
- [PR #3921](https://github.com/redhat-developer/rhdh/pull/3921) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3921/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009267102648635392)) - Playwright tests ran but some failed (128 tests, 3 workers)
- [PR #3921](https://github.com/redhat-developer/rhdh/pull/3921) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3921/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009217192406552576)) - Playwright tests ran but some failed (128 tests, 3 workers)
- [PR #3921](https://github.com/redhat-developer/rhdh/pull/3921) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3921/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009688341083066368)) - Playwright tests ran but some failed (128 tests, 3 workers)
- [PR #3921](https://github.com/redhat-developer/rhdh/pull/3921) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3921/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009251130374098944)) - Playwright tests ran but some failed (128 tests, 3 workers)
- [PR #3921](https://github.com/redhat-developer/rhdh/pull/3921) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3921/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2008498577478782976)) - Playwright tests ran but some failed (128 tests, 3 workers)
- [PR #3921](https://github.com/redhat-developer/rhdh/pull/3921) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3921/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009506958431752192)) - Playwright tests ran but some failed (128 tests, 3 workers)
- [PR #3921](https://github.com/redhat-developer/rhdh/pull/3921) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3921/pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm/2009230934745812992)) - Playwright tests ran but some failed (128 tests, 3 workers)
- [PR #3923](https://github.com/redhat-developer/rhdh/pull/3923) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3923/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2001425103732084736)) - Playwright tests ran but some failed (121 tests, 3 workers)
- [PR #3923](https://github.com/redhat-developer/rhdh/pull/3923) ([job logs](https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/redhat-developer_rhdh/3923/pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm/2001279001389174784)) - Playwright tests ran but some failed (121 tests, 3 workers)
- ... and 49 more

## Most Common Playwright Test Failures

**Total test case failures:** 415

### Top Failing Test Cases

| Rank | Count | Test Name | Affected PRs |
|------|-------|-----------|--------------|
| 1 | 18 | Test Adoption Insights › Test Adoption Insights plugin: load permission policies | 3949, 3951, 3966, 3973 |
| 2 | 16 | Test Kubernetes Plugin › Verify that a user with permissions is able to access t | 3947, 3951, 3973 |
| 3 | 13 | Test RBAC › Test RBAC plugin as an admin user › Edit users and groups and update | 3921, 3947, 3964, 3970, 3973 (+1) |
| 4 | 12 | Test Kubernetes Plugin › Verify that a user without permissions is not able to a | 3947, 3951, 3973 |
| 5 | 9 | Test Topology Plugin with RBAC › Verify a user without permissions is not able t | 3947, 3973 |
| 6 | 9 | Test Topology Plugin with RBAC › Verify a user with permissions is able to acces | 3947, 3973 |
| 7 | 9 | Test Topology Plugin with RBAC › Verify a user with permissions is able to acces | 3947, 3973 |
| 8 | 9 | Test global floating action button plugin › Check if Git and Bulk import floatin | 3949, 3951, 3970, 3973, 3980 |
| 9 | 8 | Test Orchestrator RBAC › Test Orchestrator RBAC: Global Workflow Access › Test g | 3923 |
| 10 | 7 | Mark notification tests › Mark notification as read | 3920, 3947, 3949, 3966 |
| 11 | 7 | Filter critical notification tests › Filter notifications by severity - High | 3921, 3947, 3949, 3966 |
| 12 | 7 | Mark notification tests › Mark notification as saved | 3927, 3947, 3949, 3966 |
| 13 | 7 | Test RBAC › Test RBAC plugin as an admin user › Create and edit a role from the  | 3947, 3973 |
| 14 | 7 | Test RBAC › Test RBAC ownership conditional rule › Create a role with the `IsOwn | 3947, 3973 |
| 15 | 7 | Filter critical notification tests › Filter notifications by severity - Critical | 3947, 3949, 3964, 3966 |
| 16 | 7 | Filter critical notification tests › Filter notifications by severity - Normal | 3947, 3948, 3949, 3966 |
| 17 | 7 | Mark notification tests › Mark notification as unread | 3947, 3949, 3951, 3966 |
| 18 | 6 | Scorecard Plugin Tests › Displays error state for unavailable data while renderi | 3921 |
| 19 | 6 | Test RBAC › Test RBAC plugin: $currentUser alias used in conditional access poli | 3947 |
| 20 | 6 | Scorecard Plugin Tests › Import component and validate scorecard tabs for GitHub | 3947 |

### Most Problematic Spec Files

| Rank | Failures | Spec File |
|------|----------|-----------|
| 1 | 51 | `e2e/plugins/rbac/rbac.spec.ts` |
| 2 | 28 | `e2e/plugins/kubernetes/kubernetes-rbac.spec.ts` |
| 3 | 28 | `e2e/default-global-header.spec.ts` |
| 4 | 27 | `e2e/plugins/notifications/filter-notifications-by-severity.spec.ts` |
| 5 | 27 | `e2e/plugins/topology/topology-rbac.spec.ts` |
| 6 | 23 | `e2e/plugins/adoption-insights/adoption-insights.spec.ts` |
| 7 | 22 | `e2e/extensions.spec.ts` |
| 8 | 21 | `e2e/plugins/notifications/mark-notifications.spec.ts` |
| 9 | 17 | `e2e/plugins/global-floating-button.spec.ts` |
| 10 | 17 | `e2e/techdocs.spec.ts` |
| 11 | 16 | `e2e/plugins/licensed-users-info-backend/licensed-users-info.spec.ts` |
| 12 | 14 | `e2e/plugins/scorecard/scorecard.spec.ts` |
| 13 | 13 | `e2e/github-events-module.spec.ts` |
| 14 | 11 | `e2e/catalog-timestamp.spec.ts` |
| 15 | 9 | `e2e/plugins/orchestrator/orchestrator-rbac.spec.ts` |

### Failures by Error Type

| Error Type | Count | Percentage |
|------------|-------|------------|
| TimeoutError | 366 | 88% |
| Error | 45 | 10% |
| TypeError | 4 | 0% |

### Detailed Breakdown of Top 10 Failing Tests

#### 1. Test Adoption Insights › Test Adoption Insights plugin: load permission policies and conditions from files › Check UI navigation by nav bar when adoption-insights is enabled

- **Spec File:** `e2e/plugins/adoption-insights/adoption-insights.spec.ts`
- **Failure Count:** 18
- **Error Type:** TimeoutError
- **Sample Error:** `adoption-insights.spec.ts:45:5 Check UI navigation by nav bar when adoption-insights is enabled`
- **Affected PRs:** 3949, 3951, 3966, 3973

#### 2. Test Kubernetes Plugin › Verify that a user with permissions is able to access the Kubernetes plugin › Verify pod logs visibility in the Kubernetes tab

- **Spec File:** `e2e/plugins/kubernetes/kubernetes-rbac.spec.ts`
- **Failure Count:** 16
- **Error Type:** TimeoutError
- **Sample Error:** `kubernetes-rbac.spec.ts:50:5 Verify pod logs visibility in the Kubernetes tab`
- **Affected PRs:** 3947, 3951, 3973

#### 3. Test RBAC › Test RBAC plugin as an admin user › Edit users and groups and update policies of a role from the overview page

- **Spec File:** `e2e/plugins/rbac/rbac.spec.ts`
- **Failure Count:** 13
- **Error Type:** TimeoutError
- **Sample Error:** `rbac.spec.ts:405:5 Edit users and groups and update policies of a role from the overview page`
- **Affected PRs:** 3921, 3947, 3964, 3970, 3973, 3982

#### 4. Test Kubernetes Plugin › Verify that a user without permissions is not able to access parts of the Kubernetes plugin › Verify pod logs are not visible in the Kubernetes tab

- **Spec File:** `e2e/plugins/kubernetes/kubernetes-rbac.spec.ts`
- **Failure Count:** 12
- **Error Type:** TimeoutError
- **Sample Error:** `kubernetes-rbac.spec.ts:79:5 Verify pod logs are not visible in the Kubernetes tab`
- **Affected PRs:** 3947, 3951, 3973

#### 5. Test Topology Plugin with RBAC › Verify a user without permissions is not able to access parts of the Topology plugin › Verify pod logs are not visible in the Topology tab

- **Spec File:** `e2e/plugins/topology/topology-rbac.spec.ts`
- **Failure Count:** 9
- **Error Type:** TimeoutError
- **Sample Error:** `topology-rbac.spec.ts:52:5 Verify pod logs are not visible in the Topology tab`
- **Affected PRs:** 3947, 3973

#### 6. Test Topology Plugin with RBAC › Verify a user with permissions is able to access the Topology plugin › Verify pods visibility in the Topology tab

- **Spec File:** `e2e/plugins/topology/topology-rbac.spec.ts`
- **Failure Count:** 9
- **Error Type:** TimeoutError
- **Sample Error:** `topology-rbac.spec.ts:76:5 Verify pods visibility in the Topology tab`
- **Affected PRs:** 3947, 3973

#### 7. Test Topology Plugin with RBAC › Verify a user with permissions is able to access the Topology plugin › Verify pod logs visibility in the Topology tab

- **Spec File:** `e2e/plugins/topology/topology-rbac.spec.ts`
- **Failure Count:** 9
- **Error Type:** TimeoutError
- **Sample Error:** `topology-rbac.spec.ts:80:5 Verify pod logs visibility in the Topology tab`
- **Affected PRs:** 3947, 3973

#### 8. Test global floating action button plugin › Check if Git and Bulk import floating buttons are visible on the Home page

- **Spec File:** `e2e/plugins/global-floating-button.spec.ts`
- **Failure Count:** 9
- **Error Type:** TimeoutError
- **Sample Error:** `global-floating-button.spec.ts:26:3 Check if Git and Bulk import floating buttons are visible on the Home page`
- **Affected PRs:** 3949, 3951, 3970, 3973, 3980

#### 9. Test Orchestrator RBAC › Test Orchestrator RBAC: Global Workflow Access › Test global orchestrator workflow access is allowed

- **Spec File:** `e2e/plugins/orchestrator/orchestrator-rbac.spec.ts`
- **Failure Count:** 8
- **Error Type:** Error
- **Sample Error:** `orchestrator-rbac.spec.ts:112:5 Test global orchestrator workflow access is allowed`
- **Affected PRs:** 3923

#### 10. Mark notification tests › Mark notification as read

- **Spec File:** `e2e/plugins/notifications/mark-notifications.spec.ts`
- **Failure Count:** 7
- **Error Type:** TimeoutError
- **Sample Error:** `mark-notifications.spec.ts:19:3 Mark notification as read`
- **Affected PRs:** 3920, 3947, 3949, 3966
