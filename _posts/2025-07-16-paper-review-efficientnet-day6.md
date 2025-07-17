---
layout: post
title: "Paper Review: EfficientNet DAY 6 – My Experiments & What’s Next"
date: 2025-07-16
categories: paper_review
---

## 📌 Paper Info

- **Title**: *EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks*  
- **Authors**: Mingxing Tan, Quoc V. Le  
- **Link**: [arXiv 1905.11946](https://arxiv.org/abs/1905.11946)  
- **Published**: ICML 2019 (Google AI)

---

## ✅ Day 6 – My Reproduction Results

Today, I completed and summarized my reproduction experiments for EfficientNet's compound scaling strategy.  
By testing base, depth-only, width-only, and compound-scaled models on **CIFAR-10**, I was able to confirm that **compound scaling consistently delivers the highest validation accuracy and lowest loss** — even if the gap is small due to the dataset's simplicity.

---

## 📈 Summary of Experimental Results

| Model         | FLOPs (MMac) | Params (M) | Val Acc (Best) | Val Loss (Lowest) |
|---------------|--------------|------------|----------------|-------------------|
| Base (B0)     | 408.93       | 4.02       | 93.82%         | 0.2045            |
| Depth-only    | 533.91       | 4.02       | 93.85%         | **0.1951**        |
| Width-only    | 578.40       | 4.02       | 93.69%         | 0.1936            |
| Compound      | 838.07       | 4.02       | **93.98%**     | **0.1924**        |

> 📌 While differences were small, compound scaling still showed the best overall performance.  
> I expect the gap to widen on more complex datasets like **CIFAR-100** or **TinyImageNet**.

Visualizations and training logs are available in my [GitHub repo](https://github.com/hojjang98) under `Paper-Review/vision/02_efficientnet/`.

---

## 💡 Reflection & Insights

- Even simple datasets like CIFAR-10 allow meaningful comparison of scaling strategies.  
- Compound scaling becomes more valuable as **task complexity and image resolution** increase.  
- This reproduction helped me internalize the theoretical claims from the paper and practice model scaling in PyTorch.

---

## 🔭 What’s Next: Pose-Based Action Recognition

Starting today, I’m moving on to a new topic:  
**Pose-based Action Recognition**, especially for **dance genre classification** (e.g., hip-hop, waacking, etc.).

- I’ll be studying the paper:  
  **“Unsupervised 3D Pose Estimation for Hierarchical Dance Video Recognition” (Hu & Ahuja, 2021)**  
- [arXiv link](https://arxiv.org/abs/2109.09166) | [PDF](https://arxiv.org/pdf/2109.09166.pdf)
- The idea is to extract 2D keypoints via **OpenPose/BlazePose**, optionally lift them to 3D,  
  then classify pose sequences using **LSTM**.  
- It’s a clean, explainable pipeline and highly suitable for custom dance datasets (including videos I can record myself).

I believe this shift from *model scaling* to *skeleton-based temporal modeling* will give me practical insight into **human-centric vision**, especially for **motion and genre classification**.


---

## ✅ TL;DR

📍 Wrapped up my EfficientNet scaling experiments (base vs depth vs width vs compound)  
📍 Confirmed compound scaling performs best (even on CIFAR-10)  
📍 Ready to explore new tasks: Pose-based Action Recognition using keypoints  
📍 Next paper: *Action Recognition using Pose Estimation* (2019)

> Stay tuned for pose modeling, temporal sequence classification, and experiments with dance video data!
