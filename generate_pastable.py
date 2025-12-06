
import csv
from collections import defaultdict

input_file = "statementscategorized.csv"

# category → list of rows
groups = defaultdict(list)

with open(input_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cat = row["Category"].strip()
        groups[cat].append(row)

for cat, rows in groups.items():
    output_file = f"{cat}.tsv"  # tab-separated
    with open(output_file, "w", newline="", encoding="utf-8") as out:
        # write the same headers
        out.write("transaction_date\tmerchant\tamount\tCategory\n")

        for r in rows:
            out.write(f"{r['transaction_date']}\t{r['merchant']}\t{r['amount']}\n")

