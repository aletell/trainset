import pandas as pd
import dask.dataframe as dd
from datetime import datetime

def validate_csv(file_path):
    try:
        # Read CSV file in chunks using Dask
        df = dd.read_csv(file_path)

        # Ensure the CSV file has four comma-delimited columns with the header: `series, timestamp, value, label`
        expected_columns = ['series', 'timestamp', 'value', 'label']
        if list(df.columns) != expected_columns:
            raise ValueError("CSV file must have columns: 'series', 'timestamp', 'value', 'label'")

        # Validate that the `series` column contains unique names for the time series
        if not df['series'].is_unique:
            raise ValueError("The 'series' column must contain unique names for the time series")

        # Validate that the `timestamp` column contains timestamps in ISO8601 format
        try:
            df['timestamp'] = df['timestamp'].map(lambda x: datetime.fromisoformat(x))
        except ValueError:
            raise ValueError("The 'timestamp' column must contain timestamps in ISO8601 format")

        # Validate that the `value` column contains numeric scalar values
        if not pd.api.types.is_numeric_dtype(df['value']):
            raise ValueError("The 'value' column must contain numeric scalar values")

        # Validate that the `label` column contains integer representations of booleans or other valid labels
        if not pd.api.types.is_integer_dtype(df['label']):
            raise ValueError("The 'label' column must contain integer representations of booleans or other valid labels")

        return df

    except Exception as e:
        print(f"Error validating CSV file: {e}")
        return None

def process_csv(file_path):
    df = validate_csv(file_path)
    if df is not None:
        # Perform any additional processing on the DataFrame here
        print("CSV file processed successfully")
        return df
    else:
        print("CSV file processing failed")
        return None

def validate_csv_format(file_path):
    try:
        # Read CSV file in chunks using Dask
        df = dd.read_csv(file_path)

        # Check if the CSV file has the format: `series, timestamp, value, label`
        if list(df.columns) == ['series', 'timestamp', 'value', 'label']:
            return validate_csv(file_path)

        # Check if the CSV file has the format: `datetime,indoor_temperature_indoor_temperature_1,valves_valve_position,setpoint_room_regulation_RoomControl_actual_value,brightness_brightness,CO2_CO2,rel_hum_rel_hum,motion_presence_motion`
        elif list(df.columns) == ['datetime', 'indoor_temperature_indoor_temperature_1', 'valves_valve_position', 'setpoint_room_regulation_RoomControl_actual_value', 'brightness_brightness', 'CO2_CO2', 'rel_hum_rel_hum', 'motion_presence_motion']:
            # Perform any additional processing or validation for this format here
            print("CSV file with the second format processed successfully")
            return df

        else:
            raise ValueError("CSV file must have one of the specified formats")

    except Exception as e:
        print(f"Error validating CSV file format: {e}")
        return None
