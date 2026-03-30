import re

with open("app.py", "r", encoding="utf-8") as f:
    text = f.read()

new_css = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono&display=swap');
:root{--primary:#00f2fe;--secondary:#4facfe;--accent:#38bdf8;--bg:#0b0f19;--card:rgba(30,41,59,0.5);--glow:rgba(0,242,254,0.4);}
*{box-sizing:border-box;transition:all 0.3s cubic-bezier(0.4,0,0.2,1);}
body,.gradio-container{background:radial-gradient(circle at top center,#0f172a,#0b0f19)!important;font-family:'Outfit',sans-serif!important;color:#e2e8f0!important;}
.main-header{text-align:center;padding:3rem 0;position:relative;}
.main-header::after{content:'';position:absolute;top:0;left:50%;transform:translateX(-50%);width:250px;height:250px;background:var(--glow);filter:blur(120px);z-index:-1;}
.main-header h1{font-size:3.5rem;font-weight:800;margin:0;background:linear-gradient(to right,#4facfe,#00f2fe);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:-1px;text-shadow:0 0 30px rgba(0,242,254,0.3);}
.glass-card{background:var(--card)!important;backdrop-filter:blur(32px) saturate(200%);border:1px solid rgba(255,255,255,0.08)!important;border-radius:24px!important;box-shadow:0 10px 40px -10px rgba(0,0,0,0.8),inset 0 1px 0 rgba(255,255,255,0.1)!important;padding:2.5rem!important;}
.result-display{border-radius:24px;padding:2.5rem;margin-bottom:20px;border:1px solid rgba(255,255,255,0.1);text-align:center;backdrop-filter:blur(24px);position:relative;overflow:hidden;}
.result-genuine{background:linear-gradient(145deg,rgba(16,185,129,0.1),rgba(5,150,105,0.2))!important;border-color:rgba(16,185,129,0.3)!important;color:#10b981!important;box-shadow:0 0 30px rgba(16,185,129,0.15)!important;animation:pulse-glow-green 3s infinite ease-in-out!important;}
@keyframes pulse-glow-green{50%{box-shadow:0 0 50px rgba(16,185,129,0.3)!important;border-color:rgba(16,185,129,0.6)!important;}}
.result-fake{background:linear-gradient(145deg,rgba(244,63,94,0.1),rgba(225,29,72,0.2))!important;border-color:rgba(244,63,94,0.3)!important;color:#f43f5e!important;box-shadow:0 0 40px rgba(244,63,94,0.15)!important;animation:pulse-glow-red 2s infinite ease-in-out!important;}
@keyframes pulse-glow-red{50%{box-shadow:0 0 60px rgba(244,63,94,0.4)!important;border-color:rgba(244,63,94,0.6)!important;}}
.result-uncertain{background:linear-gradient(145deg,rgba(245,158,11,0.1),rgba(217,119,6,0.2))!important;border-color:rgba(245,158,11,0.3)!important;color:#f59e0b!important;box-shadow:0 0 40px rgba(245,158,11,0.15)!important;animation:pulse-glow-yellow 2s infinite ease-in-out!important;}
@keyframes pulse-glow-yellow{50%{box-shadow:0 0 60px rgba(245,158,11,0.4)!important;border-color:rgba(245,158,11,0.6)!important;}}
.verdict-text{font-size:2.5rem;font-weight:800;margin-bottom:8px;letter-spacing:-1px;}
.confidence-bar{font-family:'JetBrains Mono',monospace;font-size:1.1rem;opacity:0.9;font-weight:600;}
.status-badge{display:inline-block;padding:6px 16px;border-radius:100px;font-size:0.75rem;font-weight:800;text-transform:uppercase;margin-bottom:12px;border:1px solid currentColor;letter-spacing:2px;}
.primary-btn{background:linear-gradient(135deg,#4facfe,#00f2fe)!important;border:1px solid rgba(0,242,254,0.4)!important;border-radius:16px!important;font-weight:800!important;color:#0b0f19!important;box-shadow:0 4px 20px rgba(0,242,254,0.3)!important;padding:12px 24px!important;text-transform:uppercase;letter-spacing:1px;}
.primary-btn:hover{transform:translateY(-2px);box-shadow:0 8px 30px rgba(0,242,254,0.5)!important;}
.info-card{background:rgba(255,255,255,0.02)!important;border:1px solid rgba(255,255,255,0.05)!important;border-radius:16px!important;padding:16px!important;backdrop-filter:blur(10px);}
.info-card label{color:#64748b!important;font-weight:600!important;text-transform:uppercase!important;font-size:0.75rem!important;letter-spacing:1px!important;}
.info-card input{background:transparent!important;border:none!important;color:#f8fafc!important;font-family:'JetBrains Mono',monospace!important;font-size:1.2rem!important;font-weight:600!important;}
.obs-box{background:rgba(0,242,254,0.03)!important;padding:24px;border-radius:20px;margin-top:24px;border:1px solid rgba(0,242,254,0.1)!important;color:#cbd5e1!important;line-height:1.7;}
.obs-box b{color:#38bdf8;font-size:1.1rem;text-transform:uppercase;letter-spacing:1px;}
.viz-container{border-radius:24px;overflow:hidden;margin-top:16px;border:1px solid rgba(255,255,255,0.05);background:rgba(0,0,0,0.3);box-shadow:inset 0 0 30px rgba(0,0,0,0.6);}
.tabs > div > button{font-size:1.1rem!important;font-weight:600!important;border-radius:12px!important;color:#94a3b8!important;border:1px solid transparent!important;background:transparent!important;}
.tabs > div > button.selected{background:rgba(0,242,254,0.1)!important;color:#00f2fe!important;border:1px solid rgba(0,242,254,0.3)!important;box-shadow:0 0 20px rgba(0,242,254,0.1)!important;}
div[data-testid="audio"] { border: 2px dashed rgba(0,242,254,0.3) !important; background: rgba(0,242,254,0.02) !important; border-radius: 24px !important; transition: all 0.3s ease; animation: upload-pulse 3s infinite ease-in-out; }
div[data-testid="audio"]:hover { border-color: rgba(0,242,254,0.8) !important; background: rgba(0,242,254,0.05) !important; }
@keyframes upload-pulse { 50% { box-shadow: 0 0 40px rgba(0,242,254,0.15) inset; } }
"""

# Replace the css block
text = re.sub(r'css = """[\s\S]*?"""', f'css = """\n{new_css}\n"""', text)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated clinical tech theme.")
