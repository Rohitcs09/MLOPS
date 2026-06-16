from openai import OpenAI

# -------------------------------
# 1️⃣ Python part (Setup)
# -------------------------------
client = OpenAI(api_key="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")

# -------------------------------
# 2️⃣ DevOps data (Logs)
# -------------------------------
with open("jenkins.log") as f:
    logs = f.read()

# -------------------------------
# 3️⃣ Prompt (Instruction)
# -------------------------------
prompt = f"""
You are a DevOps SRE.

Analyze the Jenkins logs below.
1. Find root cause
2. Explain impact
3. Suggest fix

Logs:
{logs}
"""

# -------------------------------
# 4️⃣ LLM CALL (⭐ THIS IS LLM ⭐)
# -------------------------------
response = client.chat.completions.create(
    model="gpt-5.2",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.2
)

# -------------------------------
# 5️⃣ Output (Python)
# -------------------------------
print("=== LLM ANALYSIS ===")
print(response.choices[0].message.content)

