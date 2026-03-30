import re

with open("app.py", "r", encoding="utf-8") as f:
    text = f.read()

bubble_card_css = """
.bubble-card {
    position: relative;
    overflow: hidden;
    z-index: 1;
    transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)!important;
}
.bubble-card::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: rgba(0, 242, 254, 0.05);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    transition: width 0.6s ease, height 0.6s ease;
    z-index: -1;
}
.bubble-card:hover::before {
    width: 400px;
    height: 400px;
}
.bubble-card:hover {
    transform: translateY(-8px) scale(1.02)!important;
    border-color: rgba(0, 242, 254, 0.3)!important;
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4)!important;
}
"""

# Insert CSS into app.py
text = text.replace('div[data-testid="audio"] {', bubble_card_css + '\ndiv[data-testid="audio"] {')

# Find the 4 divs and inject the class
target_div = '<div style="padding:1.5rem;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);border-radius:16px;">'
new_div = '<div class="bubble-card" style="padding:1.5rem;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);border-radius:16px;cursor:pointer;">'

text = text.replace(target_div, new_div)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(text)
print("Added bubble effect to architecture cards.")
