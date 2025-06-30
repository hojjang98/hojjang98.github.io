---
layout: post
title: "Daily Study Log 16"
date: 2025-05-13
category: study_log
---

Today I focused on improving the food image classifier I started yesterday.  
The first model was like a sleepy turtle 🐢 — cute but very, very slow (and kind of blind).  
Time to wake it up with some fine-tuning magic and proper evaluation.

---

## 🔧 What I Did Today

- Enabled fine-tuning for the top 100 layers of `ResNet50`
- Adjusted the `ImageDataGenerator` to be less aggressive (because maybe the model couldn’t handle spicy augmentations 🌶️)
- Added `ReduceLROnPlateau` to dynamically lower learning rate
- Introduced `EarlyStopping` to avoid wasting time when the model gets lazy
- Extended training to 50 epochs (with early exit)
- Added proper evaluation: `confusion_matrix`, `classification_report`, and `accuracy_score`

---

## 📉 Results & Observations

- Accuracy was still around **14%** — ouch  
- Confusion matrix revealed prediction bias: the model kept guessing the same few classes
- Class distribution in `y_pred` showed heavy imbalance — not a good sign
- Turns out: I was training on **CPU** the entire time 😭  
  (1 epoch ≈ 90 seconds. Now it makes sense.)

---

## 💾 Takeaway & Action Plan

Despite the low score, I learned a lot today:  
- Fine-tuning needs time (and power)
- Evaluation tells a bigger story than accuracy alone
- And most importantly: **don’t forget to check if you’re using your GPU**

Tomorrow?  
**GPU setup. No excuses.**  
It’s time to make this model sprint, not crawl.

---

## 🧠 Reflection

This project is starting to feel real.  
I’m tuning layers, inspecting predictions, fixing data flow —  
and slowly turning this from a hobby into a discipline.

Today wasn’t a big win. But it was a *true* step forward.  
And that’s more than enough.

