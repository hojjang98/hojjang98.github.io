---
layout: post
title: "Daily Study Log 4"
date: 2025-04-15
category: study_log
---

Today marks the first real step in my **Sales Forecasting for Small Business** project.

Why?  
Because after exploring Seoul’s open business datasets and running my own store in the past, I wanted to **visualize and analyze actual sales trends** across different neighborhoods and industries.

---

## 📌 What I did today

1. **Loaded the raw dataset** from Seoul’s commercial analysis platform  
   - Format: `.xlsx` (2024 data)
   - Structure: Quarterly sales by district (`행정동`) and industry category (`서비스_업종_코드_명`)
2. **Cleaned the dataset**  
   - Checked for missing values and basic structure using `df.info()` / `df.describe()`
3. **Grouped sales by district + quarter**  
   - Created a pivot-like structure to analyze trends
4. **Visualized Top 10 industries in Q4 2024**  
   - Used `matplotlib` and configured Korean font (`Malgun Gothic`) to avoid text issues
   - Horizontal bar plot to show industry-wise revenue dominance

---

## 💡 Takeaways

- Basic structure is ready — the data is clean and well-organized
- Certain industries clearly dominate (especially seafood, fruits/vegetables)
- Need to investigate how trends shift **over time** and **by region**

---

## 🚧 Next steps

- Add time-series plots by industry and neighborhood
- Try a geographical visualization (Seoul choropleth map?)
- Consider log transformation to address large sales variance
- Create README and translate key column names

---

That's it for Day 1 — clean start, clear structure, and one solid chart! 😎  
Stay tuned for more insights as this project unfolds.

