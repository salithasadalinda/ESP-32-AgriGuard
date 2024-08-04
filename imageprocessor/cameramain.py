import cv2
import urllib.request
import numpy as np
import time
import cv2
from ultralytics import YOLO
# from imageprocessor.mqtt.send_mqtt import mqtt_publish_msg
from db import cnx_pool,create_log
import datetime
import torch
from torchvision import transforms
from PIL import Image
##########################################################mqttp#############################################
import paho.mqtt.client as mqtt
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

##########################################################yolo model####################################
# Load the YOLOv8 model
#model = YOLO("yolov8n_elephant_100.pt")
model=YOLO("C:/Users/admin/Downloads/Wildlife-Conservation-Detection-main/best.pt")
# Define the transformation
transform = transforms.Compose([
    transforms.Resize((480, 640)),  # Resize to YOLOv8 input size
    transforms.ToTensor(),  # Convert the image to a tensor
])

# Replace the URL with the IP camera's stream URL
url = 'http://192.168.8.104/cam-hi.jpg'
# test: injection(!)
url = 'https://www.thoughtco.com/thmb/q4t3OQkJIwiyTHnV4Pve34f4Ygo%3D/2250x1500/filters:fill(auto%2C1)/167003501-56a0089e5f9b58eba4ae8f93.jpg'

sensor='sensor1'
user=21 # user name
desired_fps = 15 # desired frame rate in fps

# cv2.namedWindow(f"live Cam Testing{user}/{sensor}", cv2.WINDOW_AUTOSIZE)
class_names = [
    "elephant", "monkey", "parrot", "rabbit", "peacock", "cow"
    # Add more class names as needed
]
# Define the desired frame rate and compute the delay

frame_delay = int(1000 / desired_fps)  # milliseconds

priv_log=set()# check and solve double message problem
while True:
    try:
        # Read a frame from the URL
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        frame = cv2.imdecode(imgnp, -1)
        transformed_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        frame = transform(transformed_image).unsqueeze(0)
        

        if frame is None:
            # If decoding failed, print an error message and continue
            print("Error: Failed to decode image")
            continue
        
        ####################################pipeline start##################################
        # Run YOLOv8 inference on the frame
        results = model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Check if there are any detections
        if results[0].boxes is not None:
            # Print the detected results
            detected_class_labels = set() # create a set to avoid duplicates
            for result in results[0].boxes:
                # Get the bounding box coordinates
                x1, y1, x2, y2 = result.xyxy[0].cpu().numpy()
                # Get the confidence score
                confidence = result.conf[0].cpu().numpy()
                # Get the class ID
                class_id = int(result.cls[0].cpu().numpy())
                # Get the class label
                class_label = class_names[class_id]
                # adding detected result to the set
                detected_class_labels.add(class_label)
                # print(f"Class: {class_label}, ID: {class_id}, Confidence: {confidence}, Box: [{x1}, {y1}, {x2}, {y2}]")
            #condition double tap detected confidance and accuracy null detection
            if detected_class_labels!=priv_log and detected_class_labels!= set():
                # sent mqtt message
                mqtt_publish_msg(sen1=sensor,user1=user,detected_animal = f"{detected_class_labels}")
                # create mysql log for the detected animal or human    
                now = datetime.datetime.now()
                create_log(sensorid=sensor, name=f'{detected_class_labels}', date=now.strftime("%Y-%m-%d"), log_time=now.strftime("%H:%M:%S"), userid=user)
                # send detection result intu image blob to see the case really
                priv_log=detected_class_labels
        
        ####################################piipeline stop##################################

        # Display the frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Wait for the specified delay to achieve the desired FPS
        key = cv2.waitKey(frame_delay)
        if key == ord('q'):
            break

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)  # Wait a bit before retrying in case of errors

cv2.destroyAllWindows()
