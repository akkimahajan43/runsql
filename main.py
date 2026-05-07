from groq import Groq
from dotenv import load_dotenv
import os
# -----------------------------
# GROQ API KEY
# -----------------------------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

print("🤖 Chatbot (Groq Streaming): Type 'quit', 'exit' or 'bye' to STOP\n")

while True:
    user_input = input("👤You: ")
    if user_input.lower() in["quit","exit","bye"]:
        print("\n 🤖 Chatbot: Goodbye!")
        break

    print("🤖 Chatbot: ", end="", flush=True)

    stream = client.chat.completions.create(
        model = "llama-3.3-70b-versatile", #or "llama3-8b-8192"
        messages=[
            {"role":"system", "content": "You are a helpful chatbot"},
            {"role":"user", "content": user_input}
        ],
        stream = True #Enable Streaming
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)

    print() #new line after response