import re

with open("app.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Add CSS class for bubble effect
bubble_css = """
.status-pill {
    display: inline-block;
    padding: 10px 20px;
    font-size: 0.85rem;
    font-weight: 600;
    border-radius: 12px;
    transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)!important;
    cursor: default;
    position: relative;
    overflow: hidden;
    z-index: 1;
}
.status-pill::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    transition: width 0.6s ease, height 0.6s ease;
    z-index: -1;
}
.status-pill:hover::before {
    width: 300px;
    height: 300px;
}
.status-pill:hover {
    transform: translateY(-5px) scale(1.05)!important;
    border-radius: 18px!important;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5)!important;
}
"""

# Insert CSS before the ending """
text = text.replace('div[data-testid="audio"] {', bubble_css + '\ndiv[data-testid="audio"] {')

# 2. Modify the spans to use the class
o1 = '<span style="background:rgba(139,92,246,0.15);border:1px solid rgba(139,92,246,0.4);border-radius:12px;padding:10px 20px;font-size:0.85rem;font-weight:600;color:#e9d5ff;box-shadow:0 4px 15px rgba(139,92,246,0.2);">'
o2 = '<span style="background:rgba(236,72,153,0.15);border:1px solid rgba(6,182,212,0.4);border-radius:12px;padding:10px 20px;font-size:0.85rem;font-weight:600;color:#cffafe;box-shadow:0 4px 15px rgba(6,182,212,0.2);">'
o3 = '<span style="background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.4);border-radius:12px;padding:10px 20px;font-size:0.85rem;font-weight:600;color:#d1fae5;box-shadow:0 4px 15px rgba(16,185,129,0.2);">'

n1 = '<span class="status-pill" style="background:rgba(139,92,246,0.15);border:1px solid rgba(139,92,246,0.4);color:#e9d5ff;box-shadow:0 4px 15px rgba(139,92,246,0.2);">'
n2 = '<span class="status-pill" style="background:rgba(236,72,153,0.15);border:1px solid rgba(6,182,212,0.4);color:#cffafe;box-shadow:0 4px 15px rgba(6,182,212,0.2);">'
n3 = '<span class="status-pill" style="background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.4);color:#d1fae5;box-shadow:0 4px 15px rgba(16,185,129,0.2);">'

text = text.replace(o1, n1)
text = text.replace(o2, n2)
text = text.replace(o3, n3)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(text)
print("Bubble effect injected.")
