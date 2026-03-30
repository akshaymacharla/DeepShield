import re

with open("app.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace main-header styles
new_header_css = """
.main-header{text-align:center;padding:4rem 0 3rem;position:relative;margin-bottom:2rem;border-bottom:1px solid rgba(255,255,255,0.05);}
.main-header::after{content:'';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:400px;height:200px;background:var(--glow);filter:blur(150px);z-index:-1;}
.main-header::before{content:'[ DEFENSE GRID ACTIVE ]';display:inline-block;padding:6px 16px;background:rgba(0,242,254,0.05);border:1px solid rgba(0,242,254,0.3);border-radius:100px;color:#00f2fe;font-family:'JetBrains Mono',monospace;font-size:0.75rem;letter-spacing:3px;margin-bottom:20px;box-shadow:0 0 20px rgba(0,242,254,0.15);}
.main-header h1{font-size:4.5rem;font-weight:900;margin:0;background:linear-gradient(180deg,#ffffff 0%,#00f2fe 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:-2px;text-shadow:0 15px 50px rgba(0,242,254,0.4);line-height:1.1;text-transform:uppercase;}
.main-header p{font-family:'JetBrains Mono',monospace;font-size:1rem;color:#4facfe;letter-spacing:5px;text-transform:uppercase;margin-top:1rem;font-weight:600;}
"""

text = re.sub(r'\.main-header\{.*?\}', '', text)
text = re.sub(r'\.main-header::after\{.*?\}', '', text)
text = re.sub(r'\.main-header h1\{.*?\}', new_header_css.strip(), text)

# Replace tabs styles
new_tabs_css = """
.tab-nav{border-bottom:1px solid rgba(255,255,255,0.05)!important;gap:15px!important;justify-content:center!important;padding-bottom:15px!important;margin-bottom:2rem!important;}
.tabs > div > button{font-size:1.1rem!important;font-weight:600!important;border-radius:12px!important;color:#64748b!important;border:1px solid rgba(255,255,255,0.05)!important;background:rgba(255,255,255,0.02)!important;border-bottom:none!important;padding:12px 24px!important;}
.tabs > div > button:hover{color:#e2e8f0!important;border-color:rgba(0,242,254,0.3)!important;}
.tabs > div > button.selected{background:rgba(0,242,254,0.1)!important;color:#00f2fe!important;border:1px solid rgba(0,242,254,0.4)!important;box-shadow:0 0 25px rgba(0,242,254,0.2)!important;}
"""

text = re.sub(r'\.tabs > div > button\{.*?\}', '', text)
text = re.sub(r'\.tabs > div > button\.selected\{.*?\}', new_tabs_css.strip(), text)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(text)
print("Header upgrade completely injected.")
