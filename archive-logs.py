#!/usr/bin/env python3
"""Archive CI logs by gzipping all uncompressed files in ci-logs directory."""

import argparse
import gzip
import os
import sys

# Gzip magic bytes
GZIP_MAGIC = b"\x1f\x8b"


def is_gzipped(filepath: str) -> bool:
    """Check if a file is already gzip compressed by reading magic bytes."""
    try:
        with open(filepath, "rb") as f:
            magic = f.read(2)
            return magic == GZIP_MAGIC
    except (IOError, OSError):
        return False


def get_file_size(filepath: str) -> int:
    """Get file size in bytes."""
    try:
        return os.path.getsize(filepath)
    except OSError:
        return 0


def gzip_file(filepath: str) -> tuple[bool, int, int]:
    """
    Gzip a file in place.

    Returns:
        tuple of (success, original_size, compressed_size)
    """
    try:
        original_size = get_file_size(filepath)

        with open(filepath, "rb") as f:
            data = f.read()

        with gzip.open(filepath, "wb", compresslevel=9) as f:
            f.write(data)

        compressed_size = get_file_size(filepath)
        return True, original_size, compressed_size
    except Exception as e:
        print(f"Error gzipping {filepath}: {e}")
        return False, 0, 0


def find_uncompressed_files(directory: str, skip_extensions: set[str] | None = None) -> list[str]:
    """
    Find all files that are not gzip compressed.

    Args:
        directory: Directory to scan
        skip_extensions: File extensions to skip (e.g., {'.gz', '.webm', '.png'})

    Returns:
        List of file paths that are not gzip compressed
    """
    if skip_extensions is None:
        skip_extensions = set()

    uncompressed_files = []

    for root, _, files in os.walk(directory):
        for filename in files:
            # Skip files with certain extensions
            _, ext = os.path.splitext(filename)
            if ext.lower() in skip_extensions:
                continue

            filepath = os.path.join(root, filename)

            # Skip if already gzipped
            if is_gzipped(filepath):
                continue

            # Skip empty files
            if get_file_size(filepath) == 0:
                continue

            uncompressed_files.append(filepath)

    return uncompressed_files


def format_size(size_bytes: int) -> str:
    """Format bytes as human-readable string."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def main():
    parser = argparse.ArgumentParser(
        description="Archive CI logs by gzipping all uncompressed files."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default="ci-logs",
        help="Directory to archive (default: ci-logs)",
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Show what would be compressed without actually compressing",
    )
    parser.add_argument(
        "--include-binary",
        action="store_true",
        help="Include binary formats that don't compress well (.webm, .png, .jpg, .jpeg, .gif, .mp4, .zip)",
    )
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a directory")
        sys.exit(1)

    # Extensions to skip - these are already compressed or binary
    skip_extensions = {".gz", ".gzip"}
    if not args.include_binary:
        skip_extensions.update({".webm", ".png", ".jpg", ".jpeg", ".gif", ".mp4", ".zip"})

    print(f"Scanning {args.directory} for uncompressed files...")
    uncompressed_files = find_uncompressed_files(args.directory, skip_extensions)
    print(f"Found {len(uncompressed_files)} uncompressed files")

    if not uncompressed_files:
        print("Nothing to compress.")
        return

    if args.dry_run:
        print("\nDry run - would compress:")
        total_size = 0
        for filepath in uncompressed_files:
            size = get_file_size(filepath)
            total_size += size
            print(f"  {filepath} ({format_size(size)})")
        print(f"\nTotal: {len(uncompressed_files)} files, {format_size(total_size)}")
        return

    success_count = 0
    error_count = 0
    total_original = 0
    total_compressed = 0

    for i, filepath in enumerate(uncompressed_files, 1):
        success, original_size, compressed_size = gzip_file(filepath)
        if success:
            success_count += 1
            total_original += original_size
            total_compressed += compressed_size
            savings = original_size - compressed_size
            pct = (savings / original_size * 100) if original_size > 0 else 0
            print(
                f"[{i}/{len(uncompressed_files)}] Compressed: {filepath} "
                f"({format_size(original_size)} -> {format_size(compressed_size)}, -{pct:.0f}%)"
            )
        else:
            error_count += 1

    print(f"\nDone!")
    print(f"  Compressed: {success_count} files")
    print(f"  Errors: {error_count} files")
    if total_original > 0:
        total_savings = total_original - total_compressed
        pct = total_savings / total_original * 100
        print(f"  Space saved: {format_size(total_savings)} ({pct:.1f}%)")
        print(f"  Original size: {format_size(total_original)}")
        print(f"  Compressed size: {format_size(total_compressed)}")


if __name__ == "__main__":
    main()
