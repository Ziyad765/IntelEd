# emotion_detector.py
import cv2
from openvino.runtime import Core

class EmotionDetector:
    def __init__(self, model_xml, model_bin):
        core = Core()
        self.model = core.read_model(model=model_xml, weights=model_bin)
        self.compiled_model = core.compile_model(self.model, "CPU")
        self.input_layer = self.compiled_model.input(0)
        self.output_layer = self.compiled_model.output(0)

    def detect_emotion(self, frame):
        """Detect the emotion from a single frame."""
        resized_image = cv2.resize(frame, (64, 64))  # Adjust size based on your model
        input_data = resized_image.transpose(2, 0, 1)[None]  # Adjust channels if needed

        # Perform inference on the frame
        result = self.compiled_model([input_data])[self.output_layer]

        # Define emotions (based on your model output format)
        emotions = ["neutral", "happy", "sad", "angry", "surprised"]

        # Return the emotion with the highest probability
        return emotions[result.argmax()]

    def start_detection(self):
        """Continuously capture frames from webcam and detect emotions."""
        cap = cv2.VideoCapture(0)  # Start webcam
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Detect emotion in the frame
            emotion = self.detect_emotion(frame)
            
            # Display emotion on webcam feed
            cv2.putText(frame, f"Emotion: {emotion}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow("Emotion Detection", frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
