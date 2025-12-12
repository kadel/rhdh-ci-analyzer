#!/usr/bin/env python3
"""
Analyze JUnit XML test results and generate statistics of most failing tests.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict
import argparse
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TestFailure:
    """Represents a single test failure instance."""
    test_name: str
    classname: str
    message: str
    pr_number: str
    run_id: str
    file_path: str


@dataclass
class TestStats:
    """Statistics for a single test."""
    test_name: str
    classname: str
    failure_count: int = 0
    failures: list = field(default_factory=list)
    error_messages: list = field(default_factory=list)
    affected_prs: set = field(default_factory=set)


@dataclass
class AnalysisMetadata:
    """Metadata about the analysis run."""
    files_analyzed: int = 0
    prs_analyzed: set = field(default_factory=set)
    runs_analyzed: set = field(default_factory=set)


def extract_pr_and_run_from_path(file_path: str) -> tuple[str, str]:
    """Extract PR number and run ID from the file path."""
    parts = Path(file_path).parts
    pr_number = "unknown"
    run_id = "unknown"
    
    for i, part in enumerate(parts):
        if part.isdigit() and len(part) <= 5:  # PR numbers are typically short
            pr_number = part
        elif part.isdigit() and len(part) > 15:  # Run IDs are long numbers
            run_id = part
    
    return pr_number, run_id


def parse_junit_file(file_path: Path) -> list[TestFailure]:
    """Parse a JUnit XML file and extract all failures."""
    failures = []
    
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"  Warning: Could not parse {file_path}: {e}")
        return failures
    except Exception as e:
        print(f"  Warning: Error reading {file_path}: {e}")
        return failures
    
    pr_number, run_id = extract_pr_and_run_from_path(str(file_path))
    
    # Handle both <testsuites><testsuite>... and <testsuite>... formats
    if root.tag == "testsuites":
        testsuites = root.findall(".//testsuite")
    elif root.tag == "testsuite":
        testsuites = [root]
    else:
        testsuites = root.findall(".//testsuite")
    
    for testsuite in testsuites:
        for testcase in testsuite.findall("testcase"):
            test_name = testcase.get("name", "unknown")
            classname = testcase.get("classname", testsuite.get("name", "unknown"))
            
            # Check for failures
            failure = testcase.find("failure")
            if failure is not None:
                message = failure.get("message", "")
                if not message:
                    message = failure.text[:200] if failure.text else "No message"
                
                failures.append(TestFailure(
                    test_name=test_name,
                    classname=classname,
                    message=message,
                    pr_number=pr_number,
                    run_id=run_id,
                    file_path=str(file_path)
                ))
            
            # Check for errors (different from failures)
            error = testcase.find("error")
            if error is not None:
                message = error.get("message", "")
                if not message:
                    message = error.text[:200] if error.text else "No message"
                
                failures.append(TestFailure(
                    test_name=test_name,
                    classname=classname,
                    message=f"[ERROR] {message}",
                    pr_number=pr_number,
                    run_id=run_id,
                    file_path=str(file_path)
                ))
    
    return failures


def find_junit_files(base_path: Path, pattern: str = "**/junit-results*.xml") -> list[Path]:
    """Find all JUnit result files matching the pattern."""
    files = list(base_path.glob(pattern))
    
    # Filter out processed/original duplicates - prefer original files
    unique_files = {}
    for f in files:
        # Create a normalized key based on the directory and base name
        key = str(f.parent / f.name.replace(".processed.xml", "").replace(".original.xml", ""))
        
        # Skip processed files if we already have the original
        if ".processed.xml" in f.name:
            if key not in unique_files:
                unique_files[key] = f
        elif ".original.xml" in f.name:
            unique_files[key] = f  # Original takes precedence
        else:
            unique_files[key] = f
    
    return list(unique_files.values())


def analyze_failures(base_path: Path, pattern: str = "**/junit-results*.xml") -> tuple[dict[str, TestStats], AnalysisMetadata]:
    """Analyze all JUnit files and aggregate failure statistics."""
    junit_files = find_junit_files(base_path, pattern)
    
    print(f"Found {len(junit_files)} JUnit result files to analyze")
    print("-" * 60)
    
    # Track metadata
    metadata = AnalysisMetadata(files_analyzed=len(junit_files))
    
    # Aggregate stats by test name (combining classname + test name for uniqueness)
    stats: dict[str, TestStats] = defaultdict(lambda: TestStats("", ""))
    
    # Track unique run IDs to avoid counting same failure multiple times from duplicated files
    seen_failures: set[tuple] = set()
    
    for file_path in junit_files:
        # Extract PR and run info for metadata tracking
        pr_number, run_id = extract_pr_and_run_from_path(str(file_path))
        if pr_number != "unknown":
            metadata.prs_analyzed.add(pr_number)
        if run_id != "unknown":
            metadata.runs_analyzed.add(run_id)
        
        failures = parse_junit_file(file_path)
        
        for failure in failures:
            # Create unique key to avoid counting duplicates
            failure_key = (failure.test_name, failure.classname, failure.pr_number, failure.run_id)
            
            if failure_key in seen_failures:
                continue
            seen_failures.add(failure_key)
            
            # Use combination of classname and test name as unique identifier
            test_key = f"{failure.classname} › {failure.test_name}"
            
            if stats[test_key].test_name == "":
                stats[test_key] = TestStats(
                    test_name=failure.test_name,
                    classname=failure.classname
                )
            
            stats[test_key].failure_count += 1
            stats[test_key].failures.append(failure)
            stats[test_key].affected_prs.add(failure.pr_number)
            
            # Store unique error messages (truncated)
            short_msg = failure.message[:100]
            if short_msg not in stats[test_key].error_messages:
                stats[test_key].error_messages.append(short_msg)
    
    return dict(stats), metadata


def print_report(stats: dict[str, TestStats], metadata: AnalysisMetadata, top_n: int = 20):
    """Print a formatted report of the most failing tests."""
    # Sort by failure count
    sorted_stats = sorted(stats.values(), key=lambda x: x.failure_count, reverse=True)
    
    print("\n" + "=" * 80)
    print("🔴 MOST FAILING TESTS REPORT")
    print("=" * 80)
    
    print(f"\n📂 Files analyzed: {metadata.files_analyzed}")
    print(f"🔀 PRs analyzed: {len(metadata.prs_analyzed)}")
    print(f"🏃 CI Runs analyzed: {len(metadata.runs_analyzed)}")
    
    total_failures = sum(s.failure_count for s in sorted_stats)
    print(f"\n❌ Total unique test failures: {total_failures}")
    print(f"🧪 Unique failing tests: {len(sorted_stats)}")
    print(f"📋 Showing top {min(top_n, len(sorted_stats))} most failing tests:\n")
    
    print("-" * 80)
    
    for i, test_stat in enumerate(sorted_stats[:top_n], 1):
        prs = sorted(test_stat.affected_prs)
        pr_str = ", ".join(prs[:5])
        if len(prs) > 5:
            pr_str += f", ... ({len(prs)} total)"
        
        print(f"\n#{i} [{test_stat.failure_count} failures] - Affected PRs: {pr_str}")
        print(f"   📁 {test_stat.classname}")
        print(f"   🧪 {test_stat.test_name}")
        
        if test_stat.error_messages:
            print(f"   💬 Error: {test_stat.error_messages[0][:80]}...")
    
    print("\n" + "=" * 80)
    
    # Summary by test file/class
    print("\n📊 FAILURES BY TEST FILE:")
    print("-" * 80)
    
    file_stats = defaultdict(int)
    for test_stat in sorted_stats:
        file_stats[test_stat.classname] += test_stat.failure_count
    
    sorted_file_stats = sorted(file_stats.items(), key=lambda x: x[1], reverse=True)
    
    for classname, count in sorted_file_stats[:15]:
        print(f"  {count:3d} failures  │  {classname}")
    
    print("\n" + "=" * 80)


def export_csv(stats: dict[str, TestStats], output_file: Path):
    """Export statistics to CSV file."""
    import csv
    
    sorted_stats = sorted(stats.values(), key=lambda x: x.failure_count, reverse=True)
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Rank', 'Failure Count', 'Test File', 'Test Name', 'Affected PRs', 'Sample Error'])
        
        for i, test_stat in enumerate(sorted_stats, 1):
            prs = ", ".join(sorted(test_stat.affected_prs))
            error = test_stat.error_messages[0][:100] if test_stat.error_messages else ""
            writer.writerow([i, test_stat.failure_count, test_stat.classname, test_stat.test_name, prs, error])
    
    print(f"\n📄 CSV report exported to: {output_file}")


def export_markdown(stats: dict[str, TestStats], metadata: AnalysisMetadata, output_file: Path, top_n: int = 20):
    """Export statistics to Markdown file."""
    from datetime import datetime
    
    sorted_stats = sorted(stats.values(), key=lambda x: x.failure_count, reverse=True)
    total_failures = sum(s.failure_count for s in sorted_stats)
    
    # Calculate failures by test file
    file_stats = defaultdict(int)
    for test_stat in sorted_stats:
        file_stats[test_stat.classname] += test_stat.failure_count
    sorted_file_stats = sorted(file_stats.items(), key=lambda x: x[1], reverse=True)
    
    # Collect all affected PRs (from failures)
    all_prs_with_failures = set()
    for test_stat in sorted_stats:
        all_prs_with_failures.update(test_stat.affected_prs)
    
    lines = []
    lines.append("# 🔴 Test Failure Analysis Report")
    lines.append("")
    lines.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    lines.append("")
    
    # Analysis scope section
    lines.append("## 📂 Analysis Scope")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| JUnit Files Analyzed | {metadata.files_analyzed} |")
    lines.append(f"| PRs Analyzed | {len(metadata.prs_analyzed)} |")
    lines.append(f"| CI Runs Analyzed | {len(metadata.runs_analyzed)} |")
    lines.append("")
    
    # Summary section
    lines.append("## 📊 Failure Summary")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Total Failures | {total_failures} |")
    lines.append(f"| Unique Failing Tests | {len(sorted_stats)} |")
    lines.append(f"| PRs with Failures | {len(all_prs_with_failures)} |")
    lines.append(f"| Test Files with Failures | {len(file_stats)} |")
    lines.append("")
    
    # Top failing tests table
    lines.append(f"## 🧪 Top {min(top_n, len(sorted_stats))} Most Failing Tests")
    lines.append("")
    lines.append("| Rank | Failures | Test File | Test Name | Affected PRs |")
    lines.append("|:----:|:--------:|-----------|-----------|--------------|")
    
    for i, test_stat in enumerate(sorted_stats[:top_n], 1):
        prs = sorted(test_stat.affected_prs)
        pr_str = ", ".join(prs[:5])
        if len(prs) > 5:
            pr_str += f" (+{len(prs) - 5} more)"
        
        # Escape pipe characters in test names
        classname = test_stat.classname.replace("|", "\\|")
        test_name = test_stat.test_name.replace("|", "\\|")
        
        lines.append(f"| {i} | {test_stat.failure_count} | `{classname}` | {test_name} | {pr_str} |")
    
    lines.append("")
    
    # Failures by test file
    lines.append("## 📁 Failures by Test File")
    lines.append("")
    lines.append("| Failures | Test File |")
    lines.append("|:--------:|-----------|")
    
    for classname, count in sorted_file_stats[:15]:
        classname_escaped = classname.replace("|", "\\|")
        lines.append(f"| {count} | `{classname_escaped}` |")
    
    lines.append("")
    
    # Detailed failure information
    lines.append("## 📋 Detailed Failure Information")
    lines.append("")
    
    for i, test_stat in enumerate(sorted_stats[:top_n], 1):
        prs = sorted(test_stat.affected_prs)
        
        lines.append(f"### {i}. {test_stat.test_name}")
        lines.append("")
        lines.append(f"- **Test File:** `{test_stat.classname}`")
        lines.append(f"- **Failure Count:** {test_stat.failure_count}")
        lines.append(f"- **Affected PRs:** {', '.join(prs)}")
        lines.append("")
        
        if test_stat.error_messages:
            lines.append("**Error Message:**")
            lines.append("```")
            lines.append(test_stat.error_messages[0][:300])
            lines.append("```")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write("\n".join(lines))
    
    print(f"\n📝 Markdown report exported to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Analyze JUnit XML test results for failure statistics")
    parser.add_argument("path", nargs="?", default="./ci-logs", 
                        help="Path to search for JUnit files (default: ./ci-logs)")
    parser.add_argument("--pattern", default="**/junit-results*.xml",
                        help="Glob pattern for JUnit files (default: **/junit-results*.xml)")
    parser.add_argument("--top", type=int, default=20,
                        help="Number of top failing tests to show (default: 20)")
    parser.add_argument("--csv", type=str, default=None,
                        help="Export results to CSV file")
    parser.add_argument("--markdown", "--md", type=str, default=None,
                        help="Export results to Markdown file")
    
    args = parser.parse_args()
    
    base_path = Path(args.path)
    
    if not base_path.exists():
        print(f"Error: Path '{base_path}' does not exist")
        return 1
    
    stats, metadata = analyze_failures(base_path, args.pattern)
    
    if not stats:
        print("No test failures found!")
        print(f"\n📂 Files analyzed: {metadata.files_analyzed}")
        print(f"🔀 PRs analyzed: {len(metadata.prs_analyzed)}")
        print(f"🏃 CI Runs analyzed: {len(metadata.runs_analyzed)}")
        return 0
    
    print_report(stats, metadata, args.top)
    
    if args.csv:
        export_csv(stats, Path(args.csv))
    
    if args.markdown:
        export_markdown(stats, metadata, Path(args.markdown), args.top)
    
    return 0


if __name__ == "__main__":
    exit(main())

