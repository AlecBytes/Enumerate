import re
import csv
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import re
import logging

logger = logging.getLogger(__name__)

import re
import logging

logger = logging.getLogger(__name__)

def extract_balances_from_first_file(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()

    balances = {}
    seen_accounts = set()

    i = 0
    while i < len(content):
        line = content[i]

        # Stop processing if line starts with "TOTALS:"
        if re.match(r'^\s*TOTALS:', line):
            break

        # Regex for valid accounts (requires >=7 alphanumeric chars, adjust to your needs)
        match = re.search(r'^\s*(\d+[A-Za-z0-9]{3,})\s+.*?(\d[\d,]*\.\d+)(CR)?\s*$', line)
        if match:
            account_no = match.group(1)
            balance_str = match.group(2).replace(',', '')
            is_credit = bool(match.group(3))

            balance_total = float(balance_str)
            # If "CR" is present, make the balance negative
            if is_credit:
                balance_total = -balance_total

            # Look at the next line to detect previous owners
            if i + 1 < len(content):
                next_line = content[i+1]
                # If the next line has an asterisk in it (e.g. "MOTA*"), mark this account as a previous owner
                if '*' in next_line:
                    account_no += '*'

            # If we've already seen this exact account_no, append '*'
            # Don't this we need this anymore, we changed the logic to check for detectin prev owners
            # if account_no in seen_accounts:
            #     account_no += '*'
            # seen_accounts.add(account_no)

            balances[account_no] = balance_total
            logger.info(f"Extracted: {account_no} with balance {balance_total}")

        i += 1

    return balances




def extract_balances_from_second_file(file_path):#
    logger.info(f"Reading Excel file: {file_path}")
    df = pd.read_excel(file_path, sheet_name='Owner Balances', skiprows=4)
    balances = {}
    current_account = None

    for _, row in df.iterrows():
        acct_val = row.get('Account#', None)
        if pd.notna(acct_val):
            acct_str = str(acct_val)
            # Stop if "Summary" account
            if acct_str.lower() == "summary":
                break
            
            # Check if owner has '*', and if so, append '*' to the account number
            owner_val = str(row.get('Owner', ''))
            if '*' in owner_val:
                acct_str += '*'
            
            # Update the current account for subsequent rows
            current_account = acct_str

        # If there's still no valid account, skip
        if not current_account:
            continue

        # Parse the balance if it’s not NaN
        balance_val = row.get('Balance', None)
        if pd.notna(balance_val):
            # Convert string forms like "($390.00)" to negative floats
            if isinstance(balance_val, str):
                balance_val = balance_val.replace(',', '').strip()
                if balance_val.startswith('(') and balance_val.endswith(')'):
                    balance_val = -float(balance_val.strip('()'))
                else:
                    balance_val = float(balance_val)

            # Store in the balances dict under the current account
            balances[current_account] = balance_val

    return balances


def main():
    import tkinter as tk
    from tkinter import filedialog

    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a file dialog to select the first file
    file_path1 = filedialog.askopenfilename(
        title="Select the first .PRT file",
        filetypes=[("PRT files", "*.PRT"), ("All files", "*.*")]
    )
    if not file_path1:
        logger.error("No first file selected.")
        return

    # Extract balances from the first file
    balances_TOPSPro = extract_balances_from_first_file(file_path1)
    logger.info(f"Number of accounts in first file: {len(balances_TOPSPro)}")

    # Open a file dialog to select the second file
    file_path2 = filedialog.askopenfilename(
        title="Select the second Excel file",
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
    )
    if not file_path2:
        logger.error("No second file selected.")
        return

    # Extract balances from the second file
    balances_Central = extract_balances_from_second_file(file_path2)
    logger.info(f"Number of accounts in second file: {len(balances_Central)}")

    # Prompt for the location to save the output CSV file with a default file name
    output_file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        initialfile="AR_bal_Pro_vs_Central.csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if not output_file_path:
        logger.error("No output file selected.")
        return

    # Write the mismatched balances to the output CSV file
    with open(output_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Account No.', 'TOPS Pro', 'Central'])

        all_accounts = set(balances_TOPSPro.keys()).union(set(balances_Central.keys()))
        tolerance = 0.01  # Define a tolerance for floating-point comparison
        for account_no in all_accounts:
            balance_Pro = balances_TOPSPro.get(account_no, 0)
            balance_Central = balances_Central.get(account_no, 0)
            if (balance_Pro != 0 or balance_Central != 0) and abs(balance_Pro - balance_Central) > tolerance:
                csvwriter.writerow([account_no, balance_Pro, balance_Central])

    logger.info(f"Mismatched balances have been written to {output_file_path}")


if __name__ == "__main__":
    main()
