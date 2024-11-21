import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print(f"Connected with code: {rc}")
    # Subscribe to all Zigbee2MQTT topics
    client.subscribe("zigbee2mqtt/#")
    print("Subscribed to topics")

def on_message(client, userdata, msg):
    print("\nReceived message:")
    print(f"Topic: {msg.topic}")
    try:
        payload = json.loads(msg.payload.decode())
        print(f"Data: {payload}")
        # If temperature data exists
        if 'temperature' in payload:
            print(f"Temperature: {payload['temperature']}°C")
        if 'humidity' in payload:
            print(f"Humidity: {payload['humidity']}%")
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