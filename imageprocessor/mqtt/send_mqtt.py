import paho.mqtt.client as mqtt
import time
# MQTT broker details
mqtt_broker = "test.mosquitto.org"
mqtt_port = 1883
# Create a new MQTT client instance
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# Connect to the MQTT broker


def mqtt_publish_msg(sen1="sensor1",user1='user1',detected_animal = "elephant"):
    client.connect(mqtt_broker, mqtt_port, 60)
    # Publish a message to the topic
    # detected animal types {0:'human',1:'elephant',2:'monkey',3:'parrot',4:'rabbit'}
    client.publish(f"agri9urd/{user1}/{sen1}/dettype", detected_animal)
    # Disconnect from the broker
    client.disconnect()

while True:
    mqtt_publish_msg(sen1="sensor1",user1='21',detected_animal = "{'elephant'}")
    #add a delay
    time.sleep(15)
    