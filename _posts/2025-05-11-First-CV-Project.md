---
layout: post
title: "🍱 First Computer Vision Attempt – Fighting with TensorFlow"
date: 2025-05-11
---

Today I officially started my first computer vision project — a food image classifier.  
Sounds simple, right? Load some pictures, train a model, done.  
Yeah, no. I spent half the day just fighting with TensorFlow instead 😂

---

## 🛠️ Environment Setup (aka pain)

I thought I’d just “quickly test some code” but got hit with a combo of errors:

- `DLL load failed` (classic Windows + TensorFlow issue)
- `PIL.Image not found`
- `scipy not installed`
- Oh, and “Please restart your kernel”… about 17 times 🙃

It honestly felt like I was debugging my laptop more than writing code.  
But hey — I didn’t quit.

---

## ✅ What I Actually Got Done

- Set up a fresh conda environment and linked it to Jupyter
- Used `ImageDataGenerator` to load and preprocess food images
- Built a ResNet50-based model with transfer learning (no fine-tuning yet)
- Got `flow_from_directory()` working with 36 classes
- Didn’t throw my laptop out the window (barely)

---

## 📅 What’s Next?

- Actually train the model with `model.fit()`
- Plot accuracy/loss curves
- Save the model (`model.h5`)
- Try out predictions — maybe I’ll feed it my lunch and see what it thinks?

---

## 🧠 Reflection

No big results today — but I *did* get the pipeline running.  
And that’s a win in my book.

Sometimes progress just looks like installing packages, restarting kernels, and not giving up.  
Tomorrow, the model gets to do the learning. Today? That was all me.

