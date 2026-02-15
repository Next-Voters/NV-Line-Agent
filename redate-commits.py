#!/usr/bin/env python3
"""
Script to change commit dates for NV-Line-Agent repository
Dynamically redistributes commits between Jan 10, 2026 and Feb 15, 2026
"""

import subprocess
import sys
from datetime import datetime

def get_commit_hashes():
    """Get all commit hashes in reverse chronological order (oldest first)"""
    result = subprocess.run(
        ['git', 'log', '--reverse', '--format=%H'],
        capture_output=True,
        text=True,
        check=True
    )
    commits = result.stdout.strip().split('\n')
    return [c for c in commits if c]


def generate_dates(num_commits):
    """
    Generate evenly spaced timestamps between:
    Jan 10, 2026 09:00:00
    Feb 15, 2026 15:00:00
    """
    if num_commits == 0:
        return []

    start = datetime(2026, 1, 10, 9, 0, 0)
    end = datetime(2026, 2, 15, 15, 0, 0)

    if num_commits == 1:
        return [start.strftime("%Y-%m-%d %H:%M:%S")]

    delta = (end - start) / (num_commits - 1)

    dates = []
    for i in range(num_commits):
        dt = start + (delta * i)
        dates.append(dt.strftime("%Y-%m-%d %H:%M:%S"))

    return dates


def rewrite_history(commit_hashes, dates):
    """Rewrite git history with new dates"""

    if len(commit_hashes) != len(dates):
        raise ValueError(
            f"Commit count ({len(commit_hashes)}) does not match date count ({len(dates)})"
        )

    print(f"Rewriting history for {len(commit_hashes)} commits...\n")

    commit_date_map = dict(zip(commit_hashes, dates))

    filter_script = "case $GIT_COMMIT in\n"
    for commit, date in commit_date_map.items():
        filter_script += f"    {commit})\n"
        filter_script += f'        export GIT_AUTHOR_DATE="{date}"\n'
        filter_script += f'        export GIT_COMMITTER_DATE="{date}"\n'
        filter_script += "        ;;\n"
    filter_script += "esac"

    try:
        subprocess.run(
            ['git', 'filter-branch', '-f', '--env-filter', filter_script, '--', '--all'],
            check=True
        )
        print("✓ Successfully rewrote git history!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error rewriting history: {e}")
        return False


def main():
    print("=" * 70)
    print("Git Commit Date Rewriter")
    print("=" * 70)
    print("\n⚠️  WARNING: This rewrites git history and requires force push!")
    print("⚠️  Make sure you have a backup of your repository!\n")

    response = input("Do you want to continue? (yes/no): ").lower().strip()
    if response != 'yes':
        print("Aborted.")
        sys.exit(0)

    try:
        print("\nFetching commit hashes...")
        commits = get_commit_hashes()
        print(f"Found {len(commits)} commits")

        if not commits:
            print("No commits found.")
            sys.exit(0)

        dates = generate_dates(len(commits))

        print("\nPreview (first 5 and last 5):")
        print("-" * 70)

        preview_count = min(5, len(commits))

        for i in range(preview_count):
            print(f"{commits[i][:8]}... → {dates[i]}")

        if len(commits) > 10:
            print("...")

        for i in range(len(commits) - preview_count, len(commits)):
            print(f"{commits[i][:8]}... → {dates[i]}")

        print("-" * 70)

        response = input("\nProceed with rewriting? (yes/no): ").lower().strip()
        if response != 'yes':
            print("Aborted.")
            sys.exit(0)

        if rewrite_history(commits, dates):
            print("\nNext steps:")
            print("1. Review changes:")
            print("   git log --oneline --date=format:'%Y-%m-%d %H:%M' --pretty=format:'%h %ad %s'")
            print("\n2. Force push:")
            print("   git push origin main --force")
            print("\n⚠️  Coordinate with collaborators before force pushing.")
        else:
            sys.exit(1)

    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
