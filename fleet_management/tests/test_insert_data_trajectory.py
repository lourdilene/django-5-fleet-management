import os
from unittest.mock import patch, MagicMock, mock_open
from django.test import TestCase
from fleet_management.automate.insert_data_trajectory import create_db_connection, create_table, cache_taxi_ids, insert_data, main

class TestDatabase(TestCase):
    @patch('fleet_management.automate.insert_data_trajectory.psycopg2.connect')
    def test_create_db_connection(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        conn = create_db_connection()

        self.assertEqual(conn, mock_connection)

    @patch('fleet_management.automate.insert_data_trajectory.psycopg2.connect')
    def test_create_table(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor

        create_table(mock_connection)

        mock_cursor.execute.assert_called_once()

    @patch('fleet_management.automate.insert_data_trajectory.psycopg2.connect')
    def test_cache_taxi_ids(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [(1,), (2,)]

        taxi_ids = cache_taxi_ids(mock_connection)

        self.assertEqual(taxi_ids, {1, 2})

    @patch('fleet_management.automate.insert_data_trajectory.psycopg2.connect')
    @patch('builtins.open', mock_open(read_data="2024-01-01,10.0,20.0\n2024-01-02,15.0,25.0\n"))
    def insert_data(conn, directory, taxi_ids):
        cursor = conn.cursor()
        trajectories_dir = os.path.join(directory, "trajectories")
        if not os.path.exists(trajectories_dir):
            print(f"Error: Directory {trajectories_dir} does not exist.")
            return
        
        file_list = sorted(os.listdir(trajectories_dir), key=natural_sort_key)
        for filename in file_list:
            if filename.endswith(".txt"):
                taxi_id = int(os.path.splitext(filename)[0])
                file_path = os.path.join(trajectories_dir, filename)
                print(f"Processing file: {file_path}")
                if taxi_id in taxi_ids:
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            data = line.strip().split(',')
                            date, latitude, longitude = data[0], float(data[1]), float(data[2])
                            cursor.execute("INSERT INTO fleet_management_trajectory (date, latitude, longitude, taxi_id) VALUES (%s, %s, %s, %s)", (date, latitude, longitude, taxi_id))
                    conn.commit()
                    print(f"File processed: {file_path}")
                else:
                    print(f"Skipping file: taxi_id {taxi_id} does not exist in fleet_management_taxi")
                print("------------------------------")
        cursor.close()

    @patch('fleet_management.automate.insert_data_trajectory.create_db_connection')
    @patch('fleet_management.automate.insert_data_trajectory.create_table')
    @patch('fleet_management.automate.insert_data_trajectory.insert_data')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main(self, mock_parse_args, mock_insert_data, mock_create_table, mock_create_db_connection):

        mock_parse_args.return_value = MagicMock(directory='directory')

        main()

        mock_create_db_connection.assert_called_once()
        mock_create_table.assert_called_once()
        mock_insert_data.assert_called_once()
