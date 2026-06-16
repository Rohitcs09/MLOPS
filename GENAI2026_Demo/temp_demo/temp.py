from openai import OpenAI

# Replace with your OpenAI API Key
API_KEY = "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"

client = OpenAI(api_key=API_KEY)

PROMPT = """
Write a short story about a Robot.
keep it under 100 words.
"""

temperatures = [0, 0.7, 1.5]

print("\n==============================")
print(" GPT TEMPERATURE DEMO")
print("==============================")

for temp in temperatures:

    print("\n")
    print("=" * 60)
    print(f"TEMPERATURE = {temp}")
    print("=" * 60)

    try:
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

    except Exception as e:
        print(f"ERROR: {e}")

print("\nDemo Completed Successfully!")
