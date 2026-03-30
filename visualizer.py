import librosa
import librosa.display
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import io
from PIL import Image

def plot_spectrogram(audio_path):
    """
    Create a spectrogram visualization matching model's sr=22050.
    """
    try:
        # Match training sr exactly
        y, sr = librosa.load(audio_path, sr=22050, res_type='kaiser_fast', duration=5.0)

        if y is None or len(y) == 0:
            raise ValueError("Unable to load audio file")

        fig, axes = plt.subplots(2, 1, figsize=(12, 10))
        fig.patch.set_facecolor('#0f0f2e')
        for ax in axes:
            ax.set_facecolor('#0f0f2e')
            ax.tick_params(colors='#94a3b8')
            for spine in ax.spines.values():
                spine.set_color('#1e293b')

        # Mel Spectrogram
        try:
            mel = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
            mel_db = librosa.power_to_db(mel, ref=np.max)
            img = librosa.display.specshow(
                mel_db, sr=sr, x_axis='time', y_axis='mel',
                ax=axes[0], cmap='magma'
            )
            axes[0].set_title("Mel Spectrogram", color='white', fontweight='bold')
            fig.colorbar(img, ax=axes[0], format='%+2.0f dB')
        except: pass

        # Waveform
        try:
            times = np.linspace(0, len(y) / sr, len(y))
            axes[1].plot(times, y, color='#06b6d4', linewidth=0.7)
            axes[1].set_title("Waveform (Amplitude)", color='white', fontweight='bold')
        except: pass

        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=120, bbox_inches='tight', facecolor='#0f0f2e')
        plt.close()
        buf.seek(0)
        return np.array(Image.open(buf))

    except Exception:
        plt.close('all')
        blank = np.zeros((600, 800, 3), dtype=np.uint8)
        blank[:, :] = [15, 15, 46]
        return blank# updated
