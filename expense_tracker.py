import csv
import argparse
import os
from datetime import datetime

# CSV File Name
CSV_FILE = "expenses.csv"

# Ensure CSV file exists with headers
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount", "Description"])


# Function to Add an Expense
def add_expense(category, amount, description):
    date = datetime.now().strftime("%Y-%m-%d")
    
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])
    
    print(f"✅ Expense Added: {category} - {amount} - {description}")


# Function to View All Expenses
def view_expenses():
    with open(CSV_FILE, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        
        print("\n📌 Your Expenses:")
        for row in reader:
            print(f"{row[0]} | {row[1]} | Rs.{row[2]} | {row[3]}")
    

# Function to Filter Expenses by Date or Category
def filter_expenses(category=None, start_date=None, end_date=None):
    with open(CSV_FILE, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row

        filtered_expenses = []
        for row in reader:
            date, cat, amount, description = row
            
            # Convert date to datetime object
            date_obj = datetime.strptime(date, "%Y-%m-%d")

            # Apply filters
            if category and cat.lower() != category.lower():
                continue
            
            if start_date and date_obj < datetime.strptime(start_date, "%Y-%m-%d"):
                continue

            if end_date and date_obj > datetime.strptime(end_date, "%Y-%m-%d"):
                continue

            filtered_expenses.append(row)

        # Display filtered results
        print("\n📌 Filtered Expenses:")
        for row in filtered_expenses:
            print(f"{row[0]} | {row[1]} | Rs.{row[2]} | {row[3]}")
        
        if not filtered_expenses:
            print("❌ No matching records found.")


# CLI with Argparse
def main():
    parser = argparse.ArgumentParser(description="Simple Expense Tracker")

    parser.add_argument("--add", nargs=3, metavar=("CATEGORY", "AMOUNT", "DESCRIPTION"), help="Add a new expense")
    parser.add_argument("--view", action="store_true", help="View all expenses")

    # ✅ Fix: Separate optional arguments for filtering
    parser.add_argument("--filter-category", metavar="CATEGORY", help="Filter expenses by category")
    parser.add_argument("--filter-start-date", metavar="START_DATE", help="Filter expenses from this date (YYYY-MM-DD)")
    parser.add_argument("--filter-end-date", metavar="END_DATE", help="Filter expenses until this date (YYYY-MM-DD)")

    args = parser.parse_args()

    if args.add:
        category, amount, description = args.add
        add_expense(category, amount, description)

    elif args.view:
        view_expenses()

    elif args.filter_category or args.filter_start_date or args.filter_end_date:
        filter_expenses(category=args.filter_category, start_date=args.filter_start_date, end_date=args.filter_end_date)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
