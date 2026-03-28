import gradio as gr
import joblib
import numpy as np
import os
import librosa
import datetime
import tempfile
import traceback
from detector import predict, extract_features
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
    except:
        print("⚠ Models not found. Please train/calibrate first.")
        return None, None

model, scaler = load_models()

from reporter import HAS_FPDF
if not HAS_FPDF:
    print("WARNING: 'fpdf2' not found. Forensic reports will be generated in .txt format.")

# ── ADVANCED GLASSMORPHISM CSS ──
css = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono&display=swap');
:root {
    --primary: #8b5cf6; --secondary: #06b6d4; --accent: #f43f5e;
    --bg: #030712; --card: rgba(17, 24, 39, 0.7);
}
* { box-sizing: border-box; transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1); }
body, .gradio-container {
    background: radial-gradient(circle at top right, #0f172a, #030712) !important;
    font-family: 'Outfit', sans-serif !important; color: #f8fafc !important;
}
.main-header { text-align: center; padding: 2.5rem 0 1.5rem; }
.main-header h1 {
    font-size: 3.2rem; font-weight: 800; margin: 0;
    background: linear-gradient(to right, #a78bfa, #22d3ee, #a78bfa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: -2px;
}
.glass-card {
    background: var(--card) !important;
    backdrop-filter: blur(16px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 20px !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8) !important;
    padding: 1.5rem !important;
}
.result-display {
    border-radius: 20px; padding: 2rem; margin-bottom: 20px;
    border: 2px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    text-align: center;
    backdrop-filter: blur(10px);
}
.result-genuine { 
    background: linear-gradient(145deg, rgba(34, 197, 94, 0.3), rgba(21, 128, 61, 0.4)) !important;
    border-color: #22c55e !important; color: #4ade80 !important; 
    box-shadow: 0 0 30px rgba(34, 197, 94, 0.3) !important;
    animation: pulse-glow-green 2s infinite ease-in-out !important;
}
@keyframes pulse-glow-green {
    50% { box-shadow: 0 0 50px rgba(34, 197, 94, 0.5) !important; transform: scale(1.01); }
}
.result-fake { 
    background: linear-gradient(145deg, rgba(220, 38, 38, 0.5), rgba(153, 27, 27, 0.6)) !important;
    border-color: #ef4444 !important; color: white !important;
    box-shadow: 0 0 40px rgba(220, 38, 38, 0.5) !important;
    text-transform: uppercase; letter-spacing: 2px;
    animation: pulse-glow-red 1.5s infinite ease-in-out !important;
}
@keyframes pulse-glow-red {
    50% { box-shadow: 0 0 60px rgba(220, 38, 38, 0.7) !important; transform: scale(1.02); }
}
.result-suspicious {
    background: linear-gradient(145deg, rgba(245, 158, 11, 0.4), rgba(180, 83, 9, 0.5)) !important;
    border-color: #fbbf24 !important; color: #fbbf24 !important;
    box-shadow: 0 0 30px rgba(245, 158, 11, 0.3) !important;
}
.verdict-text { font-size: 2.2rem; font-weight: 800; margin-bottom: 5px; }
.confidence-bar { font-family: 'JetBrains Mono', monospace; font-size: 1rem; opacity: 0.9; font-weight: 600; }

.status-badge {
    display: inline-block; padding: 3px 10px; border-radius: 100px;
    font-size: 0.7rem; font-weight: 800; text-transform: uppercase;
    margin-bottom: 8px; border: 1px solid currentColor;
}

.primary-btn {
    background: linear-gradient(135deg, #7c3aed, #0891b2) !important;
    border: none !important; border-radius: 12px !important;
    font-weight: 700 !important; color: white !important;
    box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3) !important;
    padding: 10px 20px !important;
}
.primary-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(124, 58, 237, 0.5) !important; }

.info-card {
    background: rgba(6, 182, 212, 0.05) !important;
    border: 1px solid rgba(6, 182, 212, 0.2) !important;
    border-radius: 12px !important; padding: 12px !important;
    box-shadow: inset 0 0 15px rgba(6, 182, 212, 0.05) !important;
}
.info-card label { 
    color: #22d3ee !important; font-weight: 800 !important; 
    text-transform: uppercase !important; font-size: 0.75rem !important;
    letter-spacing: 0.5px !important; margin-bottom: 4px !important;
}
.info-card input {
    background: rgba(0,0,0,0.2) !important; border: 1px solid rgba(255,255,255,0.05) !important;
    color: #f8fafc !important; font-family: 'JetBrains Mono', monospace !important;
}

.obs-box {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(139, 92, 246, 0.1)) !important;
    padding: 20px; border-radius: 16px; margin-top: 20px;
    border: 1px solid rgba(6, 182, 212, 0.3) !important;
    box-shadow: 0 4px 15px rgba(6, 182, 212, 0.1);
    color: #e2e8f0 !important;
}
.obs-box b { color: #22d3ee; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 1px; }

.doc-box {
    background: transparent !important; border: none !important; margin-top: 10px;
}
.doc-box .gr-box, .doc-box .gr-form { background: transparent !important; border: none !important; }
.doc-box [data-testid="block-label"] { display: none !important; }
.doc-box .file-preview { 
    background: rgba(255,255,255,0.05) !important; 
    border: 1px dashed rgba(255,255,255,0.2) !important; 
    border-radius: 12px !important;
}

.history-table { border-radius: 12px; overflow: hidden; border: 1px solid rgba(255,255,255,0.05); }

.viz-container { border-radius: 16px; overflow: hidden; margin-top: 10px; border: 1px solid rgba(255,255,255,0.1); }
"""

def analyze_voice(audio_input, threshold=0.5, history=None):
    if history is None: history = []
    if audio_input is None:
        return ("<div class='verdict-text' style='color:#94a3b8'>AWAITING SAMPLE...</div>", None, None, "—", "—", "—", "—", history, None, "")

    try:
        global model, scaler
        if model is None: model, scaler = load_models()
        if model is None: return ("<div class='verdict-text' style='color:#f43f5e'>ERROR: Model Not Found</div>", None, None, "—", "—", "—", "—", history, None, "")
        
        prob_fake, reasoning = predict(audio_input, model, scaler)
        prob_real = 1 - prob_fake

        # Verdict logic and Styling
        if prob_fake >= threshold + 0.25:
            color, label, icon, cls = "#f43f5e", "DEEPFAKE DETECTED", "⚠", "result-fake"
        elif prob_fake >= threshold:
            color, label, icon, cls = "#fbbf24", "SUSPICIOUS ACTIVITY", "﹖", "result-suspicious"
        else:
            color, label, icon, cls = "#22c55e", "GENUINE HUMAN", "✓", "result-genuine"

        verdict_html = f"""
        <div class="result-display {cls}">
            <div class="status-badge">{label}</div>
            <div class="verdict-text">{icon} {label}</div>
            <div class="confidence-bar">{prob_fake*100:.1f}% AI SYNTHETIC • {prob_real*100:.1f}% HUMAN ORGANIC</div>
        </div>
        """
        
        reasoning_html = f"<div class='obs-box'><b>AI FORENSIC OBSERVATION:</b><br>" + "<br>".join(reasoning) + "</div>"
        
        spec_img = plot_spectrogram(audio_input)
        feat_chart = plot_feature_chart(audio_input)
        
        y, sr = librosa.load(audio_input, sr=22050, duration=5.0)
        duration = f"{len(y)/sr:.2f}s"
        try:
            centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
            avg_pitch = f"{int(np.nanmean(centroid))} Hz"
        except: avg_pitch = "—"

        # Report
        r_pdf = os.path.join(tempfile.gettempdir(), f"Report_{datetime.datetime.now().strftime('%H%M%S')}.pdf")
        r_txt = os.path.join(tempfile.gettempdir(), f"Report_{datetime.datetime.now().strftime('%H%M%S')}.txt")
        generate_pdf_report(os.path.basename(audio_input), prob_fake, label, duration, avg_pitch, reasoning, r_pdf)
        if not os.path.exists(r_pdf):
            with open(r_txt, "w", encoding="utf-8") as f: 
                f.write(f"DEEPVOICE SHIELD REPORT\nResult: {label}\nConf: {prob_fake*100:.1f}%\n")
            final_report = r_txt
        else: final_report = r_pdf

        # 5. Handle History (Robust to Pandas/List)
        if hasattr(history, 'values'): # If it's a pandas DataFrame
            history = history.values.tolist()
        elif history is None:
            history = []

        history = [[os.path.basename(audio_input), label, f"{prob_fake*100:.1f}%", datetime.datetime.now().strftime("%H:%M")]] + history
        return (verdict_html, spec_img, feat_chart, duration, avg_pitch, f"{prob_fake*100:.1f}%", label, history, final_report, reasoning_html)

    except Exception as e:
        traceback.print_exc()
        # Ensure history is returned as list even on error
        if hasattr(history, 'values'): history = history.values.tolist()
        return (f"<div class='verdict-text' style='color:#f43f5e'>ANALYSIS FAILED: {str(e)}</div>", None, None, "—", "—", "—", "—", history, None, "")


def batch_analyze(files, threshold=0.5):
    results = []
    if not files: return results
    for f in files:
        try:
            prob, _ = predict(f.name, model, scaler)
            v = "FAKE" if prob >= threshold + 0.25 else ("SUSPICIOUS" if prob >= threshold else "REAL")
            results.append([os.path.basename(f.name), v, f"{prob*100:.1f}%", datetime.datetime.now().strftime("%H:%M")])
        except:
            results.append([os.path.basename(f.name), "ERROR", "—", "—"])
    return results

with gr.Blocks(title="DeepVoice Shield Pro") as demo:
    gr.HTML("<div class='main-header'><h1>DEEPVOICE SHIELD PRO</h1><p style='opacity:0.6'>Advanced Forensic Audio Verification Suite</p></div>")

    with gr.Tabs():
        with gr.TabItem("🔍 Forensic Lab"):
            with gr.Row():
                with gr.Column(scale=4):
                    with gr.Column(elem_classes=["glass-card"]):
                        audio_input = gr.Audio(label="Audio Evidence", type="filepath")
                        analyze_btn = gr.Button("🔍 START ANALYSIS", variant="primary", elem_classes=["primary-btn"])
                    
                    threshold = gr.Slider(0.3, 0.8, 0.5, step=0.05, label="Sensitivity")
                    
                    with gr.Row():
                        d_out = gr.Textbox(label="Duration", interactive=False, elem_classes=["info-card"])
                        p_out = gr.Textbox(label="Pitch/Mag", interactive=False, elem_classes=["info-card"])
                    with gr.Row():
                        c_out = gr.Textbox(label="AI Conf %", interactive=False, elem_classes=["info-card"])
                        r_out = gr.Textbox(label="Threat", interactive=False, elem_classes=["info-card"])
                
                with gr.Column(scale=5):
                    v_out = gr.HTML("<div class='result-display' style='opacity:0.5'>AWAITING EVIDENCE...</div>")
                    reason_out = gr.HTML()
                    report_out = gr.File(label="📄 Forensic Report", elem_classes=["doc-box"])

            with gr.Row():
                spec_out = gr.Image(label="Spectrogram", elem_classes=["viz-container"])
                feat_out = gr.Image(label="Feature Breakdown", elem_classes=["viz-container"])

            history = gr.Dataframe(headers=["File", "Verdict", "Conf", "Time"], elem_classes=["history-table"])
            analyze_btn.click(analyze_voice, [audio_input, threshold, history], [v_out, spec_out, feat_out, d_out, p_out, c_out, r_out, history, report_out, reason_out])

        with gr.TabItem("🗳️ Batch Audit"):
            with gr.Column(elem_classes=["glass-card"]):
                b_files = gr.File(label="Upload Samples", file_count="multiple")
                b_btn = gr.Button("🚀 START SCAN", variant="primary", elem_classes=["primary-btn"])
                b_out = gr.Dataframe(headers=["File", "Result", "Conf", "Time"])
                b_btn.click(batch_analyze, [b_files, threshold], b_out)

if __name__ == "__main__":
    demo.launch(share=True, css=css)