import os
import argparse
import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv

def create_db_connection():
    try:
        conn = psycopg2.connect(
            dbname='local_db',
            user='local_user',
            password='local_password',
            host='172.19.0.2',
            port='5432'
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fleet_management_taxi (
        id SERIAL PRIMARY KEY,
        id INTEGER,
        plate TEXT
    )
    """)
    conn.commit()
    cursor.close()

def insert_data(conn, directory):
    cursor = conn.cursor()
    taxi_file_path = os.path.join(directory, "taxis", "taxi.txt")
    with open(taxi_file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            id, plate = line.strip().split(',')
            cursor.execute("INSERT INTO fleet_management_taxi (id, plate) VALUES (%s, %s)", (id, plate))
    conn.commit()
    cursor.close()

def main():
    parser = argparse.ArgumentParser(description='Insert taxi data into PostgreSQL database')
    parser.add_argument('directory', type=str, help='Path to the directory containing taxi.txt')
    args = parser.parse_args()

    conn = create_db_connection()
    create_table(conn)

    insert_data(conn, args.directory)

    print("Taxi data inserted successfully!")

if __name__ == "__main__":
    main()