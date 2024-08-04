import torch
from torchvision import transforms
from PIL import Image
import cv2

# Define the transformation
transform = transforms.Compose([
    transforms.Resize((640, 640)),  # Resize to YOLOv8 input size
    transforms.ToTensor(),  # Convert the image to a tensor
])

# Initialize video capture (0 for the default camera)
cap = cv2.VideoCapture('testor.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to PIL image
    input_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Apply the transformation
    transformed_image = transform(input_image).unsqueeze(0)

    # Now you can pass `transformed_image` to your YOLOv8 model
    # For example:
    # outputs = yolov8_model(transformed_image)

    # Display the frame (Optional, for debugging purposes)
    cv2.imshow('Transformed Frame', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()
cv2.destroyAllWindows()

