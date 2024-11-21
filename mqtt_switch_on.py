# pip3 install paho-mqtt python-dotenv
import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv

# .env file:
# SWITCH_ID=<your_switch_id>
load_dotenv()
SWITCH_ID = os.getenv("SWITCH_ID")

def switch_control(state):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect("localhost", 1883, 60)

    topic = f"zigbee2mqtt/{SWITCH_ID}/set"
    payload = json.dumps({"state": state})
    client.publish(topic, payload)
    client.disconnect()

# examples:
switch_control("ON")  # turn on
# switch_control("OFF")  # turn off
