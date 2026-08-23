import csv, os, librosa, numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,confusion_matrix
from sklearn.model_selection import train_test_split
static_path = r"D:\project\web\D_daignosis\myapp\static\\"
def training():
    print("Training started")
    header = "chroma_stft spectral_centroid spectral_bandwidth rolloff zero_crossing_rate"
    for i in range(1,21):
        header = header + " mfcc" + str(i)
    header += " label"
    print(header)
    headers_list = header.split(" ")
    print(headers_list)
    print(len(headers_list))
    file = open(r"D:\project\web\D_daignosis\pddataser\new_features.csv", "w", newline='')
    with file:
        writer = csv.writer(file)
        writer.writerow(headers_list)
    labels_list= ['No PD', 'PD']
    for foldername in labels_list:
        print("Reading in ", foldername)
        for filename in os.listdir(r"D:\project\web\D_daignosis\pddataser\\" + foldername):
            print(filename)
            file_name = r"D:\project\web\D_daignosis\pddataser\\" + foldername + "\\" + filename
            aa = []
            signal, sr = librosa.load(file_name, mono=True)

            # feature extraction

            chroma_stft = librosa.feature.chroma_stft(y=signal, sr=sr)
            spec_centroid= librosa.feature.spectral_centroid(y=signal, sr=sr)
            spec_bandwidth = librosa.feature.spectral_bandwidth(y=signal, sr=sr)
            roll_off= librosa.feature.spectral_rolloff(y=signal, sr=sr)
            zero_crossing = librosa.feature.zero_crossing_rate(y=signal)
            mfcc = librosa.feature.mfcc(y=signal, sr=sr)

            # mean value calculation

            aa.append(np.mean(chroma_stft))
            aa.append(np.mean(spec_centroid))
            aa.append(np.mean(spec_bandwidth))
            aa.append(np.mean(roll_off))
            aa.append(np.mean(zero_crossing))

            for a in mfcc:
                aa.append(np.mean(a))
            aa.append(foldername)

            # writing extracted features to csv file

            file = open(r"D:\project\web\D_daignosis\pddataser\new_features.csv", "a", newline='')
            with file:
                writer = csv.writer(file)
                writer.writerow(aa)

    return "Training completed!"

training()