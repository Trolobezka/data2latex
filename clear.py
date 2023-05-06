from pathlib import Path
from shutil import rmtree
from typing import List

if __name__ == "__main__":
    found_paths: List[Path] = []
    search_patterns: List[str] = [
        "dist",
        "build",
        "*/*.egg-info",
        "__pycache__",
        "src/**/__pycache__",
        "tests/**/__pycache__",
        "docs/**/__pycache__",
        "docs/_build",
        "docs/[!i]*.rst",
    ]
    root = Path(".")

    for search_path in search_patterns:
        found_paths.extend(list(root.glob(search_path)))

    if len(found_paths) == 0:
        print("Already clear\n")
        exit()

    print("Found paths:\n")
    for p in found_paths:
        print(p)

    answer = input("\nRemove (y/n)? ")
    print()

    if answer.strip().lower() == "y":
        for p in found_paths:
            try:
                if p.is_file():
                    p.unlink()
                else:
                    rmtree(p)
                print(f"Removed: {p}")
            except:
                print(f"ERROR: {p}")
        print()
