import cv2
import numpy as np
from tensorflow.keras.models import model_from_json
import winsound  # Import the winsound module

# Load Face Detection Model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load Anti-Spoofing Model graph
json_file = open('antispoofing_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)

# Load antispoofing model weights
model.load_weights('antispoofing_model.h5')
print("Model loaded from disk")

# Start video capture
video = cv2.VideoCapture(0)

while True:
    try:
        # Read frame from video stream
        ret, frame = video.read()
        
        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            # Extract face region
            face = frame[y-5:y+h+5, x-5:x+w+5]
            
            # Resize face to a fixed size
            resized_face = cv2.resize(face, (160, 160))
            
            # Preprocess face image
            resized_face = resized_face.astype("float") / 255.0
            resized_face = np.expand_dims(resized_face, axis=0)
            
            # Pass face through the anti-spoofing model
            preds = model.predict(resized_face)[0]
            
            # Determine if the face is real or fake
            if preds > 0.5:
                label = 'FAKE'
                color = (0, 0, 255)  # Red for fake
                # Activate buzzer for fake face
                winsound.Beep(1000, 500)  # Beep at 1000 Hz for 500 ms
            else:
                label = 'Real'
                color = (0, 255, 0)  # Green for real
            
            # Draw rectangle around the face and display label
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        
        # Display frame
        cv2.imshow('frame', frame)
        
        # Check for user input to quit
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
            
    except Exception as e:
        print("Error:", e)

# Release video capture object and close all OpenCV windows
video.release()
cv2.destroyAllWindows()
