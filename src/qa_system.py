import pyttsx3
import speech_recognition as sr
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import cv2
import threading
import random
from collections import Counter
from fer import FER
from g4f.client import Client


# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize message list with an introductory message
messages = [
    {"role": "system", "content": "Your name is IntelEd. You are designed to respond to users' queries and help them learn. You should adjust responses based on the user's mood."},
]

# Define fun responses based on mood
fun_responses = {
    "happy": ["That's great to hear! Why don't you tell me a joke?", "I'm glad you're happy! Keep smiling! 😊"],
    "sad": ["I'm here for you! Want to talk about it?", "It's okay to feel sad sometimes. How can I cheer you up?"],
    "neutral": ["That's interesting! How about we chat about something fun?", "What else is on your mind?"],
}

# Initialize emotion detector
detector = FER()

# Initialize GPT client
client = Client()

def GPT(message, mood):
    global messages
    combined_message = f"Question: {message} | Mood: {mood} (This is the user's emotional state)"
    
    # Append user message to messages list
    messages.append({'role': 'user', 'content': combined_message})  

    try:
        # Send the combined message to the AI model
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Change model if necessary
            messages=messages
        )

        if isinstance(response, dict) and 'choices' in response:
            ms = response['choices'][0]['message']['content']
        else:
            ms = response or "   "

        # Append AI response to the message history
        messages.append({'role': 'assistant', 'content': ms})
        return ms
    except Exception as e:
        print(f"Error with the AI model request: {e}")
        return "Sorry, something went wrong with the AI provider."

def speak(text):
    """Text-to-speech output."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to the user's speech and convert it to text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
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
    """Detect the user's mood based on their facial expression."""
    cap = cv2.VideoCapture(0)
    emotions_detected = []

    for _ in range(10):  # Capture 10 frames for mood detection
        ret, frame = cap.read()
        if ret:
            # Detect emotion using FER (Facial Expression Recognition)
            emotions = detector.detect_emotions(frame)
            if emotions:
                dominant_emotion = max(emotions[0]['emotions'], key=emotions[0]['emotions'].get)
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
    """Process the user's query and return the AI's response."""
    mood = detect_mood()
    response = GPT(query, mood)

    fun_response = random.choice(fun_responses.get(mood, ["I'm here for you!"]))
    
    # Output the responses via speech
    speak(response)
    speak(fun_response)

    return response, fun_response

def send_query(query):
    """Display the user's query and AI's responses on the UI."""
    if query.strip():
        response, fun_response = handle_query(query)
        
        response_box.configure(state=tk.NORMAL)
        response_box.insert(tk.END, f"You: {query}\n", 'user')
        response_box.insert(tk.END, f"IntelEd: {response}\n", 'bot')
        response_box.insert(tk.END, f"IntelEd (fun): {fun_response}\n\n", 'fun')
        response_box.configure(state=tk.DISABLED)
        response_box.see(tk.END)

def listen_thread():
    """Continuously listen for user input."""
    while True:
        user_query = listen()
        if user_query:
            send_query(user_query)

# Tkinter UI setup
window = tk.Tk()
window.title("IntelEd: AI Learning Companion")
window.geometry("450x700")
window.configure(bg="#2E3440")

# Tkinter style
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 10), foreground="#D8DEE9", background="#5E81AC")
style.configure("TLabel", font=("Helvetica", 12), foreground="#ECEFF4", background="#2E3440")
style.configure("TEntry", font=("Helvetica", 12), foreground="#3B4252", padding=5)

# Title label
title_label = ttk.Label(window, text="IntelEd", font=("Helvetica", 20, "bold"), background="#5E81AC", foreground="#ECEFF4")
title_label.pack(pady=10)

# Response display box
response_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, state=tk.DISABLED, bg="#3B4252", fg="#D8DEE9", font=("Helvetica", 12))
response_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
response_box.tag_config('user', foreground="#A3BE8C", font=("Helvetica", 12, "bold"))
response_box.tag_config('bot', foreground="#BF616A", font=("Helvetica", 12, "italic"))
response_box.tag_config('fun', foreground="#EBCB8B", font=("Helvetica", 12))

# Input frame and button
input_frame = ttk.Frame(window)
input_frame.pack(pady=5, fill=tk.X)
input_box = ttk.Entry(input_frame, width=50)
input_box.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

send_button = ttk.Button(input_frame, text="Send", command=lambda: send_query(input_box.get()))
send_button.pack(side=tk.RIGHT, padx=5)

def quit_application():
    """Close application."""
    cv2.destroyAllWindows()  
    window.quit()

def stop_all():
    """Stop all ongoing processes."""
    cv2.destroyAllWindows()
    window.quit() 

stop_button = ttk.Button(window, text="Stop All", command=stop_all)
stop_button.pack(pady=10)

window.bind('<q>', lambda event: quit_application())

def on_enter(event):
    """Handle Enter key press."""
    send_query(input_box.get())
    input_box.delete(0, tk.END)  

input_box.bind('<Return>', on_enter)

# Start the listening thread for continuous listening
threading.Thread(target=listen_thread, daemon=True).start()

window.mainloop()
