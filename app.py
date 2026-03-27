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

# ── Dynamic Model Loading ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'models', 'scaler.pkl')

try:
    model  = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print(f"✅ Models loaded successfully from {BASE_DIR}")
except Exception as e:
    print(f"❌ Error loading models: {e}")
    model = None
    scaler = None

css = """
* { box-sizing: border-box; }
body, .gradio-container {
    background: linear-gradient(135deg, #0a0a1a 0%, #0f0f2e 100%) !important;
    font-family: 'Inter', sans-serif !important;
}
.main-header { text-align: center; padding: 2rem 0 1rem; }
.main-header h1 {
    font-size: 2.4rem; font-weight: 700;
    background: linear-gradient(90deg, #7c3aed, #06b6d4);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.main-header p { color: #94a3b8; font-size: 1rem; }
.result-box {
    border-radius: 16px; padding: 1.5rem; text-align: center;
    font-size: 1.4rem; font-weight: 700; letter-spacing: 1px;
}
.result-genuine {
    background: linear-gradient(135deg, #052e16, #14532d);
    border: 1.5px solid #22c55e; color: #4ade80;
}
.result-fake {
    background: linear-gradient(135deg, #450a0a, #7f1d1d);
    border: 1.5px solid #ef4444; color: #f87171;
}
.gr-button-primary {
    background: linear-gradient(90deg, #7c3aed, #2563eb) !important;
    border: none !important; border-radius: 12px !important;
    font-size: 1.1rem !important; font-weight: 600 !important;
    padding: 0.8rem 2rem !important; color: white !important;
}
.feature-tag {
    display: inline-block; background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.4); color: #a78bfa;
    border-radius: 20px; padding: 3px 12px; font-size: 0.8rem; margin: 3px;
}
"""

def analyze_voice(audio_input, threshold=0.5, history=None):
    if history is None: history = []
    
    if audio_input is None:
        return (
            "<div class='result-box' style='background:#1e1e3f;color:#64748b'>"
            "Upload or record an audio sample to analyze</div>",
            None, None, "—", "—", "—", "—", history
        )

    if model is None or scaler is None:
        return ("<div class='result-box' style='color:#f87171'>⚠ Error: Models not loaded. Check console.</div>",
                None, None, "—", "—", "—", "—", history)

    try:
        # Step 1: Run model
        # detector.py handles all audio loading and resampling to 16kHz
        prob_fake = predict(audio_input, model, scaler)
        prob_real = 1 - prob_fake

        # Step 2: Determine verdict
        if prob_fake >= threshold + 0.25:
            verdict_html = f"<div class='result-box result-fake'>⚠ DEEPFAKE DETECTED<div style='font-size:0.9rem;margin-top:8px;font-weight:400;color:#fca5a5'>{prob_fake*100:.1f}% synth likelihood</div></div>"
            risk_level = "HIGH RISK"
        elif prob_fake >= threshold:
            verdict_html = f"<div class='result-box' style='background:linear-gradient(135deg,#3d2900,#713f12);border:1.5px solid #f59e0b;color:#fcd34d'>⚡ SUSPICIOUS<div style='font-size:0.9rem;margin-top:8px;font-weight:400'>{prob_fake*100:.1f}% synth likelihood</div></div>"
            risk_level = "MEDIUM"
        else:
            verdict_html = f"<div class='result-box result-genuine'>✓ GENUINE VOICE<div style='font-size:0.9rem;margin-top:8px;font-weight:400;color:#86efac'>{prob_real*100:.1f}% human likelihood</div></div>"
            risk_level = "LOW RISK"

        bar_color = "linear-gradient(90deg,#ef4444,#dc2626)" if prob_fake >= threshold + 0.25 else ("linear-gradient(90deg,#f59e0b,#d97706)" if prob_fake >= threshold else "linear-gradient(90deg,#22c55e,#16a34a)")
        confidence_html = f"<div style='margin-top:12px'><div style='color:#94a3b8;font-size:0.8rem;margin-bottom:6px'>CONFIDENCE METER</div><div style='background:#1e1e3f;border-radius:8px;height:18px;overflow:hidden'><div style='height:100%;width:{prob_fake*100:.1f}%;background:{bar_color};border-radius:8px'></div></div><div style='display:flex;justify-content:space-between;color:#475569;font-size:0.7rem;margin-top:3px'><span>Real</span><span>Synth</span></div></div>"
        full_verdict = verdict_html + confidence_html

        # Step 3: Visuals
        try: spec_img = plot_spectrogram(audio_input)
        except Exception: spec_img = None
        
        try: feature_chart = plot_feature_chart(audio_input)
        except Exception: feature_chart = None

        # Step 4: Metadata
        try:
            y, sr = librosa.load(audio_input, sr=16000, duration=5.0)
            duration = f"{len(y)/sr:.2f}s"
            # Use centroid as a pitch proxy
            cent = librosa.feature.spectral_centroid(y=y, sr=sr)
            avg_pitch = f"{int(np.mean(cent))} Hz"
        except:
            duration, avg_pitch = "—", "—"

        # Step 5: History
        res_label = "FAKE" if prob_fake >= threshold + 0.25 else ("SUSPICIOUS" if prob_fake >= threshold else "REAL")
        new_row = [os.path.basename(audio_input), res_label, f"{prob_fake*100:.1f}%", risk_level, datetime.datetime.now().strftime("%H:%M:%S")]
        updated_history = [new_row] + (history if isinstance(history, list) else [])

        return (full_verdict, spec_img, feature_chart, duration, avg_pitch, f"{prob_fake*100:.1f}%", risk_level, updated_history)

    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        traceback.print_exc()
        return (f"<div class='result-box' style='color:#f87171'>⚠ Error: {str(e)}</div>", None, None, "—", "—", "—", "—", history)


with gr.Blocks(css=css, title="DeepVoice Shield") as demo:
    gr.HTML("<div class='main-header'><h1>DeepVoice Shield</h1><p>AI-powered deepfake voice detection — verify authenticity</p></div>")

    with gr.Row():
        with gr.Column(scale=1):
            # FIXED: type="filepath" is much more reliable for various audio formats
            audio_input = gr.Audio(label="Voice Sample", type="filepath", sources=["upload", "microphone"])
            threshold_slider = gr.Slider(minimum=0.3, maximum=0.8, value=0.5, step=0.05, label="Sensitivity")
            analyze_btn = gr.Button("🔍 Analyze Voice", variant="primary")
            with gr.Row():
                duration_out = gr.Textbox(label="Duration", interactive=False)
                pitch_out    = gr.Textbox(label="Avg Pitch", interactive=False)
            with gr.Row():
                synthetic_prob = gr.Textbox(label="Synthetic Probability", interactive=False)
                risk_out       = gr.Textbox(label="Risk Level", interactive=False)

        with gr.Column(scale=1):
            verdict_out = gr.HTML("<div class='result-box' style='background:#1e1e3f;color:#475569'>Awaiting analysis...</div>")
            spectrogram_out = gr.Image(label="SPECTROGRAM")
            feature_chart_out = gr.Image(label="FEATURE BREAKDOWN")

    history_table = gr.Dataframe(headers=["File", "Result", "Conf", "Risk", "Time"], datatype=["str", "str", "str", "str", "str"], wrap=True)

    analyze_btn.click(
        fn=analyze_voice,
        inputs=[audio_input, threshold_slider, history_table],
        outputs=[verdict_out, spectrogram_out, feature_chart_out, duration_out, pitch_out, synthetic_prob, risk_out, history_table]
    )

if __name__ == "__main__":
    demo.launch(share=True)