import cv2
from ultralytics import YOLO
from send_mqtt import mqtt_publish_msg
from db import cnx_pool

# Load the YOLOv8 model
model = YOLO("yolov8n_elephant.pt")

# model inputs
video_path = 'testor.mp4'
sensor='sensor1'
user='user1'

# Define the class names (make sure this matches your model's classes)
class_names = [
    "elephant", "monkey", "parrot", "rabbit", "peacock", "cow"
    # Add more class names as needed
]
# Open the video file

cap = cv2.VideoCapture(video_path)

# Loop through the video frames
priv_log=set()# check and solve double message problem

while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()
    if success:
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
                print(f"Class: {class_label}, ID: {class_id}, Confidence: {confidence}, Box: [{x1}, {y1}, {x2}, {y2}]")
            #condition double tap detected confidance and accuracy
            if detected_class_labels!=priv_log:
                # TODO: implement db logger
                # sent mqtt message
                mqtt_publish_msg(sen1=sensor,user1=user,detected_animal = f"{detected_class_labels}")
                # create mysql log for the detected animal or human             
                
        else:
            print("No detections in this frame.")

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
