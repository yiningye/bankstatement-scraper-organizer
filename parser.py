import re
import csv
from datetime import datetime

date_pattern = re.compile(r"\b\d{2}/\d{2}/\d{4}\b")
amount_pattern = re.compile(r"-?\$\d+\.\d{2}")

def parse_blocks(lines):
    records = []
    buffer = []

    def process_block(block):
        text = " ".join(block)

        # extract dates
        dates = date_pattern.findall(text)
        if len(dates) < 2:
            return None
        txn_date = dates[0]

        # merchant = text between first and second date
        first = text.find(dates[0]) + len(dates[0])
        second = text.find(dates[1], first)
        merchant = text[first:second].strip()

        # extract amount
        amt_match = amount_pattern.search(text)
        if not amt_match:
            return None
        amount = amt_match.group().replace("$", "")

        return [txn_date, merchant, amount]

    for line in lines:
        if (line.startswith("Expand transaction for Transaction date:") and not line.endswith("Payment")):
            if buffer:
                rec = process_block(buffer)
                if rec:
                    records.append(rec)
                buffer = []
                
        buffer.append(line)
    
    

    # last block
    if buffer:
        rec = process_block(buffer)
        if rec:
            records.append(rec)
    records.sort(key=lambda x: x[0])

    return records


def write_csv(records, out_path):
    with open(out_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["transaction_date", "merchant", "amount"])
        w.writerows(records)


if __name__ == "__main__":
    with open("transactions.txt") as f:
        lines = [l.strip() for l in f if l.strip()]
    
    records = parse_blocks(lines)
    print(records)

    write_csv(records, "transactions.csv")
