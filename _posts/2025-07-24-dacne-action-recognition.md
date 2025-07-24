---
title: "Daily Study Log 53"
date: 2025-07-23
layout: post
category: study_log
---

🧠 **Daily Study Log [2025-07-23]**  
Today's focus was on idea generation, competition modeling, paper review and practical implementation, along with team discussion and feedback sharing.  
A solid day of both solo and collaborative learning.

---

## 💡 Project Idea — *Trust or Trick? Detecting Suspicious Movie Reviews through Behavioral Signals*

Outlined a new NLP project designed to identify potentially deceptive or promotional movie reviews.  
The model focuses on mismatches between **star ratings and textual sentiment**, along with **reviewer metadata** to detect anomalies.

Key elements:
- Sentiment vs. star score inconsistency detection  
- Repetitive use of promotional keywords  
- Reviewer behavior analysis (e.g. single 5-star, no review history)  
- Clustering suspicious review bursts  
- Visualizations: heatmaps and review similarity graphs  
- Important considerations: privacy, fairness, false positives

---

## 📚 TOEIC Practice

Continued TOEIC study with a focus on consistency.  
Practiced grammar (e.g. part 5), phrasal verbs, and reading sections.  
Goal was to reinforce habits and maintain test readiness.

---

## 🏆 Competition — *Electricity Usage Forecasting* (DACON)

Tracked submission progress and improvements across multiple experiments:

| No. | Description                                | Details                                                             | SMAPE         |
|-----|--------------------------------------------|----------------------------------------------------------------------|---------------|
| 4   | RandomSearchCV tuning (XGBoost)            | Basic feature set, 3-fold CV                                        | 17.75976      |
| 5   | Hold-out validation + Feature Engineering  | Date-based split, temporal + building features + Voting ensemble    | 16.15700      |
| 6   | Optuna tuning + Ensemble                   | Individually tuned XGB/LGBM/GBR with Optuna, then ensembled         | **11.33852**  |

**Notes**:
- RandomSearchCV improved local performance but showed overfitting signs  
- Submission 5 introduced hold-out strategy and meaningful temporal features  
- Submission 6 used per-model Optuna tuning → major improvement on public board

**Next plans**:
- Try `StackingRegressor` instead of voting  
- Train models per building type (e.g. hospitals vs. offices)  
- Introduce lag and rolling features  
- Consider time-based weighting for recent samples

---

## 📄 Paper Review — *Unsupervised 3D Pose Estimation for Hierarchical Dance Video Recognition*

Completed the full reading of the paper and prepared for implementation.  
Key takeaways:
- Semi-supervised 3D pose estimation achieves ~47mm MPJPE on Human3.6M  
- Genre classification improved most when combining 3D pose and inferred motion  
- Future direction: motion synthesis, unsupervised pretraining

---

## 🧪 Practice — 국민체조 Pose Estimation

Tested 2D skeleton extraction from a YouTube video of 국민체조 (National Calisthenics).  
Extracted frames and processed them using pose estimation code.  
Uploaded the notebook: `2D_Pose_Feature_Builder.ipynb`  
This forms the foundation for further experiments in skeleton similarity and feedback systems.

---

## 🧠 Paper Study Group — Feedback & Discussion

- Shared the 국민체조 code implementation with the group; feedback was positive  
- Discussed practical applications of the code in motion feedback  
- Compared different papers on pose-based evaluation and matching metrics  
- Explored potential for extending to healthcare and user-facing feedback systems

---

## ✅ TL;DR

📍 **Idea**: Designed "Trust or Trick?" suspicious review detection project  
📍 **TOEIC**: Practiced grammar, reading, and reviewed idioms  
📍 **Competition**: Logged 3 key submissions; Optuna + ensemble was the strongest  
📍 **Paper**: Fully read HDVR paper and prepared to implement  
📍 **Practice**: Ran 국민체조 2D skeleton estimation  
📍 **Study Group**: Shared code and discussed paper-based extensions

---
