import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os

# Create main window
root = tk.Tk()
root.title("Transaction Categorizer")
root.geometry("900x600")

# Force light colors explicitly
root.configure(bg='white')
root.option_add('*background', 'white')
root.option_add('*foreground', 'black')
root.option_add('*Button.background', 'lightgray')
root.option_add('*Button.foreground', 'black')

# Sample data from your question
transactions = [
    ("01/27/2026", "POP MART Americas Inc. NEW YORK NY", -43.74, ""),
    ("01/27/2026", "MINT MOBILE 800-683-7392 CA", -10.5, ""),
    ("01/28/2026", "Amazon.com*E61LG7YB3 Amzn.com/billWA", -13.33, ""),
    ("01/28/2026", "Amazon.com*6J7FM2D53 Amzn.com/billWA", -8.42, ""),
    ("01/31/2026", "Amazon.com*Z79IC31O3 Amzn.com/billWA", -23.1, ""),
    ("02/02/2026", "ICE CENTER OF CUPERTINO CUPERTINO CA", -20.0, "")
]

categories = ["Food", "Shopping", "Entertainment", "Bills", "Transport", "Other"]
category_vars = []

def create_gui():
    # Main container
    main_frame = tk.Frame(root, bg='white')
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Title
    title = tk.Label(main_frame, text="💰 Transaction Categorizer", 
                    font=('Arial', 18, 'bold'), 
                    bg='white', fg='black')
    title.pack(pady=10)
    
    # Create a frame for the table
    table_frame = tk.Frame(main_frame, bg='white')
    table_frame.pack(fill='both', expand=True, pady=10)
    
    # Create headers
    headers = tk.Frame(table_frame, bg='#4CAF50')
    headers.pack(fill='x')
    
    tk.Label(headers, text="Date", width=12, anchor='w', 
            bg='#4CAF50', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5, pady=5)
    tk.Label(headers, text="Description", width=50, anchor='w', 
            bg='#4CAF50', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5, pady=5)
    tk.Label(headers, text="Amount", width=12, anchor='w', 
            bg='#4CAF50', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5, pady=5)
    tk.Label(headers, text="Category", width=15, anchor='w', 
            bg='#4CAF50', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5, pady=5)
    
    # Create a canvas for scrolling
    canvas = tk.Canvas(table_frame, bg='white', highlightthickness=0)
    scrollbar = tk.Scrollbar(table_frame, orient='vertical', command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg='white')
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Pack canvas and scrollbar
    canvas.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    
    # Create transaction rows
    for i, (date, desc, amount, category) in enumerate(transactions):
        # Alternate row colors
        bg_color = '#FFFFFF' if i % 2 == 0 else '#F8F8F8'
        
        row_frame = tk.Frame(scrollable_frame, bg=bg_color)
        row_frame.pack(fill='x', pady=1)
        
        # Date
        tk.Label(row_frame, text=date, width=12, anchor='w', 
                bg=bg_color, fg='black').pack(side='left', padx=5, pady=5)
        
        # Description
        short_desc = (desc[:55] + "...") if len(desc) > 55 else desc
        tk.Label(row_frame, text=short_desc, width=50, anchor='w', 
                bg=bg_color, fg='black').pack(side='left', padx=5, pady=5)
        
        # Amount
        amount_color = '#D32F2F' if amount < 0 else '#388E3C'  # Red for negative, green for positive
        tk.Label(row_frame, text=f"${abs(amount):.2f}", width=12, anchor='w',
                bg=bg_color, fg=amount_color).pack(side='left', padx=5, pady=5)
        
        # Category dropdown
        var = tk.StringVar(value=category)
        category_vars.append(var)
        
        # Use OptionMenu for simplicity
        dropdown_frame = tk.Frame(row_frame, bg=bg_color)
        dropdown_frame.pack(side='left', padx=5, pady=5)
        
        option_menu = tk.OptionMenu(dropdown_frame, var, "", *categories)
        option_menu.config(bg=bg_color, fg='black', width=12)
        option_menu.pack()
    
    # Control panel
    control_frame = tk.Frame(main_frame, bg='white')
    control_frame.pack(fill='x', pady=20)
    
    # Add category section
    tk.Label(control_frame, text="Add New Category:", bg='white', fg='black').pack(side='left', padx=5)
    
    new_cat_var = tk.StringVar()
    tk.Entry(control_frame, textvariable=new_cat_var, width=20).pack(side='left', padx=5)
    
    def add_category():
        new_cat = new_cat_var.get().strip()
        if new_cat and new_cat not in categories:
            categories.append(new_cat)
            new_cat_var.set("")
            status_label.config(text=f"✓ Added category: {new_cat}")
            
            # Update all dropdowns
            for i, var in enumerate(category_vars):
                # Recreate the option menu with new categories
                for widget in scrollable_frame.winfo_children()[i].winfo_children()[-1].winfo_children():
                    if isinstance(widget, tk.OptionMenu):
                        widget.destroy()
                
                # Create new dropdown
                row_frame = scrollable_frame.winfo_children()[i]
                dropdown_frame = tk.Frame(row_frame, bg=row_frame.cget('bg'))
                dropdown_frame.pack(side='left', padx=5, pady=5)
                
                new_menu = tk.OptionMenu(dropdown_frame, var, "", *categories)
                new_menu.config(bg=row_frame.cget('bg'), fg='black', width=12)
                new_menu.pack()
        elif new_cat in categories:
            messagebox.showwarning("Warning", f"Category '{new_cat}' already exists!")
    
    tk.Button(control_frame, text="Add", command=add_category, 
             bg='#2196F3', fg='white', padx=15).pack(side='left', padx=5)
    
    # Action buttons
    button_frame = tk.Frame(main_frame, bg='white')
    button_frame.pack(pady=10)
    
    def save_csv():
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'Description', 'Amount', 'Category'])
                for (date, desc, amount, _), var in zip(transactions, category_vars):
                    writer.writerow([date, desc, f"${amount}", var.get() or "Uncategorized"])
            
            status_label.config(text=f"✓ Saved to {os.path.basename(filename)}")
            messagebox.showinfo("Success", f"File saved:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def export_by_category():
        # Group by category
        categorized = {}
        for (date, desc, amount, _), var in zip(transactions, category_vars):
            category = var.get() or "Uncategorized"
            if category not in categorized:
                categorized[category] = []
            categorized[category].append((date, desc, amount))
        
        folder = filedialog.askdirectory(title="Select folder to save files")
        if not folder:
            return
        
        try:
            # Save main file
            main_file = os.path.join(folder, "all_transactions.csv")
            with open(main_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Category', 'Date', 'Description', 'Amount'])
                for category, items in categorized.items():
                    for date, desc, amount in items:
                        writer.writerow([category, date, desc, f"${amount}"])
            
            # Save individual files
            for category, items in categorized.items():
                if category != "Uncategorized":
                    safe_name = category.replace(" ", "_").lower()
                    cat_file = os.path.join(folder, f"{safe_name}.csv")
                    with open(cat_file, 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Date', 'Description', 'Amount'])
                        for date, desc, amount in items:
                            writer.writerow([date, desc, f"${amount}"])
            
            status_label.config(text=f"✓ Exported to {folder}")
            messagebox.showinfo("Success", f"Files saved in:\n{folder}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def show_summary():
        summary = {}
        total = 0
        
        for (date, desc, amount, _), var in zip(transactions, category_vars):
            category = var.get() or "Uncategorized"
            if category not in summary:
                summary[category] = {'count': 0, 'total': 0}
            summary[category]['count'] += 1
            summary[category]['total'] += abs(amount)
            total += abs(amount)
        
        # Create summary window
        summary_window = tk.Toplevel(root)
        summary_window.title("Transaction Summary")
        summary_window.geometry("400x400")
        summary_window.configure(bg='white')
        
        text = tk.Text(summary_window, bg='white', fg='black', padx=10, pady=10)
        text.pack(fill='both', expand=True)
        
        text.insert('end', "TRANSACTION SUMMARY\n", 'title')
        text.insert('end', "=" * 40 + "\n\n")
        
        for category, data in sorted(summary.items()):
            text.insert('end', f"{category}:\n")
            text.insert('end', f"  Count: {data['count']} transactions\n")
            text.insert('end', f"  Total: ${data['total']:.2f}\n\n")
        
        text.insert('end', f"\nGRAND TOTAL: ${total:.2f}\n", 'total')
        
        # Configure tags
        text.tag_config('title', font=('Arial', 14, 'bold'), foreground='#2E7D32')
        text.tag_config('total', font=('Arial', 12, 'bold'), foreground='#1565C0')
        
        text.config(state='disabled')
    
    # Create buttons
    button_style = {'padx': 20, 'pady': 8, 'font': ('Arial', 10)}
    
    tk.Button(button_frame, text="💾 Save to CSV", command=save_csv,
             bg='#4CAF50', fg='white', **button_style).pack(side='left', padx=5)
    
    tk.Button(button_frame, text="📊 Show Summary", command=show_summary,
             bg='#2196F3', fg='white', **button_style).pack(side='left', padx=5)
    
    tk.Button(button_frame, text="📁 Export by Category", command=export_by_category,
             bg='#FF9800', fg='white', **button_style).pack(side='left', padx=5)
    
    tk.Button(button_frame, text="❌ Exit", command=root.quit,
             bg='#F44336', fg='white', **button_style).pack(side='left', padx=5)
    
    # Status bar
    global status_label
    status_label = tk.Label(root, text="✓ Ready - Loaded 6 sample transactions", 
                          bg='#E8F5E8', fg='#2E7D32', anchor='w', 
                          font=('Arial', 10), relief='sunken')
    status_label.pack(side='bottom', fill='x')

# Run the application
create_gui()
root.mainloop()