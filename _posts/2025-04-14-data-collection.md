---
layout: post
title: "Step 1 – Finding a Good Dataset Ain’t Easy"
date: 2025-04-14
---

Okay, so today I started digging for data.

I thought it’d be simple — go to some public data site, download a clean CSV with sales numbers, and boom: ready for EDA.

Turns out, nope.  
Most “open” datasets are just business listings or metadata.  
Like... I don’t need a list of coffee shops. I need to know **how much coffee they sold**.

I was about to give up, but then — jackpot.  
I found this beautiful file from the Seoul Open Data platform with *estimated* monthly sales by business type.  
Actual numbers. Per quarter. With breakdowns by day, gender, age group, even time of day.  
Not perfect, but totally usable.

---

## 🧾 File I grabbed

- `서울시 상권분석서비스(추정매출-서울시).csv`
- Contains:
  - total sales per month  
  - weekday/weekend splits  
  - daily patterns  
  - gender & age-based transaction counts  
  - and more goodies  

I haven’t even opened it in pandas yet, but just reading the column names made me smile.

---

## 🧠 So what now?

I’m gonna take the night to look around for maybe 1 or 2 more datasets —  
either to add as features or to cross-check this one.

Tomorrow I’ll open up Jupyter and get into the first real EDA notebook.  
Excited to finally see what the data *feels* like when I mess with it.

This part’s always weirdly satisfying.

---

Stay tuned.
