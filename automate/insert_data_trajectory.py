import os
import re
import argparse
import psycopg2
from psycopg2 import extras

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
    CREATE TABLE IF NOT EXISTS fleet_management_trajectory (
        id SERIAL PRIMARY KEY,
        date TIMESTAMP,
        latitude FLOAT,
        longitude FLOAT,
        taxi_id INTEGER,
        FOREIGN KEY (taxi_id) REFERENCES fleet_management_taxi (taxi_id)
    )
    """)
    conn.commit()
    cursor.close()

def cache_taxi_ids(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM fleet_management_taxi")
    taxi_ids = set(row[0] for row in cursor.fetchall())
    cursor.close()
    return taxi_ids

def natural_sort_key(s):
    """Define uma chave de classificação que realiza uma ordenação numérica natural."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def insert_data(conn, directory, taxi_ids):
    cursor = conn.cursor()
    trajectories_dir = os.path.join(directory, "trajectories")
    # Listar arquivos e ordenar numericamente pelo nome
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
                        date, latitude, longitude = data[1], float(data[2]), float(data[3])
                        cursor.execute("INSERT INTO fleet_management_trajectory (date, latitude, longitude, taxi_id) VALUES (%s, %s, %s, %s)", (date, latitude, longitude, taxi_id))
                conn.commit()
                print(f"File processed: {file_path}")
            else:
                print(f"Skipping file: taxi_id {taxi_id} does not exist in fleet_management_taxi")
            print("------------------------------")
    cursor.close()

def main():
    parser = argparse.ArgumentParser(description='Insert trajectory data into PostgreSQL database')
    parser.add_argument('directory', type=str, help='Path to the directory containing trajectories')
    args = parser.parse_args()

    conn = create_db_connection()
    create_table(conn)
    taxi_ids = cache_taxi_ids(conn)

    insert_data(conn, args.directory, taxi_ids)

    print("All trajectory data inserted successfully!")

if __name__ == "__main__":
    main()
