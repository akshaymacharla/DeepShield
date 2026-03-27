import os
import numpy as np
import librosa
import joblib
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler

REAL_FOLDER = "dataset/real"
FAKE_FOLDER = "dataset/fake"

def extract_features(file):

    audio, sr = librosa.load(file, sr=None)

    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    mfcc_mean = np.mean(mfcc, axis=1)

    spectral = np.mean(librosa.feature.spectral_centroid(y=audio, sr=sr))
    zcr = np.mean(librosa.feature.zero_crossing_rate(audio))

    features = np.hstack([mfcc_mean, spectral, zcr])

    return features


X = []
y = []

print("Loading REAL voices...")

for file in os.listdir(REAL_FOLDER):

    if file.endswith(".wav"):

        path = os.path.join(REAL_FOLDER, file)

        try:
            X.append(extract_features(path))
            y.append(0)
            print("Processed real:", file)

        except:
            print("Skipped:", file)


print("Loading FAKE voices...")

for file in os.listdir(FAKE_FOLDER):

    if file.endswith(".wav"):

        path = os.path.join(FAKE_FOLDER, file)

        try:
            X.append(extract_features(path))
            y.append(1)
            print("Processed fake:", file)

        except:
            print("Skipped:", file)


X = np.array(X)
y = np.array(y)

print("Dataset shape:", X.shape)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.1
)

model.fit(X_scaled, y)

os.makedirs("models", exist_ok=True)

joblib.dump(
    {"model": model, "scaler": scaler},
    "models/model.pkl"
)

print("Training complete!")
print("Model saved to models/model.pkl")