from openai import OpenAI
from dotenv import load_dotenv
import os

# Load API Key
load_dotenv()

client = OpenAI(api_key="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")


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
