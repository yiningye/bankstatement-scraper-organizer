import csv
import tkinter as tk
from tkinter import filedialog, messagebox

transactions = []
headers = []
current_index = 0
categorized = []

CATEGORIES = ["Rent", "Pet", "Water", "Electricity", "Car Insurance", "Phone", "Gas", "Travel", "Pet", "Medical Expense", "Groceries", "Socialization", "UnsortedAmazon", "Other", "Charity", "Investment"]

def load_csv():
    global transactions, headers, current_index, categorized
    path = "expenses.csv"
    if not path:
        return
    with open(path, newline="") as f:
        reader = csv.reader(f)
        data = list(reader)
    if not data:
        return
    headers = data[0]
    transactions = data[1:]
    categorized = [None] * len(transactions)
    current_index = 0
    show_transaction()

def show_transaction():
    if current_index >= len(transactions):
        messagebox.showinfo("Done", "All transactions categorized!")
        return
    for widget in frame.winfo_children():
        widget.destroy()

    t = transactions[current_index]
    tk.Label(frame, text="Transaction:", font=("Arial", 14)).pack(pady=5)
    tk.Label(frame, text=", ".join(t), wraplength=500).pack(pady=5)

    tk.Label(frame, text="Choose category:", font=("Arial", 12)).pack(pady=5)
    for cat in CATEGORIES:
        btn = tk.Button(frame, text=cat, width=15,
                        command=lambda c=cat: categorize(c))
        btn.pack(pady=2)

def categorize(category):
    global current_index
    categorized[current_index] = category
    current_index += 1
    show_transaction()

def save_results():
    if not transactions or not categorized:
        return
    path = "statementscategorized.csv"
    if not path:
        return
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers + ["Category"])
        for row, cat in zip(transactions, categorized):
            writer.writerow(row + [cat])
    messagebox.showinfo("Saved", f"Saved categorized transactions to {path}")

root = tk.Tk()
root.title("Transaction Sorting GAME OOH LALA SO FUN")

tk.Button(root, text="Load CSV", command=load_csv).pack(pady=5)
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Button(root, text="Save Results", command=save_results).pack(pady=5)

root.mainloop()