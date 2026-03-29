import os
import librosa
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

# --- 1. Set dataset paths ---
base_dir = os.path.dirname(__file__)
REAL_PATH = os.path.join(base_dir, "dataset", "real")
FAKE_PATH = os.path.join(base_dir, "dataset", "fake")

print("REAL_PATH:", REAL_PATH)
print("FAKE_PATH:", FAKE_PATH)

real_files = [f for f in os.listdir(REAL_PATH) if f.endswith(('.wav', '.mp3', '.flac'))] if os.path.exists(REAL_PATH) else []
fake_files = [f for f in os.listdir(FAKE_PATH) if f.endswith(('.wav', '.mp3', '.flac'))] if os.path.exists(FAKE_PATH) else []

print(f"REAL FILES: {len(real_files)}")
print(f"FAKE FILES: {len(fake_files)}")

if len(real_files) == 0 or len(fake_files) == 0:
    raise ValueError("❌ No audio files found. Make sure dataset/real and dataset/fake have audio files.")


# --- 2. Feature Extraction ---
def extract_features(file):
    try:
        audio, sr = librosa.load(file, sr=22050, duration=5.0)

        target_len = 22050 * 5
        if len(audio) < target_len:
            audio = np.pad(audio, (0, target_len - len(audio)))
        audio = audio[:target_len]

        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
        mfcc_mean = np.mean(mfcc.T, axis=0)
        mfcc_std  = np.std(mfcc.T,  axis=0)

        chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
        chroma_mean = np.mean(chroma.T, axis=0)

        mel = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=128)
        mel_mean = np.mean(mel.T, axis=0)

        zcr = np.mean(librosa.feature.zero_crossing_rate(y=audio))
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio, sr=sr))
        spectral_rolloff  = np.mean(librosa.feature.spectral_rolloff(y=audio, sr=sr))

        return np.hstack((
            mfcc_mean, mfcc_std, chroma_mean, mel_mean,
            [zcr, spectral_centroid, spectral_rolloff]
        ))
    except Exception as e:
        raise ValueError(f"Feature extraction failed for {file}: {e}")


# --- 3. Augment audio to expand tiny datasets ---
def augment_audio(audio, sr):
    """
    Generate multiple augmented variants of a single audio clip.
    Covers pitch shift, time stretch, noise injection, and gain scaling.
    Each variant produces a meaningfully different feature vector.
    """
    augmented = []

    # Original
    augmented.append(audio.copy())

    # Pitch shift up
    try:
        augmented.append(librosa.effects.pitch_shift(audio, sr=sr, n_steps=1.5))
    except Exception:
        pass

    # Pitch shift down
    try:
        augmented.append(librosa.effects.pitch_shift(audio, sr=sr, n_steps=-1.5))
    except Exception:
        pass

    # Time stretch faster
    try:
        stretched = librosa.effects.time_stretch(audio, rate=1.1)
        target_len = 22050 * 5
        if len(stretched) < target_len:
            stretched = np.pad(stretched, (0, target_len - len(stretched)))
        augmented.append(stretched[:target_len])
    except Exception:
        pass

    # Time stretch slower
    try:
        stretched = librosa.effects.time_stretch(audio, rate=0.9)
        target_len = 22050 * 5
        if len(stretched) < target_len:
            stretched = np.pad(stretched, (0, target_len - len(stretched)))
        augmented.append(stretched[:target_len])
    except Exception:
        pass

    # Add mild white noise
    noise = np.random.normal(0, 0.003, audio.shape)
    augmented.append(audio + noise)

    # Add stronger noise
    noise2 = np.random.normal(0, 0.008, audio.shape)
    augmented.append(audio + noise2)

    # Gain down
    augmented.append(audio * 0.7)

    # Gain up (clipped)
    augmented.append(np.clip(audio * 1.3, -1.0, 1.0))

    return augmented


def extract_features_from_audio(audio, sr):
    """Extract features directly from a numpy audio array."""
    target_len = 22050 * 5
    if len(audio) < target_len:
        audio = np.pad(audio, (0, target_len - len(audio)))
    audio = audio[:target_len]

    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    mfcc_mean = np.mean(mfcc.T, axis=0)
    mfcc_std  = np.std(mfcc.T,  axis=0)

    chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
    chroma_mean = np.mean(chroma.T, axis=0)

    mel = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=128)
    mel_mean = np.mean(mel.T, axis=0)

    zcr = np.mean(librosa.feature.zero_crossing_rate(y=audio))
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio, sr=sr))
    spectral_rolloff  = np.mean(librosa.feature.spectral_rolloff(y=audio, sr=sr))

    return np.hstack((
        mfcc_mean, mfcc_std, chroma_mean, mel_mean,
        [zcr, spectral_centroid, spectral_rolloff]
    ))


# --- 4. Load dataset with augmentation ---
X, y = [], []

print("\nLoading and augmenting REAL samples...")
for file in real_files:
    try:
        audio, sr = librosa.load(os.path.join(REAL_PATH, file), sr=22050, duration=5.0)
        for aug_audio in augment_audio(audio, sr):
            try:
                X.append(extract_features_from_audio(aug_audio, sr))
                y.append(0)
            except Exception as e:
                print(f"  Augmentation failed for {file}: {e}")
        print(f"  ✅ {file} → {len(augment_audio(audio, sr))} variants")
    except Exception as e:
        print(f"  ❌ Error loading {file}: {e}")

print("\nLoading and augmenting FAKE samples...")
for file in fake_files:
    try:
        audio, sr = librosa.load(os.path.join(FAKE_PATH, file), sr=22050, duration=5.0)
        for aug_audio in augment_audio(audio, sr):
            try:
                X.append(extract_features_from_audio(aug_audio, sr))
                y.append(1)
            except Exception as e:
                print(f"  Augmentation failed for {file}: {e}")
        print(f"  ✅ {file} → {len(augment_audio(audio, sr))} variants")
    except Exception as e:
        print(f"  ❌ Error loading {file}: {e}")

X = np.array(X)
y = np.array(y)

print(f"\n📊 Dataset after augmentation: {len(y)} samples | Real: {sum(y==0)} | Fake: {sum(y==1)}")

if len(y) < 4:
    raise ValueError("❌ Still too few samples after augmentation. Add more audio files to dataset/real and dataset/fake.")

# --- 5. Scale ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --- 6. Train — use cross-val if dataset is small, otherwise split ---
model = XGBClassifier(
    n_estimators=200,
    max_depth=4,          # shallower to avoid overfitting on small data
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    use_label_encoder=False,
    eval_metric='logloss',
    random_state=42
)

if len(y) >= 10:
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"\n✅ Accuracy on held-out set: {acc*100:.1f}%")
else:
    # Too few samples for a split — train on all, report train accuracy
    model.fit(X_scaled, y)
    acc = accuracy_score(y, model.predict(X_scaled))
    print(f"\n⚠ Dataset small — trained on all samples. Train accuracy: {acc*100:.1f}%")
    print("  → Add more audio files to dataset/real and dataset/fake for a reliable model.")

# --- 7. Save ---
os.makedirs(os.path.join(base_dir, "models"), exist_ok=True)
joblib.dump(model,  os.path.join(base_dir, "models", "model.pkl"))
joblib.dump(scaler, os.path.join(base_dir, "models", "scaler.pkl"))

# Save accuracy to meta.txt so Command Center can display it
with open(os.path.join(base_dir, "models", "meta.txt"), "w") as f:
    f.write(f"accuracy: {acc*100:.1f}%\n")
    f.write(f"samples: {len(y)}\n")
    f.write(f"real: {sum(y==0)}\n")
    f.write(f"fake: {sum(y==1)}\n")

print("\n✅ Model, scaler, and meta saved successfully!")
print(f"   Real variants: {sum(y==0)}  |  Fake variants: {sum(y==1)}")
print("\n💡 TIP: For best results, add 20+ real and 20+ fake audio files to your dataset folders.")