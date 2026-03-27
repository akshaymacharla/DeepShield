import os
import librosa
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

# --- 1. Set dataset paths ---
base_dir = os.path.dirname(__file__)
REAL_PATH = os.path.join(base_dir, "dataset", "real")
FAKE_PATH = os.path.join(base_dir, "dataset", "fake")

# --- 2. Debug: check folders and files ---
print("REAL_PATH:", REAL_PATH)
print("FAKE_PATH:", FAKE_PATH)

real_files = os.listdir(REAL_PATH) if os.path.exists(REAL_PATH) else []
fake_files = os.listdir(FAKE_PATH) if os.path.exists(FAKE_PATH) else []

print("REAL FILES:", len(real_files))
print("FAKE FILES:", len(fake_files))

if len(real_files) == 0 or len(fake_files) == 0:
    raise ValueError("❌ No audio files found. Make sure dataset/real and dataset/fake have audio files.")

# --- 3. Feature extraction function ---
def extract_features(file):
    audio, sr = librosa.load(file, res_type='kaiser_fast', duration=5.0)

    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    mfcc_mean = np.mean(mfcc.T, axis=0)
    mfcc_std = np.std(mfcc.T, axis=0)

    chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
    chroma_mean = np.mean(chroma.T, axis=0)

    mel = librosa.feature.melspectrogram(y=audio, sr=sr)
    mel_mean = np.mean(mel.T, axis=0)

    zcr = np.mean(librosa.feature.zero_crossing_rate(y=audio))
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio, sr=sr))
    spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=audio, sr=sr))

    features = np.hstack((
        mfcc_mean, mfcc_std,
        chroma_mean, mel_mean,
        [zcr, spectral_centroid, spectral_rolloff]
    ))
    return features

# --- 4. Load dataset ---
X, y = [], []

for file in real_files:
    if file.endswith(('.wav', '.mp3', '.flac')):
        try:
            X.append(extract_features(os.path.join(REAL_PATH, file)))
            y.append(0)
        except Exception as e:
            print(f"Error processing {file}: {e}")

for file in fake_files:
    if file.endswith(('.wav', '.mp3', '.flac')):
        try:
            X.append(extract_features(os.path.join(FAKE_PATH, file)))
            y.append(1)
        except Exception as e:
            print(f"Error processing {file}: {e}")

X = np.array(X)
y = np.array(y)

print(f"Dataset loaded: {len(y)} samples | Real: {sum(y==0)} | Fake: {sum(y==1)}")

# --- 5. Scale and split ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# --- 6. Train model ---
model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.1,
    use_label_encoder=False,
    eval_metric='logloss'
)
model.fit(X_train, y_train)

acc = accuracy_score(y_test, model.predict(X_test))
print(f"✅ Accuracy: {acc*100:.1f}%")

# --- 7. Save model ---
os.makedirs(os.path.join(base_dir, "models"), exist_ok=True)
joblib.dump(model, os.path.join(base_dir, "models", "model.pkl"))
joblib.dump(scaler, os.path.join(base_dir, "models", "scaler.pkl"))
print("Model and Scaler saved successfully!")