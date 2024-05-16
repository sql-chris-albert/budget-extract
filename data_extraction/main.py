import PyPDF2
import pandas as pd

# Path to the PDF file
pdf_path = '.\\data\\FY_2024_2025_Board_of_Education_Final_Budget.pdf'

def extract_text_from_page(pdf_path, page_number):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        if page_number < 0 or page_number >= len(pdf_reader.pages):
            return "Invalid page number"
        
        page = pdf_reader.pages[page_number]
        text = page.extract_text()
    
    return text

def parse_table_from_text(text):
    # Split the text into lines
    lines = text.split('\n')
    
    # Initialize lists to store the data
    descriptions, fy24_budgets, fy25_budgets, increases, perc_increases = [], [], [], [], []

    # Iterate over each line and extract data
    for line in lines:
        # Remove any leading/trailing whitespace
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
        
        # Check if the line contains budget data
        parts = line.split()
        
        # Try to identify budget data by looking for numbers with commas or periods
        budget_data_indices = [i for i, part in enumerate(parts) if any(char.isdigit() for char in part)]
        
        # Check if we have at least four parts that seem to be budget data
        if len(budget_data_indices) >= 4:
            # Extract the last four elements as budget data
            fy24_budget = parts[budget_data_indices[-4]].replace(',', '').replace('$', '')
            fy25_budget = parts[budget_data_indices[-3]].replace(',', '').replace('$', '')
            increase = parts[budget_data_indices[-2]].replace(',', '').replace('$', '')
            perc_increase = parts[budget_data_indices[-1]].replace('%', '')
            
            # Join the rest of the parts to form the description
            description = ' '.join(parts[:budget_data_indices[-4]])
            
            # Append the data to the lists
            descriptions.append(description)
            fy24_budgets.append(fy24_budget)
            fy25_budgets.append(fy25_budget)
            increases.append(increase)
            perc_increases.append(perc_increase)

    # Create a DataFrame from the extracted data
    df = pd.DataFrame({
        'Description': descriptions,
        'FY24 Budget ($)': fy24_budgets,
        'Proposed FY25 Budget ($)': fy25_budgets,
        'Increase/(Decrease) ($)': increases,
        'Percent Increase/(Decrease) (%)': perc_increases
    })

    return df

if __name__ == "__main__":
    page_number = 18  # Page numbers are zero-indexed

    # Extract text from the specified page
    page_text = extract_text_from_page(pdf_path, page_number)
    
    # Parse the table from the extracted text
    df = parse_table_from_text(page_text)
    
    # Print the DataFrame
    print(df)

    # Save the DataFrame to a CSV file
    csv_file_path = "budget_data.csv"
    df.to_csv(csv_file_path, index=False)
    print(f"DataFrame saved to {csv_file_path}")