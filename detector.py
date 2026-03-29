import librosa
import numpy as np


def extract_features(file):
    """
    Extract audio features matching the train_model.py exactly.
    """
    try:
        audio, sr = librosa.load(file, sr=22050, duration=5.0)

        if audio is None or len(audio) == 0:
            raise ValueError("Audio file is empty or corrupted")

        target_len = 22050 * 5
        if len(audio) < target_len:
            audio = np.pad(audio, (0, target_len - len(audio)))

        audio = audio[:target_len]

        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
        mfcc_mean = np.mean(mfcc.T, axis=0)
        mfcc_std  = np.std(mfcc.T,  axis=0)

        chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
        chroma_mean = np.mean(chroma.T, axis=0)

        mel = librosa.feature.melspectrogram(y=audio, sr=sr)
        mel_mean = np.mean(mel.T, axis=0)

        zcr = np.mean(librosa.feature.zero_crossing_rate(y=audio))
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio, sr=sr))
        spectral_rolloff  = np.mean(librosa.feature.spectral_rolloff(y=audio, sr=sr))

        features = np.hstack((
            mfcc_mean,        # 40
            mfcc_std,         # 40
            chroma_mean,      # 12
            mel_mean,         # 128
            [zcr, spectral_centroid, spectral_rolloff]  # 3
        ))
        return features

    except Exception as e:
        # Re-raise with clear message but do NOT double-wrap
        raise RuntimeError(f"Feature extraction failed: {str(e)}")


def get_ai_reasoning(features):
    """
    Expert heuristic analysis of features to provide human-readable red flags.
    """
    reasons = []

    mfcc_std_mean = np.mean(features[40:80])
    if mfcc_std_mean < 0.7:
        reasons.append("[!] High voice stability (Common AI monotone artifact)")

    # features[222] = spectral_rolloff
    if len(features) > 222 and features[222] < 2000:
        reasons.append("[!] Compressed frequency response detected")

    # features[220] = zcr
    if len(features) > 220 and features[220] < 0.05:
        reasons.append("[!] Sub-natural phoneme transitions detected")

    if not reasons:
        reasons.append("[OK] Voice displays natural organic variance and noise profile")

    return reasons


def predict(file, model, scaler):
    """
    Predict probability and return AI reasoning.
    Returns (prob_fake: float, reasoning: list) or raises RuntimeError.
    """
    # Guard: catch everything and return a safe tuple — never raise into Gradio/ASGI
    try:
        features = extract_features(file)
        reasoning = get_ai_reasoning(features)

        features_reshaped = features.reshape(1, -1)
        features_scaled = scaler.transform(features_reshaped)
        prob_fake = float(model.predict_proba(features_scaled)[0][1])

        return prob_fake, reasoning

    except RuntimeError:
        raise  # already well-formatted, let app.py catch it
    except Exception as e:
        raise RuntimeError(f"Prediction failed: {str(e)}")