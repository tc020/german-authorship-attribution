"""Create the labels, milestones and issues from roadmap.toml on GitHub.

Needs the GitHub CLI (https://cli.github.com), logged in once with `gh auth login`.
Run it inside your local clone of the repository:

    python scripts/create_roadmap.py --dry-run    # only show what would be created
    python scripts/create_roadmap.py              # create everything

Running it twice is safe: labels are updated, milestones and issues that already
exist (same title) are skipped.
"""
import argparse
import json
import subprocess
import sys
import time
import tomllib
from pathlib import Path


def gh(*args, stdin=None):
    """Run a GitHub CLI command and return its output; stop on errors."""
    result = subprocess.run(["gh", *args], input=stdin, capture_output=True,
                            text=True, encoding="utf-8")
    if result.returncode != 0:
        sys.exit(f"Error in `gh {' '.join(args[:2])}`:\n{result.stderr.strip()}")
    return result.stdout


def validate(roadmap):
    """Every label and milestone an issue refers to must be defined."""
    labels = {label["name"] for label in roadmap["label"]}
    milestones = {m["title"] for m in roadmap["milestone"]}
    problems = []
    for issue in roadmap["issue"]:
        problems += [f"{issue['title']!r}: unknown label {name!r}"
                     for name in issue.get("labels", []) if name not in labels]
        if "milestone" in issue and issue["milestone"] not in milestones:
            problems.append(f"{issue['title']!r}: unknown milestone {issue['milestone']!r}")
    if problems:
        sys.exit("roadmap.toml has errors:\n  " + "\n  ".join(problems))


def main():
    parser = argparse.ArgumentParser(description="Create GitHub labels, milestones and issues.")
    parser.add_argument("--file", type=Path, default=Path(__file__).with_name("roadmap.toml"))
    parser.add_argument("--dry-run", action="store_true", help="only print what would be created")
    args = parser.parse_args()

    roadmap = tomllib.loads(args.file.read_text(encoding="utf-8"))
    validate(roadmap)

    if args.dry_run:
        for label in roadmap["label"]:
            print(f"label      {label['name']}")
        for milestone in roadmap["milestone"]:
            print(f"milestone  {milestone['title']}")
        for issue in roadmap["issue"]:
            print(f"issue      {issue['title']}  [{issue.get('milestone', 'no milestone')}]")
        return

    for label in roadmap["label"]:
        gh("label", "create", label["name"], "--color", label["color"],
           "--description", label.get("description", ""), "--force")
        print(f"label      {label['name']}")

    existing = {m["title"] for m in json.loads(
        gh("api", "repos/{owner}/{repo}/milestones?state=all&per_page=100") or "[]")}
    for milestone in roadmap["milestone"]:
        if milestone["title"] in existing:
            print(f"exists     {milestone['title']}")
            continue
        gh("api", "repos/{owner}/{repo}/milestones",
           "-f", f"title={milestone['title']}",
           "-f", f"description={milestone.get('description', '')}")
        print(f"milestone  {milestone['title']}")

    existing = {i["title"] for i in json.loads(
        gh("issue", "list", "--state", "all", "--limit", "1000", "--json", "title") or "[]")}
    for issue in roadmap["issue"]:
        if issue["title"] in existing:
            print(f"exists     {issue['title']}")
            continue
        cmd = ["issue", "create", "--title", issue["title"], "--body-file", "-"]
        for name in issue.get("labels", []):
            cmd += ["--label", name]
        if "milestone" in issue:
            cmd += ["--milestone", issue["milestone"]]
        print(f"issue      {issue['title']}  {gh(*cmd, stdin=issue['body'].strip() + chr(10)).strip()}")
        time.sleep(1)  # GitHub asks for a pause between content-creating requests


if __name__ == "__main__":
    main()
