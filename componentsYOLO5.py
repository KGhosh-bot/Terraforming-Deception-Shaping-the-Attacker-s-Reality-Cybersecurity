import numpy as np
import cv2
import torch
from yolov5 import detect
import json

def image_preprocessing(image_path):
    # Read the image from the specified path
    image = cv2.imread(image_path)

    # Resize the image to a standard size for better processing
    image = cv2.resize(image, (416, 416))

    # Normalize the image values to a range of 0 to 1
    image = image / 255.0

    # Convert the image to a NumPy array
    image = np.array(image)

    return image

def extract_features(image_path):

    image = image_preprocessing(image_path)
    # Apply Canny edge detection to find edges in the image
    edges = cv2.Canny(image, 50, 150)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)

    # Apply morphological operations to clean up the edge image
    kernel = np.ones((3, 3), np.uint8)
    closed = cv2.morphologyEx(gray_image, cv2.MORPH_CLOSE, kernel)
    opening = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel)

    # Find contours (connected regions) in the edge image
    contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Extract feature descriptors for each contour
    features = []
    for contour in contours:
        # Calculate the Hu moments of the contour
        moments = cv2.HuMoments(contour)
        feature = np.array(moments)

        # Add the feature to the list of features
        features.append(feature)

    return features

def detect_components(image_path):

    features= extract_features(image_path)
    # Load the pre-trained or custom YOLOv5 model
    model.load("path/to/model")

    # Convert the image to a format compatible with the YOLOv5 model
    image = torch.from_numpy(image).float().permute(2, 0, 1)

    # Run the YOLOv5 model to detect components and predict class labels
    detections = model(image)

    # Extract bounding boxes and class labels for detected components
    boxes = detections[0]['boxes'].cpu().numpy()
    classes = detections[0]['labels'].cpu().numpy()

    # Map detected components to Docker images
    detected_components_to_docker_images = []
    for i, box in enumerate(boxes):
        class_label = classes[i]
        feature = features[i]

        docker_image = load_configuration("config.json")[class_label]
        detected_components_to_docker_images.append((box, class_label, docker_image))

        # Draw bounding boxes on the image
        image_with_boxes = image.copy()
        color = (0, 255, 0)  # Green color for the bounding boxes
        cv2.rectangle(image_with_boxes, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), color, 2)

    # Save the image with bounding boxes
    cv2.imwrite("/project/images/output_image.jpg", image_with_boxes)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return detected_components_to_docker_images

def load_configuration(config_path):
    # Read the configuration file
    with open(config_path) as f:
        configuration = json.load(f)

    # Convert the configuration to a dictionary or data structure
    component_to_docker_image_mapping = {}
    for component_type, docker_image in configuration.items():
        component_to_docker_image_mapping[component_type] = docker_image

    return component_to_docker_image_mapping
