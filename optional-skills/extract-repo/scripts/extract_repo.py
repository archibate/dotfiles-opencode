#!/usr/bin/env uv run python3
# /// script
# dependencies = ["rich", "questionary"]
# ///
"""
Download a GitHub repo as clean source code (no .git history).

Usage:
    uv run extract_repo.py [URL] [OPTIONS]
    uv run extract_repo.py --list
    uv run extract_repo.py --remove

Arguments:
    URL                  GitHub repository URL (prompted if omitted)

Options:
    -n, --dry-run        Show what would happen without cloning
    -l, --list           List all managed repos (newest first)
    -r, --remove         Remove managed repos interactively
    -h, --help           Show this help message

Examples:
    uv run extract_repo.py https://github.com/user/repo
    uv run extract_repo.py https://github.com/user/repo/blob/main/README.md
    uv run extract_repo.py --list
    uv run extract_repo.py --remove
"""

import argparse
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import questionary
from rich.console import Console
from rich.table import Table

console = Console()

WORKDIR = Path.home() / ".extracted_repos" / "WORKDIR"
MARKER = ".extract_repo"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download a GitHub repo as clean source code (no .git history).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  extract_repo.py https://github.com/user/repo
  extract_repo.py --list
  extract_repo.py --remove
""",
    )
    parser.add_argument(
        "url", nargs="?", help="GitHub repository URL (prompted if omitted)"
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Show what would happen without cloning",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        dest="list_repos",
        help="List all managed repos (newest first)",
    )
    parser.add_argument(
        "-r", "--remove", action="store_true", help="Remove managed repos interactively"
    )
    return parser.parse_args()


def ask_url() -> str:
    try:
        return input("GitHub repo URL: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)


def normalize_url(url: str) -> str | None:
    """Extract repo root URL from any GitHub URL. Returns None if invalid."""
    pattern = r"^https://github\.com/([\w.-]+)/([\w.-]+)"
    match = re.match(pattern, url)
    if not match:
        return None
    owner, repo = match.groups()
    repo = repo.removesuffix(".git")
    return f"https://github.com/{owner}/{repo}"


def extract_name(url: str) -> str:
    """Extract repo name from normalized URL."""
    return url.rstrip("/").split("/")[-1]


def resolve_path(name: str) -> tuple[Path, str | None]:
    """Return (target_path, conflict_note). conflict_note is None if no conflict."""
    base = WORKDIR / name
    if not base.exists():
        return base, None

    suffix = 2
    while True:
        candidate = WORKDIR / f"{name}-{suffix}"
        if not candidate.exists():
            return candidate, f"{name} already exists"
        suffix += 1


def clone_shallow(url: str, target: Path) -> bool:
    result = subprocess.run(
        ["git", "clone", "--depth", "1", url, str(target)],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def remove_git(target: Path) -> None:
    git_dir = target / ".git"
    if git_dir.exists():
        shutil.rmtree(git_dir)


def create_marker(target: Path) -> None:
    """Create .extract_repo marker file."""
    marker_path = target / MARKER
    marker_path.touch()


def get_managed_repos() -> list[tuple[Path, float]]:
    """Return list of (repo_path, mtime) for all managed repos, sorted newest first."""
    repos = []
    if not WORKDIR.exists():
        return repos

    for item in WORKDIR.iterdir():
        if item.is_dir():
            marker = item / MARKER
            if marker.exists():
                repos.append((item, marker.stat().st_mtime))

    repos.sort(key=lambda x: x[1], reverse=True)
    return repos


def format_age(mtime: float) -> str:
    """Format mtime as human-readable age."""
    delta = datetime.now().timestamp() - mtime
    if delta < 60:
        return "just now"
    if delta < 3600:
        mins = int(delta / 60)
        return f"{mins} min ago" if mins == 1 else f"{mins} mins ago"
    if delta < 86400:
        hours = int(delta / 3600)
        return f"{hours} hour ago" if hours == 1 else f"{hours} hours ago"
    days = int(delta / 86400)
    return f"{days} day ago" if days == 1 else f"{days} days ago"


def list_repos() -> list[tuple[Path, float]]:
    """List all managed repos. Returns the list for reuse."""
    repos = get_managed_repos()
    if not repos:
        console.print("[dim]No managed repos found.[/dim]")
        return []

    table = Table(show_header=True, header_style="bold", box=None, padding=(0, 2))
    table.add_column("#", style="dim", width=3)
    table.add_column("Repository", style="cyan")
    table.add_column("Age", style="dim")

    for i, (repo_path, mtime) in enumerate(repos, 1):
        table.add_row(str(i), repo_path.name, format_age(mtime))

    console.print()
    console.print(table)
    console.print()
    return repos


def parse_selection(selection: str, max_val: int) -> list[int]:
    """Parse user selection like '1,3,5' or '1-3' or '1,3-5'. Returns sorted indices."""
    indices = set()
    parts = selection.replace(" ", "").split(",")

    for part in parts:
        if "-" in part:
            try:
                start, end = part.split("-", 1)
                start, end = int(start), int(end)
                if 1 <= start <= end <= max_val:
                    indices.update(range(start, end + 1))
            except ValueError:
                continue
        else:
            try:
                val = int(part)
                if 1 <= val <= max_val:
                    indices.add(val)
            except ValueError:
                continue

    return sorted(indices)


def remove_repos() -> None:
    """Interactive removal of managed repos."""
    repos = get_managed_repos()
    if not repos:
        console.print("[dim]No managed repos found.[/dim]")
        return

    choices = [
        questionary.Choice(
            title=f"{repo_path.name:<30} ({format_age(mtime)})",
            value=repo_path,
        )
        for repo_path, mtime in repos
    ]

    selected = questionary.checkbox(
        "Select repos to remove (↑↓ navigate, space select, enter confirm):",
        choices=choices,
    ).ask()

    if not selected:
        console.print("[dim]Cancelled.[/dim]")
        return

    for repo_path in selected:
        shutil.rmtree(repo_path, ignore_errors=True)
        console.print(f"[red]Removed:[/red] {repo_path.name}")


def clone_repo(args: argparse.Namespace) -> None:
    """Handle the clone workflow."""
    url = args.url or ask_url()

    repo_url = normalize_url(url)
    if not repo_url:
        console.print(f"[red]Error:[/red] Invalid GitHub URL: {url}")
        sys.exit(1)

    name = extract_name(repo_url)
    target, conflict_note = resolve_path(name)

    if args.dry_run:
        console.print("[dim]dry-run[/dim]")
        if url != repo_url:
            console.print(f"  Input:  [dim]{url}[/dim]")
            console.print(f"  Normalized: [cyan]{repo_url}[/cyan]")
        else:
            console.print(f"  Clone: [cyan]{repo_url}[/cyan]")
        console.print(f"  Target: [cyan]{target}[/cyan]")
        if conflict_note:
            console.print(f"  [yellow]({conflict_note})[/yellow]")
        return

    with console.status("[bold]Cloning...", spinner="dots"):
        success = clone_shallow(repo_url, target)

    if not success:
        console.print("[red]Failed to clone repository.[/red]")
        sys.exit(1)

    remove_git(target)
    create_marker(target)
    console.print(f"[green]Done![/green] {name}")
    console.print(f"[bold]cd {target}[/bold]")


def main() -> None:
    args = parse_args()

    if args.list_repos:
        list_repos()
    elif args.remove:
        remove_repos()
    else:
        clone_repo(args)


if __name__ == "__main__":
    main()
