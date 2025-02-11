# AR Balance Match

This program compares account balances between TOPS Pro and Central and identifies mismatched balances.

## Prerequisites

- Ensure you have the necessary permissions to run executables on your system.
- Ensure you have the required reports from TOPS Pro and Central.

## Steps to Use

1. **Generate Reports:**
   - In TOPS Pro, run the Owner Balance Summary report, check classic mode, and save the report to a file with a `.PRT` extension.
   - In Central, run the Owner Balance Report and save the report to an Excel file.

2. **Run the Program:**
   - Execute `AR_balance_match.exe`.

3. **Select Files:**
   - First, select the TOPS Pro `.PRT` file when prompted.
   - Next, select the Central Excel file when prompted.

4. **Save the Output:**
   - Choose a location and save the output file. The default file name is `AR_bal_Pro_vs_Central.csv`.

5. **Review the Output:**
   - The output file will show the accounts with balance totals that do not match.
   - Use this information to make adjustments in Central until the grand total matches.

## Example Usage

1. Run the Owner Balance Summary report in TOPS Pro, check classic mode, and save it (`AR0001.PRT`).
2. Run the Owner Balance Report in Central and save it as `CentralReport.xlsx`.
3. Execute `AR_balance_match.exe`.
4. Select `TOPSProReport.PRT` when prompted.
5. Select `CentralReport.xlsx` when prompted.
6. Save the output file as `AR_bal_Pro_vs_Central.csv`.
7. Open `AR_bal_Pro_vs_Central.csv` to review mismatched balances and make necessary adjustments in Central.

## Notes

- Ensure the reports are generated correctly and saved in the appropriate formats.
- The program will prompt you to select the files and save the output file.
- The output file will contain columns for Account No., TOPS Pro balance, and Central balance.

## Troubleshooting

- If you encounter any issues, ensure the file paths are correct and the files are in the expected formats.
- If the executable is flagged by Windows security, you may need to allow it to run or sign the executable with a trusted certificate.

## Contact

For any issues or questions, please contact alexander.patterson@goenumerate.com.