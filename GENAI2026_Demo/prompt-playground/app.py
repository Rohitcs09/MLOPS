from openai import OpenAI
from prompt_templates import PROMPTS

# Put your API Key here
client = OpenAI(
    api_key=""
)

print("\n====== AI Prompt Playground ======\n")

role = input("Enter Role: ").lower()
task = input("Enter Task: ")
output_format = input("Output Format (table/json/bullets): ")
constraints = input("Constraints: ")

template = PROMPTS.get(
    role,
    """
You are an AI assistant.

Task:
{task}

Output Format:
{output_format}

Constraints:
{constraints}
"""
)

prompt = template.format(
    task=task,
    output_format=output_format,
    constraints=constraints
)

print("\nGenerated Prompt:\n")
print(prompt)

print("\nCalling OpenAI...\n")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.7
)

print("\n========== AI RESPONSE ==========\n")
print(response.choices[0].message.content)
