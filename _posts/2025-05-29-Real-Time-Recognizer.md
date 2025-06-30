---
layout: post
title: "Daily Study Log 27"
date: 2025-05-21
category: study_log
---

# 🧠 [2025-05-29] Fine-Tuning the Real-Time Recognizer + CIFAR-10 CNN Practice

Today I focused on two key areas:

1. Continuing CNN architecture studies with CIFAR-10 as a baseline dataset  
2. Running **two major experiments** on the **Real-Time Daily Activity Recognizer**, which I had fully reset yesterday (2025/05/28)

---

## 🧪 1. CIFAR-10 CNN Classifier (Book-based Practice)

As part of my deep learning fundamentals, I replicated a CNN-based CIFAR-10 classifier following a book tutorial.

### ✅ What I Did

- Loaded CIFAR-10 via `keras.datasets`
- Preprocessed integer labels with `to_categorical`
- Constructed a simple CNN with:
  - `Conv2D`, `MaxPooling2D`, `Flatten`, `Dense`, and `Dropout`
- Identified and corrected common mistakes like:
  - `input_shape=(...)` syntax
  - Typos in label variables (`y_trian` vs `y_train`)

### 🧠 Key Takeaways

- Practicing basic architecture helped reinforce layer-wise understanding
- Debugging minor issues greatly improved my attention to syntax and logic
- This exercise provided a useful baseline for evaluating deeper models

---

## 🔁 2. Real-Time Activity Recognizer — Model Experiments

After resetting the project yesterday, I ran two structured experiments today aimed at improving validation performance and resolving class confusion (notably with `brushing_teeth`).

---

### 🧪 Experiment A – Fine-Tuning with Class Weighting

- **Backbone**: MobileNetV2 (last 20 layers unfrozen)  
- **Augmentation**: Moderate (rotation ±30°, channel/brightness shift, etc.)  
- **Regularization**: Dropout(0.5), `class_weight` applied for `walking`  
- **Training**: EarlyStopping + ReduceLROnPlateau  
- **Result**:  
  - **Best Val Acc**: `0.5370` at Epoch 9  
  - Fine-tuning gave a **+10% improvement** over frozen backbone  
  - Train/Val gap narrowed, training behavior more stable  
  - 📈  
    ![exp_a](https://github.com/hojjang98/CV-Projects/blob/main/real-time-daily-activity-recognizer/figures/20250529_experiment_a.png)

---

### 🧪 Experiment B – Addressing Class Confusion

- **Focus**: Reduce misclassifications to `brushing_teeth`  
- **Augmentation**: More aggressive (rotation ±45°, zoom 0.4, brightness 0.6–1.4, etc.)  
- **Same Backbone**: MobileNetV2, last 20 layers unfrozen  
- **Result**:  
  - Validation accuracy similar (`~0.54`) but with **healthier learning dynamics**  
  - Overfitting signs reduced, validation loss decreased steadily  
  - Misclassification pattern began to improve  
  - 📈  
    ![exp_b](https://github.com/hojjang98/CV-Projects/blob/main/real-time-daily-activity-recognizer/figures/20250529_experiment_b.png)

---

### 🧠 Overall Insights

> "Refining after a reset works — and clearer logs give better direction."

- Transfer learning with fine-tuning is significantly better than frozen models
- Class weighting and aggressive augmentation helped reduce class imbalance issues
- Focusing on class-specific misclassification (`brushing_teeth`) was a valuable strategy

---

## 🎯 Next Steps

- 📸 Complete image crawling (aiming for ~3000 images/class)
- 🤖 Try stronger backbones (EfficientNetB0, ResNet50, etc.)
- 🧪 Apply class-specific augmentation
- 🔍 Analyze updated confusion matrices

---

Even though I started fresh yesterday, today marked the **first meaningful progress** in the rebuilt pipeline.  
Performance is improving steadily — and I'm just getting started.
