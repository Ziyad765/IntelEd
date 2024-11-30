from content_adapter import ContentAdapter

# Initialize the content adapter
adapter = ContentAdapter("lessons/")

# Test lessons for different emotions
for emotion in ["happy", "sad", "neutral"]:
    lesson = adapter.get_lesson(emotion)
    print(f"Emotion: {emotion}")
    print(f"Lesson: {lesson}")
    print("-" * 50)
