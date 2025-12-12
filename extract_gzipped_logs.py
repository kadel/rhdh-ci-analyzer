#!/usr/bin/env python3
"""Extract all gzipped build-log.txt files, overwriting with decompressed content."""

import gzip
import os
import subprocess


def find_gzipped_txt_files(directory: str) -> list[str]:
    """Find all .txt files that are actually gzip compressed."""
    gzipped_files = []

    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".txt"):
                filepath = os.path.join(root, filename)
                try:
                    result = subprocess.run(
                        ["file", filepath],
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    if "gzip" in result.stdout.lower():
                        gzipped_files.append(filepath)
                except subprocess.CalledProcessError:
                    continue

    return gzipped_files


def extract_gzipped_file(filepath: str) -> bool:
    """Extract a gzipped file, overwriting with decompressed content."""
    try:
        with gzip.open(filepath, "rb") as f:
            decompressed_data = f.read()

        with open(filepath, "wb") as f:
            f.write(decompressed_data)

        return True
    except Exception as e:
        print(f"Error extracting {filepath}: {e}")
        return False


def main():
    directory = "ci-logs"

    print(f"Scanning {directory} for gzipped .txt files...")
    gzipped_files = find_gzipped_txt_files(directory)
    print(f"Found {len(gzipped_files)} gzipped .txt files")

    success_count = 0
    error_count = 0

    for i, filepath in enumerate(gzipped_files, 1):
        if extract_gzipped_file(filepath):
            success_count += 1
            print(f"[{i}/{len(gzipped_files)}] Extracted: {filepath}")
        else:
            error_count += 1

    print(f"\nDone! Extracted: {success_count}, Errors: {error_count}")


if __name__ == "__main__":
    main()
