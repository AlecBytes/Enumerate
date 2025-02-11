import csv
import tkinter as tk
from tkinter import filedialog
import os

def process_csv(file_path, output_path):
    def parse_amount(amount_str):
        amount_str = amount_str.replace(',', '').strip()
        if not amount_str:
            return 0.0
        if amount_str.startswith('(') and amount_str.endswith(')'):
            return -float(amount_str[1:-1])
        return float(amount_str)

    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        with open(output_path, mode='w', newline='') as output_file:
            fieldnames = ['GL Account', 'Account Description', 'Current Balance']
            csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            for row in csv_reader:
                gl_account = row['General Ledger Account Numbers']
                account_description = row['Department']
                current_balance = parse_amount(row['Amount'])
                if current_balance != 0:
                    csv_writer.writerow({
                        'GL Account': gl_account,
                        'Account Description': account_description,
                        'Current Balance': current_balance
                    })

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_dir = os.path.join(folder_path, 'output')
        os.makedirs(output_dir, exist_ok=True)
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".csv"):
                file_path = os.path.join(folder_path, file_name)
                input_filename = os.path.splitext(file_name)[0]
                output_filename = f"{input_filename}_output.csv"
                output_path = os.path.join(output_dir, output_filename)
                process_csv(file_path, output_path)

if __name__ == "__main__":
    select_folder()