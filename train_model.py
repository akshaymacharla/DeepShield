import os
import librosa
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

# IMPORTANT: Utilizing unified preprocessing pipeline to guarantee consistency with live inference
from detector import extract_features

base_dir = os.path.dirname(__file__)
REAL_PATH = os.path.join(base_dir, "dataset", "real")
FAKE_PATH = os.path.join(base_dir, "dataset", "fake")

real_files = [f for f in os.listdir(REAL_PATH) if f.endswith(('.wav', '.mp3', '.flac'))] if os.path.exists(REAL_PATH) else []
fake_files = [f for f in os.listdir(FAKE_PATH) if f.endswith(('.wav', '.mp3', '.flac'))] if os.path.exists(FAKE_PATH) else []

if len(real_files) == 0 or len(fake_files) == 0:
    print("Warning: Missing files in dataset/real or dataset/fake")

def augment_audio(y, sr):
    """Augmentation logic before final 3s truncation."""
    augmented = [y.copy()]
    try: augmented.append(librosa.effects.pitch_shift(y, sr=sr, n_steps=1.5))
    except: pass
    try: augmented.append(librosa.effects.pitch_shift(y, sr=sr, n_steps=-1.5))
    except: pass
    try: augmented.append(librosa.effects.time_stretch(y, rate=1.1))
    except: pass
    try: augmented.append(librosa.effects.time_stretch(y, rate=0.9))
    except: pass
    
    augmented.append(y + np.random.normal(0, 0.003, y.shape))
    augmented.append(y + np.random.normal(0, 0.008, y.shape))
    augmented.append(y * 0.7)
    augmented.append(np.clip(y * 1.3, -1.0, 1.0))
    return augmented

def process_and_extract_for_training(file_path):
    """
    Simulates the exact same preprocessing path as detector.preprocess_audio
    but performs augmentation correctly before standardizing length.
    """
    y_raw, sr = librosa.load(file_path, sr=16000, mono=True)
    y_trimmed, _ = librosa.effects.trim(y_raw, top_db=30)
    if len(y_trimmed) > sr * 0.5:
        y_raw = y_trimmed
    
    y_raw = librosa.util.normalize(y_raw)
    feats_list = []
    
    for aug_y in augment_audio(y_raw, sr):
        # EXACT 3 SECONDS
        target_len = sr * 3
        if len(aug_y) > target_len:
            aug_y = aug_y[:target_len]
        else:
            aug_y = np.pad(aug_y, (0, target_len - len(aug_y)))
            
        feats = extract_features(aug_y, sr)
        feats_list.append(feats)
        
    return feats_list

X, y_labels = [], []

print("\nLoading REAL samples...")
for f in real_files:
    try:
        feats = process_and_extract_for_training(os.path.join(REAL_PATH, f))
        X.extend(feats)
        y_labels.extend([0]*len(feats))
    except Exception as e:
        print(f"Error processing {f}: {e}")

print("\nLoading FAKE samples...")
for f in fake_files:
    try:
        feats = process_and_extract_for_training(os.path.join(FAKE_PATH, f))
        X.extend(feats)
        y_labels.extend([1]*len(feats))
    except Exception as e:
        print(f"Error processing {f}: {e}")

X = np.array(X)
y_labels = np.array(y_labels)

if len(y_labels) < 4:
    print("Not enough data to train. Please add more audio to the dataset.")
else:
    print(f"\n📊 Total Dataset: {len(y_labels)} (Real: {sum(y_labels==0)} | Fake: {sum(y_labels==1)})")
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = XGBClassifier(
        n_estimators=200, max_depth=4, learning_rate=0.05,
        subsample=0.8, colsample_bytree=0.8, use_label_encoder=False,
        eval_metric='logloss', random_state=42
    )

    if len(y_labels) >= 10:
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y_labels, test_size=0.2, random_state=42, stratify=y_labels
        )
        model.fit(X_train, y_train)
        acc = accuracy_score(y_test, model.predict(X_test))
    else:
        model.fit(X_scaled, y_labels)
        acc = accuracy_score(y_labels, model.predict(X_scaled))

    os.makedirs(os.path.join(base_dir, "models"), exist_ok=True)
    joblib.dump(model,  os.path.join(base_dir, "models", "model.pkl"))
    joblib.dump(scaler, os.path.join(base_dir, "models", "scaler.pkl"))

    with open(os.path.join(base_dir, "models", "meta.txt"), "w") as f:
        f.write(f"accuracy: {acc*100:.1f}%\n")
        f.write(f"samples: {len(y_labels)}\n")
        f.write(f"real: {sum(y_labels==0)}\n")
        f.write(f"fake: {sum(y_labels==1)}\n")

    print(f"\n✅ Training Complete. Accuracy: {acc*100:.1f}% Model saved!")
