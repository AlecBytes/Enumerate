import os
import pandas as pd
import logging
from tkinter import Tk, filedialog

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_csv_files(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Process each CSV file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, f"filtered_{filename}")

            try:
                # Read the CSV file
                df = pd.read_csv(input_file_path)

                # Ensure column names are stripped of leading/trailing spaces
                df.columns = df.columns.str.strip()

                # Filter rows where 'Owner ID' ends with 'H001'
                filtered_df = df[df['Owner ID'].str.endswith('H001', na=False)]

                # Select the required columns
                result_df = filtered_df[['Owner ID', 'Account Number']]

                # Save the result to the output file
                result_df.to_csv(output_file_path, index=False)
                logger.info(f"Processed file: {filename}")

            except Exception as e:
                logger.warning(f"Failed to process file: {filename}. Error: {e}")

def main():
    # Hide the root Tkinter window
    root = Tk()
    root.withdraw()

    # Ask the user to select a folder
    input_folder = filedialog.askdirectory(title="Select Folder with CSV Files")
    if not input_folder:
        logger.warning("No folder selected. Exiting.")
        return

    # Define the output folder
    output_folder = os.path.join(input_folder, 'output')

    # Process the CSV files
    process_csv_files(input_folder, output_folder)

if __name__ == "__main__":
    main()