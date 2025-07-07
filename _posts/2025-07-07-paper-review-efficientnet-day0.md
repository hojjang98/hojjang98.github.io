---
layout: post
title: "Paper Review: EfficientNet DAY 1"
date: 2025-07-07
categories: paper_review
---

## 📌 Paper Info

- **Title**: *EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks*  
- **Authors**: Mingxing Tan, Quoc V. Le  
- **Link**: [arXiv 1905.11946](https://arxiv.org/abs/1905.11946)  
- **Published**: ICML 2019 (Google AI)  
- **Code**: Available in TensorFlow, PyTorch (via `timm` library)  

---

## 🧠 Day 1 Preview – Understanding the Big Picture

### ✅ Focus

Today’s goal was to get a conceptual overview of the EfficientNet paper — focusing on its motivation, main contribution, and high-level architecture strategy.

---

## 🏗️ Core Idea: Compound Scaling

Traditional model scaling often increases **only one dimension** (depth / width / resolution).  
EfficientNet proposes **compound scaling** — a principled way to scale **all three dimensions simultaneously** using fixed scaling coefficients.

This approach helps the model achieve better accuracy **without** drastically increasing computation.

---

## 🔍 Key Design Highlights

- **Base architecture**: EfficientNet-B0 built on **MobileNetV2** inverted residual blocks  
- **Search method**: Used **Neural Architecture Search (NAS)** to find the best base model  
- **Scaling**:  
  - Define constants: α (depth), β (width), γ (resolution)  
  - Apply:  
    \[
    \text{depth} \propto \alpha^\phi,\quad 
    \text{width} \propto \beta^\phi,\quad 
    \text{resolution} \propto \gamma^\phi
    \]  
    (for scaling coefficient φ)  

---

## 🧠 Initial Thoughts

- The compound scaling idea is intuitive yet surprisingly underexplored in older models  
- I like that the paper balances *accuracy* and *efficiency* with a clean design flow  
- The fact that EfficientNet outperforms larger models with fewer FLOPs is both elegant and practical  

---

## 🔜 Next Step

In the next review (DAY 2), I’ll dive deeper into:

- EfficientNet-B0 architecture layout  
- Scaling coefficients (α, β, γ) used in real cases  
- Performance comparisons across B0–B7 models  

---

## ✅ Summary

EfficientNet introduces a unified scaling framework that outperforms conventional CNN scaling methods.  
By combining NAS with compound scaling, it sets a new standard for accuracy-per-computation in deep learning.

> 📌 **Note**: Full architecture diagrams and implementation insights will be reviewed in the next session.
