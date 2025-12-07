# bankstatement-scraper-organizer

1. Navigate to Bank of America and click on the date sorter so it sorts in increasing date. This is so that we dont get the extra "expand" text.
2. Copy and paste all of the transactions from each of your credit cards for this month into transactions.txt. Each entry should looks something like "Expand transaction for Transaction date: 11/10/2025 TIGER NOODLE HOUSE HOUSTON TX 11/10/2025	Expand transaction for Transaction date: 11/10/2025TIGER NOODLE HOUSE HOUSTON TX	Type Purchases
$49.65	"
3. Next we will run the parser.py using python3 "parser.py" and it will turn it into a table called transactions.csv with each row being a transaction and it will be also sorted in order. 
4. Next we will run the sort.py using python3 "sort.py" and it will make us manually sort each of the transactions into categories and when finished it will save it into a csv file called statementscategorized.csv.
5. Next we will run the generate_pastable.py using python3 "generate_pastable.py" and it will generate a folder called category_tsvs and inside will be multiple csv files each representing the transactions for each category. Copy and paste these into google sheets for each categories' sheet.
