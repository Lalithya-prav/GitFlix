import subprocess

def get_raw_commits(repo_path="."):
    """
    Level 1: Runs 'git log' via subprocess to get commit metadata.
    Format string output: commit_hash|author|date|message
    """
    cmd = [
        "git",
        "-C", repo_path,
        "log",
        "--pretty=format:%h|%an|%ad|%s",
        "--date=short"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        if not output:
            return []
        return output.split("\n")
    except subprocess.CalledProcessError:
        print(f"Error: '{repo_path}' is not a valid Git repository or has no commits.")
        return None

def get_commit_stats(repo_path="."):
    """
    Level 2: Parses raw commits AND extracts line changes (files, insertions, deletions).
    Returns a list of commit dictionaries in chronological order.
    """
    raw_commits = get_raw_commits(repo_path)
    if raw_commits is None or len(raw_commits) == 0:
        return []

    parsed_commits = []

    for line in raw_commits:
        parts = line.split("|")
        if len(parts) < 4:
            continue
        
        sha, author, date, message = parts[0], parts[1], parts[2], parts[3]

        # Run git show to fetch line modification stats for this specific commit
        stat_cmd = [
            "git",
            "-C", repo_path,
            "show",
            "--shortstat",
            "--format=",
            sha
        ]
        stat_result = subprocess.run(stat_cmd, capture_output=True, text=True)
        stat_text = stat_result.stdout.strip()

        files_changed = 0
        insertions = 0
        deletions = 0

        # Example stat_text output: "2 files changed, 45 insertions(+), 12 deletions(-)"
        if stat_text:
            for chunk in stat_text.split(","):
                chunk = chunk.strip()
                if "file" in chunk:
                    files_changed = int(chunk.split()[0])
                elif "insertion" in chunk:
                    insertions = int(chunk.split()[0])
                elif "deletion" in chunk:
                    deletions = int(chunk.split()[0])

        parsed_commits.append({
            "sha": sha,
            "author": author,
            "date": date,
            "message": message,
            "files_changed": files_changed,
            "insertions": insertions,
            "deletions": deletions
        })

    # Reverse list so oldest commit comes first (chronological order for replay)
    return list(reversed(parsed_commits))


if __name__ == "__main__":
    print("🔍 Testing GitFlix Parser...\n")
    commits = get_commit_stats(".")
    
    if not commits:
        print("⚠️ No commits found! Follow the testing steps below to add a commit first.")
    else:
        print(f"✅ Successfully parsed {len(commits)} commit(s):\n")
        for idx, c in enumerate(commits, 1):
            print(f"[{idx}] {c['date']} | {c['sha']} | {c['author']} : '{c['message']}'")
            print(f"    └─ Files: {c['files_changed']} | +{c['insertions']} | -{c['deletions']}\n")