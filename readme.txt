# Deep Learning for Automated Glaucoma Detection

A Multi-Modal Biomarker Fusion Approach

## 📌 Overview

Glaucoma is a leading cause of irreversible blindness worldwide. Early detection is critical, but traditional single-modality methods often fail to capture the full disease picture.
This project proposes a multi-modal deep learning system that integrates structural and functional biomarkers to improve glaucoma detection accuracy.

## 🚀 Features

* Extraction of Cup-to-Disc Ratio (CDR) using CNNs from fundus images
* 3D CNN-based analysis of Retinal Nerve Fiber Layer (RNFL) thickness from OCT scans
* ResNet50 + Feature Pyramid Network (FPN) for Peripapillary Atrophy (PPA) segmentation
* LSTM-based RNN for visual field progression tracking
* Meta-learning fusion model with attention mechanism to integrate biomarkers
* Achieved 92.3% accuracy, outperforming single-modality models

## 🧑‍💻 Methodology

1. Dataset: GRAPE dataset with fundus images, OCT scans, and visual field test results
2. Preprocessing: Cleaning, imputation, normalization of imaging and clinical data
3. Biomarker Extraction:

   * CNN → Cup-to-Disc Ratio (CDR)
   * 3D CNN → RNFL Thickness
   * ResNet50 + FPN → PPA Segmentation
   * LSTM (RNN) → Progression Rate
4. Fusion Model: Meta-learning framework with attention for final classification

## 📊 Results

* Accuracy: 92.3%
* Sensitivity: 91.7%
* Specificity: 93.1%
* Outperforms single-biomarker models and demonstrates potential for early glaucoma screening


## 🖼️ System Architecture

![System Architecture](diagrams/system_architecture.png)

## 📌 Conclusion

This project demonstrates that integrating multiple structural and functional biomarkers using deep learning can significantly improve glaucoma detection. The system supports ophthalmologists with objective, automated assessments, enabling earlier diagnosis and better patient outcomes.

## 🔗 References

* Huang et al., GRAPE Dataset (2023)
* Li et al., CNN-based Glaucoma Detection (2018)
* Medeiros et al., Multi-modal AI for Glaucoma (2019)

