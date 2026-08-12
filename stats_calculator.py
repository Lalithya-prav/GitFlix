from collections import Counter
from datetime import datetime
from git_parser import get_commit_stats

def calculate_repo_stats(commits):
    """
    Level 3: Analyzes a list of parsed commit dictionaries and calculates
    high-level repository statistics.
    """
    if not commits:
        return None

    total_commits = len(commits)
    
    # Cumulative stats
    total_insertions = sum(c["insertions"] for c in commits)
    total_deletions = sum(c["deletions"] for c in commits)
    total_files_changed = sum(c["files_changed"] for c in commits)

    # Author analysis
    authors_counter = Counter(c["author"] for c in commits)
    top_author, top_author_commits = authors_counter.most_common(1)[0]
    unique_contributors = len(authors_counter)

    # Date / Lifespan analysis
    dates = [datetime.strptime(c["date"], "%Y-%m-%d") for c in commits]
    first_commit_date = min(dates)
    last_commit_date = max(dates)
    lifespan_days = (last_commit_date - first_commit_date).days + 1

    # Find biggest commit (most total line modifications)
    biggest_commit = max(
        commits,
        key=lambda c: c["insertions"] + c["deletions"],
        default=commits[0]
    )

    return {
        "total_commits": total_commits,
        "unique_contributors": unique_contributors,
        "top_author": top_author,
        "top_author_commits": top_author_commits,
        "total_insertions": total_insertions,
        "total_deletions": total_deletions,
        "net_lines": total_insertions - total_deletions,
        "total_files_changed": total_files_changed,
        "start_date": first_commit_date.strftime("%Y-%m-%d"),
        "latest_date": last_commit_date.strftime("%Y-%m-%d"),
        "lifespan_days": lifespan_days,
        "biggest_commit": biggest_commit
    }


if __name__ == "__main__":
    print("📈 Testing Stats Calculator...\n")
    
    # Get parsed commits from current directory
    raw_data = get_commit_stats(".")
    stats = calculate_repo_stats(raw_data)

    if not stats:
        print("⚠️ No commit data available to calculate stats.")
    else:
        print("✅ Calculated Repository Summary:")
        print("----------------------------------------")
        print(f"• Total Commits:     {stats['total_commits']}")
        print(f"• Contributors:      {stats['unique_contributors']} (Top: {stats['top_author']} - {stats['top_author_commits']} commits)")
        print(f"• Project Lifespan:  {stats['lifespan_days']} day(s) [{stats['start_date']} to {stats['latest_date']}]")
        print(f"• Lines Added:       +{stats['total_insertions']}")
        print(f"• Lines Deleted:     -{stats['total_deletions']}")
        print(f"• Net Code Growth:   {stats['net_lines']} lines")
        print(f"• Biggest Commit:    {stats['biggest_commit']['sha']} by {stats['biggest_commit']['author']} ('{stats['biggest_commit']['message']}')")
        print("----------------------------------------\n")