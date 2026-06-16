complaint = "I ordered shoes online but received the wrong size."

print("\n========= BEFORE AI / HARD CODED LOGIC =========\n")

# HARD-CODED RULES
if "wrong size" in complaint.lower():
    category = "Delivery Issue"
elif "refund" in complaint.lower():
    category = "Refund Issue"
else:
    category = "Unknown"

print(f"Complaint: {complaint}")
print(f"Detected Category: {category}")

print("\nProblem with Traditional Logic:")
print("- Needs manual rules")
print("- Cannot understand meaning")
print("- Fails for different sentence styles")
print("- Not scalable")
