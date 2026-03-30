import re

with open("app.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace CSS Root Variables
text = re.sub(
    r":root\{--primary:#06b6d4;--secondary:#6366f1;--accent:#f43f5e;--bg:#09090b;--card:rgba\(9,9,11,0.65\);--glow:rgba\(99,102,241,0.5\);\}",
    ":root{--primary:#f97316;--secondary:#8b5cf6;--accent:#ec4899;--bg:#030712;--card:rgba(15,23,42,0.65);--glow:rgba(236,72,153,0.5);}",
    text
)

# Background gradient
text = re.sub(
    r"radial-gradient\(circle at top center,#1e1b4b,#09090b\)",
    "radial-gradient(circle at top center,#2e1065,#030712)",
    text
)

# Header Gradient
text = re.sub(
    r"linear-gradient\(to right,#818cf8,#22d3ee,#818cf8\)",
    "linear-gradient(to right,#f97316,#ec4899,#f97316)",
    text
)
text = re.sub(
    r"text-shadow:0 0 40px rgba\(34,211,238,0.3\)",
    "text-shadow:0 0 40px rgba(249,115,22,0.3)",
    text
)

# Button gradient
text = re.sub(
    r"linear-gradient\(135deg,#6366f1,#06b6d4\)",
    "linear-gradient(135deg,#8b5cf6,#f97316)",
    text
)
text = re.sub(
    r"box-shadow:0 4px 20px rgba\(99,102,241,0.4\)",
    "box-shadow:0 4px 20px rgba(249,115,22,0.4)",
    text
)
text = re.sub(
    r"box-shadow:0 10px 30px rgba\(99,102,241,0.6\)",
    "box-shadow:0 10px 30px rgba(249,115,22,0.6)",
    text
)

# Observation Box Customizations
text = re.sub(
    r"rgba\(99,102,241,0.05\)",
    "rgba(139,92,246,0.05)",
    text
)
text = re.sub(
    r"rgba\(99,102,241,0.2\)",
    "rgba(139,92,246,0.2)",
    text
)
text = re.sub(
    r"color:#818cf8",
    "color:#c4b5fd",
    text
)

# Hero Section inline colors
text = text.replace("rgba(6,182,212,0.15)", "rgba(236,72,153,0.15)")
text = text.replace("color:#22d3ee", "color:#f9a8d4")
text = text.replace("color:#67e8f9", "color:#f9a8d4")
text = text.replace("color:#a5b4fc", "color:#fbcfe8")
text = text.replace("color:#c4b5fd", "color:#d8b4fe")
text = text.replace("rgba(99,102,241,0.1)", "rgba(139,92,246,0.1)")
text = text.replace("rgba(99,102,241,0.3)", "rgba(139,92,246,0.3)")
text = text.replace("color:#818cf8", "color:#c4b5fd")
text = text.replace("rgba(99,102,241,0.15)", "rgba(139,92,246,0.15)")
text = text.replace("rgba(99,102,241,0.4)", "rgba(139,92,246,0.4)")
text = text.replace("color:#c7d2fe", "color:#e9d5ff")
text = text.replace("rgba(99,102,241,0.2)", "rgba(139,92,246,0.2)")

# Fake/Uncertain Badges (Change fake to hot pink, uncertain to neon orange)
# result-fake
text = re.sub(
    r"rgba\(244,63,94,0.15\).*?rgba\(225,29,72,0.25\)",
    "rgba(236,72,153,0.15),rgba(219,39,119,0.25)",
    text
)
text = re.sub(
    r"rgba\(244,63,94,0.4\)",
    "rgba(236,72,153,0.4)",
    text
)
text = re.sub(
    r"color:#f43f5e",
    "color:#ec4899",
    text
)
text = re.sub(
    r"rgba\(244,63,94,0.2\)",
    "rgba(236,72,153,0.2)",
    text
)
text = re.sub(
    r"rgba\(244,63,94,0.5\)",
    "rgba(236,72,153,0.5)",
    text
)
text = re.sub(
    r"rgba\(244,63,94,0.8\)",
    "rgba(236,72,153,0.8)",
    text
)

# result-uncertain
text = re.sub(
    r"rgba\(234,179,8,0.15\).*?rgba\(202,138,4,0.25\)",
    "rgba(249,115,22,0.15),rgba(234,88,12,0.25)",
    text
)
text = re.sub(
    r"rgba\(234,179,8,0.4\)",
    "rgba(249,115,22,0.4)",
    text
)
text = re.sub(
    r"color:#eab308",
    "color:#f97316",
    text
)
text = re.sub(
    r"rgba\(234,179,8,0.2\)",
    "rgba(249,115,22,0.2)",
    text
)
text = re.sub(
    r"rgba\(234,179,8,0.5\)",
    "rgba(249,115,22,0.5)",
    text
)
text = re.sub(
    r"rgba\(234,179,8,0.8\)",
    "rgba(249,115,22,0.8)",
    text
)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(text)
print("Theme successfully updated!")
