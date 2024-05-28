import streamlit as st
import pandas as pd

# Set page layout to wide
st.set_page_config(layout="wide")

dir_data = './data_refined/'

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

# Function to highlight columns from the second dataset
def highlight_v2_cols(s):
    return ['background-color: yellow' if '_2' in c else '' for c in s.index]

# List of CSV files
csv_files = {
    'FY24-25 BOE Budget V1': 'FY24-25_BOE_V1.csv',
    'FY24-25 BOE Budget V2': 'FY24-25_BOE_V2.csv',
    # 'Budget Data 3': 'budget_data_3.csv'
}

# Streamlit app
def main():
    st.title("Budget Data Comparison Viewer")

    # File selection for Dataset 1
    selected_file_1 = st.selectbox("Select the first CSV file", list(csv_files.keys()), key='file1')
    file_path_1 = dir_data + csv_files[selected_file_1]
    
    # File selection for Dataset 2
    selected_file_2 = st.selectbox("Select the second CSV file", list(csv_files.keys()), key='file2')
    file_path_2 = dir_data + csv_files[selected_file_2]
    
    # Load the CSV data
    data1 = load_data(file_path_1)
    data2 = load_data(file_path_2)
    
    # Convert the Description column to lowercase for case-insensitive join
    data1['Description'] = data1['Description'].str.lower()
    data2['Description'] = data2['Description'].str.lower()

    # Join the datasets on the "Description" column
    if "Description" in data1.columns and "Description" in data2.columns:
        joined_data = pd.merge(data1, data2, on="Description", suffixes=('_1', '_2'))
    else:
        st.error("Both datasets must contain a 'Description' column.")
        return

    # Search functionality
    search_query = st.text_input("Search")
    
    filtered_data = filter_data(joined_data, search_query)
    
    # Apply highlighting to the dataframe
    styled_data = filtered_data.style.apply(highlight_v2_cols, axis=1)
    
    # Display the styled dataframe with sortable and filterable columns
    st.dataframe(styled_data, height=1000)
    
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
