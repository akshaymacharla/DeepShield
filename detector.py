import librosa
import numpy as np

def extract_features(file):
    """
    Extract audio features matching the train_model.py exactly.
    """
    try:
        audio, sr = librosa.load(file, res_type='kaiser_fast', duration=5.0)

        if audio is None or len(audio) == 0:
            raise ValueError("Audio file is empty or corrupted")

        if len(audio) < 22050:
            audio = np.pad(audio, (0, 22050 - len(audio)))
        
        audio = audio[:22050 * 5]

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
            mfcc_mean,       # 40
            mfcc_std,        # 40
            chroma_mean,     # 12
            mel_mean,        # 128
            [zcr, spectral_centroid, spectral_rolloff] # 3
        ))
        return features

    except Exception as e:
        raise ValueError(f"Feature extraction failed: {str(e)}")


def get_ai_reasoning(features):
    """
    Expert heuristic analysis of features to provide human-readable red flags.
    Based on common deepfake artifacts.
    """
    reasons = []
    
    # 1. Pitch Stability (infer from MFCC std, features 40-79)
    mfcc_std_mean = np.mean(features[40:80])
    if mfcc_std_mean < 1.0:
        reasons.append("[!] Unnatural voice stability detected (AI-like monotone)")
    
    # 2. Spectral Roll-off (High frequency cut-off)
    # features[222] = spectral_rolloff
    if features[222] < 3000:
        reasons.append("[!] Lack of high-frequency natural breath noise")
        
    # 3. ZCR (Zero Crossing Rate)
    # features[220] = zcr
    if features[220] < 0.05:
        reasons.append("[!] Sub-natural phoneme transitions detected")

    if not reasons:
        reasons.append("[OK] Voice displays natural organic variance and noise profile")
        
    return reasons


def predict(file, model, scaler):
    """
    Predict probability and return AI reasoning.
    """
    try:
        features = extract_features(file)
        
        # Get reasoning before scaling
        reasoning = get_ai_reasoning(features)
        
        # Scale and predict
        features_reshaped = features.reshape(1, -1)
        features_scaled = scaler.transform(features_reshaped)
        prob_fake = model.predict_proba(features_scaled)[0][1]
        
        return float(prob_fake), reasoning
    except Exception as e:
        raise ValueError(str(e))