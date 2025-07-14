---
layout: post
title: "Paper Review: EfficientNet DAY 4 – Scaling Results & Cost-Effective Model Analysis"
date: 2025-07-14
categories: paper_review
---

## 📌 Paper Info

- **Title**: *EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks*  
- **Authors**: Mingxing Tan, Quoc V. Le  
- **Link**: [arXiv 1905.11946](https://arxiv.org/abs/1905.11946)  
- **Published**: ICML 2019 (Google AI)

---

## 📊 Day 4 – Scaling Results & Cost-Effective Model Analysis

Today’s session focused on **Section 4.3: Scaling Results**, which evaluates how the EfficientNet family (B0~B7) performs as the compound scaling coefficient \\( \phi \\) increases. The paper compares accuracy, parameter size, and computational cost (FLOPs), and provides practical guidance on selecting the right model for different resource settings.

---

## 🧮 Scaling Setup Recap

The compound scaling method is applied as follows:

$$
\text{depth} \propto \alpha^{\phi}, \quad \text{width} \propto \beta^{\phi}, \quad \text{resolution} \propto \gamma^{\phi}
$$

- Fixed coefficients: \\( \alpha = 1.2, \beta = 1.1, \gamma = 1.15 \\)  
- Constraint: \\( \alpha \cdot \beta^2 \cdot \gamma^2 \approx 2 \\)  
- These values were discovered via grid search on **B0**, then applied to generate B1~B7.

This approach allows a **balanced and predictable scaling** of model complexity.

---

## 📈 Table 2: Comparing EfficientNet-B0 to B7

Table 2 in the paper presents a clear trend:

| Model | Params | FLOPs | Top-1 Acc (%) |
|-------|--------|-------|----------------|
| B0    | 5.3M   | 0.39B | 77.1           |
| B3    | 12M    | 1.8B  | 81.6           |
| B7    | 66M    | 37B   | 84.3           |

### ✅ Key Observations:
- **Efficiency**: Compared to ResNet-50 or MobileNet, EfficientNet achieves **higher accuracy with fewer FLOPs and parameters**.
- **Diminishing Returns**: After B4, additional FLOPs result in **less significant gains** (e.g., B6 to B7 yields ~0.5% improvement despite major FLOPs increase).
- **Logarithmic Gain**: Accuracy improvement **slows down** as resources grow, roughly following a logarithmic trend.

---

## 🔍 Interpretation of Returns

**At what point do returns diminish?**  
> Performance gains start flattening notably around **B4 to B5**, where doubling FLOPs yields <1% improvement in accuracy.

This suggests that for many real-world applications, **mid-sized models (B2~B4)** offer the best **cost-performance trade-off**.

---

## 💡 Cost-Effective Choice

In my analysis, **EfficientNet-B3** stands out as the most cost-effective:
- Delivers over **81% Top-1 accuracy**
- Requires only **1.8B FLOPs**
- Outperforms ResNet-50 (16.7B FLOPs, 78.8% accuracy)

This makes it ideal for use cases where **high accuracy** is needed without massive computational resources.

---

## 💬 Personal Reflection

The compound scaling framework shows its strength here: with a **single set of scaling coefficients**, EfficientNet scales smoothly from edge-device models (B0/B1) to high-end configurations (B6/B7).  

By analyzing Table 2, I’ve gained a clearer understanding of **how to choose the right model depending on resource constraints**, and the point at which **adding more compute no longer justifies the cost**.

> 🔖 Stay tuned for Day 5, where I’ll dive into the **Ablation Study (Section 4.4)** and explore why compound scaling outperforms single-dimension scaling!
