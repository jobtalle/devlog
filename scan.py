import sys
import subprocess
from pathlib import Path

EXTENSIONS = {".c", ".cpp", ".h", ".py"}
EXCLUDED_DIRS = {
    ".git",
    ".vs",
    "lib",
    "include",
    "x64",
}


def is_excluded(path):
    p = Path(path)
    return any(part in EXCLUDED_DIRS for part in p.parts)

def get_repo_root(path):
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(result.stdout.strip())

def git_command(repo_dir, args):
    result = subprocess.run(
        ["git", "-C", str(repo_dir)] + args,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def get_files_at_commit(repo_root, commit):
    output = git_command(repo_root, ["ls-tree", "-r", "--name-only", commit])
    return output.splitlines()


def get_file_content(repo_dir, commit, path):
    result = subprocess.run(
        ["git", "-C", str(repo_dir), "show", f"{commit}:{path}"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"git show failed for {path}: {result.stderr.strip()}")
        return ""

    return result.stdout


def main():
    if len(sys.argv) != 3:
        print("Usage: python count_lines_git.py <repo_dir> <commit>")
        sys.exit(1)

    repo_path = Path(sys.argv[1]).resolve()
    commit = sys.argv[2]

    repo_root = get_repo_root(repo_path)

    files = get_files_at_commit(repo_root, commit)

    file_count = 0
    line_count = 0

    for f in files:
        p = Path(f)

        if is_excluded(p):
            continue

        if p.suffix.lower() in EXTENSIONS:
            print(f"Scanning {p}")

            content = get_file_content(repo_root, commit, f)
            line_count += len(content.splitlines())
            file_count += 1

    print(f"Files found: {file_count}")
    print(f"Total lines: {line_count}")


if __name__ == "__main__":
    main()