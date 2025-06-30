---
layout: post
title: "Daily Study Log 28"
date: 2025-05-21
category: study_log
---

# 🧠 [2025-05-30] Revisiting CNN Fundamentals with CIFAR-10

Today, I didn’t have time to work on the Real-Time Activity Recognizer.  
So I focused solely on reinforcing my basic CNN knowledge using the CIFAR-10 dataset.

---

## 🧪 CIFAR-10 CNN Classifier (Book-based Practice)

As part of deepening my CNN fundamentals, I went back to basics using a guided book tutorial on CIFAR-10.

### ✅ What I Did

- Loaded CIFAR-10 via `keras.datasets`
- Converted labels with `to_categorical`
- Built a CNN with:
  - `Conv2D`, `MaxPooling2D`, `Flatten`, `Dense`, and `Dropout`
- Practiced with different layer settings and resolved:
  - Syntax mistakes (e.g., `input_shape=(...)`)
  - Typos like `y_trian` → `y_train`

### 🧠 Key Takeaways

- Practicing on simpler datasets like CIFAR-10 helps build layer-wise intuition
- Debugging small bugs enhances attention to detail and logic
- This practice serves as a solid foundation for more complex CV models

---

## 🎯 Next Steps

- ⏭️ Resume Real-Time Activity Recognizer training tomorrow
- 📊 Compare baseline CNN vs MobileNetV2 performance on same-class subsets
- 📁 Keep logs and commit updated notebook versions on GitHub

---

Small step today, but important.  
Deep learning foundations matter — and this was a good brush-up session.
