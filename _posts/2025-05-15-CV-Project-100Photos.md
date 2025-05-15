---
layout: post
title: "📷 Crawling More, Learning More – Accuracy Breaks 50%"
date: 2025-05-15
---

Today marked another big step forward for my food image classifier.  
After reaching ~41% accuracy yesterday with 36-class data I collected using Selenium,  
I decided to **push the dataset further** — aiming for 100+ images per class.

And the result?  
> **Accuracy has officially broken the 50% barrier – hitting 56%.** 💥  
That’s no longer random guessing — it’s learning.

---

## 🛠️ What I Did Today

- Performed a **second round of crawling** for underrepresented food categories
- Ensured **100+ images per class** across all 36 classes
- Removed duplicates and restructured the dataset folders
- Re-trained the same `MobileNetV2` model with the expanded dataset

---

## 📈 Results

- **Accuracy improved from 41% to 56%** 🚀
- This is the **first time the model passed 50% accuracy**
- Some classes like `sweet potato` and `watermelon` showed **recall over 0.6**
- Confusion matrix indicates **real learning**, not just guessing anymore
- Class imbalance still affects some predictions, but overall performance is far more robust

---

## 💡 Insight

> "Better data beats better models — every time."

No architectural changes were made.  
The only change was **more and better data**, and the result was a significant accuracy jump.  
It reminded me again that **data engineering is just as important as modeling**.

---

## 🎯 Next Steps

- Address class imbalance (e.g. `class_weight='balanced'`, oversampling)
- Try out new architectures like `EfficientNetB0` or `ConvNeXt`
- Visualize attention with `Grad-CAM` to understand model focus
- Build a quick demo app with Streamlit for sharing results

---

This phase taught me something critical:  
> You can't tune your way out of bad data.  
You have to **build a solid foundation first** — and that starts with the dataset.
