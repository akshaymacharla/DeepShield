with open("app.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("DEEPSHIELD", "DeepShield")
text = text.replace("Deepshield", "DeepShield")
text = text.replace("deepshield", "DeepShield")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated casing to DeepShield.")
