import tabula
import pandas as pd

# Path to the PDF file
pdf_path = '.\\data\\FY_24-25_Board_of_Finance_Revised_Budget_6-4-24_Referendum.pdf'

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
    # Create file with headers
    headers = ['Description', 'FY24Budget', 'FY25Budget', 'Change', 'ChangePercent']
    df = pd.DataFrame(columns=headers)
    csv_file_path = 'budget_data.csv'
    df.to_csv(csv_file_path, index=False)

    # Set page range
    start_page = 93  # Starting page number (1-indexed for tabula)
    end_page = 98    # Ending page number (1-indexed for tabula)

    # Initialize an empty DataFrame
    df = pd.DataFrame()

    for page in range(start_page, end_page + 1):
        print(page)
        # Extract tables from the specified range of pages
        df = extract_tables_from_pages(pdf_path, page)
        new_row = pd.DataFrame([df.columns], columns=df.columns)
        df = pd.concat([new_row, df]).reset_index(drop=True)
        # Remove last 6 rows if last page
        if page == end_page:
            df = df.iloc[:-6]

        # Drop 2nd column
        df.drop(df.columns[1], axis=1, inplace=True)
        # Drop 3rd column
        df.drop(df.columns[2], axis=1, inplace=True)
        # Drop 4th column
        df.drop(df.columns[3], axis=1, inplace=True)
        # Remove space characters in the 2nd column
        df.iloc[:, 1] = df.iloc[:, 1].astype(str).str.replace(' ', '')
        # Remove space characters in the 3rd column
        df.iloc[:, 2] = df.iloc[:, 2].astype(str).str.replace(' ', '')

        if df is not None:
            # Print the DataFrame
            print(df)
            
            # Save the DataFrame to CSV
            df.to_csv(csv_file_path, mode='a', index=False, header=False)
            print(f"DataFrame saved to {csv_file_path}")
        else:
            print(f'No table found on page {page}')
