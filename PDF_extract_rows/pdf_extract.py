import PyPDF2
import csv
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

def extract_text_from_pdf(pdf_path):
    pdf_file = open(pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    pdf_file.close()
    return text

def save_text_to_csv(text, csv_path):
    lines = text.split('\n')
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for line in lines:
            writer.writerow([line])

if __name__ == "__main__":
    # Hide the root window
    Tk().withdraw()
    
    # Prompt the user to select the PDF file
    pdf_path = askopenfilename(title="Select PDF file", filetypes=[("PDF files", "*.pdf")])
    
    if pdf_path:
        # Prompt the user to select the location to save the CSV file
        csv_path = asksaveasfilename(title="Save CSV file", defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        
        if csv_path:
            text = extract_text_from_pdf(pdf_path)
            save_text_to_csv(text, csv_path)
            print(f"Text extracted from {pdf_path} and saved to {csv_path}")
        else:
            print("No location selected for saving the CSV file.")
    else:
        print("No file selected.")