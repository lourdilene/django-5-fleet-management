from unittest.mock import patch, MagicMock, mock_open
from django.test import TestCase
from fleet_management.automate.insert_data_taxi import create_db_connection, create_table, insert_data, main

class TestDatabase(TestCase):
    @patch('fleet_management.automate.insert_data_taxi.psycopg2.connect')
    def test_create_db_connection(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        conn = create_db_connection()

        self.assertEqual(conn, mock_connection)

    @patch('fleet_management.automate.insert_data_taxi.psycopg2.connect')
    def test_create_table(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor

        create_table(mock_connection)

        mock_cursor.execute.assert_called_once()

    @patch('fleet_management.automate.insert_data_taxi.psycopg2.connect')
    def test_insert_data(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor

        with patch('builtins.open', mock_open(read_data="1,ABC123\n2,DEF456\n")):
            insert_data(mock_connection, 'directory')

        mock_cursor.execute.assert_called()

    @patch('fleet_management.automate.insert_data_taxi.create_db_connection')
    @patch('fleet_management.automate.insert_data_taxi.create_table')
    @patch('fleet_management.automate.insert_data_taxi.insert_data')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main(self, mock_parse_args, mock_insert_data, mock_create_table, mock_create_db_connection):

        mock_parse_args.return_value = MagicMock(directory='directory')

        main()

        mock_create_db_connection.assert_called_once()
        mock_create_table.assert_called_once()
        mock_insert_data.assert_called_once()
