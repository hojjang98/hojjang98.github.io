# 📅 2025-05-27 – 🧠 Full Fine-Tuning & Realization: Maybe I Need More Data?

Today I ran the most complete version of my real-time daily activity recognizer yet.  
Used all the tricks—warmup, fine-tuning, dropout tuning, and light augmentation.  
It worked... okay. But it made me wonder: maybe the real bottleneck is data?

---

## 🧰 What I Did

- 🧠 Fully fine-tuned `MobileNetV2` after 3-epoch warm-up
- 🔓 Unfroze **all layers** and recompiled with low learning rate
- 🔁 Applied **light augmentation**: low rotation, zoom, horizontal flip
- ❌ Removed `class_weight` to avoid over-regularization
- 💧 Lowered `Dropout` to 0.1 to improve feature expressiveness
- 📉 Used `EarlyStopping`, `ReduceLROnPlateau`, `ModelCheckpoint`

---

## 🧪 Results (Take 3)

| Metric              | Value     |
|---------------------|-----------|
| ✅ Train Accuracy    | ~0.68xx   |
| ✅ Val Accuracy      | ~0.61xx   |
| 📉 Train Loss        | ~0.87xx   |
| 📉 Val Loss          | ~1.04xx   |

The model didn’t regress—but it didn’t improve either.  
It feels like I’m hitting a **glass ceiling** in performance.

---

## ✨ What I Learned

- 🔍 Lowering dropout helped recover some performance
- 📦 Removing `class_weight` led to slightly more stable validation
- 🧼 Light augmentation was better than aggressive transformation
- 🔓 Unfreezing all layers didn’t hurt—but didn’t boost much either

---

## 📚 Personal Study Progress

Today I also decided to start uploading **chapter-based DL study notebooks**  
to my GitHub as part of a new `dl-chapter-notebooks` collection.  
Theory + code, structured by concept, for long-term reference and review.

---

## 🧠 Questions in My Head

- 🤔 Is my current dataset (~1000 images/class) just **too limited**?
- 🏃 Some classes (e.g., brushing, washing face) are hard to distinguish visually
- 📈 Is 61% my current ceiling? Or can I still push past it with smarter tuning?

---

## 🎯 Next Moves

- 🧪 Try removing `BatchNormalization` layers as an experiment
- 🌀 Add CutMix or MixUp to simulate higher data diversity
- 🔍 Manually inspect failure cases with `confusion_matrix` or Grad-CAM
- 🚀 Final goal: Push **Val Accuracy > 70%**, then deploy with OpenCV

