import os
import csv
import numpy as np
import librosa
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import joblib

# ----------------------------
# TRAINING FUNCTION
# ----------------------------

def training():
    # dataset path (change as needed)
    dataset_path = r"D:\project\web\D_daignosis\pddataser"

    # header creation
    header = "chroma_stft spectral_centroid spectral_bandwidth rolloff zero_crossing_rate"
    for i in range(1, 21):
        header += f" mfcc{i}"
    header += " label"

    header_list = header.split(" ")
    print("✅ Header Columns:", len(header_list))

    # CSV file to save features
    csv_file = os.path.join(dataset_path, "new_features.csv")
    with open(csv_file, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header_list)

    # class labels (folders)
    labels = ['No PD', 'PD']

    features = []
    labels_list = []

    for label in labels:
        folder_path = os.path.join(dataset_path, label)
        for filename in os.listdir(folder_path):
            if filename.endswith(".wav"):
                file_path = os.path.join(folder_path, filename)
                print("🎵 Processing:", file_path)

                # Load audio
                signal, sr = librosa.load(file_path, mono=True)

                # Extract features
                chroma_stft = librosa.feature.chroma_stft(y=signal, sr=sr)
                spec_centroid = librosa.feature.spectral_centroid(y=signal, sr=sr)
                spec_bandwidth = librosa.feature.spectral_bandwidth(y=signal, sr=sr)
                rolloff = librosa.feature.spectral_rolloff(y=signal, sr=sr)
                zero_crossing = librosa.feature.zero_crossing_rate(y=signal)
                mfcc = librosa.feature.mfcc(y=signal, sr=sr)

                data = [
                    np.mean(chroma_stft),
                    np.mean(spec_centroid),
                    np.mean(spec_bandwidth),
                    np.mean(rolloff),
                    np.mean(zero_crossing)
                ]

                for coeff in mfcc:
                    data.append(np.mean(coeff))

                data.append(label)
                features.append(data[:-1])
                labels_list.append(label)

                # Write to CSV
                with open(csv_file, "a", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(data)

    # ----------------------------
    # TRAINING MODEL
    # ----------------------------
    print("\n🧠 Training model...")
    X_train, X_test, y_train, y_test = train_test_split(features, labels_list, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Accuracy
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print("✅ Training Completed!")
    print("🎯 Accuracy:", round(acc * 100, 2), "%")

    # Save Model
    joblib.dump(model, os.path.join(dataset_path, "pd_new_model.pkl"))
    print("💾 Model saved as pd_new_model.pkl")


# ----------------------------
# RUN TRAINING
# ----------------------------
if __name__ == "__main__":
    training()
