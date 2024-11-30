from qa_system import QuestionAnsweringSystem

# Initialize the Q&A system
qa_system = QuestionAnsweringSystem()

# Ask a question
question = "What is machine learning?"
answer = qa_system.ask_question(question)
print(f"Question: {question}")
print(f"Answer: {answer}")
