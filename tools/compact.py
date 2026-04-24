from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()


def compact(messages, summary_instructions=None):
    """
    Returns a short blurb summary the chat history
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    summary_messages = [
        {
            "role": "system",
            "content": (
                "You are a chat summarizer. "
                "Summarize the conversation into 1–5 concise sentences. "
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


SCHEMA = {
    "type": "function",
    "function": {
        "name": "compact",
        "description": (
            "Summarize the current chat session to reduce context length."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "summary_instructions": {
                    "type": "string",
                    "description": (
                        "Preserve all decisions made and summarize "
                        "in 1-5 sentences"
                    )
                }
            },
            "required": [],
        },
    },
},
