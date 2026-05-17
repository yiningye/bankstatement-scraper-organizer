import re
import csv
from datetime import datetime

date_pattern = re.compile(r"\b\d{2}/\d{2}/\d{4}\b")
amount_pattern = re.compile(r"-?\$[\d,]+\.\d{2}")
TRANSACTION_TYPES = ("Deposit", "Other Payment", "Virtual Card", "Debit Card")

def parse_creditcard_blocks(lines):
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
        amount = float(
            amt_match.group().replace("$", "").replace(",", "")
        ) * -1

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

    return records
# -------------------
# Debit card parser
# -------------------
def parse_debitcard_blocks(transactions):
    # Each transaction uses 5 elements: date, merchant, view/edit, transaction line, blank
    parsed = []
    for i in range(0, len(transactions), 5):
        date = transactions[i].strip()                  # remove extra spaces/tabs
        merchant = transactions[i+1].strip().replace(',', '')           # merchant/description
        transaction_line = transactions[i+3].strip()  # contains type and amount
        type_amt_arr = transaction_line.split('\t')
        if type_amt_arr[0] not in TRANSACTION_TYPES:
            continue
        amount = float(type_amt_arr[1].replace('$', '').replace(',', ''))       # split by tab and take amount
        parsed.append((date, merchant, amount))
    print(parsed)
    return parsed

def split_expenses_and_income(records):
    expenses = []
    payments = []

    for date, merchant, amount in records:
        if amount < 0:
            expenses.append([date, merchant, amount])
        elif amount > 0:
            payments.append([date, merchant, amount])
            print(merchant, amount,"payments")

    return expenses, payments

def write_csv(records, out_path):
    with open(out_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["transaction_date", "merchant", "amount"])
        w.writerows(records)


if __name__ == "__main__":
    with open("1.paste/creditcard_transactions.txt") as f:
        creditcard_lines = [l.strip() for l in f if l.strip()]
    
    with open("1.paste/debitcard_transactions.txt") as f:
        debitcard_lines = [l.rstrip("\n") for l in f]
    print(debitcard_lines,"debitcard lines")
    creditcard_records = parse_creditcard_blocks(creditcard_lines)
    debitcard_records = parse_debitcard_blocks(debitcard_lines)
    # print("debitcard_records:", debitcard_records)
    
    records = creditcard_records + debitcard_records
    
    records.sort(key=lambda x: x[0])
    
    expenses, income = split_expenses_and_income(records)
    
    write_csv(expenses, "expenses.csv")
    write_csv(income, "income.csv")
    print(debitcard_records)
