# bankstatement-scraper-organizer

1. Navigate to Bank of America. Before copying the transactions, click on the date sorter so it sorts in increasing date. This is so that we dont get the extra "expand" text.
2. Copy and paste all of the transactions from each of your credit cards for this month into creditcard_transactions.txt. Each entry should looks something like "Expand transaction for Transaction date: 11/10/2025 TIGER NOODLE HOUSE HOUSTON TX 11/10/2025	Expand transaction for Transaction date: 11/10/2025TIGER NOODLE HOUSE HOUSTON TX	Type Purchases
$49.65	"
3. Copy and paste all of the transactions from each of your debit cards for this month into debitcard_transactions.txt. Each entry should look something like "01/21/2026	
PP*APPLE.COM/BILL 01/20 PURCHASE 402-935-7733 CA
View/Edit
Virtual Card	-$10.99	$2,180.79	"
3. Next we will run the parser.py using "python parser.py" and it will turn it into a table called expenses.csv with each row being a transaction and it will be also sorted in order of purchasing date.
4. Go through the csv and for any transaction where it is unclear what kind of item you purchased, find out what that item is and add it to the merchant name, so that it will be easier for you to sort the transactions. Make sure to not remove any commas or disturb the structure of the csv.
4. Next we will run the sort.py using "python sort.py" and it will make us manually sort each of the transactions into categories and when finished click save. It will save it into a csv file called statementscategorized.csv.
5. Next we will run the generate_pastable.py using "python generate_pastable.py" and it will generate a folder called category_tsvs and inside will be multiple csv files each representing the transactions for each category. Copy and paste these into google sheets for each categories' sheet.
