# Road-Crash-Data-Analysis

## Overview
This project analyzes road crash data from **Raleigh, North Carolina (2015–2022)** to uncover insights into crash trends, contributing factors, and key patterns. The objective is to provide actionable insights that can inform decision-making to improve road safety.

---

## Objectives
- Identify trends in crash occurrences based on **location, time, and weather conditions**.
- Analyze **road features** and their impact on accidents.
- Evaluate the role of weather conditions like rain in crashes and fatalities.
- Examine the **most harmful events** contributing to severe crashes and deaths.
- Determine crash frequencies by **month, day of the week, and hour of the day**.

---

## Dataset
The dataset was sourced from [Raleigh Crash Data](https://data.raleighnc.gov/), and it includes:
- Crash locations (road names, distances from roads)
- Weather conditions during crashes
- Crash dates and times
- Most harmful crash events
- Driver, passenger, and pedestrian counts

---

## Tools and Technologies
- **Python Libraries**: `Pandas`, `Seaborn`, `Matplotlib`, `Statsmodels`
- **Data Visualization**: Bar plots, heatmaps, and trend lines
- **Data Cleaning**: Removal of irrelevant and redundant columns, data renaming for uniformity
- **Exploratory Data Analysis (EDA)**: Insights on crash trends by time, location, and conditions

---

## Key Findings

1. **Weather Impact**:
   - Only about **5% of crashes** were influenced by weather.
   - **Rain** was the most significant weather condition, contributing to both crashes and fatalities.

2. **Crash Timing**:
   - **October** had the highest number of crashes, while **July** had the least.
   - **Fridays** saw the highest crash frequency.
   - Crashes peaked at **5:00 PM**, corresponding to evening traffic hours.

3. **Crash Locations**:
   - **I-40** had the highest number of crashes, regardless of weather conditions.
   - Crashes occurred most frequently either **on the road** or within **100 feet of the road**.

4. **Most Harmful Events**:
   - **Rear-end collisions** were the leading cause of fatal crashes.

---

## Data Cleaning
Steps taken to clean and preprocess the data:
1. Removed redundant columns like `X`, `Y`, and irrelevant fields such as `UpdateDate`, `key_crash`, `LocalUse`, and `LocationCity`.
2. Standardized road names for consistency (e.g., "40" → "I-40").
3. Filtered crash locations with more than **50 incidents** to focus on significant roads.
4. Converted distances (miles → feet) for uniformity.
5. Renamed events and features for uniform data categories.

---

## Visualizations
- **Crash Frequency by Road**: Bar chart of crashes on top 10 roads.
- **Weather-Based Crashes**: Bar chart of crashes caused by rain and other weather conditions.
- **Time Analysis**:
  - Monthly crash frequencies.
  - Daily crash trends.
  - Hourly crash frequencies.
- **Fatalities**:
  - Fatalities by road and month.
  - Fatalities by harmful events.

---
