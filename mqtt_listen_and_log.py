import paho.mqtt.client as mqtt
import json
from datetime import datetime
import os
import time

LOG_DIR = "../sensor_logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

START_TIME = time.time()

def log_to_file(sensor_id, data_type, value):
    seconds = time.time() - START_TIME
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"{LOG_DIR}/{sensor_id}_{data_type}.csv"
    
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("seconds;value;timestamp\n")

    with open(filename, "a") as f:
        f.write(f"{seconds:.3f};{value};{timestamp}\n")

def on_connect(client, userdata, flags, rc):
    print(f"Connected with code: {rc}")
    client.subscribe("zigbee2mqtt/#")
    print("Subscribed to topics")

def on_message(client, userdata, msg):
    print("\nReceived message:")
    print(f"Topic: {msg.topic}")
    try:
        data = json.loads(msg.payload.decode())
        print(f"Data: {data}")

        sensor_id = msg.topic.split('/')[-1]

        sensor_data = None
        if isinstance(data, dict):
            if 'message' in data:
                try:
                    message_parts = data['message'].split("payload '")
                    if len(message_parts) > 1:
                        sensor_data = json.loads(message_parts[1].rstrip("'"))
                except:
                    sensor_data = data
            else:
                sensor_data = data

        if sensor_data:
            if 'temperature' in sensor_data:
                temperature = sensor_data['temperature']
                print(f"Temperature: {temperature}°C")
                log_to_file(sensor_id, "temperature", temperature)

            if 'humidity' in sensor_data:
                humidity = sensor_data['humidity']
                print(f"Humidity: {humidity}%")
                log_to_file(sensor_id, "humidity", humidity)

    except json.JSONDecodeError:
        print(f"Raw data: {msg.payload.decode()}")
    except Exception as e:
        print(f"Error: {e}")

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Subscribed with QoS: {granted_qos}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

try:
    print(f"Program started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    client.connect("localhost", 1883, 60)
    print("Starting to listen...")
    client.loop_forever()

except Exception as e:
    print(f"Connection error: {e}")
