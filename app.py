import gradio as gr
import joblib
import numpy as np
import os
import librosa
import datetime
import tempfile
import soundfile as sf
import traceback
from detector import predict, extract_features
from visualizer import plot_spectrogram
from charts import plot_feature_chart
from reporter import generate_pdf_report

# ── Dynamic Model Loading ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'models', 'scaler.pkl')

try:
    model  = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print(f"✅ Models loaded successfully")
except Exception as e:
    print(f"❌ Error loading models: {e}")
    model, scaler = None, None

css = """
* { box-sizing: border-box; transition: all 0.3s ease; }
body, .gradio-container {
    background: linear-gradient(135deg, #020205 0%, #0a0a25 100%) !important;
    font-family: 'Inter', sans-serif !important;
    color: white !important;
}
.main-header { text-align: center; padding: 2.5rem 0 1.5rem; }
.main-header h1 {
    font-size: 3.2rem; font-weight: 900;
    background: linear-gradient(90deg, #8b5cf6, #06b6d4, #8b5cf6);
    background-size: 200% auto;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: shine 3s linear infinite;
    margin-bottom: 0.5rem; letter-spacing: -1px;
}
@keyframes shine { to { background-position: 200% center; } }

.result-box {
    border-radius: 16px; padding: 2.5rem; text-align: center;
    font-size: 1.8rem; font-weight: 800; border: 2px solid rgba(255,255,255,0.1);
    margin-bottom: 25px; backdrop-filter: blur(10px);
    background: rgba(139, 92, 246, 0.1) !important; /* Initial subtle violet */
    color: rgba(255,255,255,0.9);
}
.result-genuine { 
    background: linear-gradient(145deg, rgba(34, 197, 94, 0.4), rgba(21, 128, 61, 0.5)) !important;
    border-color: #22c55e !important; color: #4ade80 !important; 
    box-shadow: 0 0 30px rgba(34, 197, 94, 0.2);
}
.result-fake { 
    background: linear-gradient(145deg, #dc2626, #991b1b) !important;
    border-color: #ef4444 !important; color: white !important;
    box-shadow: 0 0 40px rgba(220, 38, 38, 0.4);
    text-transform: uppercase; letter-spacing: 2px;
}
.gr-button-primary {
    background: linear-gradient(90deg, #f97316, #ef4444) !important;
    border: none !important; border-radius: 14px !important;
    font-weight: 800 !important; font-size: 1.2rem !important;
    box-shadow: 0 8px 20px rgba(239, 68, 68, 0.3) !important;
    padding: 12px 24px !important;
}
.gr-button-primary:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 12px 25px rgba(239, 68, 68, 0.5) !important;
}

.xai-box {
    background: linear-gradient(135deg, rgba(124, 58, 237, 0.3), rgba(76, 29, 149, 0.4)) !important;
    padding: 20px; border-radius: 16px; margin-top: 20px;
    font-size: 1.1rem; line-height: 1.6; border: 1px solid rgba(139, 92, 246, 0.5);
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.2);
    color: #f3e8ff !important;
}
.xai-box b { color: #e9d5ff; font-size: 1.2rem; display: block; margin-bottom: 8px; }

/* ── AGGRESSIVE CUSTOMIZATION FOR DOWNLOAD BOX ── */
.report-download {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(8, 145, 178, 0.3)) !important;
    border: 2px solid #06b6d4 !important;
    border-radius: 16px !important;
    box-shadow: 0 0 30px rgba(6, 182, 212, 0.3) !important;
}
.report-download .label, .report-download .label span { 
    background: linear-gradient(90deg, #0891b2, #06b6d4) !important; 
    color: white !important; font-weight: 800 !important;
    border-bottom: 1px solid rgba(255,255,255,0.2) !important;
}
.report-download .file-preview, .report-download .file-preview * { 
    background: rgba(6, 182, 212, 0.1) !important; 
    color: #cffafe !important;
    border: none !important;
}
.report-download:hover { transform: scale(1.01); box-shadow: 0 0 50px rgba(6, 182, 212, 0.5) !important; }

/* ── INFO CARDS (NO GREY) ── */
.info-card {
    background: linear-gradient(145deg, rgba(124, 58, 237, 0.2), rgba(30, 41, 59, 0.4)) !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
    border-radius: 14px !important;
    box-shadow: inset 0 0 10px rgba(139, 92, 246, 0.1) !important;
}
.info-card label {
    background: transparent !important;
    color: #c4b5fd !important;
    font-weight: 800 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
}
.info-card input {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #22d3ee !important;
    font-weight: 800 !important;
    font-size: 1.2rem !important;
}

.gr-audio, .gr-file, .gr-image { 
    border-radius: 16px !important; border: 1px solid rgba(255,255,255,0.1) !important;
    background: rgba(255,255,255,0.03) !important;
}
.large-image img { object-fit: contain !important; height: 100% !important; width: 100% !important; }
"""

def analyze_voice(audio_input, threshold=0.5, history=None):
    if history is None: history = []
    if audio_input is None:
        return ("<div class='result-box'>Upload audio to analyze</div>", None, None, "—", "—", "—", "—", history, None, "")

    try:
        # 1. Run prediction
        prob_fake, reasoning = predict(audio_input, model, scaler)
        prob_real = 1 - prob_fake

        # 2. Verdict
        if prob_fake >= threshold + 0.25:
            verdict_html = f"<div class='result-box result-fake'>&#9888; DEEPFAKE DETECTED<br><small style='font-size:0.95rem; opacity:0.95; font-weight:500'>{prob_fake*100:.1f}% AI PROBABILITY • CRITICAL RISK</small></div>"
            risk_label = "HIGH RISK"
        elif prob_fake >= threshold:
            verdict_html = f"<div class='result-box' style='background:linear-gradient(145deg, rgba(245,158,11,0.5), rgba(180,83,9,0.6));color:#fbbf24;border-color:#f59e0b;box-shadow:0 0 25px rgba(245,158,11,0.3)'>&#9888; SUSPICIOUS ACTIVITY<br><small style='font-size:0.95rem'>{prob_fake*100:.1f}% synthetic likelihood</small></div>"
            risk_label = "MEDIUM"
        else:
            verdict_html = f"<div class='result-box result-genuine'>&#10004; GENUINE VOICE<br><small style='font-size:0.95rem'>{prob_real*100:.1f}% organic human match</small></div>"
            risk_label = "LOW RISK"

        # 3. AI Reasoning HTML
        reasoning_html = "<div class='xai-box'><b>AI Forensic Observation:</b>" + "<br>".join(reasoning) + "</div>"
        
        # 4. Visuals & Metadata
        spec_img = plot_spectrogram(audio_input)
        feat_chart = plot_feature_chart(audio_input)
        y, sr = librosa.load(audio_input, sr=16000, duration=5.0)
        duration = f"{len(y)/sr:.2f}s"
        avg_pitch = f"{int(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))} Hz"

        # 5. Generate PDF Report
        report_path = os.path.join(tempfile.gettempdir(), f"Forensic_Report_{datetime.datetime.now().strftime('%H%M%S')}.pdf")
        generate_pdf_report(os.path.basename(audio_input), prob_fake, risk_label, duration, avg_pitch, reasoning, report_path)

        # 6. History
        res_label = "FAKE" if prob_fake >= threshold + 0.25 else ("SUSPICIOUS" if prob_fake >= threshold else "REAL")
        new_row = [os.path.basename(audio_input), res_label, f"{prob_fake*100:.1f}%", risk_label, datetime.datetime.now().strftime("%H:%M:%S")]
        updated_history = [new_row] + (history if isinstance(history, list) else [])

        return (verdict_html, spec_img, feat_chart, duration, avg_pitch, f"{prob_fake*100:.1f}%", risk_label, updated_history, report_path, reasoning_html)

    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return (f"<div class='result-box' style='color:#ef4444'>Error: {str(e)}</div>", None, None, "—", "—", "—", "—", history, None, "")

def batch_analyze(files, threshold=0.5):
    results = []
    if not files: return results
    for f in files:
        try:
            prob, _ = predict(f.name, model, scaler)
            verdict = "FAKE" if prob >= threshold + 0.25 else ("SUSPICIOUS" if prob >= threshold else "REAL")
            results.append([os.path.basename(f.name), verdict, f"{prob*100:.1f}%", datetime.datetime.now().strftime("%H:%M:%S")])
        except:
            results.append([os.path.basename(f.name), "ERROR", "—", "—"])
    return results

with gr.Blocks(title="DeepVoice Shield Pro") as demo:
    gr.HTML("<div class='main-header'><h1>DeepVoice Shield Pro</h1><p style='font-size:1.2rem; opacity:0.8'>Professional AI Forensic Suite for Voice Authentication</p></div>")

    with gr.Tabs():
        with gr.TabItem("🔍 Standard Analysis"):
            with gr.Row():
                with gr.Column(scale=1):
                    audio_input = gr.Audio(label="Source Audio", type="filepath")
                    threshold_slider = gr.Slider(0.3, 0.8, 0.5, step=0.05, label="Detection Sensitivity")
                    analyze_btn = gr.Button("🔍 Execute AI Forensic Analysis", variant="primary")
                    with gr.Row():
                        duration_out = gr.Textbox(label="Audio Duration", interactive=False, elem_classes=["info-card"])
                        pitch_out    = gr.Textbox(label="Signal Magnitude", interactive=False, elem_classes=["info-card"])
                    with gr.Row():
                        synthetic_prob = gr.Textbox(label="AI Conf %", interactive=False, elem_classes=["info-card"])
                        risk_out       = gr.Textbox(label="Threat Level", interactive=False, elem_classes=["info-card"])
                
                with gr.Column(scale=1):
                    verdict_out = gr.HTML("<div class='result-box' style='color: white; font-weight: bold;'>Awaiting data analysis...</div>")
                    reasoning_out = gr.HTML()
                    report_out = gr.File(label="📄 Download Forensic Audit Report", elem_classes=["report-download"])

            with gr.Column():
                gr.Markdown("### 📊 Forensic Signal Visualization")
                spectrogram_out = gr.Image(label="Spectrogram Analysis", height=600, elem_classes=["large-image"])
                feat_out = gr.Image(label="Feature Breakdown", height=600, elem_classes=["large-image"])

            history_table = gr.Dataframe(headers=["File", "Result", "Conf", "Risk", "Time"], wrap=True)
            analyze_btn.click(analyze_voice, [audio_input, threshold_slider, history_table], 
                              [verdict_out, spectrogram_out, feat_out, duration_out, pitch_out, synthetic_prob, risk_out, history_table, report_out, reasoning_out])

        with gr.TabItem("🗳️ Batch Forensic Sweep"):
            gr.Markdown("### 🗳️ Professional Batch Audit System")
            batch_input = gr.File(label="Select High-Volume Samples", file_count="multiple", file_types=["audio"])
            batch_btn = gr.Button("🚀 Start Multi-File Forensic Scan", variant="primary")
            batch_out = gr.Dataframe(headers=["Filename", "Audit Result", "AI Confidence", "Timestamp"])
            batch_btn.click(batch_analyze, [batch_input, threshold_slider], batch_out)

if __name__ == "__main__":
    demo.launch(share=True, css=css)