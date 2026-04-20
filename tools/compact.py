from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()


def compact(messages, summary_instructions=None):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    summary_messages = [
        {
            "role": "system",
            "content": (
                "You are a chat summarizer. "
                "Summarize the conversation into 1–5 concise lines. "
                "Keep key facts, tool outputs, and user intent. "
                "Remove unnecessary detail."
            ),
        },
        {
            "role": "user",
            "content": str(messages),
        },
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=summary_messages,
    )

    return response.choices[0].message.content
