---
layout: post
title: "📸 Real-World in Real-Time – Starting Daily Activity Recognition"
date: 2025-05-20
---

Today, I kicked off a brand-new computer vision project:  
**Real-Time Daily Activity Recognition** based on webcam input and CNNs.

It’s my first time working on a project that’s meant to react *live* to human actions — like brushing teeth, eating, or typing — and I’m already hooked on the challenge.

---

## 🚀 What I Did (Start of the Project)

- 🧠 Decided on the project scope: real-time activity classification from webcam images
- 🗂️ Selected 8 daily activities: `brushing_teeth`, `eating`, `drinking`, `typing`, `reading`, `sleeping`, `walking`, `washing_face`
- 🔍 Designed precise image search keywords like `"person reading book"` instead of `"reading"` to increase quality
- 📸 Crawled **400+ images per class** using Bing image search
- 🧼 Filtered corrupted or unopenable image files using `PIL.Image.verify`
- 📁 Saved the dataset locally under `images/` directory (to later split into `train/val`)
- ⚠️ Took care to avoid any copyright violation by *not redistributing* the dataset — it’s for learning only

---

## 💭 What I Learned

- Specific keywords like `"person brushing teeth"` yield **way better results** than vague ones like `"brushing"`  
- Real-world data is messy: you always need to clean up after crawling  
- Data labeling by folder name is super convenient when working with `ImageDataGenerator`

---

## 🌱 What’s Next

- 🔨 Split the dataset into `train/val` with proper ratio (80/20)
- 🧪 Build and train a CNN using `MobileNetV2` as a base
- 🎯 Evaluate initial performance and decide whether fine-tuning is needed
- 🖥️ Eventually: hook the trained model up to OpenCV for **real-time webcam inference**

---

## 🗓️ Reflection

It’s exciting to move beyond static classification and into something reactive.  
This project feels a bit more personal — it’s recognizing the kind of daily behaviors I actually do.

Tomorrow I’ll dive into model training.  
For now, the dataset is ready — and so am I.

> “You can’t train a model on data you haven’t gathered.  
>  Today was about *gathering*.”

