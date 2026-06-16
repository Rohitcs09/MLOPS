from openai import OpenAI
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Initialize OpenAI client
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key="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")


# Sample complaint
complaint = """
I ordered a mobile phone online,
but received the wrong color.
Customer support is not responding,
and I need urgent replacement.
"""

print("\n========= WITH LLM / OPENAI =========\n")

prompt = f"""
Analyze the following customer complaint.

Complaint:
{complaint}

Provide:
1. Sentiment
2. Main Problem
3. Priority Level
4. Short Summary
5. Suggested Customer Support Reply
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are an intelligent AI complaint analyzer."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.5
)

result = response.choices[0].message.content

print(result)
