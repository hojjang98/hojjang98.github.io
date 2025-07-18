---
layout: post
title: "Daily Study Log 15"
date: 2025-05-12
category: study_log
---

Today I completed training my first image classification model.  
It’s based on ResNet50 and built to recognize food images.  
Was it perfect? Nah. Was it mine? Hell yes. 😎

---

## 🔧 What I Did Today

- Connected a pre-trained `ResNet50` as a feature extractor  
- Added custom `GlobalAveragePooling` + `Dense` layers on top  
- Froze the base model (no fine-tuning yet)  
- Used `categorical_crossentropy` for loss and `Adam` for optimization  
- Trained the model for 10 epochs with `ImageDataGenerator`  
- Watched accuracy crawl up slowly like a lazy snail 🐌

---

## 📈 Results & Evaluation

- Plotted `accuracy` and `loss` graphs — they’re moving in the right direction (thankfully)
- Built a confusion matrix — most classes were okay, but `paprika` and `pomegranate` confused the heck out of the model
- Visualized sample predictions — some hits, some misses, but it’s working!

---

## 💾 Model Saved!

```python
model.save('models/food_classifier_resnet50.h5')
```

That file now holds all my effort, frustration, and "why is my accuracy still 0.1" moments.

---

## 🧠 Reflection

I finally feel like I’m *understanding* how these pieces fit together:  
generators, model layers, predictions, evaluation.  
It’s not just running code anymore — I get it now.  
And honestly? That feels better than any accuracy score.

Tomorrow? Maybe fine-tuning.  
Today? We celebrate 🥳
