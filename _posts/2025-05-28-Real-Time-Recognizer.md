# 📅 2025-05-28 – 🔁 Rebooting the Recognizer, Building CNNs from Scratch

Today, I made a conscious decision to **reset the Real-Time Daily Activity Recognizer project** entirely.  
I deleted all previous images, models, and experimental logs. I'm starting clean — from crawling data to training models.  
At the same time, I studied basic **CNN model architecture using Keras** and built my first one manually.

---

## 🧰 What I Did

- 🗑️ Cleared all existing image datasets and training logs  
- 📂 Reorganized folder structure: unified images under `/images/[class_name]`  
- 📸 Started crawling new image datasets (~3000/class planned)  
- 🧠 Reviewed `Sequential()` model setup in Keras  
- 🔧 Built a CNN from scratch using `Conv2D`, `MaxPooling2D`, `Flatten`, `Dense`  
- 💬 Added inline comments to improve code clarity (for GitHub documentation)  

---

## 📚 Personal Study Progress

- ✅ Revisited convolutional neural networks fundamentals  
- ✅ Learned layer-wise roles: Conv, Pooling, Flatten, Dense, Softmax  
- ✅ Practiced writing annotated CNN code in Python  
- ✅ Reorganized GitHub project directory for cleaner long-term structure  

---

## ✨ What I Learned

- 🔁 Sometimes a clean slate is better than tweaking endlessly  
- 🧠 Even basic CNNs can teach a lot when built from scratch  
- 📦 Structure and clarity in code = better reproducibility  
- 🛠️ It's okay to slow down if that means getting it right  

---

## 🧠 Reflections

> “Going back to square one isn’t failure. It’s the commitment to doing things better.”

---

## 🎯 Next Moves

- 🏗️ Finish crawling ~3000 images per class  
- 🧪 Begin experimenting with the new dataset  
- 📊 Set up real-time webcam input using OpenCV  
- 🎯 Goal: Achieve >70% validation accuracy on 8-class activity classification
