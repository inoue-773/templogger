import requests
import mysql.connector
import time
from datetime import datetime

# Define the API URLs
TEMPERATURE_API = "http://nickyboy-server.dynns.com:2525/temperature"
HUMIDITY_API = "http://nickyboy-server.dynns.com:2525/humidity"
PRESSURE_API = "http://nickyboy-server.dynns.com:2525/pressure"

# Database connection details
DB_HOST = "mysql://root:xrVZjpxfKDqwjNELXeLleaEwDPlEBllk@viaduct.proxy.rlwy.net:12023/railway"
DB_USER = "root"
DB_PASSWORD = "xrVZjpxfKDqwjNELXeLleaEwDPlEBllk"
DB_NAME = "railway"

# Establish the database connection
db_connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

# Function to create the necessary table if it doesn't exist
def create_table():
    cursor = db_connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        temperature FLOAT,
        humidity FLOAT,
        pressure FLOAT
    )
    """)
    db_connection.commit()

# Function to insert data into the database
def insert_data(temperature, humidity, pressure):
    cursor = db_connection.cursor()
    timestamp = datetime.now()
    cursor.execute("""
    INSERT INTO sensor_data (timestamp, temperature, humidity, pressure)
    VALUES (%s, %s, %s, %s)
    """, (timestamp, temperature, humidity, pressure))
    db_connection.commit()

# Function to get data from the APIs
def get_data():
    try:
        temperature = requests.get(TEMPERATURE_API).json()['temperature']
        humidity = requests.get(HUMIDITY_API).json()['humidity']
        pressure = requests.get(PRESSURE_API).json()['pressure']
        return temperature, humidity, pressure
    except Exception as e:
        print(f"Error getting data: {e}")
        return None, None, None

# Create the table if it doesn't exist
create_table()

# Main loop to fetch data every 1 minute
while True:
    temperature, humidity, pressure = get_data()
    if temperature is not None and humidity is not None and pressure is not None:
        insert_data(temperature, humidity, pressure)
        print(f"Data inserted: {datetime.now()} - Temp: {temperature}, Humidity: {humidity}, Pressure: {pressure}")
    else:
        print("Failed to retrieve data")
    time.sleep(60)
