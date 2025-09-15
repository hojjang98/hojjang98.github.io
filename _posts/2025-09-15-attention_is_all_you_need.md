---
layout: post  
title: "Paper Review: Attention Is All You Need – DAY 5"  
date: 2025-09-12
categories: paper_review  
mathjax: true  
---

> 📚 [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)  
> 🏆 Published in **NeurIPS 2017**

## ✅ Day 5 – Training & Results  

---

### 📌 Optimizer & Learning Rate Schedule  
- The authors used **Adam optimizer** with slightly unusual settings (tuned to make training stable).  
- Instead of fixing the learning rate, they used a **warmup strategy**:  
  - At first, the learning rate gradually increases (so the model doesn’t “shock” itself with big updates).  
  - After a certain point, it slowly decreases, letting the model fine-tune without overshooting.  
- This schedule made training more reliable and efficient.  

---

### 📌 Regularization  
- **Dropout (0.1)**: randomly ignores some parts of the network during training → prevents overfitting.  
- **Label smoothing (0.1)**: instead of teaching the model that the “correct” answer is 100% right and others 0%, it softens the labels a bit.  
  - This encourages the model to stay flexible and not become overconfident.  
  - As a result, it generalizes better to unseen data.  

---

### 📌 Training Details  
- **Batch size**: trained on very large groups of tokens (25,000 at once), which speeds up learning.  
- **Hardware**: used 8 powerful NVIDIA P100 GPUs.  
- **Time**: surprisingly fast — only about 12 hours to reach top performance.  
- **Model sizes**:  
  - **Base model**: ~65 million parameters  
  - **Big model**: ~213 million parameters, with wider and deeper layers  

---

### 📌 Results – Translation Benchmarks  
- **English → German** (WMT 2014): achieved **28.4 BLEU**, about **+2.0 better** than the best previous system.  
- **English → French** (WMT 2014): achieved **41.8 BLEU**, setting a new single-model state of the art.  
- These results showed the Transformer could outperform RNNs and CNNs not just in speed, but also in quality.  

---

### 📌 Additional Experiments  
- The Transformer also worked well on **English constituency parsing**, a task very different from translation.  
- This proved the model’s versatility: it’s not limited to one domain.  

---

### 📌 Key Takeaways (Day 5)  
1. Smart training schedule (warmup + gradual decay) stabilized learning.  
2. Dropout and label smoothing prevented overfitting and boosted generalization.  
3. Training was efficient — **world-class results in just 12 hours**.  
4. The Transformer demonstrated it could be a **scalable, general-purpose architecture**, not just for translation.  

---

### 🧠 Final Thoughts (Day 5)  
Day 5 tied everything together: the paper not only introduced a new architecture, but also showed how **careful training strategies** and **regularization tricks** made it both efficient and powerful. It’s clear why the Transformer quickly became the foundation for today’s NLP (and beyond).  
