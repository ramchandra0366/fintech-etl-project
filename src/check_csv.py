
from pathlib import Path
import csv

file_path = Path(
    r"E:\Fintech Project\data\transactions.csv"
)

print("FILE EXISTS:", file_path.exists())
print("FILE SIZE:", file_path.stat().st_size if file_path.exists() else 0)

with file_path.open("r", encoding="utf-8-sig", newline="") as file:
    first_line = file.readline()
    print("FIRST LINE:", repr(first_line))

    file.seek(0)

    sample = file.read(2048)
    file.seek(0)

    print("SAMPLE:", repr(sample))

    dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
    print("DETECTED DELIMITER:", repr(dialect.delimiter))

    reader = csv.DictReader(file, dialect=dialect)
    print("DETECTED COLUMNS:", reader.fieldnames)

    for row in reader:
        print(row)
