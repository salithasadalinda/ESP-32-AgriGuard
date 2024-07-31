import paho.mqtt.client as mqtt


# MQTT broker details
mqtt_broker = "test.mosquitto.org"  # Replace with your broker's IP or hostname
mqtt_port = 1883


# Callback function when a message is received
def on_message(client, userdata, message):
    print(f"Message received: {message.payload.decode()} on topic {message.topic}")

# Create a new MQTT client instance
client = mqtt.Client()

# Assign the on_message callback function
client.on_message = on_message

# Connect to the MQTT broker
client.connect(mqtt_broker, mqtt_port, 60)

# Subscribe to the topic
user1='user1'
sen1='sen1'
client.subscribe(f"agri9urd/{user1}/{sen1}/dettype")

# Start the MQTT client
client.loop_start()

print("Subscribed to topic 'agri9urd/dettype'")

# Keep the script running to listen for messages
try:
    while True:
        
        pass
except KeyboardInterrupt:
    print("Exiting...")
    client.loop_stop()
    client.disconnect()


def subscribe_to_topic(client, user1, sen1):
    topic = f"agri9urd/{user1}/{sen1}/dettype"
    client.subscribe(topic)
    print(f"Subscribed to topic '{topic}'")
