#!/usr/bin/env python3
"""Student Attendance Cleaner.

Reads messy attendance records from a text file, cleans them with a list
comprehension, removes duplicates with a set, sorts the names, and saves a
clean CSV file.
"""

from __future__ import annotations

import csv
from pathlib import Path

INPUT_FILE = Path("attendance.txt")
OUTPUT_FILE = Path("attendance_clean.csv")
OUTPUT_HEADER = ["student_name"]


def read_attendance() -> list[str]:
    """Read one student name per line from attendance.txt."""
    try:
        with INPUT_FILE.open("r", encoding="utf-8") as input_file:
            return input_file.read().splitlines()
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} was not found. No attendance records were processed.")
        return []
    except OSError as error:
        print(f"Error: could not read {INPUT_FILE}: {error}")
        return []


def clean_names(raw_names: list[str]) -> list[str]:
    """Normalize spacing and capitalization with a single list comprehension."""
    return [" ".join(name.strip().split()).title()
            for name in raw_names if name.strip()]


def unique_sorted_names(cleaned_names: list[str]) -> list[str]:
    """Return alphabetically sorted unique names."""
    return sorted(set(cleaned_names))


def write_clean_names(names: list[str]) -> bool:
    """Save the cleaned, sorted names to attendance_clean.csv."""
    try:
        with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(OUTPUT_HEADER)
            writer.writerows([[name] for name in names])
    except OSError as error:
        print(f"Error: could not write {OUTPUT_FILE}: {error}")
        return False

    print(f"Saved {len(names)} cleaned name(s) to {OUTPUT_FILE}.")
    return True


def print_report(raw_names: list[str], cleaned_names: list[str],
                 unique_names: list[str]) -> None:
    """Show the original count, unique count, and the cleaned sorted list."""
    original_count = sum(1 for name in raw_names if name.strip())
    print("\nAttendance Cleaning Report")
    print("=" * 27)
    print(f"Original records: {original_count}")
    print(f"Cleaned records:  {len(cleaned_names)}")
    print(f"Unique students:  {len(unique_names)}")
    print(f"Duplicate entries removed: {original_count - len(unique_names)}")
    print("\nCleaned and sorted attendance list:")

    if not unique_names:
        print("  (no student names found)")
        return

    for index, name in enumerate(unique_names, start=1):
        print(f"  {index:>2}. {name}")


def main() -> int:
    """Run the attendance cleaner and return a process exit code."""
    raw_names = read_attendance()
    cleaned_names = clean_names(raw_names)
    unique_names = unique_sorted_names(cleaned_names)
    print_report(raw_names, cleaned_names, unique_names)

    if not raw_names:
        print(f"Add student names to {INPUT_FILE} and run the program again.")
        return 1

    if not write_clean_names(unique_names):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())