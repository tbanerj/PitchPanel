import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_advice(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a vocal coach helping singers improve."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=300,
    )
    return response["choices"][0]["message"]["content"]
