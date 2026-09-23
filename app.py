"""
Expense Tracker - a command-line app built with plain Python.
Features: add, view, delete, category summary, monthly report, CSV export.
Data is saved in expenses.json so it persists between runs.
"""

import csv
import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"
CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"]


# ---------- File handling ----------

def load_expenses():
    """Load expenses from the JSON file. Returns an empty list if none exist."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Could not read the data file. Starting with an empty list.")
        return []


def save_expenses(expenses):
    """Save the expenses list to the JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)


# ---------- Input helpers (with validation) ----------

def get_amount():
    while True:
        try:
            amount = float(input("Amount (Rs): "))
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Please enter a valid number.")


def get_date():
    while True:
        raw = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
        if raw == "":
            return datetime.now().strftime("%Y-%m-%d")
        try:
            datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print("Invalid date. Use the format YYYY-MM-DD.")


def get_category():
    print("Categories:")
    for i, name in enumerate(CATEGORIES, start=1):
        print(f"  {i}. {name}")
    while True:
        choice = input("Choose category number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        print("Invalid choice. Try again.")


# ---------- Core features ----------

def add_expense(expenses):
    title = input("Title (e.g. Lunch): ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    amount = get_amount()
    category = get_category()
    date = get_date()

    new_id = max((e["id"] for e in expenses), default=0) + 1
    expenses.append(
        {"id": new_id, "title": title, "amount": amount,
         "category": category, "date": date}
    )
    save_expenses(expenses)
    print(f"Added: {title} - Rs {amount:.2f}")


def print_table(items):
    if not items:
        print("No expenses found.")
        return
    print(f"\n{'ID':<5}{'Date':<13}{'Category':<15}{'Title':<22}{'Amount':>10}")
    print("-" * 65)
    for e in items:
        print(f"{e['id']:<5}{e['date']:<13}{e['category']:<15}"
              f"{e['title'][:20]:<22}{e['amount']:>10.2f}")
    print("-" * 65)
    print(f"{'Total':<55}{sum(e['amount'] for e in items):>10.2f}")


def view_expenses(expenses):
    ordered = sorted(expenses, key=lambda e: e["date"], reverse=True)
    print_table(ordered)


def delete_expense(expenses):
    view_expenses(expenses)
    if not expenses:
        return
    try:
        target = int(input("Enter ID to delete: "))
    except ValueError:
        print("Please enter a valid ID.")
        return
    for e in expenses:
        if e["id"] == target:
            expenses.remove(e)
            save_expenses(expenses)
            print(f"Deleted: {e['title']}")
            return
    print("No expense with that ID.")


def category_summary(expenses):
    if not expenses:
        print("No expenses yet.")
        return
    totals = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
    grand_total = sum(totals.values())
    print("\nSpending by category")
    print("-" * 40)
    for cat, amt in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        percent = (amt / grand_total) * 100
        bar = "#" * int(percent // 5)
        print(f"{cat:<15}{amt:>9.2f}  {percent:5.1f}%  {bar}")
    print("-" * 40)
    print(f"{'Total':<15}{grand_total:>9.2f}")


def monthly_report(expenses):
    month = input("Enter month (YYYY-MM, Enter for current): ").strip()
    if month == "":
        month = datetime.now().strftime("%Y-%m")
    filtered = [e for e in expenses if e["date"].startswith(month)]
    print(f"\nReport for {month}")
    print_table(filtered)


def export_csv(expenses):
    if not expenses:
        print("Nothing to export.")
        return
    with open("expenses_export.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=["id", "date", "category", "title", "amount"]
        )
        writer.writeheader()
        writer.writerows(expenses)
    print("Exported to expenses_export.csv")


# ---------- Main menu ----------

def show_menu():
    print("\n===== EXPENSE TRACKER =====")
    print("1. Add expense")
    print("2. View all expenses")
    print("3. Delete expense")
    print("4. Category summary")
    print("5. Monthly report")
    print("6. Export to CSV")
    print("7. Exit")


def main():
    expenses = load_expenses()
    actions = {
        "1": add_expense,
        "2": view_expenses,
        "3": delete_expense,
        "4": category_summary,
        "5": monthly_report,
        "6": export_csv,
    }
    while True:
        show_menu()
        choice = input("Choose an option (1-7): ").strip()
        if choice == "7":
            print("Goodbye! Your data is saved.")
            break
        action = actions.get(choice)
        if action:
            action(expenses)
        else:
            print("Invalid option. Please choose 1-7.")


if __name__ == "__main__":
    main()