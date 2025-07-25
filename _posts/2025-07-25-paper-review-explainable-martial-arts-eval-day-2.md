---
layout: post  
title: "Paper Review: Explainable Skeletal Assessment for Martial Arts – DAY 2"  
date: 2025-07-25  
categories: paper_review  
mathjax: true  
---

> 📚 [https://doi.org/10.1038/s41598-024-83475-4](https://doi.org/10.1038/s41598-024-83475-4)

## ✅ Day 2 – Literature & Method Review: Foundations Behind the Framework

Today’s reading focused on the **foundation** of the proposed scoring framework —  
including how previous motion analysis methods compare, and how this paper constructs a full pipeline from skeleton data to explainable output.

---

## 📚 What I Read – From Motion Capture to Alignment Logic

### 📌 Key Literature Threads

- **Motion Capture Types**:
  - *Wearable*: Infrared (lab-accurate), IMU (portable but sparse)
  - *Markerless*: RGB-D (e.g., Kinect), 2D/3D Pose Estimation (OpenPose, HRNet, BlazePose)

- **Evaluation Approaches**:
  1. **Rule-based**: Hard thresholds from experts (simple but not generalizable)  
  2. **Similarity metrics**: DTW, cosine, Euclidean (scoring but not interpretable)  
  3. **Model-based**: Regressors/classifiers for learning performance → higher accuracy, but often black-box

---

## ⚙️ Method Overview

### 🔹 Skeleton Feature Extraction  
- MediaPipe is used to extract 3D skeleton coordinates (33 joints)  
- 18 angles are computed from body parts (shoulder, elbow, hip, knee, torso)  
- Each angle is calculated as:

$$
A_i = \arccos \left( \frac{\vec{v_1} \cdot \vec{v_2}}{|\vec{v_1}||\vec{v_2}|} \right) \cdot \frac{180}{\pi}
$$

---

### 🔹 Feature Alignment  
- Uses **Dynamic Time Warping (DTW)** to align motions temporally  
- A 32-frame template is created from the top-performing sequence  
- All others are aligned to this reference → compensates for speed/rhythm differences

---

### 🔹 Regression & Ensemble  
- Base models: Linear, Lasso, SVM, KNN, Decision Tree, Random Forest, Bagging  
- Uses **adaptive weighting** → models with lower RMSE get higher weights  
- Final score = weighted average of all predictions

---

### 🔹 Explainability (SHAP)  
- Global SHAP: shows which features consistently influence scores  
- Local SHAP: explains why a specific motion got its score  
- Makes feedback **joint-specific and interpretable**

---

## 💡 Why This Matters

This section gave me insight into:

- Why *alignment* isn't just a preprocessing step — it’s the backbone of fair comparison  
- How classic models (DT, SVM) can be repurposed for scoring if aligned features are strong  
- The value of **temporal normalization** in movement analysis  
- How interpretability doesn’t require deep nets — just good features and clear scoring logic

> A solid skeleton feature design + fair alignment + transparent scoring = usable real-world evaluation system.

---

## 🛠️ What I’ll Implement Next

- Define 2D skeleton angles using MediaPipe keypoints  
- Build a 32-frame DTW-based alignment system  
- Train multiple regressors (e.g., Ridge, KNN, RF)  
- Weight model outputs by validation RMSE  
- Try SHAP (or cosine error maps) to highlight important joints

---

## 🔭 What’s Coming on Day 3

- Evaluate aligned vs. non-aligned features  
- Compare model-based vs. similarity-based scoring  
- Try visualizing SHAP impact over sequence heatmaps  
- See if scoring outperforms average human inter-rater agreement

---

## 📝 Reflection

Today’s section helped ground the project:  
alignment and angle feature design may actually **matter more than model choice**.  
Also, I realized that explainability doesn't have to wait until the end — it can shape how we choose and evaluate input features from the start.

The idea of using scoring models *not just for labels*, but for **feedback** is now clearer than ever.

---
