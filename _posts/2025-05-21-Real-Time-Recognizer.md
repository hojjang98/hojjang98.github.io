---
layout: post
title: "Daily Study Log 22"
date: 2025-05-21
category: study_log
---

Today I took the next step in my daily activity recognition project:  
**Model training.**  
It was my first time training a real-time classifier using a pre-trained CNN backbone, and the results made me smile.

---

## 🔄 What I Did

- 📂 Split my crawled dataset into `train/` and `val/` folders (80/20)
- 🧪 Created a data generator pipeline with augmentation for training, and normalization for validation
- 🧠 Built a CNN using **MobileNetV2** as base + `GlobalAveragePooling + Dense + Softmax`
- ⚙️ Compiled the model with `Adam` optimizer, `categorical_crossentropy` loss, and `accuracy` as metric
- 📉 Used `EarlyStopping`, `ReduceLROnPlateau`, and `ModelCheckpoint` as callbacks
- 🚀 Trained the model for up to 30 epochs — with early stopping triggered
- 📊 Visualized training and validation accuracy/loss curves
- 🧾 Extracted best scores:  
  - **Train Accuracy**: 0.8512  
  - **Val Accuracy**: 0.5592  
  - (Previous The first-day's best was 0.17 😅)

---

## 💭 What I Learned

- 🏗️ **Transfer learning is powerful**: even with limited data, MobileNetV2 performed far better than expected
- 🎯 **Data augmentation** significantly improves generalization — especially horizontal flips and random zooms
- ⏸️ **EarlyStopping** is a life-saver: it prevents overfitting *and* saves time
- 📉 **Learning rate matters**: letting it adapt with `ReduceLROnPlateau` helps avoid dead ends

---

## 📌 If I Had More Time...

- Fine-tune the later layers of MobileNetV2
- Add `Dropout` to improve generalization
- Add `confusion_matrix` and `classification_report` to better understand misclassifications
- Explore `Grad-CAM` to visualize model attention
- Connect to OpenCV for **real-time webcam prediction**

---

## ✅ Final Metrics

- **Train Accuracy**: 0.8512  
- **Validation Accuracy**: 0.5592  
- **Best Model Saved To**: `best_model.h5`  
- Model: `MobileNetV2 (frozen)` + custom Dense  
- Epochs: Early stopped at 13 / 30

---

## 🌱 Final Reflection

This was more than a training run — it was a **checkpoint** in learning.  
I didn’t just train a model. I *understood every line I wrote*.

> “At 17% I was frustrated.  
> At 55%, I’m proud.  
> Not because it’s perfect — but because I built it right.”

Tomorrow, maybe it’s time to make it run in real time.

