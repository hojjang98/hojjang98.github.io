---
layout: post  
title: "Paper Review: Explainable Skeletal Assessment for Martial Arts – DAY 1"  
date: 2025-07-24  
categories: paper_review  
mathjax: true  
---

> 📚 [https://doi.org/10.1038/s41598-024-83475-4](https://doi.org/10.1038/s41598-024-83475-4)

## ✅ Day 1 – Explainable Skeleton-Based Evaluation: From Reading to Application

Today I reviewed a paper that aligns perfectly with my long-term goal:  
building **interpretable movement evaluation systems** based on pose estimation.  
Unlike classification-only pipelines, this study dives into **scoring**, **alignment**, and **explanation** — all with a practical and reproducible approach.

---

## 🧠 What I Read – `Explainable Skeletal Assessment` (Scientific Reports, 2025)

### 🎯 Purpose

- Develop a motion evaluation framework that is:
  - **Quantitative** (scores performance),
  - **Aligned** (accounts for variation between performers),
  - **Explainable** (highlights which joints/motions influenced results).

### 📂 Key Components

1. **Input**: Skeleton sequences from both reference (expert) and target (trainee) movements  
2. **Alignment**:
   - Spatial: **Procrustes Analysis**  
   - Temporal: **Dynamic Time Warping (DTW)**
3. **Modeling**:
   - Decision Tree, Logistic Regression, LSTM used to predict skill level or score
4. **Explanation**:
   - **SHAP** values visualize which joints contributed most to final predictions

---

## 💡 Why This Matters

This paper helped me:

- Understand how motion scoring can go beyond classification into **interpretable evaluation**
- Realize the value of **alignment methods** in making comparisons fairer
- See how combining **traditional ML models** and **SHAP** can yield intuitive, robust outputs
- Think about **how to make feedback actionable**, not just accurate

> The transition from black-box genre recognition to explainable scoring is essential for real-world use in sports, fitness, or dance.

---

## 📊 My Implementation Plan (So Far)

This paper will influence my next prototype module. Planned steps:

- Use 2D pose data (MediaPipe) instead of 3D  
- Apply Procrustes + DTW to align a reference pose and a trainee video  
- Score similarity via cosine + statistical features  
- Later add model-based scoring (e.g., shallow tree or regression model)  
- Integrate **SHAP** or heatmap-based visualization to show which joints "failed"

---

## 🔭 Next Steps (aka Day 2 Plan)

- Collect 2D pose data with more consistent structure  
- Reimplement Procrustes + DTW alignment in my notebook  
- Compare frame-level vs. sequence-level evaluation  
- Try multi-sample evaluation: one reference vs. many attempts  
- Visualize joint influence maps from SHAP or cosine error stats

---

## 📝 Reflection

This paper gives structure to my vague ideas about explainable dance evaluation.  
It doesn't try to "solve everything" with deep learning but instead shows how **simple techniques + smart alignment + explainability** can work together.  
A big takeaway: **use alignment not just for preprocessing but as part of the model logic**.  
Next, I’ll build a mini-pipeline using DTW-aligned 2D pose features and map frame-level scores back to visuals.

This could evolve into a feedback system for **dance, fitness coaching, or rehab scenarios** — just like I originally envisioned.

---
