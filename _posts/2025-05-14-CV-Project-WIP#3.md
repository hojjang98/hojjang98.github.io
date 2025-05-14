---
layout: post
title: "🍙 Crawling into Results – Why Models Alone Won’t Save You"
date: 2025-05-13
---


Today, the food image classifier got its biggest meal yet: real data.  
After days of tuning layers and adjusting learning rates, I finally asked the real question:  
> “What if the model isn’t the problem?” 🤔

Turns out, it wasn’t.

---

## 🦾 What I Did Today

- Switched focus from model tuning to **data expansion**
- Built a Google Image crawler using Selenium
- Scraped and organized **36 classes worth of food images**
- Cleaned corrupted images & restructured the dataset
- Trained a fresh `MobileNetV2` on the newly built dataset

---

## 📈 Results

- Accuracy jumped from **~14% to 41%** 🚀
- Confusion matrix actually shows learning — not just guessing anymore
- Class balance still needs work, but now we’re at least in the game

---

## ❗ Takeaway: It’s Not Just the Model

Changing architectures is like swapping out shoes.  
But if you’re walking on broken ground (aka messy data), it doesn’t matter what you wear.  
> **Data quality and quantity** beat fancy layers. Every. Single. Time.

---

## 🧭 Next Steps

- Fine-tune MobileNetV2 now that the base is strong
- Try `EfficientNetB0` or `ConvNeXt` for a comparison
- Experiment with **Grad-CAM** to visualize attention
- Deploy a simple UI (maybe with Streamlit?) for demo

---

## 🧠 Reflection

This was the first time I collected and cleaned my own dataset.  
Watching the crawler “hunt” images and seeing them fill up folders in real-time was...  
kind of thrilling. 😅

It made me realize:  
Modeling is just the tip of the iceberg.  
Real work (and real growth) starts when you build your own data pipeline.

Today, I stopped tuning a broken violin.  
Instead, I learned to string it myself.

