from openai import OpenAI
import os

client = OpenAI(api_key="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")

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
