from openai import OpenAI
from dotenv import load_dotenv
import os

# Load API Key
load_dotenv()

client = OpenAI(api_key="")


PROMPT = """
Write a short story about a robot.
Keep it under 80 words.
"""

temperatures = [0, 0.7, 1.5]

print("\n==============================")
print(" GPT TEMPERATURE DEMO")
print("==============================\n")

for temp in temperatures:

    print(f"\n🔥 Temperature = {temp}")
    print("-" * 50)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=temp,
        messages=[
            {
                "role": "user",
                "content": PROMPT
            }
        ]
    )

    print(response.choices[0].message.content)
    print("\n")
