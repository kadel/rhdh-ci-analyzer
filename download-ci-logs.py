#!/usr/bin/env python3
"""
Script to download CI logs for a specific job from GCS.
Usage: python download-ci-logs.py [output_directory]

Rewritten from download-ci-logs.sh using google-cloud-storage library.
"""

import argparse
import fnmatch
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from google.cloud import storage
from google.cloud.storage import transfer_manager


# Configuration
BUCKET_NAME = "test-platform-results"
BUCKET_PREFIX = "pr-logs/pull/redhat-developer_rhdh"
JOB_NAMES = [
    "pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm",
    "pull-ci-redhat-developer-rhdh-release-1.8-e2e-ocp-helm",
]
EXCLUDE_PATTERNS = ["*gather-extra*", "*gather-audit-logs*"]
MEDIA_EXCLUDE_PATTERNS = [
    "*trace.zip",    # Playwright traces (~102G)
    "*.webm",        # Test videos (~77G)
    "*.tar",         # must-gather tarballs (~32G)
    "*.png",         # Screenshots (~2.5G)
    "*.gstmp",       # Temp/staging files (~3G)
]
MAX_PRS = 200
MAX_WORKERS = 10


def list_prs(client: storage.Client, bucket_name: str, prefix: str, max_prs: int) -> list[str]:
    """List all PR directories from the bucket."""
    # Use delimiter to get only the top-level directories (PRs)
    blobs = client.list_blobs(bucket_name, prefix=f"{prefix}/", delimiter="/")
    
    # We need to iterate to populate prefixes
    list(blobs)  # Consume the iterator to get prefixes
    
    # Extract PR numbers from prefixes
    # prefix format: "pr-logs/pull/redhat-developer_rhdh/1234/"
    pr_numbers = [
        parts[-1]
        for blob_prefix in blobs.prefixes
        if (parts := blob_prefix.rstrip("/").split("/")) and parts[-1].isdigit()
    ]
    
    # Sort by PR number descending and limit
    pr_numbers.sort(key=int, reverse=True)
    return pr_numbers[:max_prs]


def should_exclude(blob_name: str, patterns: list[str]) -> bool:
    """Check if blob matches any exclude pattern."""
    return any(fnmatch.fnmatch(blob_name, pattern) for pattern in patterns)


def download_pr_job(
    client: storage.Client,
    bucket_name: str,
    bucket_prefix: str,
    pr: str,
    job_name: str,
    output_dir: Path,
    exclude_patterns: list[str],
) -> tuple[str, str, bool, int]:
    """Download all logs for a specific PR and job.
    
    Returns: (pr, job_name, success, file_count)
    """
    job_prefix = f"{bucket_prefix}/{pr}/{job_name}/"
    local_path = output_dir / pr / job_name
    
    # List all blobs for this job
    blobs = list(client.list_blobs(bucket_name, prefix=job_prefix))
    
    if not blobs:
        return (pr, job_name, False, 0)
    
    # Filter out excluded blobs
    blobs_to_download = [
        blob for blob in blobs
        if not should_exclude(blob.name, exclude_patterns)
    ]
    
    if not blobs_to_download:
        return (pr, job_name, False, 0)
    
    # Create local directory
    local_path.mkdir(parents=True, exist_ok=True)
    
    # Prepare blob-file pairs for download
    blob_file_pairs = []
    for blob in blobs_to_download:
        # Calculate relative path from job prefix
        relative_path = blob.name[len(job_prefix):]
        if not relative_path:  # Skip if it's a directory marker
            continue
        
        local_file = local_path / relative_path
        local_file.parent.mkdir(parents=True, exist_ok=True)
        blob_file_pairs.append((blob, str(local_file)))
    
    if not blob_file_pairs:
        return (pr, job_name, False, 0)
    
    # Download files using transfer manager
    try:
        results = transfer_manager.download_many(
            blob_file_pairs,
            max_workers=4,
            skip_if_exists=True,
        )
        
        # Count successful downloads
        success_count = sum(1 for r in results if not isinstance(r, Exception))
        return (pr, job_name, True, success_count)
    
    except Exception as e:
        print(f"  PR #{pr}: Warning: Failed to download some files for {job_name}: {e}")
        return (pr, job_name, False, 0)


def download_pr(
    client: storage.Client,
    bucket_name: str,
    bucket_prefix: str,
    pr: str,
    job_names: list[str],
    output_dir: Path,
    exclude_patterns: list[str],
) -> tuple[str, bool]:
    """Download all jobs for a PR.
    
    Returns: (pr, found_any)
    """
    found_any = False
    
    for job_name in job_names:
        job_prefix = f"{bucket_prefix}/{pr}/{job_name}/"
        
        # Quick check if job exists by listing with max_results=1
        blobs = list(client.list_blobs(bucket_name, prefix=job_prefix, max_results=1))
        
        if blobs:
            print(f"PR #{pr}: Found job {job_name}, downloading runs...")
            _, _, success, file_count = download_pr_job(
                client, bucket_name, bucket_prefix, pr, job_name, output_dir, exclude_patterns
            )
            if success:
                print(f"  PR #{pr}: Downloaded {file_count} file(s) for {job_name}")
                found_any = True
        else:
            print(f"PR #{pr}: Skipped - job {job_name} not found")
    
    return (pr, found_any)


def main():
    parser = argparse.ArgumentParser(
        description="Download CI logs for specific jobs from GCS"
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default="./ci-logs",
        help="Output directory for downloaded logs (default: ./ci-logs)",
    )
    parser.add_argument(
        "--max-prs",
        type=int,
        default=MAX_PRS,
        help=f"Maximum number of PRs to process (default: {MAX_PRS})",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=MAX_WORKERS,
        help=f"Maximum parallel workers (default: {MAX_WORKERS})",
    )
    parser.add_argument(
        "--job-names",
        nargs="+",
        default=JOB_NAMES,
        help="Job names to download",
    )
    parser.add_argument(
        "--exclude-media",
        action="store_true",
        help="Exclude large media files (traces, videos, screenshots, tarballs) to save ~90%% storage",
    )

    args = parser.parse_args()

    # Build exclude patterns
    exclude_patterns = EXCLUDE_PATTERNS.copy()
    if args.exclude_media:
        exclude_patterns.extend(MEDIA_EXCLUDE_PATTERNS)
    
    output_dir = Path(args.output_dir)
    
    print(f"Downloading logs for jobs: {', '.join(args.job_names)}")
    print(f"Output directory: {output_dir}")
    print("-" * 40)
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize storage client (anonymous for public bucket)
    client = storage.Client.create_anonymous_client()
    
    # List PRs
    print("Fetching list of PRs...")
    pr_list = list_prs(client, BUCKET_NAME, BUCKET_PREFIX, args.max_prs)
    
    if not pr_list:
        print("No PRs found or unable to access bucket")
        sys.exit(1)
    
    print(f"Found {len(pr_list)} PRs")
    print("-" * 40)
    
    downloaded = 0
    skipped = 0
    
    # Process PRs in parallel
    print(f"Running downloads in parallel (max {args.max_workers} jobs)...")
    
    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        futures = {
            executor.submit(
                download_pr,
                client,
                BUCKET_NAME,
                BUCKET_PREFIX,
                pr,
                args.job_names,
                output_dir,
                exclude_patterns,
            ): pr
            for pr in pr_list
        }
        
        for future in as_completed(futures):
            pr = futures[future]
            try:
                _, found_any = future.result()
                if found_any:
                    downloaded += 1
                else:
                    skipped += 1
            except Exception as e:
                print(f"PR #{pr}: Error processing: {e}")
                skipped += 1
    
    print("-" * 40)
    print("Complete!")
    print(f"PRs with job downloaded: {downloaded}")
    print(f"PRs without this job: {skipped}")
    print(f"Logs saved to: {output_dir}")


if __name__ == "__main__":
    main()

