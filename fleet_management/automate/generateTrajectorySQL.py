import random
from datetime import datetime, timedelta

def generate_coordinate(start, end):
    return start + random.random() * (end - start)

def generate_datetime(start, end):
    delta = end - start
    random_delta = random.random() * delta.total_seconds()
    return start + timedelta(seconds=random_delta)

start_date = datetime(2024, 2, 2, 7, 0, 0)
end_date = datetime(2024, 2, 2, 20, 0, 0)

start_latitude = -50.6948108
end_latitude = -48.2719388
start_longitude = -2.6435809
end_longitude = -7.1429848

with open('automate/trajectory.sql', 'w') as file:
    for _ in range(45):
        random_date = generate_datetime(start_date, end_date)
        latitude = generate_coordinate(start_latitude, end_latitude)
        longitude = generate_coordinate(start_longitude, end_longitude)
        sql_command = f"INSERT INTO trajectories (taxi_id, date, latitude, longitude) VALUES ('1', '{random_date}', {latitude}, {longitude});\n"
        file.write(sql_command)
