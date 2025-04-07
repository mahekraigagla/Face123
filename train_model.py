import cv2
import os
import numpy as np
from PIL import Image
import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def train_model():
    # Paths
    haarcasecade_path = "haarcascade_frontalface_default.xml"
    trainimage_path = "TrainingImage"
    trainimagelabel_path = "TrainingImageLabel/Trainner.yml"
    
    # Create TrainingImageLabel directory if it doesn't exist
    if not os.path.exists("TrainingImageLabel"):
        os.makedirs("TrainingImageLabel")
    
    # Initialize face recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(haarcasecade_path)
    
    # Get faces and IDs
    faces = []
    Ids = []
    
    # Get all subdirectories in TrainingImage
    for root, dirs, files in os.walk(trainimage_path):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):
                path = os.path.join(root, file)
                # Get the ID from the filename (format: User.id.jpg)
                Id = int(os.path.split(path)[-1].split("_")[1])
                # Convert image to grayscale
                pilImage = Image.open(path).convert('L')
                imageNp = np.array(pilImage, 'uint8')
                faces.append(imageNp)
                Ids.append(Id)
    
    if len(faces) == 0:
        print("No training images found!")
        text_to_speech("No training images found!")
        return
    
    # Train the model
    recognizer.train(faces, np.array(Ids))
    recognizer.save(trainimagelabel_path)
    
    print("Model trained successfully!")
    text_to_speech("Model trained successfully!")

if __name__ == "__main__":
    train_model() 