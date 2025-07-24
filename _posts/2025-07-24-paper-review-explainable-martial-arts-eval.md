# 📄 Explainable Quality Assessment of Effective Aligned Skeletal Representations for Martial Arts Movements by Multi-Machine Learning Decisions

> 📚 [https://doi.org/10.1038/s41598-024-83475-4](https://doi.org/10.1038/s41598-024-83475-4)

## ✨ Key Contributions

- Proposes an **explainable motion assessment framework** using skeletal alignment and machine learning.
- Combines **Procrustes Analysis** and **Dynamic Time Warping (DTW)** to spatially and temporally align movement sequences.
- Trains multiple ML models (Decision Tree, Logistic Regression, LSTM) to **quantify motion quality**.
- Applies **SHAP** to interpret model decisions and identify influential joints or motion features.

## 🎯 Problem Definition

- Traditional martial arts evaluation relies on **subjective human judgment**, leading to:
  - Inconsistencies in scoring,
  - Difficulty providing real-time feedback,
  - Lack of standardization across evaluators.
- The goal is to develop an **objective, reproducible, and interpretable** evaluation method based on skeletal movement data.

## 🧠 Method / Architecture

1. **Data Collection**  
   - Skeleton sequences from experts (reference) and trainees (evaluation target)

2. **Preprocessing & Alignment**  
   - Interpolation for missing joints  
   - Normalization of joint coordinates  
   - Spatial alignment via **Procrustes Analysis**  
   - Temporal alignment via **DTW**

3. **Modeling & Evaluation**  
   - Input: aligned skeleton features  
   - Models: Decision Tree, Logistic Regression, LSTM, etc.  
   - Output: motion quality score (classification or regression)

4. **Explainability**  
   - Use **SHAP values** to determine which joints contributed most to the final evaluation

## 🧪 Experiments & Results

- Multi-model ensemble improves performance over single model baselines
- Evaluation scores correlated well with expert human judgment
- SHAP visualizations confirmed **interpretability**, showing intuitive joint influences (e.g., key kicks or punches)

## 🚫 Limitations

- Relies on **high-quality pose estimation**; noise in joint detection can reduce alignment accuracy
- May not generalize well across **different martial arts styles** without retraining
- The alignment step adds computational cost and may hinder real-time use

## 🔭 Future Ideas

- Integrate with **real-time skeleton tracking** for instant feedback during training
- Extend to other domains like **dance**, **sports coaching**, or **rehabilitation**
- Explore **3D pose data** for richer motion representation and depth-aware evaluation

## 🔁 Personal Reflections

- This paper offers a **practical bridge** between pose estimation and interpretable movement assessment, aligning closely with my project goals.
- I appreciated the use of **multiple ML models** rather than a single black-box approach.
- The emphasis on explainability (via SHAP) makes this work **trustworthy** and suitable for real-world applications like **skill training systems** or **fitness apps**.
- Inspired me to implement a **lightweight version** using my own data and test explainability on simpler motions like kicks or punches.
