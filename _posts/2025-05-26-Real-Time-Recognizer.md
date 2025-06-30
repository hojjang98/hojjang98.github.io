---
layout: post
title: "Daily Study Log 24"
date: 2025-05-21
category: study_log
---

# 📅 2025-05-26 – 🧹 Cleaning Up the Dataset & 🧠 Retraining MobileNetV2

Today I finally tamed my messy dataset and got a cleaner training loop running.  
Merged data, deleted junk, retrained the model. It felt... productive 😌

---

## 🧰 What I Did

- 🖼️ Crawled ~1000 images per class using Selenium & Google Images
- 🗂️ Merged `images/` and `images2/` into one big `merged/` folder
- 🔁 Renamed duplicate filenames automatically
- 🧹 Cleaned corrupt/unreadable `.jpg` files using a PIL script
- ✂️ Split everything into `train/` and `val/` (80/20)
- 🔧 Retrained MobileNetV2 with an upgraded classifier and fine-tuning

---

## 🚫 Corrupt Image Filtering

```python
def clean_corrupt_images(root_dir):
    ...
```

- Removed `.jpg` files that caused `UnidentifiedImageError`
- Ran the cleaner on both `train/` and `val/` directories
- 🗑️ ~10–30 trash files deleted without mercy

---

## 🧠 Final Model Setup

- Base: `MobileNetV2(weights="imagenet", include_top=False)`
- Layers Unfrozen: Last **40**
- Classifier:
  - `GlobalAvgPooling2D`
  - `Dense(256, relu)`
  - `Dropout(0.3)`
  - `Dense(128, relu)`
  - `Softmax`
- Optimizer: `Adam(1e-4)`
- Callbacks: `EarlyStopping`, `ReduceLROnPlateau`, `ModelCheckpoint`

---

## 📊 Results (Take 2)

| Metric              | Value     |
|---------------------|-----------|
| ✅ Train Accuracy    | ~0.77xx   |
| ✅ Val Accuracy      | ~0.61xx   |
| 📉 Train Loss        | ~0.60xx   |
| 📉 Val Loss          | ~1.09xx   |

Nothing groundbreaking, but definitely **cleaner and more stable** than round one.

---

## ✨ What I Learned

- 🧼 Cleaning up your data *before* training really does pay off
- 🔁 Merging datasets is totally fine if filenames are managed
- 🧠 A deeper classifier helped boost expressiveness
- 🔓 Partial fine-tuning > no fine-tuning (in this case)

---

## 🎯 Next Moves

- 🔁 Try out `EfficientNet` or `ConvNeXt` backbones
- 🎨 Stronger data augmentation (color, brightness, blur?)
- 🎥 Real-time webcam inference with OpenCV
- 🚀 Validation accuracy goal: **60%+**, then chase the big **70%**

```
