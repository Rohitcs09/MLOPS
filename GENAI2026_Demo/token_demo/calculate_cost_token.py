import tiktoken

# Demo Pricing
COST_PER_TOKEN = 1  # $1 per token (Demo Only)

encoding = tiktoken.encoding_for_model("gpt-4o")

text = input("Enter Prompt: ")

tokens = encoding.encode(text)

token_count = len(tokens)
total_cost = token_count * COST_PER_TOKEN

print("\n========== RESULT ==========")
print(f"Prompt: {text}")
print(f"Total Tokens: {token_count}")
print(f"Cost Per Token: ${COST_PER_TOKEN}")
print(f"Total Cost: ${total_cost}")
