# Seasonal Agriculture Performance Analysis & Predictive Modeling

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4%2B-orange.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Ensemble-red.svg)](https://xgboost.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Edunet Foundation × VOIS for Tech (Vodafone Idea Foundation) — Data Analytics Internship**  
> **Intern**: Sathiyamoorthi K | **Institution**: IFET College of Engineering  
> **AICTE STU ID**: `STU663c9352627131715245906` | **Internship ID**: `INTERNSHIP_17830691666a4779eecfe8a`  
> **Duration**: 10th August 2026 – 10th September 2026 (4 Weeks)

---

## 📌 Project Overview

This project is the **Major Capstone Deliverable** of the **Edunet Foundation Internship**, powered by **VOIS for Tech** (Vodafone Idea Foundation) in collaboration with **AICTE**. The program equips technical students with hands-on, project-based learning in **Data Analytics** through mentored real-world problem solving.

Agricultural activities in India are heavily contingent on seasonal variations in environmental factors, resource availability, and soil fertility. Raw farm data often obscures the underlying seasonal trends that govern crop yields and farm profitability.

This repository provides an end-to-end data science and machine learning solution analyzing **4,000 farm records** across **8 major Indian states**, **8 crop types**, and **3 agricultural seasons** (Kharif, Rabi, and Zaid).

### Key Objectives:
1. **Seasonal Performance Analysis**: Investigate how crop yield, input costs, revenues, and water efficiency shift across seasons.
2. **Hypothesis Testing**: Statistically confirm seasonal variations using One-Way ANOVA ($p < 0.001$).
3. **Dual Machine Learning Architecture**:
   - **Crop Yield Predictor (Regression)**: Forecasts `Yield_Tonnes_Ha` ($R^2 = 0.9900$, MAE = $0.46$ t/ha).
   - **Farm Profitability Classifier (Classification)**: Assesses financial feasibility ($92.25\%$ Accuracy, $0.9808$ ROC-AUC).
4. **Data-Driven Agronomic Guidance**: Deliver actionable seasonal recommendations for farmers and policymakers.

---

## 📊 Dataset Description

- **Source**: `seasonal_agriculture_performance_dataset.csv`
- **Volume**: 4,000 samples $\times$ 28 attributes
- **Cropping Seasons**:
  - **Kharif** (Monsoon season): High precipitation, elevated pest risk.
  - **Rabi** (Winter season): High yield stability, cereal dominance (Wheat/Maize).
  - **Zaid** (Summer season): High temperatures, moisture stress, critical need for micro-irrigation.
- **Crops (8)**: Wheat, Rice, Maize, Pulses, Cotton, Chilli, Groundnut, Sugarcane.
- **Geographic Coverage (8 States)**: Andhra Pradesh, Maharashtra, Telangana, Karnataka, Gujarat, Tamil Nadu, Punjab, Madhya Pradesh.
- **Feature Groups**:
  - *Environmental*: Rainfall (mm), Avg Temperature (°C), Humidity (%), Sunlight Hours.
  - *Soil Chemistry*: Soil pH, Soil Moisture (%), Nitrogen, Phosphorus, Potassium (N-P-K).
  - *Agronomic Inputs*: Irrigation Method (Drip, Flood, Rainfed, Sprinkler), Fertilizer (kg/ha), Pesticide (L/ha), Seed Quality Score.
  - *Economic Metrics*: Total Cost (INR), Revenue (INR), Profit (INR), Water Efficiency ($t/1000m^3$), Disease/Pest Risk (%).

---

## 🔬 Machine Learning Performance Benchmarks

### 1. Crop Yield Prediction (`Yield_Tonnes_Ha`)
Evaluated using 5-Fold Cross-Validation on an 80/20 train/test split:

| Algorithm | Test $R^2$ | MAE (t/ha) | RMSE (t/ha) | 5-Fold CV $R^2$ Mean |
| :--- | :---: | :---: | :---: | :---: |
| **Gradient Boosting Regressor** | **0.9900** | **0.4636** | **1.3899** | **0.9735** |
| **XGBoost Regressor** | **0.9865** | **0.4994** | **1.6122** | **0.9701** |
| **Random Forest Regressor** | **0.9841** | **0.5306** | **1.7510** | **0.9679** |
| **Linear Regression** | 0.9252 | 1.8948 | 3.7974 | 0.9162 |
| **Ridge Regression** | 0.9252 | 1.9017 | 3.7970 | 0.9162 |

*Primary Determinants of Yield*: Crop Variety, Seed Quality Score, balanced N-P-K nutrient application, and irrigation technology.

### 2. Farm Profitability Classification (`Is_Profitable`)
Predicts whether a farm operation will yield net positive financial returns ($Profit > 0$):

| Classifier | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **XGBoost Classifier** | **92.25%** | **91.97%** | **92.87%** | **0.9242** | **0.9808** |
| **Random Forest Classifier** | 91.75% | 92.31% | 91.40% | 0.9185 | 0.9731 |
| **Logistic Regression** | 85.50% | 87.21% | 83.78% | 0.8546 | 0.9423 |

---

## 📈 Key Visualizations & Findings

1. **Irrigation Efficiency**: Drip irrigation consistently achieves 3x higher water efficiency ($t/1000m^3$) compared to traditional flood irrigation across all seasons.
2. **Seasonal Trade-offs**: Kharif delivers the highest gross production but exhibits a +48% increase in disease/pest vulnerability, necessitating preventive IPM measures.
3. **Economic Leaders**: Commercial cash crops (Sugarcane, Chilli, Cotton) generate the highest net profit per hectare, whereas Pulses and Groundnut provide critical soil nitrogen fixation.

---

## 📁 Repository Structure

```text
├── seasonal_agriculture_performance_analysis.ipynb  # End-to-end interactive Jupyter Notebook
├── model_pipeline.py                               # Production training & evaluation script
├── seasonal_agriculture_performance_dataset.csv     # 4,000-row agricultural dataset
├── VOIS_Major_Project_PPT_Submission_Completed.pptx # 14-slide submission-ready deck
├── outputs/                                        # High-resolution visualization figures
│   ├── seasonal_yield_profit_comparison.png
│   ├── environmental_correlation_heatmap.png
│   ├── model_actual_vs_predicted.png
│   ├── feature_importance_yield.png
│   ├── profitability_confusion_matrix.png
│   ├── irrigation_water_efficiency.png
│   ├── crop_profit_comparison.png
│   └── model_benchmark_summary.json
├── models/                                         # Serialized production models
│   ├── best_crop_yield_model.joblib
│   └── best_profit_classifier.joblib
└── README.md                                       # Documentation & Project Guide
```

---

## 🚀 Quickstart & Reproduction

### 1. Clone the Repository
```bash
git clone https://github.com/ksmashhero06/-Seasonal-Agriculture-Performance-Analysis-.git
cd -Seasonal-Agriculture-Performance-Analysis-
```

### 2. Install Dependencies
```bash
pip install pandas numpy scikit-learn xgboost scipy matplotlib seaborn joblib python-pptx
```

### 3. Run the ML Pipeline
```bash
python model_pipeline.py
```

### 4. Launch Jupyter Notebook
```bash
jupyter notebook seasonal_agriculture_performance_analysis.ipynb
```

---

## 👤 Author Information

- **Intern Name**: Sathiyamoorthi K
- **Institution**: IFET College of Engineering
- **AICTE Student ID**: `STU663c9352627131715245906`
- **Internship ID**: `INTERNSHIP_17830691666a4779eecfe8a`
- **Email**: [kkssathiyamoorthi@gmail.com](mailto:kkssathiyamoorthi@gmail.com)
- **GitHub**: [@ksmashhero06](https://github.com/ksmashhero06)
- **Program**: Edunet Foundation × VOIS for Tech (Vodafone Idea Foundation) — Data Analytics Internship
- **Duration**: 10th August 2026 – 10th September 2026
