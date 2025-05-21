import pytest
import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal
import os
import tempfile
from data_handler import parse_csv # Assuming data_handler.py is in the root

# Test Data Definitions
SAMPLE_VALID_CSV_CONTENT = """time,series,val,label
2023-01-01 00:00:00,seriesA,10,label1
2023-01-01 00:01:00,seriesA,12,label1
2023-01-01 00:00:00,seriesB,100,label2
"""

SAMPLE_VALID_NO_LABEL_CSV_CONTENT = """time,series,val
2023-01-01 00:00:00,seriesA,10
2023-01-01 00:01:00,seriesA,12
"""

SAMPLE_MISSING_COLUMN_CSV_CONTENT = """time,series,label
2023-01-01 00:00:00,seriesA,label1
"""

SAMPLE_BAD_TIME_FORMAT_CSV_CONTENT = """time,series,val
not_a_date,seriesA,10
2023-01-01 00:01:00,seriesA,12
"""

SAMPLE_EMPTY_CSV_CONTENT = "time,series,val,label\n" # Header only
SAMPLE_TRULY_EMPTY_CSV_CONTENT = "" # Completely empty

# Helper function to create temp csv
def create_temp_csv(content):
    # suffix='.csv' ensures a .csv extension, which some parsers might implicitly check
    # delete=False is important on Windows to allow pd.read_csv to open it by name.
    # The file will be cleaned up manually in a finally block or by the test runner.
    temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv', newline='')
    temp_file.write(content)
    temp_file.close() # Close the file so pandas can open it
    return temp_file.name

def test_parse_valid_csv_with_labels():
    file_path = create_temp_csv(SAMPLE_VALID_CSV_CONTENT)
    try:
        df = parse_csv(file_path)
        assert isinstance(df, pd.DataFrame)
        expected_columns = ['time', 'series', 'val', 'label']
        assert all(col in df.columns for col in expected_columns)
        assert len(df.columns) == len(expected_columns) # Ensure no extra columns
        assert pd.api.types.is_datetime64_ns_dtype(df['time'])
        assert df.shape[0] == 3 # Number of data rows
        assert df['series'].tolist() == ['seriesA', 'seriesA', 'seriesB']
        assert df['val'].tolist() == [10, 12, 100]
        assert df['label'].tolist() == ['label1', 'label1', 'label2']
    finally:
        os.remove(file_path)

def test_parse_valid_csv_without_labels():
    file_path = create_temp_csv(SAMPLE_VALID_NO_LABEL_CSV_CONTENT)
    try:
        df = parse_csv(file_path)
        assert isinstance(df, pd.DataFrame)
        expected_columns = ['time', 'series', 'val', 'label']
        assert all(col in df.columns for col in expected_columns)
        assert len(df.columns) == len(expected_columns)
        assert pd.api.types.is_datetime64_ns_dtype(df['time'])
        assert (df['label'] == '').all() # Should be added as empty strings
        assert df.shape[0] == 2
    finally:
        os.remove(file_path)

def test_parse_csv_missing_required_column():
    file_path = create_temp_csv(SAMPLE_MISSING_COLUMN_CSV_CONTENT)
    try:
        with pytest.raises(ValueError, match="Error: Missing required column: val"):
            parse_csv(file_path)
    finally:
        os.remove(file_path)

def test_parse_csv_bad_time_format():
    file_path = create_temp_csv(SAMPLE_BAD_TIME_FORMAT_CSV_CONTENT)
    try:
        # The current parse_csv raises ValueError if time conversion fails.
        # If it were to coerce, the test would be:
        # df = parse_csv(file_path)
        # assert pd.isna(df['time'].iloc[0])
        # assert pd.api.types.is_datetime64_ns_dtype(df['time'].iloc[1])
        with pytest.raises(ValueError, match="Error converting 'time' column to datetime"):
            parse_csv(file_path)
    finally:
        os.remove(file_path)

def test_parse_empty_csv_header_only():
    file_path = create_temp_csv(SAMPLE_EMPTY_CSV_CONTENT)
    try:
        df = parse_csv(file_path)
        assert isinstance(df, pd.DataFrame)
        expected_columns = ['time', 'series', 'val', 'label']
        assert all(col in df.columns for col in expected_columns)
        assert len(df.columns) == len(expected_columns)
        assert df.empty
    finally:
        os.remove(file_path)

def test_parse_truly_empty_csv():
    file_path = create_temp_csv(SAMPLE_TRULY_EMPTY_CSV_CONTENT)
    try:
        # pandas read_csv on an empty file might raise an EmptyDataError
        # or return an empty DataFrame depending on pandas version and parameters.
        # The parse_csv function should handle this, likely raising a ValueError
        # if required columns cannot be found after attempting to read.
        with pytest.raises(ValueError, match="Error: Missing required column: time"):
             parse_csv(file_path) # Or could be 'series' or 'val' depending on check order
    finally:
        os.remove(file_path)


def test_parse_file_not_found():
    with pytest.raises(FileNotFoundError, match="Error: File not found at non_existent_file.csv"):
        parse_csv("non_existent_file.csv")

# Example of a more complex test with specific values and types
def test_parse_csv_data_integrity():
    content = """time,series,val,label
2023-01-01T10:00:00Z,seriesX,1.23,event_A
2023-01-01T10:05:00Z,seriesX,4.56,
2023-01-01T10:10:00Z,seriesY,7.89,event_B
"""
    file_path = create_temp_csv(content)
    try:
        df = parse_csv(file_path)
        assert df.shape == (3, 4)
        assert df['time'].iloc[0] == pd.Timestamp('2023-01-01 10:00:00')
        assert df['series'].iloc[1] == 'seriesX'
        assert df['val'].iloc[2] == 7.89
        assert df['label'].iloc[0] == 'event_A'
        assert df['label'].iloc[1] == '' # Empty string for missing label
        assert isinstance(df['val'].dtype, pd.Float64Dtype) # if pandas >= 1.0
    finally:
        os.remove(file_path)
