---
layout: post  
title: "Paper Review: Vision Transformer – DAY 1"  
date: 2025-09-23
categories: paper_review  
---

> 📚 [https://arxiv.org/abs/2010.11929](https://arxiv.org/abs/2010.11929)  
> 🏆 Published in **ICLR 2021**  

# 📄 Vision Transformer (ViT) – Day 1

## ✨ Key Contributions
- Proposed the **first pure Transformer architecture** for large-scale image recognition.  
- Demonstrated that Transformers, when trained on **very large datasets**, can **match or outperform CNNs**.  
- Showed that **scaling laws** from NLP also apply in vision tasks.  

## 🎯 Problem Definition
- CNNs have dominated vision tasks but rely heavily on **inductive biases** (locality, translation equivariance).  
- Scaling CNNs further provides **diminishing returns**.  
- Question: Can a **convolution-free architecture** (Transformer) handle vision tasks effectively if trained on enough data?  

## 🧠 Method / Architecture
- Represent images as a **sequence of patches** (e.g., 16×16 pixels).  
- Flatten each patch and project it into embeddings.  
- Feed the sequence into a **Transformer encoder**, similar to NLP.  
- Add a special **[CLS] token** for classification.  
- Use **positional embeddings** to retain spatial information.  

## 🧪 Experiments & Results
- Initial experiments show that ViT needs **large-scale pretraining** (e.g., JFT-300M) to perform competitively.  
- With sufficient data, ViT achieves **state-of-the-art performance** on benchmarks like ImageNet.  

## 🚫 Limitations
- Requires **huge datasets** and **significant compute resources** for training.  
- Underperforms CNNs when trained only on smaller datasets without pretraining.  

## 🔭 Future Ideas
- Explore **data-efficient training** methods for ViT.  
- Combine **CNN inductive biases** with Transformers (e.g., hybrid models).  
- Extend to broader CV tasks: detection, segmentation, video understanding.  

## 🔁 Personal Reflections
- Fascinating to see how a **convolution-free approach** can rival CNNs.  
- Reinforces the importance of **scaling** in deep learning.  
- ViT feels like a **turning point** where vision starts catching up with NLP in architectural unification.  
