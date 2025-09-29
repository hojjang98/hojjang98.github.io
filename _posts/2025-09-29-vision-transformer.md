---
layout: post  
title: "Paper Review: Vision Transformer – DAY 3"  
date: 2025-09-29
categories: paper_review  
---

> 📚 [https://arxiv.org/abs/2010.11929](https://arxiv.org/abs/2010.11929)  
> 🏆 Published in **ICLR 2021**  

# 📄 Vision Transformer (ViT) – Day 3

## ✨ Key Contributions
- Demonstrated that ViT requires **large-scale pre-training** (e.g., JFT-300M) to be effective.  
- Showed ViT **outperforms ResNet baselines** when sufficient data is available.  
- Confirmed that **scaling laws** (larger models + more data = better performance) apply in vision as well as NLP.  
- Provided ablation studies on **patch size, depth, width, and regularization**, revealing their critical roles.  

---

## 🎯 Problem Definition
- CNNs benefit from strong inductive biases (locality, translation equivariance), giving them an advantage on smaller datasets.  
- ViT has fewer inductive biases and thus struggles without **massive data**.  
- The challenge: Can pre-training on large datasets + careful scaling make ViT outperform CNNs?  

---

## 🧪 Experiments & Results
1. **Pre-training**  
   - Conducted on **JFT-300M** (300M images, 18k classes).  
   - Optimization: Adam with weight decay, linear warm-up, cosine decay schedule.  
   - Regularization: dropout, stochastic depth.  

2. **Fine-tuning**  
   - Transfer learning applied to **ImageNet, CIFAR-100, VTAB**.  
   - Used **higher input resolutions** (e.g., 224×224 → 384×384) during fine-tuning for better accuracy.  

3. **Baseline Comparison**  
   - Compared with **ResNet CNNs**.  
   - ViT outperforms ResNets on **large datasets**, but ResNets remain stronger on **small datasets** due to inductive biases.  

4. **Scaling Studies**  
   - Tested ViT-Base, ViT-Large, and ViT-Huge.  
   - Performance improves consistently with **larger models and larger datasets**.  
   - Reinforces the universality of **scaling laws** in ML.  

5. **Ablation Studies**  
   - **Patch Size**: Smaller patches (16×16) → higher accuracy, larger patches (32×32) → faster but less accurate.  
   - **Depth & Width**: Increasing layers and hidden size improves performance.  
   - **Regularization**: Strong regularization improves data efficiency and stabilizes training.  

---

## 🚫 Limitations
- Requires **massive computational resources** for pre-training (JFT-300M not widely accessible).  
- Performance on small datasets without pre-training remains weak compared to CNNs.  
- Quadratic complexity of self-attention still poses scalability issues.  

---

## 🔭 Future Ideas
- Explore **data-efficient training** methods (e.g., distillation, semi-supervised learning).  
- Investigate **efficient attention mechanisms** to reduce quadratic cost.  
- Apply ViT to **tasks beyond classification**, such as detection or segmentation.  

---

## 🔁 Personal Reflections
- ViT proves that **scale can replace inductive bias**—but at the cost of accessibility.  
- Interesting how the **same scaling laws in NLP** apply almost identically to CV.  
- Ablation studies highlight that **patch size** is not a trivial hyperparameter—it fundamentally shapes model performance.  
