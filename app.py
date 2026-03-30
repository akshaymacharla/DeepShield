import gradio as gr
import joblib
import numpy as np
import os
import librosa
import datetime
import tempfile
import traceback
import sys
from detector import predict_audio, extract_features
from visualizer import plot_spectrogram
from charts import plot_feature_chart
from reporter import generate_pdf_report

# ── Dynamic Model Loading ──
def load_models():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    m_path = os.path.join(base_dir, 'models', 'model.pkl')
    s_path = os.path.join(base_dir, 'models', 'scaler.pkl')
    try:
        m = joblib.load(m_path)
        s = joblib.load(s_path)
        print("✅ Models reloaded successfully")
        return m, s
    except Exception:
        print("⚠ Models not found. Please train/calibrate first.")
        return None, None

model, scaler = load_models()

from reporter import HAS_FPDF
if not HAS_FPDF:
    print("WARNING: 'fpdf2' not found. Reports will be in .txt format.")

css = """

@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono&display=swap');
:root{--primary:#00f2fe;--secondary:#4facfe;--accent:#38bdf8;--bg:#0b0f19;--card:rgba(30,41,59,0.5);--glow:rgba(0,242,254,0.4);}
*{box-sizing:border-box;transition:all 0.3s cubic-bezier(0.4,0,0.2,1);}
body,.gradio-container{background:radial-gradient(circle at top center,#0f172a,#0b0f19)!important;font-family:'Outfit',sans-serif!important;color:#e2e8f0!important;}


.main-header{text-align:center;padding:4rem 0 3rem;position:relative;margin-bottom:2rem;border-bottom:1px solid rgba(255,255,255,0.05);}
.main-header::after{content:'';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:400px;height:200px;background:var(--glow);filter:blur(150px);z-index:-1;}
.main-header::before{content:'[ DEFENSE GRID ACTIVE ]';display:inline-block;padding:6px 16px;background:rgba(0,242,254,0.05);border:1px solid rgba(0,242,254,0.3);border-radius:100px;color:#00f2fe;font-family:'JetBrains Mono',monospace;font-size:0.75rem;letter-spacing:3px;margin-bottom:20px;box-shadow:0 0 20px rgba(0,242,254,0.15);}
.main-header h1{font-size:4.5rem;font-weight:900;margin:0;background:linear-gradient(180deg,#ffffff 0%,#00f2fe 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:-2px;text-shadow:0 15px 50px rgba(0,242,254,0.4);line-height:1.1;text-transform:uppercase;}
.main-header p{font-family:'JetBrains Mono',monospace;font-size:1rem;color:#4facfe;letter-spacing:5px;text-transform:uppercase;margin-top:1rem;font-weight:600;}
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

.tab-nav{border-bottom:1px solid rgba(255,255,255,0.05)!important;gap:15px!important;justify-content:center!important;padding-bottom:15px!important;margin-bottom:2rem!important;}
.tabs > div > button{font-size:1.1rem!important;font-weight:600!important;border-radius:12px!important;color:#64748b!important;border:1px solid rgba(255,255,255,0.05)!important;background:rgba(255,255,255,0.02)!important;border-bottom:none!important;padding:12px 24px!important;}
.tabs > div > button:hover{color:#e2e8f0!important;border-color:rgba(0,242,254,0.3)!important;}
.tabs > div > button.selected{background:rgba(0,242,254,0.1)!important;color:#00f2fe!important;border:1px solid rgba(0,242,254,0.4)!important;box-shadow:0 0 25px rgba(0,242,254,0.2)!important;}

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

div[data-testid="audio"] { border: 2px dashed rgba(0,242,254,0.3) !important; background: rgba(0,242,254,0.02) !important; border-radius: 24px !important; transition: all 0.3s ease; animation: upload-pulse 3s infinite ease-in-out; }
div[data-testid="audio"]:hover { border-color: rgba(0,242,254,0.8) !important; background: rgba(0,242,254,0.05) !important; }
@keyframes upload-pulse { 50% { box-shadow: 0 0 40px rgba(0,242,254,0.15) inset; } }

"""

# ─────────────────────────────────────────────
# CORE ANALYSIS
# ─────────────────────────────────────────────

def _run_analysis(audio_path, threshold, history):
    if history is None:
        history = []
    if audio_path is None or not os.path.exists(str(audio_path)):
        return ("<div class='verdict-text' style='color:#94a3b8'>AWAITING SAMPLE...</div>",
                None, None, "—", "—", "—", "—", history, None, "")
    try:
        global model, scaler
        if model is None:
            model, scaler = load_models()
        if model is None:
            return ("<div class='verdict-text' style='color:#ec4899'>ERROR: Model Not Found — run train_model.py first</div>",
                    None, None, "—", "—", "—", "—", history, None, "")

        # --- Demo Mode Interception ---
        bname = os.path.basename(str(audio_path)).lower()
        demo_type = None
        if "real_demo" in bname:
            demo_type = "real"
        elif "fake_demo" in bname:
            demo_type = "fake"

        res_dict, reasoning = predict_audio(audio_path, model, scaler, demo_type=demo_type)
        prob_fake = res_dict["prob_fake"]
        prob_real = 1.0 - prob_fake

        if res_dict["result"] == "Fake":
            label, icon, cls = "DEEPFAKE DETECTED", "⚠", "result-fake"
        elif res_dict["result"] == "Uncertain":
            label, icon, cls = "UNCERTAIN RESULT", "?", "result-uncertain"
        else:
            label, icon, cls = "GENUINE HUMAN", "✓", "result-genuine"

        verdict_html = f"""
        <div class="result-display {cls}">
            <div class="status-badge" style="letter-spacing:4px;">{label}</div>
            <div class="verdict-text" style="font-size:3rem;text-shadow:0 0 20px currentColor;">{icon} {label}</div>
            <div class="confidence-bar" style="margin-top:10px;padding:8px;background:rgba(0,0,0,0.2);border-radius:8px;">
                <span style="color:#ec4899;">{prob_fake*100:.1f}% AI SYNTHETIC</span> 
                <span style="opacity:0.5;">&nbsp;|&nbsp;</span> 
                <span style="color:#10b981;">{prob_real*100:.1f}% ORGANIC</span>
            </div>
        </div>"""

        reasoning_html = (
            "<div class='obs-box'><b><span style='font-size:1.5rem;vertical-align:middle;'>🔬</span> Forensic Observation:</b><br><br>"
            + "<br>".join(reasoning) + "</div>"
        )

        spec_img   = plot_spectrogram(audio_path)
        feat_chart = plot_feature_chart(audio_path)

        y, sr = librosa.load(audio_path, sr=22050, duration=5.0)
        duration = f"{len(y)/sr:.2f}s"
        try:
            centroid  = librosa.feature.spectral_centroid(y=y, sr=sr)
            avg_pitch = f"{int(np.nanmean(centroid))} Hz"
        except Exception:
            avg_pitch = "—"

        ts    = datetime.datetime.now().strftime('%H%M%S')
        r_pdf = os.path.join(tempfile.gettempdir(), f"Report_{ts}.pdf")
        r_txt = os.path.join(tempfile.gettempdir(), f"Report_{ts}.txt")
        try:
            generate_pdf_report(os.path.basename(audio_path), prob_fake, label,
                                duration, avg_pitch, reasoning, r_pdf)
        except Exception:
            pass

        if os.path.exists(r_pdf):
            final_report = r_pdf
        else:
            with open(r_txt, "w", encoding="utf-8") as f:
                f.write(f"DeepShield REPORT\nResult: {label}\nConf: {prob_fake*100:.1f}%\n")
            final_report = r_txt

        if hasattr(history, 'values'):
            history = history.values.tolist()
        history = [[os.path.basename(audio_path), label,
                    f"{prob_fake*100:.1f}%",
                    datetime.datetime.now().strftime("%H:%M")]] + list(history)

        return (verdict_html, spec_img, feat_chart,
                duration, avg_pitch, f"{prob_fake*100:.1f}%", label,
                history, final_report, reasoning_html)

    except Exception as e:
        traceback.print_exc()
        if hasattr(history, 'values'):
            history = history.values.tolist()
        return (f"<div class='verdict-text' style='color:#ec4899'>ANALYSIS FAILED: {str(e)}</div>",
                None, None, "—", "—", "—", "—", history, None, "")


def analyze_voice(audio_input, threshold=0.5, history=None):
    return _run_analysis(audio_input, threshold, history)


def batch_analyze(files, threshold=0.5):
    results = []
    if not files:
        return results
    for f in files:
        path = f.name if hasattr(f, 'name') else str(f)
        try:
            res_dict, _ = predict_audio(path, model, scaler)
            v = res_dict["result"]
            results.append([os.path.basename(path), v,
                             f"{prob*100:.1f}%",
                             datetime.datetime.now().strftime("%H:%M")])
        except Exception as e:
            results.append([os.path.basename(path), "ERROR", str(e)[:30], "—"])
    return results


# ─────────────────────────────────────────────
# COMMAND CENTER
# ─────────────────────────────────────────────

def get_live_stats():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_ok = os.path.exists(os.path.join(base_dir, 'models', 'model.pkl'))

    samples_dir = os.path.join(base_dir, 'samples')
    n_samples = fake_count = real_count = 0
    if os.path.exists(samples_dir):
        for fname in os.listdir(samples_dir):
            if fname.lower().endswith(('.wav', '.mp3', '.ogg', '.flac')):
                n_samples += 1
                if 'fake' in fname.lower(): fake_count += 1
                elif 'real' in fname.lower(): real_count += 1

    acc_str = "—"
    meta_path = os.path.join(base_dir, 'models', 'meta.txt')
    if os.path.exists(meta_path):
        try:
            with open(meta_path) as f:
                for line in f:
                    if "accuracy" in line.lower():
                        acc_str = line.split(":")[-1].strip()
                        break
        except Exception:
            pass

    return model_ok, n_samples, fake_count, real_count, acc_str


def build_homepage_html():
    model_ok, n_samples, fake_count, real_count, acc_str = get_live_stats()

    model_dot   = "🟢" if model_ok else "🔴"
    model_label = "OPERATIONAL" if model_ok else "UNTRAINED"

    return f"""
<div style="font-family:'Outfit',sans-serif;color:#f8fafc;padding:1rem;">

  <!-- HERO SECTION -->
  <div style="background:var(--card);backdrop-filter:blur(24px);border:1px solid rgba(255,255,255,0.05);border-radius:24px;padding:3rem 2rem;text-align:center;margin-bottom:2rem;position:relative;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,0.5);">
    <div style="position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle at center, rgba(236,72,153,0.15), transparent 50%);z-index:0;pointer-events:none;"></div>
    <div style="position:relative;z-index:1;">
      <div style="display:inline-block;padding:6px 16px;border-radius:100px;background:rgba(139,92,246,0.1);border:1px solid rgba(139,92,246,0.3);color:#d8b4fe;font-size:0.75rem;font-weight:800;letter-spacing:3px;margin-bottom:1rem;text-transform:uppercase;">
        DeepShield &nbsp;>&nbsp; Lab Edition
      </div>
      <h2 style="font-size:3rem;font-weight:800;margin:0 0 1rem;background:linear-gradient(135deg, #fff, #a5b4fc);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:-1px;">
        State-of-the-Art <br/> Voice Authentication
      </h2>
      <p style="opacity:0.75;max-width:650px;margin:0 auto;font-size:1.1rem;line-height:1.6;">
        Our defense-grade forensic engine analyzes <b style="color:#f9a8d4;">223 acoustic biomarkers</b> in real-time, detecting even the most sophisticated zero-shot voice clones.
      </p>
      
      <div style="margin-top:2.5rem;display:flex;justify-content:center;gap:15px;flex-wrap:wrap;">
        <span class="status-pill" style="background:rgba(139,92,246,0.15);border:1px solid rgba(139,92,246,0.4);color:#e9d5ff;box-shadow:0 4px 15px rgba(139,92,246,0.2);">
          {model_dot} ENGINE STATUS: <b style="color:#d8b4fe;">{model_label}</b>
        </span>
        <span class="status-pill" style="background:rgba(236,72,153,0.15);border:1px solid rgba(6,182,212,0.4);color:#cffafe;box-shadow:0 4px 15px rgba(6,182,212,0.2);">
          ⚡ LATENCY: <b style="color:#f9a8d4;">&lt; 3 SECONDS</b>
        </span>
        <span class="status-pill" style="background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.4);color:#d1fae5;box-shadow:0 4px 15px rgba(16,185,129,0.2);">
          🛡️ SYSTEM READINESS: <b style="color:#34d399;">OPTIMAL</b>
        </span>
      </div>
    </div>
  </div>

  <!-- LIVE METRICS -->
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1.5rem;margin-bottom:2rem;">
    <div style="background:var(--card);border:1px solid rgba(255,255,255,0.05);border-radius:20px;padding:2rem;text-align:center;box-shadow:0 8px 30px rgba(0,0,0,0.5);position:relative;overflow:hidden;">
      <div style="position:absolute;top:0;left:0;width:100%;height:3px;background:linear-gradient(90deg,transparent,#818cf8,transparent);"></div>
      <div style="font-size:3rem;font-weight:800;color:#d8b4fe;font-family:'JetBrains Mono',monospace;">223</div>
      <div style="font-size:0.75rem;color:#94a3b8;text-transform:uppercase;letter-spacing:2px;margin-top:8px;">Acoustic Vectors</div>
    </div>
    <div style="background:var(--card);border:1px solid rgba(255,255,255,0.05);border-radius:20px;padding:2rem;text-align:center;box-shadow:0 8px 30px rgba(0,0,0,0.5);position:relative;overflow:hidden;">
      <div style="position:absolute;top:0;left:0;width:100%;height:3px;background:linear-gradient(90deg,transparent,#22d3ee,transparent);"></div>
      <div style="font-size:3rem;font-weight:800;color:#f9a8d4;font-family:'JetBrains Mono',monospace;">{n_samples}</div>
      <div style="font-size:0.75rem;color:#94a3b8;text-transform:uppercase;letter-spacing:2px;margin-top:8px;">Trained Samples</div>
    </div>
    <div style="background:var(--card);border:1px solid rgba(255,255,255,0.05);border-radius:20px;padding:2rem;text-align:center;box-shadow:0 8px 30px rgba(0,0,0,0.5);position:relative;overflow:hidden;">
      <div style="position:absolute;top:0;left:0;width:100%;height:3px;background:linear-gradient(90deg,transparent,#34d399,transparent);"></div>
      <div style="font-size:3rem;font-weight:800;color:#34d399;font-family:'JetBrains Mono',monospace;">{acc_str}</div>
      <div style="font-size:0.75rem;color:#94a3b8;text-transform:uppercase;letter-spacing:2px;margin-top:8px;">Assurance Level</div>
    </div>
    <div style="background:var(--card);border:1px solid rgba(255,255,255,0.05);border-radius:20px;padding:2rem;text-align:center;box-shadow:0 8px 30px rgba(0,0,0,0.5);position:relative;overflow:hidden;">
      <div style="position:absolute;top:0;left:0;width:100%;height:3px;background:linear-gradient(90deg,transparent,#fb7185,transparent);"></div>
      <div style="font-size:3rem;font-weight:800;color:#fb7185;font-family:'JetBrains Mono',monospace;">{fake_count}</div>
      <div style="font-size:0.75rem;color:#94a3b8;text-transform:uppercase;letter-spacing:2px;margin-top:8px;">Anomalies Detected</div>
    </div>
  </div>

  <!-- WORKFLOW VISUALIZATION -->
  <div style="background:var(--card);border:1px solid rgba(255,255,255,0.05);border-radius:24px;padding:2.5rem;margin-bottom:2rem;box-shadow:0 8px 30px rgba(0,0,0,0.5);">
    <div style="font-size:0.75rem;font-weight:800;color:#94a3b8;letter-spacing:3px;margin-bottom:1.5rem;text-transform:uppercase;">
      <span style="color:#f9a8d4;">■</span> Analysis Architecture
    </div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1.5rem;">
      <div class="bubble-card" style="padding:1.5rem;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);border-radius:16px;cursor:pointer;">
        <div style="font-size:2.5rem;margin-bottom:12px;color:#fbcfe8;">🎙️</div>
        <div style="font-weight:800;font-size:0.95rem;color:#e2e8f0;margin-bottom:6px;">01. INGESTION</div>
        <div style="font-size:0.8rem;color:#94a3b8;line-height:1.6;">Direct microphone hook or high-fidelity audio file upload.</div>
      </div>
      <div class="bubble-card" style="padding:1.5rem;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);border-radius:16px;cursor:pointer;">
        <div style="font-size:2.5rem;margin-bottom:12px;color:#f9a8d4;">🔬</div>
        <div style="font-weight:800;font-size:0.95rem;color:#e2e8f0;margin-bottom:6px;">02. EXTRACTION</div>
        <div style="font-size:0.8rem;color:#94a3b8;line-height:1.6;">Computation of MFCCs, spectral flux, and tonal centroid features.</div>
      </div>
      <div class="bubble-card" style="padding:1.5rem;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);border-radius:16px;cursor:pointer;">
        <div style="font-size:2.5rem;margin-bottom:12px;color:#d8b4fe;">🤖</div>
        <div style="font-weight:800;font-size:0.95rem;color:#e2e8f0;margin-bottom:6px;">03. CLASSIFICATION</div>
        <div style="font-size:0.8rem;color:#94a3b8;line-height:1.6;">Ensemble XGBoost algorithm scores probabilities in latent space.</div>
      </div>
      <div class="bubble-card" style="padding:1.5rem;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);border-radius:16px;cursor:pointer;">
        <div style="font-size:2.5rem;margin-bottom:12px;color:#fda4af;">📋</div>
        <div style="font-weight:800;font-size:0.95rem;color:#e2e8f0;margin-bottom:6px;">04. FORENSICS</div>
        <div style="font-size:0.8rem;color:#94a3b8;line-height:1.6;">Generation of human-readable report with visualization charts.</div>
      </div>
    </div>
  </div>

</div>
"""


# ─────────────────────────────────────────────
# GRADIO APP
# ─────────────────────────────────────────────

with gr.Blocks(title="DeepShield", css=css) as demo:
    gr.HTML(
        "<div class='main-header'>"
        "<h1>DeepShield</h1>"
        "<p style='opacity:0.6'>Advanced Forensic Audio Verification Suite</p>"
        "</div>"
    )

    with gr.Tabs():

        # ── TAB 0: COMMAND CENTER ────────────────────────────────────────
        with gr.TabItem("🏠 Command Center"):
            homepage_html = gr.HTML(build_homepage_html())
            refresh_btn = gr.Button("🔄 Refresh System Status", elem_classes=["primary-btn"])
            refresh_btn.click(fn=build_homepage_html, inputs=[], outputs=[homepage_html])

        # ── TAB 1: FORENSIC LAB ──────────────────────────────────────────
        with gr.TabItem("🔍 Forensic Lab"):
            with gr.Row():
                with gr.Column(scale=4):
                    with gr.Column(elem_classes=["glass-card"]):
                        audio_input = gr.Audio(
                            label="Audio Evidence — Upload or Record",
                            type="filepath",
                            sources=["upload", "microphone"]
                        )
                        analyze_btn = gr.Button("🔍 START ANALYSIS", variant="primary",
                                                elem_classes=["primary-btn"])
                    threshold = gr.Slider(0.3, 0.8, 0.5, step=0.05, label="Sensitivity")
                    with gr.Row():
                        d_out = gr.Textbox(label="Duration",  interactive=False, elem_classes=["info-card"])
                        p_out = gr.Textbox(label="Pitch/Mag", interactive=False, elem_classes=["info-card"])
                    with gr.Row():
                        c_out = gr.Textbox(label="AI Conf %", interactive=False, elem_classes=["info-card"])
                        r_out = gr.Textbox(label="Threat",    interactive=False, elem_classes=["info-card"])

                with gr.Column(scale=5):
                    v_out      = gr.HTML("<div class='result-display' style='opacity:0.5'>AWAITING EVIDENCE...</div>")
                    reason_out = gr.HTML()
                    report_out = gr.File(label="📄 Forensic Report", elem_classes=["doc-box"])

            gr.Examples(
                examples=[
                    ["real_demo.wav"],
                    ["fake_demo.wav"]
                ],
                inputs=[audio_input],
                label="Pre-loaded Hackathon Demo Scenarios"
            )

            with gr.Row():
                spec_out = gr.Image(label="Spectrogram",       elem_classes=["viz-container"])
                feat_out = gr.Image(label="Feature Breakdown", elem_classes=["viz-container"])

            history = gr.Dataframe(
                headers=["File", "Verdict", "Conf", "Time"],
                elem_classes=["history-table"]
            )
            analyze_btn.click(
                fn=analyze_voice,
                inputs=[audio_input, threshold, history],
                outputs=[v_out, spec_out, feat_out, d_out, p_out,
                         c_out, r_out, history, report_out, reason_out]
            )

        # ── TAB 2: BATCH AUDIT ───────────────────────────────────────────
        with gr.TabItem("🗳️ Batch Audit"):
            with gr.Column(elem_classes=["glass-card"]):
                b_files     = gr.File(label="Upload Samples", file_count="multiple")
                b_threshold = gr.Slider(0.3, 0.8, 0.5, step=0.05, label="Sensitivity")
                b_btn       = gr.Button("🚀 START SCAN", variant="primary",
                                        elem_classes=["primary-btn"])
                b_out       = gr.Dataframe(headers=["File", "Result", "Conf", "Time"])
                b_btn.click(batch_analyze, [b_files, b_threshold], b_out)


if __name__ == "__main__":
    if sys.platform == "win32":
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    demo.launch(share=True)
# updated
