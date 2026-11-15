#!/usr/bin/env python3
"""Institute Expense Tracker.

A small menu-driven program that stores daily institute expenses in a CSV file.
It uses file handling, exception handling, sets, and a reusable prompt pattern.
"""

from __future__ import annotations

import csv
import math
from datetime import datetime
from pathlib import Path

# Keep configuration in constants instead of repeating literal values.
EXPENSES_FILE = Path("expenses.csv")
CSV_FIELDS = ["date", "item", "category", "amount"]
MENU_OPTIONS = ("1", "2", "3", "4")


def prompt_non_empty(label: str) -> str:
    """Return a non-empty text value entered by the user."""
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print("Error: this field cannot be empty. Please try again.")


def prompt_date() -> str:
    """Return a validated date in YYYY-MM-DD format."""
    while True:
        raw_value = input("Date (YYYY-MM-DD): ").strip()
        try:
            parsed_date = datetime.strptime(raw_value, "%Y-%m-%d").date()
        except ValueError:
            print("Error: enter a real date using YYYY-MM-DD. Please try again.")
            continue
        return parsed_date.isoformat()


def prompt_amount() -> float:
    """Return a positive, finite amount entered by the user."""
    while True:
        raw_value = input("Amount: ").strip()
        try:
            amount = float(raw_value)
            if not math.isfinite(amount):
                raise ValueError("amount must be finite")
            if amount <= 0:
                raise ValueError("amount must be greater than zero")
        except ValueError:
            print(
                f"Error: '{raw_value}' is not a valid amount. "
                "Enter a number greater than zero. Please try again."
            )
            continue
        return round(amount, 2)


def load_expenses() -> list[dict[str, str]]:
    """Load expenses from the CSV file, or return an empty list if it is missing."""
    try:
        with EXPENSES_FILE.open("r", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            if reader.fieldnames != CSV_FIELDS:
                print(
                    f"Warning: {EXPENSES_FILE} has unexpected columns. "
                    "Starting with an empty list."
                )
                return []
            return [dict(row) for row in reader]
    except FileNotFoundError:
        print(f"Info: {EXPENSES_FILE} was not found. Starting with an empty expense list.")
        return []
    except (csv.Error, OSError) as error:
        print(f"Error: could not read {EXPENSES_FILE}: {error}")
        return []


def save_expenses(expenses: list[dict[str, str]]) -> bool:
    """Write the complete expense list to the CSV file."""
    try:
        with EXPENSES_FILE.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(expenses)
    except OSError as error:
        print(f"Error: could not save {EXPENSES_FILE}: {error}")
        return False

    print(f"Saved {len(expenses)} expense(s) to {EXPENSES_FILE}.")
    return True


def add_expense(expenses: list[dict[str, str]]) -> None:
    """Collect one expense from the user and append it after a successful save."""
    print("\nAdd New Expense")
    print("-" * 16)
    expense = {
        "date": prompt_date(),
        "item": prompt_non_empty("Item name"),
        "category": prompt_non_empty("Category"),
        "amount": f"{prompt_amount():.2f}",
    }

    if save_expenses([*expenses, expense]):
        expenses.append(expense)
        print(f"Added: {expense['date']} | {expense['item']} | "
              f"{expense['category']} | {expense['amount']}")


def show_expenses(expenses: list[dict[str, str]]) -> None:
    """Display all expenses and the set of unique categories."""
    print("\nAll Expenses")
    print("-" * 12)
    if not expenses:
        print("No expenses have been recorded yet.")
        return

    print(f"{'#':>3}  {'Date':<10}  {'Item':<24}  {'Category':<16}  {'Amount':>9}")
    print("-" * 68)
    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index:>3}  {expense['date']:<10}  {expense['item']:<24}  "
            f"{expense['category']:<16}  {float(expense['amount']):>9.2f}"
        )

    categories = {expense["category"] for expense in expenses}
    print(f"\nUnique categories ({len(categories)}): {', '.join(sorted(categories))}")

    total = sum(float(expense["amount"]) for expense in expenses)
    print(f"Total of all expenses: {total:.2f}")


def show_category_totals(expenses: list[dict[str, str]]) -> None:
    """Calculate and display totals grouped by category using a set of categories."""
    print("\nExpenses by Category")
    print("-" * 20)
    if not expenses:
        print("No expenses have been recorded yet.")
        return

    totals: dict[str, float] = {}
    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0.0) + float(expense["amount"])

    unique_categories = set(totals)
    for category in sorted(unique_categories):
        print(f"{category:<20} {totals[category]:>10.2f}")

    print("-" * 31)
    print(f"{'All categories':<20} {sum(totals.values()):>10.2f}")


def print_menu() -> None:
    """Display the main menu."""
    print("\nInstitute Expense Tracker")
    print("=" * 27)
    print("1. Add New Expense")
    print("2. Show All Expenses")
    print("3. Calculate Total Expenses by Category")
    print("4. Exit")


def main() -> None:
    """Run the expense tracker menu until the user exits."""
    print("Welcome to the Institute Expense Tracker")
    expenses = load_expenses()

    while True:
        print_menu()
        choice = input("Select an option (1-4): ").strip()

        if choice not in MENU_OPTIONS:
            print(f"Error: '{choice}' is not a valid menu option. Enter 1, 2, 3, or 4.")
            continue

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            show_category_totals(expenses)
        else:
            print("Exiting the Expense Tracker. Your records remain saved.")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram stopped by the user.")