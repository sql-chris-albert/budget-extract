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
    'FY24-25 BOE 1st Budget': 'FY24-25_BOE_V1.csv',
    'FY24-25 BOE 2nd Budget': 'FY24-25_BOE_V2.csv',
    'FY24-25 BOE Budget Comparison': 'FY24-25_BOE_V1_V2_Comparison.csv'
}

# About page content
def show_about():
    st.title("About")
    st.markdown("""
    This data is proudly provided to you by Chris Albert, a local Canton resident.
    I worked on this in my spare time with no affiliation to anyone. I'm not here to take anyone's
    side in the arguments at hand. I simply want to provide folks with a better set of tools
    to understand the data our town provides.
    """)

# Main app content
def show_main():
    st.title("Canton Info")

    # Help box
    with st.expander("Help (How to use this site)"):
        st.markdown("""
        **How to use this app:**
        - **Select a dataset**: Choose a dataset from the dropdown menu
        - **Search**: Use the search box to filter data by entering keywords or phrases
        - **Sort**: Click on the column headers to change how the data is sorted
        """)

    # File selection
    selected_file = st.selectbox("Select a dataset to view", list(csv_files.keys()))
    file_path = dir_data + csv_files[selected_file]
    
    # Load the CSV data
    data = load_data(file_path)
    
    # Search functionality
    search_query = st.text_input("Search")
    
    filtered_data = filter_data(data, search_query)
    
    # Display the dataframe with sortable and filterable columns
    st.dataframe(filtered_data, height=1000)
    
    # Allow the user to download the filtered data
    csv = filtered_data.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv',
    )

# Streamlit app
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select a page", ["Main", "About"])
    
    if page == "Main":
        show_main()
    elif page == "About":
        show_about()

if __name__ == "__main__":
    main()
