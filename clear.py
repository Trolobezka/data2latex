from pathlib import Path
from shutil import rmtree
from typing import List

if __name__ == "__main__":
    paths: List[str] = []

    if Path("dist").exists():
        paths.append("dist")
    if Path("build").exists():
        paths.append("build")
    for p in Path(".").glob("*/*.egg-info"):
        paths.append(str(p))
    for p in Path(".").glob("*/__pycache__"):
        paths.append(str(p))

    if len(paths) == 0:
        print("Already clear\n")
        exit()

    print("Found paths:\n")
    for p in paths:
        print(p)

    answer = input("\nRemove (y/n)? ")
    print()

    if answer.strip().lower() == "y":
        for p in paths:
            try:
                rmtree(p)
                print(f"Removed: {p}")
            except:
                print(f"ERROR: {p}")
    print()
