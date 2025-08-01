---
layout: post  
title: "Paper Review: Explainable Skeletal Assessment for Martial Arts – DAY 3"  
date: 2025-08-01  
categories: paper_review  
mathjax: true  
---

> 📚 [https://doi.org/10.1038/s41598-024-83475-4](https://doi.org/10.1038/s41598-024-83475-4)

## ✅ Day 3 – Alignment, Ensemble, and SHAP: Inside the Core Mechanism

Today I focused on the **core algorithmic design** of the proposed framework — how it turns raw joint angles into explainable scores using alignment, ensemble regression, and SHAP-based interpretation.

---

## 🧠 What I Learned – From Feature to Final Score

### 🔧 Skeleton Feature Extraction

- MediaPipe provides 33 3D joint coordinates.  
- From these, 18 angles are computed across limbs and trunk.  
- Angle calculation formula:

$$
A_i = \arccos \left( \frac{\vec{v_1} \cdot \vec{v_2}}{|\vec{v_1}||\vec{v_2}|} \right) \cdot \frac{180}{\pi}
$$

→ This captures detailed movement articulation, including elbow bends, knee twists, torso rotation, etc.

---

### 📐 Feature Alignment

- **Procrustes Analysis** for spatial normalization (scale, rotation, translation)  
- **Dynamic Time Warping (DTW)** aligns temporal sequences to a 32-frame reference  
- Combined, they **remove rhythm and execution bias**, ensuring fair comparisons

---

### 🧠 Regression Models + Adaptive Ensemble

- 7 regressors: Linear, Lasso, SVM, KNN, DT, RF, Bagging  
- **Adaptive weighting** assigns more weight to models with lower RMSE:

$$
w_i' = \left( e^{|\text{RMSE}_i - \text{RMSE}_{\max}|} \right)^k, \quad w_i = \frac{w_i'}{\sum_j w_j'}
$$

$$
\hat{y}_{\text{final}} = \sum_i w_i \cdot \hat{y}_i
$$

→ Ensemble behaves like a human judging panel, where better performers influence more.

---

### 💡 Explainability with SHAP

- SHAP values dissect the final score into **feature-level contributions**
- **Global SHAP**: which angles matter most across all data  
- **Local SHAP**: why this specific motion got its score  
- Feedback becomes **joint-aware**, not just numerical

---

## 🔍 Insight Snapshot

> “Spatial/temporal alignment + explainable ensemble = evaluation system that’s both accurate *and* usable.”

- The **alignment phase** is not just preprocessing — it **makes regression meaningful**  
- Even simple models (like KNN, DT) become competitive with good features  
- SHAP allows **transparent, joint-level feedback**, like a virtual coach

---

## 🛠️ What I’ll Build Next

- Implement DTW-aligned angle extraction using sample dance or fitness videos  
- Create ensemble regressors with adaptive RMSE weighting  
- Add SHAP visualizations per joint/frame  
- Build Streamlit UI for real-time scoring + feedback

---

## 🔭 Day 4 Preview

- Deep dive into experimental results:  
  - Ablation: aligned vs. unaligned  
  - Scoring vs. human expert scores  
  - SHAP global/local visualization case studies  
- See whether this pipeline *actually generalizes* across datasets

---

## 📝 Reflection

Today clarified how much **alignment and angle definition** impact downstream models.  
I also liked how explainability wasn't treated as an afterthought — it’s **built into the pipeline**.

I’m now seriously thinking about how to embed this structure into **dance feedback systems** or **rehab movement scoring**.  
Even without deep learning, this paper shows a lot can be achieved with **clear structure and interpretability**.

---
