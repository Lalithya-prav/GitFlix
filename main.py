import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.text import Text

from git_parser import get_commit_stats
from stats_calculator import calculate_repo_stats

console = Console()

def build_dashboard(stats, commits, repo_path="."):
    """
    Level 4: Builds a retro multi-panel dashboard using Rich Layout,
    Tables, and Panels.
    """
    layout = Layout()

    # Split screen vertically into Header, Body, and Footer
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3)
    )

    # 1. Header Panel
    header_text = Text(f"🎬 GITFLIX — REPOSITORY HISTORY HUD | Target: {repo_path}", style="bold cyan center")
    layout["header"].update(Panel(header_text, style="cyan"))

    # 2. Split Body horizontally into Left (Metrics) and Right (Recent Feed)
    layout["body"].split_row(
        Layout(name="left", ratio=1),
        Layout(name="right", ratio=1)
    )

    # Left Panel: Metrics Table
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

    # Right Panel: Recent Commits Feed
    commits_table = Table(title="📜 Recent Commit History", expand=True, border_style="magenta")
    commits_table.add_column("SHA", style="dim yellow", width=8)
    commits_table.add_column("Author", style="magenta", width=12)
    commits_table.add_column("Message", style="white")

    # Display up to 5 most recent commits
    recent_commits = list(reversed(commits))[:5]
    for c in recent_commits:
        commits_table.add_row(c["sha"], c["author"], c["message"])

    layout["right"].update(Panel(commits_table, border_style="magenta"))

    # 3. Footer Panel
    footer_text = Text("GitFlix v1.0 | Built for Hackathon Sprint | Run with '--replay' coming soon!", style="dim center")
    layout["footer"].update(Panel(footer_text, style="white on black"))

    return layout

def main():
    # Read repo path from command line arguments, or default to '.'
    repo_path = sys.argv[1] if len(sys.argv) > 1 else "."

    console.clear()
    console.print("[bold yellow]🍿 Loading GitFlix Dashboard...[/bold yellow]\n")

    # Fetch data using our parser and calculator scripts
    commits = get_commit_stats(repo_path)
    stats = calculate_repo_stats(commits)

    if not stats:
        console.print("[bold red]Error:[/bold red] Could not analyze repository. Ensure the target path is a valid Git repo.")
        return

    console.clear()
    dashboard_layout = build_dashboard(stats, commits, repo_path)
    console.print(dashboard_layout)

if __name__ == "__main__":
    main()