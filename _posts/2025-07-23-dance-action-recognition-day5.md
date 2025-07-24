---

layout: post  
title: "Paper Review: Unsupervised 3D Pose Estimation for Hierarchical Dance Video Recognition – DAY 5"  
date: 2025-07-23  
categories: paper_review  
mathjax: true  

---

## ✅ Day 5 – From Paper to Practice: My First Experiment

After reviewing the HDVR (Hierarchical Dance Video Recognition) paper in depth,  
I wanted to start building a simplified version of the pipeline using **real pose data and my own code**.

The original paper relies on 3D lifting and motion segmentation, but I decided to begin with the **2D keypoint side**: extracting features like joint distances, angles, and velocities from pose sequences and visualizing motion.

---

## 🛠️ What I Built – `2D_Pose_Feature_Builder.ipynb`

### 🎯 Purpose

- Reproduce the **lower half of the HDVR pipeline**, focused on body part movement from pose sequences.
- Lay groundwork for temporal modeling (LSTM/TCN) using only pose-derived features.

### 📂 Functionality

- Input: `.json` or `.csv` file of 2D pose keypoints (from MediaPipe or OpenPose)
- For each frame:
  - Compute joint-to-joint **distances** (e.g., wrist to elbow)
  - Calculate joint **angles** (e.g., elbow angle from shoulder–elbow–wrist)
  - Optionally compute **velocity** over time (joint displacement)
- Visualize:
  - Skeleton overlay by frame
  - Feature value sequences (time-series)

---

## 💡 Why This Matters

This experiment helped me:

- Understand **which joints are stable vs. noisy**
- See that even **simple handcrafted features** (distances, angles) encode a lot of motion semantics
- Identify where future smoothing or filtering would help
- Confirm that **pose-only pipelines** are viable for lightweight modeling

> It was also important to validate that a full 3D lifting module isn't strictly necessary for building a useful system, especially in constrained or real-time environments.

---

## 📊 My Model Setup (So Far)

No learning model yet – this was a **feature engineering stage** only.  
But these outputs will soon be fed into a temporal model like:

- LSTM / GRU for frame-level genre classification  
- TCN for learning local body part movement patterns  
- Possibly Transformer-based encoder for attention over joint importance

---

## 🔭 Next Steps (aka Day 6 Plan)

- Integrate **pose segmentation**: split long videos into movement segments  
- Build a **sequence classifier** for genre (e.g., hip-hop vs. waacking)  
- Try movement encoding from multiple dancers simultaneously  
- Optionally explore **3D lifting** with mock or learned constraints

---

## 📝 Reflection

Implementing this part manually gave me a better grasp of why the HDVR paper's hierarchical structure makes sense.  
Rather than depending on raw pixel data or supervised 3D annotation, I can now construct **explainable, modular pipelines** based entirely on pose motion.

This also sets the foundation for a **real-time dance feedback system**, or downstream applications in fitness, rehab, or choreography assistance.

---
