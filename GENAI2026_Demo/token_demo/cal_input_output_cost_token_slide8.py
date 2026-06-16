import tiktoken

COST_PER_TOKEN = 1

encoding = tiktoken.encoding_for_model("gpt-4o")

prompt = input("Enter Prompt: ")

input_tokens = len(encoding.encode(prompt))

# Assume AI generated 50 tokens
output_tokens = 50

total_tokens = input_tokens + output_tokens

total_cost = total_tokens * COST_PER_TOKEN

print("\n====== TOKEN REPORT ======")
print(f"Input Tokens : {input_tokens}")
print(f"Output Tokens: {output_tokens}")
print(f"Total Tokens : {total_tokens}")
print(f"Total Cost   : ${total_cost}")
