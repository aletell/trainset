# Python TRAINSET - Time Series Labeling Tool

A Python-based graphical tool for labeling time series data, inspired by the original TRAINSET application. This version is built using Flask, Dash, and Plotly.

## Features

*   Upload time series data via CSV files.
*   Interactive visualization of time series.
*   Select active and reference series for display.
*   Create, assign, and manage labels for data points.
*   Label individual points by clicking.
*   Label multiple points by selecting a region (box/lasso select).
*   Export labeled data back to a CSV file.
*   User-friendly interface with on-screen instructions.

## Tech Stack

*   Python
*   Flask (for web framework and file uploads)
*   Dash (for building the interactive dashboard)
*   Plotly (for charting)
*   Pandas (for data manipulation)
*   Pytest (for unit testing)

## Setup Instructions

### Prerequisites

*   Python 3.7+
*   pip (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url> # Replace <repository_url> with the actual URL
    cd python-trainset # Or your project's directory name
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    # venv\Scripts\activate
    # On macOS/Linux
    # source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Start the Flask development server:**
    ```bash
    python app.py
    ```

2.  **Access the application:**
    *   **To upload data:** Open your web browser and go to `http://127.0.0.1:5000/`.
    *   **Main Labeling Interface:** After uploading data, you will be redirected to `http://127.0.0.1:5000/dash/`. You can also access this URL directly if data has been previously uploaded in the current session.

## Usage

Once the application is running and data is loaded:

1.  Follow the on-screen instructions provided within the application for detailed steps on loading data, selecting series, managing labels, labeling data points, and exporting your results.
2.  **Expected CSV Format:** The input CSV file should contain columns typically named `time`, `series`, `val`. An optional `label` column can be included if you have pre-existing labels.
    *   `time`: Timestamp data (parsable by Pandas, e.g., `YYYY-MM-DD HH:MM:SS`).
    *   `series`: Name or identifier for the time series.
    *   `val`: Numerical value of the series at the given time.
    *   `label` (optional): Text label associated with the data point.

## Running Tests

To run the unit tests for the backend data handling:

```bash
pytest tests/
```
