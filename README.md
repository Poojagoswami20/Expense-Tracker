# Expense Tracker (Python CLI)

A simple command-line expense tracker built with **plain Python** (no external libraries).
Made as the evaluated course project for **Python Essentials**.

## Features
- Add expenses with title, amount, category and date
- View all expenses in a clean table (newest first)
- Delete an expense by ID
- Category-wise spending summary with percentage bars
- Monthly report
- Export data to CSV
- Data saved automatically in `expenses.json`
- Input validation and error handling throughout

## Python Concepts Used
- Functions and modular code
- Lists, dictionaries, `lambda` and sorting
- File handling (JSON and CSV)
- Exception handling (`try/except`)
- Loops and conditionals
- `datetime` module for date validation

## How to Run
```bash
python expense_tracker.py
```
Requires Python 3.6 or above.

## Sample Output
```
===== EXPENSE TRACKER =====
1. Add expense
2. View all expenses
...

ID   Date         Category       Title                  Amount
-----------------------------------------------------------------
2    2026-09-23   Food           Lunch                  120.00
1    2026-09-22   Travel         Bus pass               450.00
-----------------------------------------------------------------
Total                                                   570.00
```

## Project Structure
```
expense-tracker/
├── expense_tracker.py
├── expenses.json      (created automatically on first run)
└── README.md
```

## Author
Pooja Goswami - First Year, B.Tech
