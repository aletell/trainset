import unittest
from dash import Dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.express as px
from flask import Flask
import base64
import io

from app import app, parse_contents

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.server.test_client()

    def test_upload_csv(self):
        csv_data = "series,timestamp,value,label\nseries1,2021-01-01T00:00:00Z,1.0,0\nseries1,2021-01-01T01:00:00Z,2.0,1"
        encoded_csv = base64.b64encode(csv_data.encode()).decode()
        contents = f"data:text/csv;base64,{encoded_csv}"
        filename = "test.csv"

        df = parse_contents(contents, filename)
        self.assertIsNotNone(df)
        self.assertEqual(len(df), 2)
        self.assertEqual(df.columns.tolist(), ["series", "timestamp", "value", "label"])

    def test_update_output(self):
        csv_data = "series,timestamp,value,label\nseries1,2021-01-01T00:00:00Z,1.0,0\nseries1,2021-01-01T01:00:00Z,2.0,1"
        encoded_csv = base64.b64encode(csv_data.encode()).decode()
        contents = f"data:text/csv;base64,{encoded_csv}"
        filename = "test.csv"

        with self.app.server.test_request_context():
            output = self.app.callback_map['update_output']['callback'](contents, filename)
            self.assertIsNotNone(output)
            self.assertEqual(len(output), 2)

    def test_display_hover_data(self):
        hover_data = {
            'points': [{
                'x': '2021-01-01T00:00:00Z',
                'y': 1.0,
                'curveNumber': 0
            }]
        }

        with self.app.server.test_request_context():
            output = self.app.callback_map['display_hover_data']['callback'](hover_data)
            self.assertIsNotNone(output)
            self.assertIn('Time: 2021-01-01T00:00:00Z', output)
            self.assertIn('Value: 1.0', output)
            self.assertIn('Series: 0', output)

    def test_add_label(self):
        selected_data = {
            'points': [{
                'x': '2021-01-01T00:00:00Z',
                'y': 1.0,
                'curveNumber': 0
            }]
        }

        with self.app.server.test_request_context():
            output = self.app.callback_map['add_label']['callback'](1, selected_data)
            self.assertIsNotNone(output)
            self.assertIn('Labels added.', output)

    def test_delete_label(self):
        selected_data = {
            'points': [{
                'x': '2021-01-01T00:00:00Z',
                'y': 1.0,
                'curveNumber': 0
            }]
        }

        with self.app.server.test_request_context():
            output = self.app.callback_map['delete_label']['callback'](1, selected_data)
            self.assertIsNotNone(output)
            self.assertIn('Labels deleted.', output)

if __name__ == '__main__':
    unittest.main()
