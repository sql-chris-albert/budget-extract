import tabula
import pandas as pd

# Path to the PDF file
pdf_path = '.\\data\\FY_2024_2025_Board_of_Education_Final_Budget.pdf'

def extract_tables_from_pages(pdf_path,page):
    try:
        # Extract tables from the specified range of pages
        tables = tabula.read_pdf(pdf_path, pages=page, multiple_tables=True)

        if not tables:
            return None
        
        # Concatenate all tables from the specified pages into one DataFrame
        df = pd.concat(tables, ignore_index=True)

        return df
    except Exception as e:
        print(f"Exception encountered: {e}")
        return None

if __name__ == "__main__":
    start_page = 24  # Starting page number (1-indexed for tabula)
    end_page = 24    # Ending page number (1-indexed for tabula)

    # Extract tables from the specified range of pages
    df = extract_tables_from_pages(pdf_path, start_page, end_page)

    if df is not None:
        # Print the DataFrame
        print(df)
        
        # Save the DataFrame to a CSV file
        csv_file_path = "budget_data_pages.csv"
        df.to_csv(csv_file_path, index=False)
        print(f"DataFrame saved to {csv_file_path}")
    else:
        print("No table found on the specified pages.")
