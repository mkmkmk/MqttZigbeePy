# pip3 install paho-mqtt python-dotenv

import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv

# .env file:
# SWITCH_ID=<your_switch_id>
load_dotenv()
SWITCH_ID = os.getenv("SWITCH_ID")

def switch_control(client, state):
    topic = f"zigbee2mqtt/{SWITCH_ID}/set"
    payload = json.dumps({"state": state})
    client.publish(topic, payload)

def on_connect(client, userdata, flags, rc):
    print(f"Connected with code: {rc}")
    # Subscribe to all Zigbee2MQTT topics
    client.subscribe("zigbee2mqtt/#")
    print("Subscribed to topics")

def on_message(client, userdata, msg):
    print("\nMessage received:")
    print(f"Topic: {msg.topic}")
    try:
        payload = json.loads(msg.payload.decode())
        print(f"Data: {payload}")

        # Ignore messages with empty values
        if msg.topic.endswith('/get'):
            return

        # If temperature data is present
        if 'temperature' in payload:
            temp = payload['temperature']
            print(f"Temperature: {temp}°C")

            if isinstance(temp, (int, float)):
                if temp >= 27:
                    switch_control(client, "OFF")

                if temp < 27:
                    switch_control(client, "ON")

        if 'humidity' in payload:
            print(f"Humidity: {payload['humidity']}%")

            # if payload['humidity'] > 42:
            #     switch_control(client, "ON")
            # if payload['humidity'] < 41:
            #     switch_control(client, "OFF")

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
    client.connect("localhost", 1883, 60)
    print("Starting to listen...")
    client.loop_forever()

except Exception as e:
    print(f"Connection error: {e}")