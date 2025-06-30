---
layout: post
title: "Daily Study Log 5"
date: 2025-04-16
category: study_log
---

Today was all about diving deeper into the **industry-level sales trends** from the Seoul dataset I started cleaning yesterday.

After getting the basic structure set up, I wanted to understand:

> 💭 "Which industries are consistently dominating the sales charts every quarter?"  
> 💭 "Is 한식음식점 really the MVP? Or is 노량진 수산물판매 stealing the show?"

---

## 🔍 What I explored today

1. **Grouped total sales by industry and quarter**  
   - Used `groupby` on `기준_년분기_코드` and `서비스_업종_코드_명`  
   - Aggregated national-level total sales per category

2. **Ranked the top 5 industries for each quarter in 2024**  
   - Turns out 한식음식점 (Korean restaurants) was on top more than once  
   - But seafood sales in 노량진2동? Absolutely wild numbers.  
   - That’s a district-level outlier, not an industry-wide winner

3. **Converted sales units to 억 (100M KRW)**  
   - Because yes, my eyes were bleeding from all those zeros 😅

4. **Made a grouped barplot with value labels**  
   - It actually turned out super readable. Might reuse that template again.

---

## 🧠 Insights

- Some industries (like Korean food) are steady earners across all quarters  
- Others (like seafood) show extreme spikes in one region only  
- Looks like this EDA will split nicely into **macro (industry)** and **micro (district)** levels

---

## 🔮 What’s next?

Tomorrow’s plan:
- Shift focus to **행정동 (district)-level analysis**
- Estimate **average sales per store** (e.g., 치킨집 in 강남구)
- Possibly join with 사업체 수 data to get "store-level profitability"

---

That's a wrap for today!  
Feels good to have a clear separation between nationwide industry trends vs. local insights.  
We’re building something real here 🚀

