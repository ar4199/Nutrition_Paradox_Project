# Nutrition_Paradox_Project

## 📘 Project Overview
This project analyzes **global nutrition trends**, focusing on **obesity** and **malnutrition** across different regions, age groups, and genders.  
Using **SQL**, **Python (Pandas, Matplotlib, Plotly)**, and **Streamlit**, the project provides insights into how nutrition levels have evolved globally over time.

The key goal is to **identify patterns, trends, and disparities** between countries and demographics — helping understand regions with high obesity or malnutrition and evaluate reliability using **Confidence Interval Width (CI_Width)**.

---

## 🧠 Key Objectives
1. **Analyze obesity and malnutrition trends** across years, genders, and regions.  
2. **Compare obesity vs. malnutrition** to understand health disparities.  
3. **Evaluate reliability** using `CI_Width` — narrower intervals indicate more reliable estimates.  
4. **Visualize insights interactively** using **Plotly** and **Streamlit** dashboards.  
5. Identify:
   - Top countries with **highest/lowest obesity and malnutrition**  
   - **Regions with consistent or varying estimates**  
   - **Gender-based differences**  
   - **Countries showing improvements or declines**  

---

## 🧩 Tools Used
- **Python 3.x**
- **SQL** (SQLite/MySQL)
- **Pandas** for data manipulation
- **Matplotlib & Plotly** for visualization
- **Streamlit** for dashboard creation
- **Jupyter Notebook** for data exploration

---

## 🗂️ Dataset Description
The project uses two main datasets:
- `obesity`
- `malnutrition`

Each dataset contains:
| Column Name | Description |
|--------------|-------------|
| `Region` | WHO region of the country |
| `Country_Name` | Name of the country |
| `Gender` | Male, Female, or Both |
| `AgeGroup` | Age group classification |
| `Year` | Year of observation |
| `Mean_Estimate` | Average estimated percentage of obesity or malnutrition |
| `Lower_Bound` | Lower confidence bound |
| `Upper_Bound` | Upper confidence bound |
| `CI_Width` | Difference between upper and lower bound (measure of reliability) |
| `Obesity_Level` / `Malnutrition_Level` | Categorized level for easier comparison |

---

## 📊 Key SQL Analyses
### 🔹 Obesity Queries
- Top 5 regions with highest obesity (2022)
- Average obesity by gender and age group
- Countries with increasing obesity trends
- Region-wise obesity consistency using CI_Width

### 🔹 Malnutrition Queries
- Top 5 countries with highest malnutrition
- Malnutrition trend in African region
- Gender-based and age-based malnutrition analysis
- Regions with lowest malnutrition averages

### 🔹 Combined Insights
- **Obesity vs. Malnutrition comparison by country**
- **Gender-based disparities** in both conditions
- **Countries with obesity up & malnutrition down**
- **Reliability checks** using CI_Width thresholds

---

## 📈 Visualizations

### 1. **Line Charts (Trends Over Time)**
- Displays obesity and malnutrition trends by **Region** or **Country**.
- Interactive Plotly lines show how each factor changes over time.

### 2. **Bar Charts (Comparisons)**
- Compare **Top/Bottom countries or regions** for obesity and malnutrition.
- Helps identify global outliers and progress leaders.

### 3. **Box Plots (Variability)**
- Show data **spread and variability** across regions.
- Useful to identify regions with inconsistent or extreme values.

### 4. **Heatmaps / Scatter Plots**
- Detect patterns, correlations, and **outliers** between obesity and malnutrition.
- Highlight relationships between reliability (`CI_Width`) and mean estimates.

---

## 🚀 How to Run the Project

### 🧮 1. Run the Notebook
```bash
jupyter notebook nutrition_project.ipynb
