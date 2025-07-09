---
layout: post
title: "Paper Review: EfficientNet DAY 1 – Abstract, Introduction & Motivation"
date: 2025-07-09
categories: paper_review
---

## 📌 Paper Info

- **Title**: *EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks*  
- **Authors**: Mingxing Tan, Quoc V. Le  
- **Link**: [arXiv 1905.11946](https://arxiv.org/abs/1905.11946)  
- **Published**: ICML 2019 (Google AI)  
- **Code**: Available in TensorFlow, PyTorch (via `timm` library)  

---

## 🧠 Day 1 – Abstract, Introduction & Motivation

### ✅ Focus

Today’s goal was to understand the **big picture behind EfficientNet**,  
with a close read of the **Abstract**, **Introduction**, and **Motivation** sections.  
This part sets the stage for the technical deep-dive coming up next.

---

## 📄 Abstract Summary

Convolutional Neural Networks (ConvNets) are often developed under **fixed resource constraints**,  
which leads to **inefficiencies** when scaling models.

**EfficientNet** builds on **MobileNet and ResNet** families and introduces a **compound scaling** method  
that scales depth, width, and resolution **in a balanced manner**.

Key takeaways from the abstract:

- Achieves **better accuracy and efficiency** than prior ConvNets  
- On **ImageNet**, EfficientNet-B7 hits **84.3% Top-1 accuracy** while being **8.4× smaller** and **6.1× faster**  
- Shows strong results on other datasets like **CIFAR-100** as well

---

## 🏗️ Introduction Breakdown

Traditional scaling strategies usually modify **only one aspect** of a model:

- Increase **depth** → e.g., ResNet-18 → ResNet-200  
- Widen **channels**  
- Increase **input resolution**

These approaches often require heavy **manual tuning** and result in **sub-optimal** accuracy or efficiency.

EfficientNet challenges this by asking:

> "Can we find a more principled, theoretically grounded way to scale ConvNets efficiently?"

Their answer is **compound scaling** — scaling **all three dimensions together** using fixed coefficients  
that were found through **grid search** on a base model.

The scaling equation looks like:

$$
\text{depth} \propto \alpha^\phi,\quad 
\text{width} \propto \beta^\phi,\quad 
\text{resolution} \propto \gamma^\phi
$$

Where φ is the user-controlled scaling factor, and (α, β, γ) are constants.

---

## 🚀 Motivation – Why Compound Scaling?

Most prior models scale **only one dimension** at a time,  
which often leads to **imbalanced models** and poor compute-to-accuracy trade-offs.

EfficientNet argues that:

- **Larger input resolutions** require **deeper** and **wider** networks to fully utilize the information  
- Simply scaling each axis arbitrarily can lead to **inefficient computation**  
- A **balanced scaling rule** is more effective — and surprisingly underexplored

In **Figure 1** of the paper, EfficientNet models achieve **higher accuracy with fewer parameters**  
compared to much larger networks. This highlights the effectiveness of their approach.

---

## 💬 Personal Reflection

It was refreshing to see a paper that focuses not just on raw accuracy,  
but on the **efficiency–accuracy trade-off** from a design perspective.

I liked that the **motivation was simple**:  
> “How do we scale a ConvNet *intelligently*?”

The result is not just a performant model — it’s a **scalable framework**.

---

## 🔜 What’s Next?

In **Day 2**, I’ll explore:

- How EfficientNet-B0 was built using NAS  
- What the base architecture looks like  
- How compound scaling generates B1 to B7 variants  
- Performance benchmarks on various datasets  

Stay tuned.

> 📌 **Note**: This review is based on my own reading and summary. Some sections were refined for clarity.
