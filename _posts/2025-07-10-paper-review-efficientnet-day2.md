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

## 🧠 Day 2 – Architecture & Scaling Coefficients

### ✅ Focus

Today’s reading focused on **Section 3: EfficientNet Architecture** and the accompanying explanation of the **compound scaling method in practice**.  
The authors present how they derive the baseline EfficientNet-B0 using NAS and then extend it to larger models (B1–B7) using a simple yet effective scaling rule.

---

## ⚙️ EfficientNet-B0: The Baseline

EfficientNet-B0 serves as the **base architecture**, discovered via **Neural Architecture Search (NAS)** using **MobileNetV2 blocks** as a search space.

Key design principles:

- Uses **MBConv** (Mobile Inverted Bottleneck Conv) with **SE (Squeeze-and-Excitation)**  
- Favors **smaller kernel sizes** (mostly 3x3 and 5x5)  
- Employs **swish activation** instead of ReLU  

The NAS objective balances **accuracy, latency, and parameter count**, producing a model that is both lightweight and performant.

> 📎 EfficientNet-B0: ~5.3M params, 0.39B FLOPs, 77.1% Top-1 accuracy (ImageNet)

---

## 📏 Compound Scaling Method (Expanded)

After establishing B0, the authors apply **compound scaling** to systematically generate larger models (B1–B7).  
Rather than scaling depth, width, or resolution independently, they jointly scale all three using the following rule:

$$
\begin{aligned}
\text{depth} & = \alpha^\phi \\
\text{width} & = \beta^\phi \\
\text{resolution} & = \gamma^\phi
\end{aligned}
$$

- **ϕ**: user-specified scaling factor  
- **(α, β, γ)**: constants determined via grid search  
- Constraint: \( \alpha \cdot \beta^2 \cdot \gamma^2 \approx 2 \) (to maintain fixed FLOPs growth)

This results in a family of models that scale **uniformly and predictably**.

> 📌 Example: EfficientNet-B7 achieves 84.3% Top-1 accuracy with only 66M parameters — significantly outperforming prior models at the same scale.

---

## 📊 Performance Summary (Table & Figure 1 Insight)

The compound scaling strategy is validated across several datasets:

| Model          | Params | FLOPs | Top-1 Acc (ImageNet) |
|----------------|--------|-------|-----------------------|
| EfficientNet-B0 | 5.3M  | 0.39B | 77.1%                |
| EfficientNet-B4 | 19M   | 4.2B  | 83.0%                |
| EfficientNet-B7 | 66M   | 37B   | 84.3%                |

The models demonstrate **state-of-the-art accuracy** with **orders of magnitude fewer parameters and FLOPs**, showing the effectiveness of their method.

---

## 💬 Personal Reflection

What impressed me today was how the authors resisted the urge to overcomplicate the scaling strategy.  
The **principled, constraint-driven formulation** of α, β, γ was both elegant and empirically powerful.

Moreover, using **NAS to optimize for a balanced base model**, and then applying a deterministic scaling rule, avoids expensive retraining at each scale — a huge win in practical deployment scenarios.

---

## 🔜 What’s Next?

Tomorrow in **Day 3**, I’ll cover:

- Empirical results on transfer tasks (e.g., CIFAR-100, Flowers, COCO)  
- Ablation studies on compound scaling vs. traditional methods  
- Generalization across domains (vision tasks beyond classification)

> 📝 **Note**: This review is based on my independent reading and is written to aid personal understanding and reference.
