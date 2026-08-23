# Parkin-sense-ai
A multimodal AI project for early detection of Parkinson's disease using voice and brain MRI data.

# ParkinSense AI

## Objective

The ParkinSense AI project aims to develop a multimodal machine learning framework for the early detection of Parkinson’s Disease using **voice recordings and brain MRI data**. The system analyzes speech signals to identify vocal abnormalities and processes brain MRI images to identify structural changes associated with Parkinson’s Disease.

The project uses **MFCC and spectrogram features** for voice analysis and **Convolutional Neural Networks (CNN)** for MRI analysis. The outputs from the voice and MRI models are combined using a **decision-level (late) fusion technique** to generate a final prediction indicating Parkinson’s Disease (PD) or Non-PD.

The objective is to provide an integrated and user-friendly system that can support early screening and provide diagnostic results using complementary information from voice and MRI data.

### Skills Learned

- Understanding of multimodal machine learning for healthcare applications.
- Voice signal preprocessing and feature extraction.
- MRI image preprocessing and analysis.
- MFCC and spectrogram-based voice feature extraction.
- Convolutional Neural Network (CNN) based image analysis.
- CNN-LSTM based voice model development.
- Decision-level (late) multimodal fusion.
- Model evaluation using accuracy, precision, recall, F1-score, and ROC-AUC.
- Development of an interactive system for uploading data and viewing predictions.

### Tools Used

- **Python** for machine learning and deep learning processing.
- **Flutter** for frontend development.
- **Dart** for application development.
- **HTML, CSS, JavaScript, and Bootstrap** for the interface.
- **MySQL** for database management.
- **PyCharm** for development.
- **Android Studio** for application development.

## Steps

Below are the key steps taken in the development of the ParkinSense AI system:

### 1. Data Acquisition and Preprocessing

The system uses two types of input data: **voice samples and brain MRI images**.

Voice samples are collected from datasets such as the UCI Parkinson’s dataset, while MRI images are obtained from publicly available datasets.

The voice data undergoes **noise removal, normalization, and segmentation**, while MRI images undergo **resizing, normalization, grayscale conversion, and contrast enhancement**.

*Ref 1: Data Acquisition and Preprocessing*  
This step prepares the voice and MRI data for feature extraction and model processing.



### 2. Voice Feature Extraction

The voice processing pipeline extracts acoustic features from the voice samples.

Features including **MFCC, spectrograms, jitter, shimmer, and Harmonics-to-Noise Ratio (HNR)** are used to capture characteristics of speech associated with Parkinson’s Disease.

*Ref 2: Voice Feature Extraction*  
This stage extracts meaningful acoustic information from the processed voice samples.



### 3. MRI Feature Extraction

The MRI processing pipeline analyzes brain MRI images using deep learning techniques.

Convolutional Neural Networks are used to extract meaningful features from MRI images and identify structural characteristics associated with Parkinson’s Disease.

*Ref 3: MRI Feature Extraction*  
The CNN-based MRI pipeline processes the images and extracts features for classification.



### 4. Model Training

Separate models are developed for the two modalities.

For voice analysis, a **CNN-LSTM hybrid model** is trained using MFCC and spectrogram features to detect speech abnormalities.

For MRI analysis, a **Convolutional Neural Network (CNN)** is used to classify MRI images as Parkinson’s Disease or healthy.

*Ref 4: Model Training*  
The individual voice and MRI models generate prediction probabilities for their respective modalities.



### 5. Multimodal Fusion

The prediction outputs from the voice and MRI models are combined using a **decision-level (late) fusion technique**.

The project uses a probabilistic fusion equation instead of simple averaging:

$$
P_{fused} =
\frac{P_{voice} \cdot P_{MRI}}
{(P_{voice} \cdot P_{MRI}) + (1-P_{voice})(1-P_{MRI})}
$$

where:

- `Pvoice` = probability from the voice model
- `PMRI` = probability from the MRI model

The final decision is obtained as:

```text
If Pfused ≥ 0.5 → Parkinson’s Disease (PD)

If Pfused < 0.5 → Non-PD
