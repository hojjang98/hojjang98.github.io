---
layout: post
title: "Paper Review: EfficientNet DAY 3 – Deep Dive into B0 Architecture & Scaling Coefficients"
date: 2025-07-11
categories: paper_review
---

## 📌 Paper Info

- **Title**: *EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks*  
- **Authors**: Mingxing Tan, Quoc V. Le  
- **Link**: [arXiv 1905.11946](https://arxiv.org/abs/1905.11946)  
- **Published**: ICML 2019 (Google AI)

---

## 🧠 Day 3 – Deep Dive into EfficientNet-B0 Architecture & Scaling Coefficients

Today’s study focused on understanding how the **EfficientNet-B0 baseline** is constructed via NAS, and how the **compound scaling coefficients (α, β, γ)** are derived and applied in practice.

---

## ⚙️ EfficientNet-B0: NAS-Based Baseline

EfficientNet-B0 is designed using **Neural Architecture Search (NAS)** with the same search space as **MnasNet**, but targeting a larger FLOPs budget (400M).  
The architecture balances **accuracy and efficiency** using a multi-objective function:

$$
\text{Objective} = \text{ACC}(M) \cdot \left( \frac{\text{FLOPs}(M)}{T} \right)^w
$$

- \( T = 400M \): FLOPs target  
- \( w = -0.07 \): trade-off factor between accuracy and cost  

### 🔧 Core Components:
- **MBConv blocks** (Mobile Inverted Bottlenecks)  
- **Squeeze-and-Excitation (SE)** modules for channel-wise attention  
- Expansion ratio:
  - **MBConv1** (expansion=1) used in early layers
  - **MBConv6** (expansion=6) used in later layers  
- **Skip connections** only when stride = 1 and input/output shapes match  

---

## 🧮 Compound Scaling Revisited

After defining B0, the paper introduces **compound scaling**, where model dimensions grow in a coordinated manner:

$$
\text{depth} \propto \alpha^{\phi}, \quad \text{width} \propto \beta^{\phi}, \quad \text{resolution} \propto \gamma^{\phi}
$$

- \( \phi \): user-defined scaling coefficient  
- \( \alpha = 1.2 \), \( \beta = 1.1 \), \( \gamma = 1.15 \) (found via grid search)  
- Subject to the constraint:

$$
\alpha \cdot \beta^2 \cdot \gamma^2 \approx 2
$$

This ensures FLOPs double with each unit increase in \( \phi \), making the scaling predictable and efficient.

---

## 💡 Why Find Coefficients on a Small Model?

- Searching for optimal (α, β, γ) on large models is expensive  
- EfficientNet finds them on **B0**, then applies them to B1~B7  
- This **reduces search cost** while keeping scaling behavior consistent

---

## 🔍 Key Insights

- EfficientNet-B0 is not manually designed, but NAS-optimized under computational constraints  
- MBConv blocks with SE units provide expressive yet efficient computation  
- The compound scaling method provides a **unified, constraint-aware** way to scale networks  
- FLOPs increase roughly as \( 2^{\phi} \), while keeping architecture balanced

---

## 💬 Personal Reflection

The use of a **small, well-designed base model (B0)** and then **applying uniform scaling** using simple coefficients is both **elegant and practical**.  
Instead of engineering each model version, EfficientNet grows predictably in all dimensions, delivering **SOTA accuracy with fewer resources**.

> 🔖 This post is part of an ongoing paper review series for deeper learning and long-term retention!
