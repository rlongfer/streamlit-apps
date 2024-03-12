import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
#from pydantic_settings import BaseSettings
import sys
import os

st.set_page_config(page_title='Data Profiler', layout='wide')

def get_filesize(file):
    size_bytes = sys.getsizeof(file)
    size_mb = size_bytes / (1024**2)
    return size_mb


def validate_file(file):
    filename = file.name
    name, ext = os.path.splitext(filename)
    if ext in ('.csv', '.xlsx'):
        return ext
    else:
        return False


# side bar
with st.sidebar:
    uploaded_file = st.file_uploader("Upload .csv, .xlsx files not exceeding 10MB")
    if uploaded_file is not None:
        st.write("Modes of Operation")
        minimal = st.checkbox('Do you want minimal report?')
        display_mode = st.radio('Display mode:', options=('Primary', 'Dark', 'Orange'))
        
        if display_mode == 'Dark':
            dark_mode = True
            orange_mode = False
        elif display_mode == 'Orange':
            dark_mode = False
            orange_mode = True
        else:
            dark_mode = False
            orange_mode = False

if uploaded_file is not None:
    ext = validate_file(uploaded_file)
    if ext:
        filesize = get_filesize(uploaded_file)
        if filesize <= 10:
            if ext == 'csv':
                # time load csv
                df = pd.read_csv(uploaded_file)
            else:
                xl_file = pd.ExcelFile(uploaded_file)
                sheet_tuple = tuple(xl_file.sheet_names)
                sheet_name = st.sidebar.selectbox("Select the sheet", sheet_tuple)
                df = xl_file.parse(sheet_name)

            # generate report
            with st.spinner('Generating report...'):
                pr = ProfileReport(df,
                                minimal=minimal, 
                                dark_mode=dark_mode, 
                                orange_mode=orange_mode
                                )

            st_profile_report(pr)
        else:
            st.error("Maximum allowed filesize is 10MB. Received {filesize} MB")
    else:
        st.error("Kindly upload only .csv or .xlsx")
else:
    st.title("Data Profiler")
    st.info('Upload your data file')