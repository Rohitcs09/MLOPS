from openai import OpenAI

# -------------------------------
# 1️⃣ Python part (Setup)
# -------------------------------
#client = OpenAI(api_key="")

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

