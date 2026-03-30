import librosa
import numpy as np

def preprocess_audio(file_path):
    """
    Load, resample, to mono, normalize, and exact 3s pad/trim.
    Applies noise reduction/silence trimming.
    """
    try:
        # Convert to mono, resample to 16000 Hz
        y, sr = librosa.load(file_path, sr=16000, mono=True)
        
        # Noise Robustness / Trim silence
        y_trimmed, _ = librosa.effects.trim(y, top_db=30)
        if len(y_trimmed) > sr * 0.5:  # fallback if audio completely trimmed
            y = y_trimmed
            
        # Normalize audio
        y = librosa.util.normalize(y)
        
        # Trim or pad audio to EXACTLY 3 seconds
        target_len = sr * 3
        if len(y) > target_len:
            y = y[:target_len]
        else:
            y = np.pad(y, (0, target_len - len(y)))
            
        print(f"DEBUG | Sample rate: {sr}")
        print(f"DEBUG | Audio length: 3 sec")
        return y, sr
    except Exception as e:
        raise RuntimeError(f"Preprocessing failed: {str(e)}")


def extract_features(y, sr):
    """
    Extract exact features for training and inference consistency.
    """
    try:
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
        mfcc_mean = np.mean(mfcc.T, axis=0)
        mfcc_std  = np.std(mfcc.T,  axis=0)

        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_mean = np.mean(chroma.T, axis=0)

        mel = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        mel_mean = np.mean(mel.T, axis=0)

        # Spectral contrast added for deeper acoustic analysis
        contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        contrast_mean = np.mean(contrast.T, axis=0)

        zcr = np.mean(librosa.feature.zero_crossing_rate(y=y))
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        spectral_rolloff  = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))

        features = np.hstack((
            mfcc_mean,       # 40
            mfcc_std,        # 40
            chroma_mean,     # 12
            mel_mean,        # 128
            contrast_mean,   # 7
            [zcr, spectral_centroid, spectral_rolloff]  # 3
        ))
        print(f"DEBUG | Features shape: {features.shape}")
        return features

    except Exception as e:
        raise RuntimeError(f"Feature extraction failed: {str(e)}")


def get_ai_reasoning(features, result_label):
    reasons = []

    mfcc_std_mean = np.mean(features[40:80])
    if mfcc_std_mean < 1.0:
        reasons.append("[!] Low MFCC variance — typically an AI TTS artifact")

    if result_label == "Uncertain":
        reasons.append("[~] Low Confidence (< 70%) — The acoustic signatures are highly ambiguous.")

    if not reasons:
        reasons.append("[OK] Voice displays standard organic variance and natural phonation.")

    return reasons


def predict_audio(file, model, scaler, demo_type=None):
    """
    Predict probability and return standardized result dict and reasoning.
    demo_type can be "real" or "fake" for safe demo behavior.
    """
    try:
        # --- Demo Mode Safety ---
        if demo_type == "fake":
            return {"result": "Fake", "confidence": 99.9, "prob_fake": 0.999}, ["[DEMO] Detected known synthetic clone footprint."]
        elif demo_type == "real":
            return {"result": "Real", "confidence": 99.9, "prob_fake": 0.001}, ["[DEMO] Clean, known human organic baseline."]

        # Production pipeline
        y, sr = preprocess_audio(file)
        features = extract_features(y, sr)
        
        features_reshaped = features.reshape(1, -1)
        features_scaled = scaler.transform(features_reshaped)
        
        prob_fake = float(model.predict_proba(features_scaled)[0][1])
        prob_fake_percent = prob_fake * 100.0
        prob_real_percent = 100.0 - prob_fake_percent
        
        # Confidence Handling
        max_conf = max(prob_fake_percent, prob_real_percent)
        
        if max_conf < 70.0:
            result_label = "Uncertain"
        else:
            result_label = "Fake" if prob_fake >= 0.5 else "Real"
            
        reasoning = get_ai_reasoning(features, result_label)
        
        return {
            "result": result_label,
            "confidence": max_conf,
            "prob_fake": prob_fake
        }, reasoning

    except Exception as e:
        raise RuntimeError(f"Prediction failed: {str(e)}")
