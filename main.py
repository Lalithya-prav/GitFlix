import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from rich.progress import Progress, BarColumn, TextColumn

from git_parser import get_commit_stats
from stats_calculator import calculate_repo_stats

console = Console()

def run_replay(commits):
    """
    Level 5: Replays repository history frame-by-frame chronologically.
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

        # Frame delay (pause between commits to create animation effect)
        time.sleep(1.0)

    console.print("\n[bold green]🎉 REPLAY COMPLETE! Repository timeline finished.[/bold green]\n")
    time.sleep(1.5)


def build_dashboard(stats, commits, repo_path="."):
    """
    Level 4: Builds a retro multi-panel dashboard using Rich.
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

    stats_table = Table(title="📊 Repository High-Level Metrics", expand=True, border_style="green")
    stats_table.add_column("Metric", style="bold yellow")
    stats_table.add_column("Value", style="bold white")

    stats_table.add_row("Total Commits", str(stats["total_commits"]))
    stats_table.add_row("Contributors", f"{stats['unique_contributors']}")
    stats_table.add_row("Top Contributor", f"{stats['top_author']} ({stats['top_author_commits']} commits)")
    stats_table.add_row("Project Lifespan", f"{stats['lifespan_days']} day(s)")
    stats_table.add_row("Lines Added", f"[green]+{stats['total_insertions']}[/green]")
    stats_table.add_row("Lines Deleted", f"[red]-{stats['total_deletions']}[/red]")
    stats_table.add_row("Net Code Growth", f"[bold green]{stats['net_lines']} lines[/bold green]")

    layout["left"].update(Panel(stats_table, border_style="green"))

    commits_table = Table(title="📜 Recent Commit History", expand=True, border_style="magenta")
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


def main():
    repo_path = "."
    replay_flag = False

    # Check CLI arguments for --replay flag or custom path
    for arg in sys.argv[1:]:
        if arg == "--replay":
            replay_flag = True
        else:
            repo_path = arg

    console.clear()
    console.print("[bold yellow]🍿 Loading GitFlix...[/bold yellow]\n")

    commits = get_commit_stats(repo_path)
    stats = calculate_repo_stats(commits)

    if not stats:
        console.print("[bold red]Error:[/bold red] Could not analyze repository.")
        return

    # If user passed --replay, trigger Replay Mode!
    if replay_flag:
        run_replay(commits)

    console.clear()
    dashboard_layout = build_dashboard(stats, commits, repo_path)
    console.print(dashboard_layout)


if __name__ == "__main__":
    main()