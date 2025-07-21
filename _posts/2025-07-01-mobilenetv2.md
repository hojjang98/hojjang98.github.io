---
layout: post
title: "Paper Review: MobileNetV2 DAY 1"
date: 2025-07-01
categories: paper_review
mathjax: true
---


## 📌 Paper Info

- **Title**: *MobileNetV2: Inverted Residuals and Linear Bottlenecks*  
- **Authors**: Mark Sandler, Andrew Howard, Menglong Zhu, Andrey Zhmoginov, Liang-Chieh Chen  
- **Link**: [arXiv 1801.04381](https://arxiv.org/abs/1801.04381)  
- **Published**: 2018 (Google Research)  
- **Code**: Available in TensorFlow-Slim  

---

## 🎯 Why I Chose This Paper

This paper is a great starting point for anyone interested in efficient neural network architectures.  
It introduces a simple yet powerful design that has become a foundation for many mobile-friendly models.  
Since I’m building a habit of reviewing papers and implementing key ideas, this was a perfect entry point.

---

## 🧠 Day 1 Review – Overview & Motivation

### ✅ Abstract Summary
MobileNetV2 proposes a new lightweight CNN architecture optimized for mobile and resource-constrained environments.  
It introduces **Inverted Residuals** and **Linear Bottlenecks** to reduce computation while preserving expressiveness.  
It performs well on classification, object detection (SSDLite), and segmentation tasks with a favorable trade-off between accuracy and efficiency.

### ✅ Introduction Takeaways
- Modern deep networks perform well, but are too heavy for mobile inference.
- MobileNetV2 solves this by expanding low-dimensional inputs → filtering with depthwise convolution → projecting linearly to low dimensions.
- This avoids large intermediate tensors, which reduces memory usage during inference.

### ✅ Problem Statement
Modern CNNs achieve high accuracy but are unsuitable for mobile deployment due to computational and memory demands.  
This paper addresses that challenge by introducing a module that preserves performance while dramatically reducing resource consumption.  
The core idea is to use lightweight depthwise convolutions and avoid non-linearities in narrow layers, which reduces memory footprint.

---

## 🗂 GitHub Repository

You can find my detailed review and notes here:  
🔗 [github.com/hojjang98/Paper-Review](https://github.com/hojjang98/Paper-Review/blob/main/vision/01_mobilenetv2/summary.md)

---

## 💭 Reflections

This was my first formal paper review and it was a very insightful experience.  
I learned that understanding the “motivation” behind a design is as important as understanding the design itself.  
Looking forward to digging deeper into the architecture and experiments in the next phase.

---

