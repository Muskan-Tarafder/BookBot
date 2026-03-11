import requests as http_requests
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API')
HF_API_URL = "https://juliane-hyperactive-exaltedly.ngrok-free.dev/predict"

groq_client = Groq(api_key=GROQ_API_KEY)

def query_hf_model(user_message, history):
    response = http_requests.post(HF_API_URL, json={
        'message': user_message,
        'history': history
    }, timeout=60)
    return response.json()

def query_groq(user_message, history):
    converted_history = [
        {'role':'assistant' if m['role']=='bot' else m['role'], 'content':m['content']} for m in history[-6:]
    ]
    messages = [
        {"role": "system", "content": (
            "You are a friendly book recommendation chatbot. "
            "Recommend only real books with title, author, and short description of 20 words."
            "Nudge the user to ask for book recommendations when relevant."
        )}
    ] + converted_history + [{"role": "user", "content": user_message}]

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        max_tokens=1000
    )
    return response.choices[0].message.content

def Convo(user_message, history):
    # Try HuggingFace model on Colab first
    try:
        data = query_hf_model(user_message, history)
        if not data.get('use_groq'):
            return data['reply'], 'Fine-tuned Model'
    except Exception as e:
        print(f"Colab API unavailable: {e} — falling back to Groq")
    
    # Fall back to Groq
    reply = query_groq(user_message, history)
    return reply, 'Groq'
