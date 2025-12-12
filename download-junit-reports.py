#!/usr/bin/env python3
"""
Script to download junit-results.xml files for a specific job from GCS.

Usage: python download-junit-reports.py [output_directory] [max_workers]
"""

import argparse
import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from google.cloud import storage


# Configuration
BUCKET_NAME = "test-platform-results"
PREFIX = "pr-logs/pull/redhat-developer_rhdh"
JOB_NAME = "pull-ci-redhat-developer-rhdh-main-e2e-ocp-helm"

# Known paths to junit-results.xml files (relative to run directory)
JUNIT_PATHS = [
    "artifacts/e2e-ocp-helm/redhat-developer-rhdh-ocp-helm/artifacts/showcase/junit-results.xml",
    "artifacts/e2e-ocp-helm/redhat-developer-rhdh-ocp-helm/artifacts/showcase-rbac/junit-results.xml",
]


def list_pr_directories(client: storage.Client, bucket_name: str, prefix: str) -> list[str]:
    """List all PR directories in the bucket."""
    bucket = client.bucket(bucket_name)
    
    # Use delimiter to get only "directories" at this level
    blobs = client.list_blobs(bucket_name, prefix=f"{prefix}/", delimiter="/")
    
    # We need to consume the iterator to populate prefixes
    list(blobs)  # consume iterator
    
    # Extract PR numbers from prefixes
    pr_numbers = []
    for pr_prefix in blobs.prefixes:
        # pr_prefix looks like: "pr-logs/pull/redhat-developer_rhdh/1234/"
        pr_number = pr_prefix.rstrip("/").split("/")[-1]
        try:
            pr_numbers.append(int(pr_number))
        except ValueError:
            continue
    
    # Sort in reverse order (newest first)
    pr_numbers.sort(reverse=True)
    return [str(pr) for pr in pr_numbers]


def list_run_ids(client: storage.Client, bucket_name: str, pr: str) -> list[str]:
    """List all run IDs for a PR/job combination."""
    job_prefix = f"{PREFIX}/{pr}/{JOB_NAME}/"
    
    blobs = client.list_blobs(bucket_name, prefix=job_prefix, delimiter="/")
    
    # Consume iterator to populate prefixes
    list(blobs)
    
    run_ids = []
    for run_prefix in blobs.prefixes:
        # run_prefix looks like: ".../1999164066400047104/"
        run_id = run_prefix.rstrip("/").split("/")[-1]
        run_ids.append(run_id)
    
    return run_ids


def download_file(
    client: storage.Client,
    bucket_name: str,
    blob_path: str,
    local_path: Path,
) -> tuple[str, bool, str | None]:
    """
    Download a single file from GCS.
    
    Returns:
        Tuple of (blob_path, success, error_message)
    """
    try:
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_path)
        
        # Check if blob exists
        if not blob.exists():
            return (blob_path, False, "Not found")
        
        # Create local directory if needed
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Download the file
        blob.download_to_filename(str(local_path))
        return (blob_path, True, None)
        
    except Exception as e:
        return (blob_path, False, str(e))


def main():
    parser = argparse.ArgumentParser(
        description="Download junit-results.xml files from GCS"
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default="./ci-logs",
        help="Output directory (default: ./ci-logs)",
    )
    parser.add_argument(
        "max_workers",
        nargs="?",
        type=int,
        default=10,
        help="Maximum parallel downloads (default: 10)",
    )
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir)
    max_workers = args.max_workers
    
    print(f"Downloading junit reports for job: {JOB_NAME}")
    print(f"Output directory: {output_dir}")
    print(f"Max parallel downloads: {max_workers}")
    print("-" * 40)
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize GCS client (anonymous for public bucket)
    client = storage.Client.create_anonymous_client()
    
    # List all PR directories
    print("Fetching list of PRs...")
    pr_list = list_pr_directories(client, BUCKET_NAME, PREFIX)
    
    if not pr_list:
        print("No PRs found or unable to access bucket")
        sys.exit(1)
    
    print(f"Found {len(pr_list)} PRs")
    print("-" * 40)
    
    # Statistics
    downloaded = 0
    skipped = 0
    already_exists = 0
    
    # Collect all download tasks
    download_tasks: list[tuple[str, Path, str]] = []  # (blob_path, local_path, label)
    
    for pr in pr_list:
        local_pr_path = output_dir / pr
        
        # Skip if PR directory already exists locally
        if local_pr_path.exists():
            print(f"PR #{pr}: Already exists locally, skipping...")
            already_exists += 1
            continue
        
        # List run IDs for this PR/job
        run_ids = list_run_ids(client, BUCKET_NAME, pr)
        
        if run_ids:
            print(f"PR #{pr}: Found job, queueing junit files...")
            downloaded += 1
            
            for run_id in run_ids:
                for junit_path in JUNIT_PATHS:
                    blob_path = f"{PREFIX}/{pr}/{JOB_NAME}/{run_id}/{junit_path}"
                    local_path = output_dir / pr / JOB_NAME / run_id / junit_path
                    label = f"{pr}/{run_id}/{Path(junit_path).name}"
                    
                    download_tasks.append((blob_path, local_path, label))
        else:
            skipped += 1
    
    # Execute downloads in parallel
    if download_tasks:
        print(f"\nStarting {len(download_tasks)} downloads with {max_workers} workers...")
        
        downloaded_count = 0
        failed_count = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            futures = {
                executor.submit(
                    download_file, client, BUCKET_NAME, blob_path, local_path
                ): label
                for blob_path, local_path, label in download_tasks
            }
            
            # Process results as they complete
            for future in as_completed(futures):
                label = futures[future]
                blob_path, success, error = future.result()
                
                if success:
                    print(f"  Downloaded: {label}")
                    downloaded_count += 1
                else:
                    # Only print non-"not found" errors (files might not exist)
                    if error != "Not found":
                        print(f"  Failed: {label} - {error}")
                    failed_count += 1
        
        print(f"\nDownloaded {downloaded_count} files, {failed_count} not found/failed")
    
    print("-" * 40)
    print("Complete!")
    print(f"PRs downloaded: {downloaded}")
    print(f"PRs already existed locally: {already_exists}")
    print(f"PRs without this job: {skipped}")
    print(f"Logs saved to: {output_dir}")


if __name__ == "__main__":
    main()

