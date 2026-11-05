
import csv
from pathlib import Path
from decimal import Decimal

# Find the main project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_DIR / "data" / "transactions.csv"
OUTPUT_DIR = PROJECT_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "clean_transactions.csv"


def extract_transactions(file_path):
    """Read raw transactions from a CSV file."""
    with file_path.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def transform_transactions(rows):
    """Validate records and keep successful transactions."""
    clean_rows = []

    for row in rows:
        try:
            amount = Decimal(row["amount"])

            if not row["transaction_id"].strip():
                continue

            if not row["customer_id"].strip():
                continue

            if not amount.is_finite() or amount <= 0:
                continue

            if row["status"].strip().upper() != "SUCCESS":
                continue

            row["amount"] = f"{amount:.2f}"
            clean_rows.append(row)

        except (ValueError, ArithmeticError, KeyError):
            continue

    return clean_rows


def load_transactions(rows, file_path):
    """Write validated transactions to a new CSV file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "transaction_id",
        "customer_id",
        "transaction_date",
        "amount",
        "currency",
        "status",
    ]

    with file_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    raw_rows = extract_transactions(INPUT_FILE)
    clean_rows = transform_transactions(raw_rows)
    load_transactions(clean_rows, OUTPUT_FILE)

    print(f"Rows extracted: {len(raw_rows)}")
    print(f"Successful transactions: {len(clean_rows)}")
    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
