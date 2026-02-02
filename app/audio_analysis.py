import librosa
import numpy as np

def analyze_audio(audio_path):
    y, sr = librosa.load(audio_path, sr=None)

    flatness = float(np.mean(librosa.feature.spectral_flatness(y=y)))

    pitches, _ = librosa.piptrack(y=y, sr=sr)
    pitch_values = pitches[pitches > 0]
    pitch_variance = float(np.std(pitch_values)) if pitch_values.size > 0 else 0.0

    rms = librosa.feature.rms(y=y)[0]
    energy_variance = float(np.std(rms))

    intervals = librosa.effects.split(y, top_db=25)
    silence_ratio = 1 - (np.sum(intervals[:, 1] - intervals[:, 0]) / len(y))

    return {
        "flatness": flatness,
        "pitch_variance": pitch_variance,
        "energy_variance": energy_variance,
        "silence_ratio": float(silence_ratio)
    }
