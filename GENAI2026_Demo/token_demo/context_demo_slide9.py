from openai import OpenAI
import os

client = OpenAI(api_key="")

messages = []

messages.append({
    "role": "user",
    "content": "Remember this: My favorite color is Blue."
})

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)

print("Stored in context.")

messages.append({
    "role": "user",
    "content": "What is my favorite color?"
})

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)

print(response.choices[0].message.content)
