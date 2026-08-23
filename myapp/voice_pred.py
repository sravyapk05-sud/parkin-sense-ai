import numpy as np
import librosa
import joblib

# ----------------------------
# FUNCTION: Predict new audio
# ----------------------------
def predict_audio(file_path):
    # Load trained model
    model = joblib.load(r"C:\Users\isasu\Music\project\web\D_daignosis\pddataser\pd_new_model.pkl")

    # Load the audio file
    signal, sr = librosa.load(file_path, mono=True)

    # Extract features (same as training)
    chroma_stft = librosa.feature.chroma_stft(y=signal, sr=sr)
    spec_centroid = librosa.feature.spectral_centroid(y=signal, sr=sr)
    spec_bandwidth = librosa.feature.spectral_bandwidth(y=signal, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=signal, sr=sr)
    zero_crossing = librosa.feature.zero_crossing_rate(y=signal)
    mfcc = librosa.feature.mfcc(y=signal, sr=sr)

    # Store feature means
    features = [
        np.mean(chroma_stft),
        np.mean(spec_centroid),
        np.mean(spec_bandwidth),
        np.mean(rolloff),
        np.mean(zero_crossing)
    ]

    for coeff in mfcc:
        features.append(np.mean(coeff))

    # Convert to array and reshape for model input
    features = np.array(features).reshape(1, -1)

    # Predict class
    prediction = model.predict(features)[0]

    print("🔊 Predicted Label:", prediction)
    return prediction


# ----------------------------
# MAIN
# ----------------------------

# if __name__ == "__main__":
#     # enter your test audio path here
#     test_audio = r"D:\project\web\D_daignosis\pddataser\PD\VE1VSIPTIOZ46M240120171926.wav"
#     print("🎧 Testing Audio:", test_audio)
#     result = predict_audio(test_audio)
 #    print("✅ Final Prediction:", result)
