with open("app.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("DeepVoice Shield Pro", "DeepShield")
text = text.replace("DEEPVOICE SHIELD PRO", "DEEPSHIELD")
text = text.replace("DEEPVOICE SHIELD", "DEEPSHIELD")
text = text.replace("DeepVoice Shield", "DeepShield")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(text)
print("Renamed all visual titles to DeepShield!")
