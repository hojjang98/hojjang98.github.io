---

layout: post  
title: "Paper Review: Unsupervised 3D Pose Estimation for Hierarchical Dance Video Recognition DAY 2"  
date: 2025-07-18  
categories: paper_review  

---

## 📌 Paper Info

* **Title**: *Unsupervised 3D Pose Estimation for Hierarchical Dance Video Recognition*  
* **Authors**: Xiaodan Hu, Narendra Ahuja  
* **Link**: [https://arxiv.org/abs/2109.09166](https://arxiv.org/abs/2109.09166)  
* **Published**: ICCV 2021 – University of Illinois Urbana-Champaign  
* **Code**: *Not available*

---

## 🧠 Day 2 Review — Computational Approach (Section 2)

### ✅ Step 1: 2D Pose Estimation & Tracking

Each frame \( I(t) \) is processed to estimate 2D poses \( \hat{p}^i(t) \) using OpenPose.  
Bounding boxes \( B^i(t) = (x, y, w, l) \) are used to track each dancer using the LDES tracker, maintaining per-person histograms and motion info.

---

### ✅ Step 2: Overlap Handling via Motion & Histogram

When tracking fails (e.g., due to occlusion), the algorithm detects overlap by checking directional changes in movement.  
It then predicts where the overlap will end, and re-assigns the correct dancer by comparing appearance histograms in the predicted frame.

---

### ✅ Step 3: 2D Pose Selection After Overlap

After overlap ends, multiple poses might be present in the bounding box.  
The pose most similar to the previous frame’s histogram is selected to maintain temporal consistency.

---

## ✅ Key Insights (3-Line Summary)

* The paper uses a robust 3-step tracking algorithm to handle occlusion between dancers.
* LDES tracker, motion prediction, and histogram matching ensure consistent identity tracking.
* OpenPose is used to estimate poses, but augmented with intelligent re-identification logic.

---

## 📘 New Terms

* **LDES Tracker**: A tracking method (cited as [16]) used to predict object positions across frames in low-dimensional appearance space.
* **Histogram Matching**: Comparing color distributions of bounding boxes across time to resolve identity conflicts.

---

## 🗂 GitHub Repository

Detailed markdown summary:  
🔗 [github.com/hojjang98/Paper-Review](https://github.com/hojjang98/Paper-Review)

---

## 💭 Reflections

This section gave a clear overview of how the authors handle the multi-dancer tracking problem, which is critical for dance recognition.  
The idea of using histogram-based re-identification after occlusion feels both lightweight and practical.  
I still want to understand the LDES tracker in more detail—will check citation [16] later for its internals.

---
