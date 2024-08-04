import paho.mqtt.client as mqtt

def mqtt_publish_msg(sen1="sensor1",user1=21,angle = 90):
    # MQTT broker details
    mqtt_broker = "test.mosquitto.org"
    mqtt_port = 1883
    # Create a new MQTT client instance
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    # Connect to the MQTT broker
    client.connect(mqtt_broker, mqtt_port, 60)

    # Publish a message to the topic
    # detected animal types {0:'human',1:'elephant',2:'monkey',3:'parrot',4:'rabbit'}

    client.publish(f"agri9urd/{user1}/{sen1}/cameraangle", angle)
    
    # Disconnect from the broker
    client.disconnect()


# mqtt_publish_msg(sen1="sensor1",user1='user1',detected_animal = "elephant")
import streamlit as st

st.title("Camera Setup")
angle = st.slider('Angle', 0, 180, 90)
print(angle)

mqtt_publish_msg(sen1="sensor1",user1=21,angle=f'{angle}')



