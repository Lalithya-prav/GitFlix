import json
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.text import Text

from git_parser import get_commit_stats
from stats_calculator import calculate_repo_stats

console = Console()


def run_replay(commits):
    """
    Replays repository history frame-by-frame chronologically.
    """
    if not commits:
        console.print("[bold red]No commits to replay![/bold red]")
        return

    total_commits = len(commits)
    console.clear()

    console.print("\n[bold cyan]🎬 GITFLIX PRESENTATION: REPLAYING REPOSITORY HISTORY...[/bold cyan]\n")
    time.sleep(1)

    cumulative_lines_added = 0
    cumulative_lines_deleted = 0

    for idx, c in enumerate(commits, 1):
        console.clear()

        # Update cumulative trackers
        cumulative_lines_added += c["insertions"]
        cumulative_lines_deleted += c["deletions"]

        # 1. Title Banner
        title = Text(f"🍿 GITFLIX MOVIE REEL — FRAME {idx}/{total_commits}", style="bold yellow center")

        # 2. Frame Content Table
        frame_table = Table(show_header=False, expand=True, box=None)
        frame_table.add_column("Key", style="cyan", width=20)
        frame_table.add_column("Value", style="bold white")

        frame_table.add_row("📅 Commit Date:", c["date"])
        frame_table.add_row("🔑 Commit Hash:", f"[dim yellow]{c['sha']}[/dim yellow]")
        frame_table.add_row("👤 Author:", f"[magenta]{c['author']}[/magenta]")
        frame_table.add_row("💬 Message:", f"[bold white]\"{c['message']}\"[/bold white]")
        frame_table.add_row("📁 Files Modified:", str(c["files_changed"]))
        frame_table.add_row("📈 Commit Impact:", f"[green]+{c['insertions']}[/green]  [red]-{c['deletions']}[/red]")
        frame_table.add_row("📊 Total Codebase Net:", f"[bold green]+{cumulative_lines_added - cumulative_lines_deleted} lines[/bold green]")

        # Display Frame Panel
        frame_panel = Panel(
            frame_table,
            title=f"[bold green] Commit #{idx} [/bold green]",
            subtitle="[dim]Press Ctrl+C to abort replay[/dim]",
            border_style="cyan"
        )

        console.print(Panel(title, style="yellow"))
        console.print(frame_panel)

        # Visual progress bar
        percent = int((idx / total_commits) * 100)
        bar = "█" * (percent // 5) + "░" * (20 - (percent // 5))
        console.print(f"\n[cyan]Timeline Progress:[/cyan] [{bar}] [bold yellow]{percent}%[/bold yellow]\n")

        time.sleep(1.0)

    console.print("\n[bold green]🎉 REPLAY COMPLETE! Repository timeline finished.[/bold green]\n")
    time.sleep(1.5)


def build_dashboard(stats, commits, repo_path="."):
    """
    Builds a retro multi-panel dashboard using Rich.
    """
    layout = Layout()

    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3)
    )

    header_text = Text(f"🎬 GITFLIX — REPOSITORY HISTORY HUD | Target: {repo_path}", style="bold cyan center")
    layout["header"].update(Panel(header_text, style="cyan"))

    layout["body"].split_row(
        Layout(name="left", ratio=1),
        Layout(name="right", ratio=1)
    )

    stats_table = Table(title="📊 Repository High-Level Metrics", expand=True, border_style="green", padding=(0, 1))
    stats_table.add_column("Metric", style="bold yellow")
    stats_table.add_column("Value", style="bold white")

    bg_commit = stats["biggest_commit"]
    bg_info = f"{bg_commit['sha']} (+{bg_commit['insertions']}/-{bg_commit['deletions']})"

    stats_table.add_row("Total Commits", str(stats["total_commits"]))
    stats_table.add_row("Contributors", f"{stats['unique_contributors']}")
    stats_table.add_row("Top Contributor", f"{stats['top_author']} ({stats['top_author_commits']} commits)")
    stats_table.add_row("Timeline Range", f"{stats['start_date']} ➔ {stats['latest_date']}")
    stats_table.add_row("Project Lifespan", f"{stats['lifespan_days']} day(s)")
    stats_table.add_row("Lines Added", f"[green]+{stats['total_insertions']}[/green]")
    stats_table.add_row("Lines Deleted", f"[red]-{stats['total_deletions']}[/red]")
    stats_table.add_row("Net Code Growth", f"[bold green]{stats['net_lines']} lines[/bold green]")
    stats_table.add_row("💥 Biggest Commit", f"[dim yellow]{bg_info}[/dim yellow]")

    layout["left"].update(Panel(stats_table, border_style="green"))

    commits_table = Table(title="📜 Recent Commit History", expand=True, border_style="magenta", padding=(0, 1))
    commits_table.add_column("SHA", style="dim yellow", width=8)
    commits_table.add_column("Author", style="magenta", width=12)
    commits_table.add_column("Message", style="white")

    recent_commits = list(reversed(commits))[:5]
    for c in recent_commits:
        commits_table.add_row(c["sha"], c["author"], c["message"])

    layout["right"].update(Panel(commits_table, border_style="magenta"))

    footer_text = Text("GitFlix v1.0 | Tip: Run 'python main.py --replay' for Movie Mode!", style="dim center")
    layout["footer"].update(Panel(footer_text, style="white on black"))

    return layout


def show_error(message: str, subtitle: str = "Please check the repository path and try again."):
    """Displays a retro error panel when git parsing fails."""
    console.clear()
    error_table = Table(show_header=False, expand=True, box=None)
    error_table.add_column("Icon", style="bold red", width=4)
    error_table.add_column("Message", style="bold white")

    error_table.add_row("🚫", message)
    error_table.add_row("", f"[dim]{subtitle}[/dim]")

    panel = Panel(
        error_table,
        title="[bold red] 🎬 GITFLIX ERROR [/bold red]",
        border_style="red",
        expand=False
    )
    console.print("\n", panel, "\n")


def export_json(stats, commits, filename="gitflix_data.json"):
    """
    Exports parsed repository data and statistics to a JSON file
    for the browser dashboard to consume.
    """
    data = {
        "stats": stats,
        "commits": commits
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    console.print(f"[dim green]✨ Exported shared data to {filename}[/dim green]\n")


def main():
    repo_path = "."
    replay_flag = False

    for arg in sys.argv[1:]:
        if arg == "--replay":
            replay_flag = True
        else:
            repo_path = arg

    console.clear()
    console.print("[bold yellow]🍿 Loading GitFlix...[/bold yellow]\n")

    commits = get_commit_stats(repo_path)

    if commits is None:
        show_error(
            f"'{repo_path}' is not a valid Git repository.",
            "Make sure you run GitFlix inside a git repository folder or pass a valid path."
        )
        return

    if len(commits) == 0:
        show_error(
            f"No commits found in '{repo_path}'.",
            "This repository appears to be empty. Make a commit first!"
        )
        return

    stats = calculate_repo_stats(commits)

    if not stats:
        show_error("Could not calculate statistics for this repository.")
        return

    if replay_flag:
        run_replay(commits)

    # 💾 Export data for the browser interface
    export_json(stats, commits)

    console.clear()
    dashboard_layout = build_dashboard(stats, commits, repo_path)
    console.print(dashboard_layout)


if __name__ == "__main__":
    main()