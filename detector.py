import librosa
import numpy as np

def extract_features(file):
    """
    Extract audio features matching the train_model.py exactly.
    
    CRITICAL: 
    - Default sr for librosa is 22050 (this is what train_model.py uses)
    - Res_type = 'kaiser_fast'
    - Duration = 5.0
    - NO trimming of silence (as training didn't use it)
    """
    try:
        # Load exactly like train_model.py
        # sr=None doesn't work well if we want consistency with model features, 
        # so we use 22050 which is the librosa default.
        audio, sr = librosa.load(file, res_type='kaiser_fast', duration=5.0)

        if audio is None or len(audio) == 0:
            raise ValueError("Audio file is empty or corrupted")

        # Basic padding if too short to avoid feature errors
        if len(audio) < 22050:
            audio = np.pad(audio, (0, 22050 - len(audio)))
        
        # Max limit 5s (22050 * 5 = 110250)
        audio = audio[:22050 * 5]

        # ──────────────────────────────────────────────────────────────
        # FEATURE EXTRACTION — MATCHING train_model.py EXACTLY
        # ──────────────────────────────────────────────────────────────
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


def predict(file, model, scaler):
    try:
        features = extract_features(file)
        features = features.reshape(1, -1)
        features = scaler.transform(features)
        
        # Binary Classification:
        # 0 = Real
        # 1 = Fake (Synthetic)
        prob_fake = model.predict_proba(features)[0][1]
        return float(prob_fake)
    except Exception as e:
        raise ValueError(str(e))