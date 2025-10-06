---
layout: post  
title: "Paper Review: Vision Transformer – DAY 4"  
date: 2025-10-06
categories: paper_review  
---

> 📚 [https://arxiv.org/abs/2010.11929](https://arxiv.org/abs/2010.11929)  
> 🏆 Published in **ICLR 2021**  

# 📄 Vision Transformer (ViT) – Day 4

## ✨ Key Contributions
- Summarized ViT’s **scalability**, **simplicity**, and **global receptive field** as core strengths.  
- Identified **data and compute dependency** as key limitations.  
- Established that **Transformer scaling laws** from NLP generalize successfully to vision.  

---

## 🎯 Problem Definition
- While ViT achieves strong performance at scale, its **high data and compute requirements** restrict usability.  
- The key question: How can we retain ViT’s performance without requiring massive datasets or expensive hardware?

---

## 🧠 Discussion
1. **Strengths**
   - **Scalability**: Model accuracy increases consistently with dataset and model size.  
   - **Simplicity**: Relies purely on a Transformer encoder, no convolution or handcrafted inductive bias.  
   - **Global Context Modeling**: Self-attention enables full-image dependency modeling, beyond CNN locality.  

2. **Limitations**
   - **Data Hunger**: Performs poorly when trained on small datasets like ImageNet from scratch.  
   - **Compute Cost**: Requires large-scale pre-training (e.g., JFT-300M) and high-resolution inputs.  

3. **Conclusion**
   - ViT proves that **pure Transformers** can surpass CNNs when trained at sufficient scale.  
   - However, its dependency on large data makes it less practical for low-resource applications.  

---

## 🚫 Limitations
- Still lacks **data efficiency** and **inductive biases** that aid smaller-scale learning.  
- High computational demand limits accessibility to large research labs.  

---

## 🔭 Future Ideas
- Investigate **data-efficient pretraining** (distillation, semi-supervised learning).  
- Explore **hybrid CNN-Transformer models** for better small-data performance.  
- Develop **lightweight attention mechanisms** to lower quadratic cost.  

---

## 🔁 Personal Reflections
- ViT redefines the paradigm: **“Scale over structure.”**  
- The simplicity of its architecture contrasts sharply with its massive training demands.  
- Its success bridges NLP and CV, proving the **universality of Transformer scaling laws**.  
