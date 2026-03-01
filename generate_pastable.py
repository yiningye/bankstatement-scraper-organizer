import os
import csv
from collections import defaultdict
import shutil

input_file = "statementscategorized.csv"

# category → list of rows
groups = defaultdict(list)

with open(input_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cat = row["Category"].strip()
        groups[cat].append(row)

OUTPUT_DIR = "category_tsvs"

if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
    print(f"Clear: {OUTPUT_DIR}")
else:
    print(f"Folder not found: {OUTPUT_DIR}")

for cat, rows in groups.items():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = f"category_tsvs/{cat}.tsv"  # tab-separated
    with open(output_file, "w", newline="", encoding="utf-8") as out:
        # write the same headers
        out.write("transaction_date\tmerchant\tamount\n")

        for r in rows:
            out.write(f"{r['transaction_date']}\t{r['merchant']}\t{r['amount']}\n")

