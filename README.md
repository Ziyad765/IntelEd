```markdown
# IntelEd: Personalized AI Learning Companion

## Overview

**IntelEd** is an AI-powered adaptive learning system designed to enhance education through real-time emotional analysis and personalized teaching methods. It uses **Intel OpenVINO** for emotion detection and **GPT-4o-mini** for interactive Q&A. The system dynamically adjusts the lesson content based on the user's emotional state, providing personalized learning experiences and improving student engagement.

## Features
- **Real-time Emotion Detection**: Uses Intel's **OpenVINO toolkit** to detect facial expressions through the webcam and analyze emotional states such as happy, sad, or neutral.
- **Adaptive Learning**: Based on the detected mood, the system adapts the lesson content and delivery style to improve student engagement.
- **Interactive Q&A**: Students can ask questions, and the AI provides context-aware responses, considering the user’s mood.
- **Speech Interaction**: Supports voice input through **Speech Recognition** and replies using **Text-to-Speech (TTS)**.

## Technologies Used
- **Intel OpenVINO**: For optimized inference and emotion detection.
- **GPT-4o-mini**: For AI-driven question answering.
- **Python**: Programming language used for development.
- **OpenCV**: For capturing and processing webcam video feeds.
- **Pyttsx3**: For text-to-speech functionality.
- **SpeechRecognition**: For converting speech to text.
- **Tkinter**: For the graphical user interface (GUI).

## Installation

### Prerequisites
- Python 3.6+ (recommended to use a virtual environment)
- Install **Intel OpenVINO**:
  ```bash
  pip install openvino-dev
  ```
- Install **required libraries**:
  ```bash
  pip install opencv-python pyttsx3 g4f SpeechRecognition fer
  ```

### Setting Up OpenVINO
1. Download the **emotion-recognition-retail-0003** model from Intel’s Open Model Zoo.
2. Compile and use the model with OpenVINO for emotion detection in real-time.

### Running the Project

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/your-username/IntelEd.git
   ```

2. Navigate to the project directory:
   ```bash
   cd IntelEd
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the main Python script to start the application:
   ```bash
   python src/main.py
   ```

5. The application will start, and a window with the **IntelEd** interface will open.

6. **Speak** your query after the system says "Listening..." or type your question in the input box.

## How It Works

### Emotion Detection:
- The webcam captures real-time facial expressions.
- Using **Intel OpenVINO**, the system analyzes the expressions and detects the user's emotional state (e.g., happy, sad, or neutral).
- Based on the detected emotion, the system adjusts the content delivery (lesson style) and replies accordingly.

### Interactive Learning:
- Users can ask questions related to the topic they are learning.
- The **GPT-4o-mini** model processes the question and generates context-aware responses.
- The response is then spoken aloud using **Text-to-Speech**.

### Speech and Text Interaction:
- The system can both **listen** to voice queries and **speak** back answers, making the learning process more interactive.
  

1. Fork this repository.
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/IntelEd.git
   ```
3. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
4. Make changes and commit them:
   ```bash
   git commit -am "Add feature"
   ```
5. Push to your branch:
   ```bash
   git push origin feature-name
   ```
6. Create a pull request.

## License
This project is licensed under the MIT License.

## Acknowledgments
- **Intel** for providing the **OpenVINO toolkit**.
- **OpenAI** for their **GPT-4o-mini** model.
- **Python** and **Tkinter** for making cross-platform GUI development easier.

---

## Demo Video
Here’s a walkthrough of the **IntelEd** system in action:  
[https://youtu.be/Xu4JuSgXswc]

---

### Notes:
- Ensure your **webcam** is functioning correctly, as the emotion detection is based on webcam input.
- **Microphone** access is required for voice input.
- The **IntelEd** system works best in environments with **adequate lighting** for emotion detection.
