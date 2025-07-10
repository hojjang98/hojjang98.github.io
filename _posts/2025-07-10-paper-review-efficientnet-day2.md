---
layout: post
title: "Paper Review: EfficientNet DAY 2 – Architecture & Compound Scaling in Practice"
date: 2025-07-10
categories: paper_review
---

## 📌 Paper Info

- **Title**: *EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks*  
- **Authors**: Mingxing Tan, Quoc V. Le  
- **Link**: [arXiv 1905.11946](https://arxiv.org/abs/1905.11946)  
- **Published**: ICML 2019 (Google AI)  
- **Code**: Available in TensorFlow, PyTorch (`timm` library)  

---

## 🧠 Day 2 – Architecture & Compound Scaling in Practice

### ✅ Focus

Today’s reading focused on **Section 3: EfficientNet Architecture** and the practical implementation of the **compound scaling method**.  
The paper outlines how the authors derive the baseline model EfficientNet-B0 using Neural Architecture Search (NAS), and then scale it up to EfficientNet-B1 through B7 using a simple, principled rule.

---

## ⚙️ EfficientNet-B0: The Baseline

EfficientNet-B0 is the **base model** discovered via NAS, with MobileNetV2-like blocks as the search space.

**Key architectural elements**:

- **MBConv (Mobile Inverted Bottleneck)** blocks with **Squeeze-and-Excitation (SE)** modules  
- Preference for **smaller kernels** (3×3 and 5×5)  
- **Swish activation** (instead of ReLU) for better performance  

The NAS process balances **accuracy, latency**, and **parameter count**, yielding a compact and efficient architecture.

> 📌 B0 Summary: ~5.3M params / 0.39B FLOPs / **77.1% Top-1** (ImageNet)

---

## 📏 Compound Scaling Method

Once B0 is established, the authors introduce a **compound scaling formula** to generate deeper and wider models in a balanced way:

$$
\text{depth} = \alpha^\phi,\quad
\text{width} = \beta^\phi,\quad
\text{resolution} = \gamma^\phi
$$


- **ϕ**: user-specified scaling factor  
- **(α, β, γ)**: constants derived via grid search  
- **Constraint**: \( \alpha \cdot \beta^2 \cdot \gamma^2 \approx 2 \) (to maintain constant FLOPs growth)

This leads to **uniform, predictable scaling**, resulting in the EfficientNet-B1 to B7 series.

> 📌 Example: EfficientNet-B7 achieves **84.3% Top-1** with just **66M params**, outperforming earlier large-scale models.

---

## 📊 Performance Highlights

Compound scaling consistently improves performance with fewer resources:

| Model           | Params | FLOPs | Top-1 Acc (ImageNet) |
|-----------------|--------|-------|-----------------------|
| EfficientNet-B0 | 5.3M   | 0.39B | 77.1%                |
| EfficientNet-B4 | 19M    | 4.2B  | 83.0%                |
| EfficientNet-B7 | 66M    | 37B   | 84.3%                |

This validates the method’s effectiveness: **state-of-the-art results with lower computational cost**.

---

## 💬 Personal Reflection

What stood out most today was the **elegance of the compound scaling approach**.  
Instead of treating depth, width, and resolution separately, the authors proposed a **single, constraint-based rule** — simple yet powerful.

Also, by using NAS once to generate a well-balanced base model (B0), they avoid retraining for each new scale. This makes EfficientNet extremely practical for real-world deployment.

---


> 📝 This summary reflects my personal understanding and is written as a reference log for deeper learning.
