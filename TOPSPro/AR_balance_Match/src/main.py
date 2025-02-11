import re
import csv
import pandas as pd

def extract_balances_from_first_file(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()

    balances = {}
    for line in content:
        if line.startswith('D6'):
            match = re.search(r'D6\s+(\d+).+?([\d,]+\.\d+)(CR)?\s*$', line)
            if match:
                account_no = match.group(1)
                balance_total = float(match.group(2).replace(',', ''))
                if match.group(3):  # If 'CR' is present
                    balance_total = -balance_total
                balances[account_no] = balance_total
    return balances

def extract_balances_from_second_file(file_path):
    df = pd.read_excel(file_path, sheet_name='Owner Balances', skiprows=4)
    # print(df.columns)  # Print the column names for debugging
    balances = {}
    account_no = None
    for _, row in df.iterrows():
        if pd.notna(row['Account#']):
            account_no = str(row['Account#'])
            if account_no == "Summary":
                break
        if 'Total' in str(row['Unnamed: 5']):
            balance_total = row['Balance']
            if isinstance(balance_total, str):
                balance_total = balance_total.replace(',', '')
                if balance_total.startswith('(') and balance_total.endswith(')'):
                    balance_total = -float(balance_total.strip('()'))
                else:
                    balance_total = float(balance_total)
            balances[account_no] = balance_total
    return balances

def main():
    import tkinter as tk
    from tkinter import filedialog

    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a file dialog to select the first file
    file_path1 = filedialog.askopenfilename(title="Select the first .PRT file", filetypes=[("PRT files", "*.PRT"), ("All files", "*.*")])
    if not file_path1:
        print("No first file selected.")
        return

    # Extract balances from the first file
    balances_TOPSPro = extract_balances_from_first_file(file_path1)

    # Open a file dialog to select the second file
    file_path2 = filedialog.askopenfilename(title="Select the second Excel file", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if not file_path2:
        print("No second file selected.")
        return

    # Extract balances from the second file
    balances_Central = extract_balances_from_second_file(file_path2)

    # Prompt for the location to save the output CSV file with a default file name
    output_file_path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile="AR_bal_Pro_vs_Central.csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if not output_file_path:
        print("No output file selected.")
        return

    # Write the mismatched balances to the output CSV file
    with open(output_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Account No.', 'TOPS Pro', 'Central'])

        all_accounts = set(balances_TOPSPro.keys()).union(set(balances_Central.keys()))
        tolerance = 0.01  # Define a tolerance for floating-point comparison
        for account_no in all_accounts:
            balance_Pro = balances_TOPSPro.get(account_no)
            balance_Central = balances_Central.get(account_no)
            if balance_Pro is None or balance_Central is None or abs(balance_Pro - balance_Central) > tolerance:
                csvwriter.writerow([account_no, balance_Pro, balance_Central])

    print(f"Mismatched balances have been written to {output_file_path}")

if __name__ == "__main__":
    main()