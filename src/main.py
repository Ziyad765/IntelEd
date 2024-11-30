import pyttsx3
import speech_recognition as sr
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import cv2
import threading
from collections import Counter
from openvino.runtime import Core  # OpenVINO integration
from g4f.client import Client  # Updated import for g4f.client

engine = pyttsx3.init()

messages = [
    {"role": "system", "content": "Your name is IntelEd. You are designed to respond to users' learning queries and detect their mood to help them learn better."},
    {"role": "system", "content": "You adapt your responses based on the user's mood."},
]

responses_by_mood = {
    "happy": ["That's great to hear! Let's dive into learning.", "Glad you're feeling positive! Let's start learning."],
    "sad": ["I'm here to help you. Let's make this learning journey a bit easier.", "It's okay to feel down. Let's focus on the topic at hand."],
    "neutral": ["Let's get started with today's lesson!", "What topic would you like to learn about today?"],
}

client = Client()  # Initialize the Client for new approach

# Initialize OpenVINO
core = Core()
emotion_model = core.read_model("path/to/emotion-recognition-retail-0003.xml")  # Replace with your model path
compiled_model = core.compile_model(emotion_model, "CPU")  # Use CPU for inference
output_layer = compiled_model.outputs[0]

def GPT(message, mood):
    global messages
    messages.append({'role': 'user', 'content': f"{message} (mood: {mood})"})  
    
    try:
        # Use the new Client method to get a response
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Or any model you want to use
            messages=messages
        )
        
        # Extracting the response from the API
        ms = response.choices[0].message.content if response.choices else "Sorry, I couldn't get a response."
        
        messages.append({'role': 'assistant', 'content': ms})
        return ms
    except Exception as e:
        print(f"Error with the API request: {e}")
        return "Sorry, something went wrong with the provider."

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source, timeout=10, phrase_time_limit=10)
    try:
        user_query = r.recognize_google(audio)
        print(f"User query: {user_query}")
        return user_query
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Error with the API request: {e}")
        return None

def detect_mood():
    cap = cv2.VideoCapture(0)
    emotions_detected = []
    emotion_labels = ["neutral", "happy", "sad", "surprise", "anger"]  # Update based on your model's output

    for _ in range(10):  # Capture 10 frames for mood detection
        ret, frame = cap.read()
        if ret:
            resized_frame = cv2.resize(frame, (64, 64))  # Resize frame to model's input size
            blob = cv2.dnn.blobFromImage(resized_frame, 1.0, (64, 64), (0, 0, 0), swapRB=True, crop=False)
            results = compiled_model([blob])[output_layer]
            dominant_emotion = emotion_labels[results.argmax()]  # Get the emotion with the highest probability
            emotions_detected.append(dominant_emotion)
            print(f"Detected emotion: {dominant_emotion}")

        cv2.imshow('Emotion Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if emotions_detected:
        most_common_emotion = Counter(emotions_detected).most_common(1)[0][0]
    else:
        most_common_emotion = "neutral"

    print(f"Most common detected emotion: {most_common_emotion}")
    return most_common_emotion

def handle_query(query):
    mood = detect_mood()
    response = GPT(query, mood)

    # Get a response based on the detected mood
    response_from_mood = responses_by_mood.get(mood, ["Let's proceed with the lesson."])[0]
    
    # First display the text in the response box, then speak
    response_box.configure(state=tk.NORMAL)
    response_box.insert(tk.END, f"You: {query}\n", 'user')
    response_box.insert(tk.END, f"IntelEd: {response}\n", 'bot')
    response_box.insert(tk.END, f"IntelEd (emotion-based): {response_from_mood}\n\n", 'fun')
    response_box.configure(state=tk.DISABLED)
    response_box.see(tk.END)

    # Then speak the response
    speak(response)
    speak(response_from_mood)
    
    return response, response_from_mood

def send_query(query):
    if query.strip():
        response, fun_response = handle_query(query)

def listen_thread():
    while True:
        user_query = listen()
        if user_query:
            send_query(user_query)

window = tk.Tk()
window.title("IntelEd")  # Change window title here
window.geometry("450x700")
window.configure(bg="#2E3440")

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 10), foreground="#D8DEE9", background="#5E81AC")
style.configure("TLabel", font=("Helvetica", 12), foreground="#ECEFF4", background="#2E3440")
style.configure("TEntry", font=("Helvetica", 12), foreground="#3B4252", padding=5)

title_label = ttk.Label(window, text="IntelEd", font=("Helvetica", 20, "bold"), background="#5E81AC", foreground="#ECEFF4")  # Change label here
title_label.pack(pady=10)

response_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, state=tk.DISABLED, bg="#3B4252", fg="#D8DEE9", font=("Helvetica", 12))
response_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
response_box.tag_config('user', foreground="#A3BE8C", font=("Helvetica", 12, "bold"))
response_box.tag_config('bot', foreground="#BF616A", font=("Helvetica", 12, "italic"))
response_box.tag_config('fun', foreground="#EBCB8B", font=("Helvetica", 12))

input_frame = ttk.Frame(window)
input_frame.pack(pady=5, fill=tk.X)
input_box = ttk.Entry(input_frame, width=50)
input_box.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

send_button = ttk.Button(input_frame, text="Send", command=lambda: send_query(input_box.get()))
send_button.pack(side=tk.RIGHT, padx=5)

def quit_application():
    cv2.destroyAllWindows()  
    window.quit()

def stop_all():
    cv2.destroyAllWindows()
    window.quit()

stop_button = ttk.Button(window, text="Stop All", command=stop_all)
stop_button.pack(pady=10)

window.bind('<q>', lambda event: quit_application())

def on_enter(event):
    send_query(input_box.get())
    input_box.delete(0, tk.END)  

input_box.bind('<Return>', on_enter)

threading.Thread(target=listen_thread, daemon=True).start()

window.mainloop()
