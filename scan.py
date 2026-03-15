import sys
from pathlib import Path

# Extensions to include
EXTENSIONS = {".c", ".cpp", ".h", ".py"}  # modify as needed


def count_files_and_lines(directory: Path):
    file_count = 0
    line_count = 0

    for path in directory.rglob("*"):
        if path.is_file() and path.suffix.lower() in EXTENSIONS:
            file_count += 1
            try:
                with path.open("r", encoding="utf-8", errors="ignore") as f:
                    line_count += sum(1 for _ in f)
            except Exception as e:
                print(f"Could not read {path}: {e}")

    return file_count, line_count


def main():
    if len(sys.argv) != 2:
        print("Usage: python count_lines.py <directory>")
        sys.exit(1)

    directory = Path(sys.argv[1])

    if not directory.is_dir():
        print("Error: Provided path is not a directory.")
        sys.exit(1)

    files, lines = count_files_and_lines(directory)

    print(f"Files found: {files}")
    print(f"Total lines: {lines}")


if __name__ == "__main__":
    main()