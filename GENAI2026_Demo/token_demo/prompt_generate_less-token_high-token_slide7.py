import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4o")

text = input("Enter Prompt: ")

tokens = encoding.encode(text)

print("\nTokens Used:", len(tokens))
