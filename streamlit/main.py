import streamlit as st
import pandas as pd

dir_data = '.\\data_refined\\'

# Function to load the CSV file
@st.cache_data
def load_data(file):
    data = pd.read_csv(file)
    return data

# Function to filter data based on search query
def filter_data(data, query):
    if query:
        return data[data.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    return data

# List of CSV files
csv_files = {
    'FY24-25 BOE Budget V1': 'FY24-25_BOE_V1.csv',
    'FY24-25 BOE Budget V2': 'FY24-25_BOE_V2.csv',
    #'Budget Data 3': 'budget_data_3.csv'
}

# Streamlit app
def main():
    st.title("Budget Data Viewer")

    # File selection
    selected_file = st.selectbox("Select a CSV file", list(csv_files.keys()))
    file_path = dir_data + csv_files[selected_file]
    
    # Load the CSV data
    data = load_data(file_path)
    
    # Search functionality
    search_query = st.text_input("Search")
    
    filtered_data = filter_data(data, search_query)
    
    # Display the dataframe with sortable and filterable columns
    st.dataframe(filtered_data,height=1000)
    
    # Allow the user to download the filtered data
    csv = filtered_data.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv',
    )

if __name__ == "__main__":
    main()
