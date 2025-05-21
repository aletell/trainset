import pandas as pd

def parse_csv(file_path):
    """
    Parses a CSV file, checks for required columns, and processes data.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pandas.DataFrame: The processed DataFrame.

    Raises:
        FileNotFoundError: If the file_path does not exist.
        ValueError: If required columns are missing or time conversion fails.
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File not found at {file_path}")

    required_columns = ['time', 'series', 'val']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Error: Missing required column: {col}")

    if 'label' not in df.columns:
        df['label'] = ''  # Add empty 'label' column

    try:
        df['time'] = pd.to_datetime(df['time'])
    except Exception as e:
        raise ValueError(f"Error converting 'time' column to datetime: {e}")

    return df
