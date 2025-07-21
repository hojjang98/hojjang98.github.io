---
layout: post
title: "Paper Review: EfficientNet DAY 0 – Why I Chose This Paper"
date: 2025-07-07
categories: paper_review
mathjax: true
---

## 📌 Paper Info

- **Title**: *EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks*  
- **Authors**: Mingxing Tan, Quoc V. Le  
- **Link**: [arXiv 1905.11946](https://arxiv.org/abs/1905.11946)  
- **Published**: ICML 2019 (Google AI)  
- **Code**: Available in TensorFlow, PyTorch (via `timm` library)  

---

## 🌱 Day 0 – Why EfficientNet?

### 🧩 Context

I recently finished reading the MobileNetV2 paper, which introduced the concept of **inverted residual blocks** and efficient model design for mobile devices. While reviewing it, I started wondering:

> "What’s the next step beyond MobileNetV2? How do modern lightweight models evolve from there?"

That curiosity naturally led me to **EfficientNet**, which not only **builds on MobileNetV2's architectural ideas**, but also introduces a **novel model scaling strategy** — something I hadn’t explored in depth yet.

---

### 🔍 Why I Chose This Paper

- ✅ It’s a **logical follow-up** to MobileNetV2  
- ✅ It introduces the idea of **compound scaling**, which feels both elegant and practical  
- ✅ It has had a **major impact** on model design in recent years (used in many modern libraries)  
- ✅ I wanted to understand how **NAS (Neural Architecture Search)** can be integrated with scaling strategies  

---

## 🔜 What's Next?

In **Day 1**, I’ll explore the **motivation behind EfficientNet**, what problem it's trying to solve, and how its compound scaling approach works.  
This will be followed by a breakdown of the architecture and performance benchmarks in Day 2 and beyond.

---

## 🧠 Personal Note

I’m not feeling well today, so I decided to keep things light and just share **why** I picked this paper instead of diving into technical content right away.  
Sometimes setting the stage properly helps make the reading experience more meaningful and focused.

> 📌 **Next up: EfficientNet DAY 1 – Abstract, Introduction, and Motivation**
