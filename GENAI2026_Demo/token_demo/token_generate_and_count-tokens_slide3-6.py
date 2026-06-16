import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4o")

text = "My name is Rohit Kumar and I live in Delhi and Delhi-NCR **."

tokens = encoding.encode(text)

print(f"Text: {text}")
print(f"\nNumber of Tokens: {len(tokens)}")
print(f"\nTokens:")
print(tokens)
