---

layout: post  
title: "Paper Review: Unsupervised 3D Pose Estimation for Hierarchical Dance Video Recognition DAY 4"  
date: 2025-07-22  
categories: paper_review  
mathjax: true  

---

## 📌 Paper Info

* **Title**: *Unsupervised 3D Pose Estimation for Hierarchical Dance Video Recognition*  
* **Authors**: Xiaodan Hu, Narendra Ahuja  
* **Link**: [https://arxiv.org/abs/2109.09166](https://arxiv.org/abs/2109.09166)  
* **Published**: ICCV 2021 – University of Illinois Urbana-Champaign  

---

## 🧪 Day 4 Review — Experiments, Results, and Final Insights (Section 3 & 4)

This session covers the dataset setup, 3D pose estimation accuracy, motion recognition, genre classification, and final conclusions.  
The authors evaluate their method on the **UID** (University of Illinois Dance) and **AIST++** datasets, using metrics like **MPJPE** and **F-score**.

---

### 🔹 Dataset Overview

#### 📂 UID (University of Illinois Dance)

| Attribute | Value |
|----------|-------|
| Genres | 9 |
| Total Clips | 1,143 |
| Total Frames | 2,788,157 |
| Total Duration | 108,089s |
| Min / Max Clip Length | 4s / 824s |
| Min / Max Clips per Genre | 30 / 304 |

Includes both simple (tutorial) and complex (multi-dancer, noisy background) dance videos.

#### 📂 AIST++

- 1,408 multiview dance sequences  
- 10 genres, 0.4M frames used  
- Ground-truth 3D annotations and camera parameters available  
- Used for benchmarking MPJPE performance  

---

### 🔹 3D Pose Estimation Performance (MPJPE)

#### 📈 On AIST++ Dataset

| Method | Supervision | Extra Data | MPJPE ↓ |
|--------|-------------|------------|---------|
| Martinez [ICCV'17] | Supervised | – | 110.0 |
| Wandt [CVPR'19] | Supervised | – | 323.7 |
| Pavllo [CVPR'19] | Supervised | – | 77.6 |
| Pavllo (semi-sup.) | Semi | ✖ | 446.1 |
| **Ours (semi-sup.)** | Semi | ✖ | **73.7** |
| Zhou [ICCV'17] | Weakly | ✔ | 93.1 |
| Kocabas [CVPR'19] | Self-sup. | Multiview | 87.4 |
| **Ours (unsup.)** | Unsupervised | ✖ | 246.4 |

#### 📉 On Human3.6M Dataset

| Method | Supervision | Extra Data | MPJPE ↓ |
|--------|-------------|------------|---------|
| Pavllo [CVPR'19] | Supervised | – | **46.8** |
| Ours (semi-sup.) | Semi | ✖ | **47.3** |
| Martinez [ICCV'17] | Supervised | – | 87.3 |
| Zanfir [CVPR'18] | Supervised | – | 69.0 |
| Ours (unsup.) | Unsupervised | ✖ | 82.1 |

The semi-supervised version performs on par with fully supervised models, without using any 3D ground truth.

---

### 🔹 Body Part Motion Recognition (F-score)

| Body Part | 2D Pose | 3D Pose |
|-----------|---------|---------|
| Head | 0.93 | **0.97** |
| L Shoulder | **0.95** | 0.93 |
| R Arm | 0.89 | **0.94** |
| Torso | 0.91 | **0.93** |
| Hips | 0.81 | **1.00** |
| L Foot | 0.85 | **0.98** |

3D pose leads to improved movement recognition, especially for **hips and lower body**.

---

### 🔹 Genre Recognition Accuracy (F-score)

| Input | F-score |
|----------------------------|---------|
| 2D Pose | 0.44 |
| 3D Pose | 0.47 |
| Movements (2D) | 0.50 |
| Movements (3D) | 0.55 |
| 2D + Movements (2D) | 0.73 |
| **3D + Movements (3D)** | **0.86** |

Best performance is achieved when both 3D pose and movement features are fused.

---

## ✅ Key Takeaways

- The proposed framework achieves **state-of-the-art performance** in semi-supervised 3D pose estimation.
- Movement recognition benefits greatly from **3D inputs**, especially for complex body regions.
- Genre classification reaches its peak with a **hierarchical fusion of 3D poses and part-level motion features**.

---

## 🧩 Limitations & Future Work

- The current framework is not **fully unsupervised** — genre classification still requires labeled data.
- Performance drops when the subject is small in frame or occluded.
- Future plans include:
  - Jointly training a **fully unsupervised** pose-to-genre pipeline  
  - Using motion representation to **synthesize new dance videos**  
  - Validating outputs via **human expert evaluations**

---

## 💭 Reflections

This section showcases how careful modular design can unlock performance even under limited supervision.  
The authors make a compelling case for replacing raw appearance with **pose-level abstraction**, especially for dance-related tasks.  
I’d like to test the movement fusion strategy on my own multi-person dance data and see how well it generalizes with lighter LSTMs or even Transformers.

---
