import cv2
from emotion_detector import EmotionDetector

# Initialize the emotion detector
detector = EmotionDetector("models/emotion-model.xml", "models/emotion-model.bin")

# Use the correct path for your test image
image_path = r"C:\Users\Ziyad\Pictures\Camera Roll\WIN_20241130_19_31_34_Pro.jpg"  # Update this path

# Load the image
image = cv2.imread(image_path)

if image is None:
    print("Error: Image could not be loaded. Please check the file path.")
else:
    # Detect emotion
    emotion = detector.detect_emotion(image)
    print(f"Detected Emotion: {emotion}")
