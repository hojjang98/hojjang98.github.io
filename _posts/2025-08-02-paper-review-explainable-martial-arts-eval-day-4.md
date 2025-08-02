---
layout: post  
title: "Paper Review: Explainable Skeletal Assessment for Martial Arts – DAY 4"  
date: 2025-08-02  
categories: paper_review  
mathjax: true  
---

> 📚 [https://doi.org/10.1038/s41598-024-83475-4](https://doi.org/10.1038/s41598-024-83475-4)

## ✅ Day 4 – Experiments, Performance, and Interpretability in Practice

Today I explored how the proposed system performs across different datasets, how it compares with human experts, and how SHAP helps make the scoring explainable and educational.

---

## 📊 What I Learned – From Metrics to Meaning

### 🧪 Evaluation Metrics

- Used **MAE**, **RMSE**, **sMAPE**, **R²**, **Pearson correlation**, and **ICC**  
- LOOCV (Leave-One-Out Cross Validation) used due to small sample size  
- These metrics cover both accuracy and consistency with expert scores

---

### 🔬 Performance Across Models

- Feature alignment greatly improved performance across all models  
- The proposed **adaptive weighted ensemble** achieved the best scores  
- On XSQ and PBB datasets, model even outperformed human experts in MAE  
- TaiChi results still favored expert judges — possibly due to subtler motion nuance

---

### 👥 Comparison with Experts

| Dataset | MAE (Proposed) | MAE (Expert Avg) |
|---------|----------------|------------------|
| XSQ     | **0.237**      | 0.371–0.420       |
| PBB     | **0.261**      | 0.319–0.457       |
| TaiChi  | 0.290          | **0.130–0.270**   |

→ Indicates strong generalization in most styles, but expert intuition still matters in complex domains.

---

### 💡 SHAP in Action

- **Global SHAP**: Key angles in frames 13–17, 19–23, and 31 had the biggest influence  
- **Local SHAP**: Showed which joints in which frames led to deductions or boosts  
- Partial dependency plots revealed optimal angle ranges per joint  
- Feedback is **interpretable and coachable** — not just numerical

---

## 🔍 Insight Snapshot

> “The model doesn’t just score — it *teaches*.”

- Even basic regressors perform well with good features and alignment  
- SHAP transforms black-box regression into personalized feedback  
- Ensemble + alignment bridges statistical accuracy with human-level usability

---

## 🛠️ What I’ll Build Next

- Compare SHAP output with actual dance instructor annotations  
- Build a SHAP-driven feedback system to flag common joint issues  
- Expand pipeline to support multi-style templates (e.g., waacking vs. hip-hop)  
- Explore real-time scoring using simplified keypoint subsets

---

## 📝 Reflection

This part of the paper really convinced me that **alignment and explanation together** can make ML feedback systems actually useful — not just technically accurate.

It also gave me inspiration for using this approach in **rehabilitation** or **education**, where transparency matters more than raw accuracy.

---

