"""
VOIS AICTE Major Project: Seasonal Agriculture Performance Analysis
Production-Ready Machine Learning Pipeline
- Data Preprocessing & Cleaning
- Regression Modeling: Crop Yield Prediction (Yield_Tonnes_Ha)
- Classification Modeling: Farm Profitability Prediction (Is_Profitable)
- Cross-Validation, Benchmarking & Model Export
- Generates High-Resolution Charts for PPT Presentation
"""

import os
import json
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, classification_report
)

from sklearn.linear_model import Ridge, LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, RandomForestClassifier
import xgboost as xgb

# Set plotting style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.dpi'] = 150

DATA_PATH = "seasonal_agriculture_performance_dataset.csv"
OUTPUT_DIR = "outputs"
MODEL_DIR = "models"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)


def load_and_preprocess_data(csv_path=DATA_PATH):
    print(f"[*] Loading dataset from {csv_path}...")
    df = pd.read_csv(csv_path)
    print(f"    Raw Shape: {df.shape}")

    # Remove duplicates
    df = df.drop_duplicates()

    # Create target for classification: Is_Profitable
    df['Is_Profitable'] = (df['Profit_INR'] > 0).astype(int)
    
    # Feature Engineering
    df['NPK_Total'] = df['Nitrogen_kg_ha'] + df['Phosphorus_kg_ha'] + df['Potassium_kg_ha']
    df['Rain_per_Temp'] = df['Rainfall_mm'] / (df['Avg_Temperature_C'] + 1e-5)
    
    # Impute missing values using grouping where possible
    df['Rainfall_mm'] = df.groupby(['Season', 'State'])['Rainfall_mm'].transform(
        lambda x: x.fillna(x.median())
    )
    df['Soil_Moisture_pct'] = df.groupby(['Season', 'Crop'])['Soil_Moisture_pct'].transform(
        lambda x: x.fillna(x.median())
    )
    
    # Fill remaining missing with overall median
    num_cols = df.select_dtypes(include=[np.number]).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())

    # For categorical columns
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    print(f"    Cleaned Shape: {df.shape}")
    print(f"    Total Remaining Nulls: {df.isnull().sum().sum()}")
    return df


def get_preprocessor(cat_features, num_features):
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, num_features),
            ('cat', categorical_transformer, cat_features)
        ]
    )
    return preprocessor


def train_yield_prediction_models(df):
    print("\n" + "="*60)
    print("  MODEL 1: CROP YIELD PREDICTION (REGRESSION)")
    print("="*60)

    # Features for yield prediction (exclude identifiers and future/target outputs)
    num_features = [
        'Farm_Area_Hectares', 'Rainfall_mm', 'Avg_Temperature_C', 'Humidity_pct',
        'Sunlight_Hours_Day', 'Soil_pH', 'Soil_Moisture_pct', 'Nitrogen_kg_ha',
        'Phosphorus_kg_ha', 'Potassium_kg_ha', 'Fertilizer_kg_ha', 'Pesticide_Litre_ha',
        'Seed_Quality_Score', 'Water_Used_m3', 'Water_Efficiency_t_per_1000m3',
        'Disease_Pest_Risk_pct', 'NPK_Total', 'Rain_per_Temp'
    ]
    cat_features = ['Season', 'Crop', 'State', 'Irrigation_Method']

    X = df[num_features + cat_features]
    y = df['Yield_Tonnes_Ha']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    models = {
        'Linear Regression': LinearRegression(),
        'Ridge Regression': Ridge(alpha=1.0),
        'Random Forest': RandomForestRegressor(n_estimators=150, max_depth=15, random_state=42, n_jobs=-1),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=150, learning_rate=0.08, max_depth=5, random_state=42),
        'XGBoost': xgb.XGBRegressor(n_estimators=150, learning_rate=0.08, max_depth=6, random_state=42, n_jobs=-1)
    }

    results = {}
    fitted_pipelines = {}

    for name, model in models.items():
        preprocessor = get_preprocessor(cat_features, num_features)
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('regressor', model)
        ])

        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        # 5-fold CV
        cv = KFold(n_splits=5, shuffle=True, random_state=42)
        cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring='r2', n_jobs=-1)

        results[name] = {
            'R2': round(float(r2), 4),
            'MAE': round(float(mae), 4),
            'RMSE': round(float(rmse), 4),
            'CV_R2_Mean': round(float(cv_scores.mean()), 4),
            'CV_R2_Std': round(float(cv_scores.std()), 4)
        }
        fitted_pipelines[name] = (pipeline, y_pred)

        print(f"[*] {name:20s} | R²: {r2:.4f} | MAE: {mae:.4f} | RMSE: {rmse:.4f} | CV R²: {cv_scores.mean():.4f}")

    # Best Model Selection
    best_model_name = max(results, key=lambda k: results[k]['R2'])
    best_pipeline, best_preds = fitted_pipelines[best_model_name]
    print(f"\n[+] Best Regression Model: {best_model_name} (R² = {results[best_model_name]['R2']})")

    # Save best model
    joblib.dump(best_pipeline, os.path.join(MODEL_DIR, "best_crop_yield_model.joblib"))
    print(f"    Saved model to {os.path.join(MODEL_DIR, 'best_crop_yield_model.joblib')}")

    # Extract Feature Importances if available
    try:
        regressor = best_pipeline.named_steps['regressor']
        preprocessor = best_pipeline.named_steps['preprocessor']
        cat_encoder = preprocessor.named_transformers_['cat'].named_steps['encoder']
        encoded_cat_names = list(cat_encoder.get_feature_names_out(cat_features))
        all_feature_names = num_features + encoded_cat_names

        if hasattr(regressor, 'feature_importances_'):
            importances = regressor.feature_importances_
            feat_df = pd.DataFrame({
                'Feature': all_feature_names,
                'Importance': importances
            }).sort_values('Importance', ascending=False)

            plt.figure(figsize=(10, 6))
            sns.barplot(data=feat_df.head(15), x='Importance', y='Feature', palette='viridis')
            plt.title(f"Top 15 Feature Importances ({best_model_name}) - Crop Yield Prediction", fontsize=13, fontweight='bold')
            plt.xlabel("Importance Score")
            plt.tight_layout()
            plt.savefig(os.path.join(OUTPUT_DIR, "feature_importance_yield.png"))
            plt.close()
            print(f"    Saved feature importance chart to {os.path.join(OUTPUT_DIR, 'feature_importance_yield.png')}")
    except Exception as e:
        print(f"    Note on feature importances: {e}")

    # Actual vs Predicted Plot
    plt.figure(figsize=(7, 6))
    plt.scatter(y_test, best_preds, alpha=0.5, color='#2b5c8f', edgecolors='none', s=35)
    min_val = min(y_test.min(), best_preds.min())
    max_val = max(y_test.max(), best_preds.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Ideal 1:1 Line')
    plt.title(f"Actual vs Predicted Yield ({best_model_name})\nR² = {results[best_model_name]['R2']:.4f}, RMSE = {results[best_model_name]['RMSE']:.4f}", fontsize=12, fontweight='bold')
    plt.xlabel("Actual Yield (Tonnes/Ha)")
    plt.ylabel("Predicted Yield (Tonnes/Ha)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "model_actual_vs_predicted.png"))
    plt.close()
    print(f"    Saved Actual vs Predicted plot to {os.path.join(OUTPUT_DIR, 'model_actual_vs_predicted.png')}")

    return results, X_test, y_test, best_preds, best_model_name


def train_profitability_classifier(df):
    print("\n" + "="*60)
    print("  MODEL 2: FARM PROFITABILITY CLASSIFICATION (IS_PROFITABLE)")
    print("="*60)

    # Features (excluding financial totals to avoid direct data leakage)
    num_features = [
        'Farm_Area_Hectares', 'Rainfall_mm', 'Avg_Temperature_C', 'Humidity_pct',
        'Sunlight_Hours_Day', 'Soil_pH', 'Soil_Moisture_pct', 'Nitrogen_kg_ha',
        'Phosphorus_kg_ha', 'Potassium_kg_ha', 'Fertilizer_kg_ha', 'Pesticide_Litre_ha',
        'Seed_Quality_Score', 'Market_Price_INR_Tonne', 'Water_Used_m3',
        'Water_Efficiency_t_per_1000m3', 'Disease_Pest_Risk_pct', 'Yield_Tonnes_Ha'
    ]
    cat_features = ['Season', 'Crop', 'State', 'Irrigation_Method']

    X = df[num_features + cat_features]
    y = df['Is_Profitable']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    classifiers = {
        'Logistic Regression': LogisticRegression(max_iter=500, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=150, max_depth=12, random_state=42, n_jobs=-1),
        'XGBoost': xgb.XGBClassifier(n_estimators=150, learning_rate=0.08, max_depth=5, random_state=42, eval_metric='logloss', n_jobs=-1)
    }

    clf_results = {}
    best_clf_name = None
    best_score = -1
    best_clf_pipeline = None

    for name, clf in classifiers.items():
        preprocessor = get_preprocessor(cat_features, num_features)
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', clf)
        ])

        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        y_proba = pipeline.predict_proba(X_test)[:, 1] if hasattr(pipeline, "predict_proba") else y_pred

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc = roc_auc_score(y_test, y_proba)

        clf_results[name] = {
            'Accuracy': round(float(acc), 4),
            'Precision': round(float(prec), 4),
            'Recall': round(float(rec), 4),
            'F1_Score': round(float(f1), 4),
            'ROC_AUC': round(float(roc), 4)
        }

        if f1 > best_score:
            best_score = f1
            best_clf_name = name
            best_clf_pipeline = pipeline

        print(f"[*] {name:20s} | Acc: {acc:.4f} | Prec: {prec:.4f} | Rec: {rec:.4f} | F1: {f1:.4f} | AUC: {roc:.4f}")

    joblib.dump(best_clf_pipeline, os.path.join(MODEL_DIR, "best_profit_classifier.joblib"))
    print(f"\n[+] Best Classification Model: {best_clf_name} (F1 = {clf_results[best_clf_name]['F1_Score']})")
    print(f"    Saved classifier to {os.path.join(MODEL_DIR, 'best_profit_classifier.joblib')}")

    # Confusion matrix
    y_pred_best = best_clf_pipeline.predict(X_test)
    cm = confusion_matrix(y_test, y_pred_best)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Loss/Breakeven (0)', 'Profitable (1)'],
                yticklabels=['Loss/Breakeven (0)', 'Profitable (1)'])
    plt.title(f"Confusion Matrix ({best_clf_name})\nAccuracy: {clf_results[best_clf_name]['Accuracy']*100:.1f}%", fontsize=12, fontweight='bold')
    plt.xlabel("Predicted Class")
    plt.ylabel("Actual Class")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "profitability_confusion_matrix.png"))
    plt.close()
    print(f"    Saved confusion matrix to {os.path.join(OUTPUT_DIR, 'profitability_confusion_matrix.png')}")

    return clf_results, best_clf_name


def generate_presentation_visuals(df):
    print("\n" + "="*60)
    print("  GENERATING PRESENTATION VISUALIZATIONS FOR PPT SLIDES")
    print("="*60)

    # 1. Seasonal Yield & Profit Overview
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    sns.barplot(data=df, x='Season', y='Yield_Tonnes_Ha', ax=axes[0], palette='crest', ci=None, estimator=np.mean)
    axes[0].set_title("Mean Yield by Agricultural Season", fontsize=12, fontweight='bold')
    axes[0].set_ylabel("Yield (Tonnes/Ha)")
    for p in axes[0].patches:
        axes[0].annotate(f"{p.get_height():.2f}", (p.get_x() + p.get_width() / 2., p.get_height() / 2),
                         ha='center', va='center', color='white', fontweight='bold')

    sns.barplot(data=df, x='Season', y='Profit_INR', ax=axes[1], palette='flare', ci=None, estimator=np.mean)
    axes[1].set_title("Mean Profit by Agricultural Season", fontsize=12, fontweight='bold')
    axes[1].set_ylabel("Profit (INR)")
    for p in axes[1].patches:
        axes[1].annotate(f"₹{p.get_height():,.0f}", (p.get_x() + p.get_width() / 2., p.get_height() / 2),
                         ha='center', va='center', color='white', fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "seasonal_yield_profit_comparison.png"))
    plt.close()
    print("    [1] Saved seasonal_yield_profit_comparison.png")

    # 2. Environmental Heatmap (Weather, Soil & Yield)
    plt.figure(figsize=(12, 9))
    env_cols = [
        'Rainfall_mm', 'Avg_Temperature_C', 'Humidity_pct', 'Sunlight_Hours_Day',
        'Soil_pH', 'Soil_Moisture_pct', 'Nitrogen_kg_ha', 'Phosphorus_kg_ha',
        'Potassium_kg_ha', 'Fertilizer_kg_ha', 'Yield_Tonnes_Ha', 'Profit_INR',
        'Water_Efficiency_t_per_1000m3', 'Disease_Pest_Risk_pct'
    ]
    corr = df[env_cols].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, cmap='vlag', center=0, annot=True, fmt='.2f', square=True, linewidths=.5, cbar_kws={"shrink": .8})
    plt.title("Correlation Matrix: Agronomic, Environmental & Economic Metrics", fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "environmental_correlation_heatmap.png"))
    plt.close()
    print("    [2] Saved environmental_correlation_heatmap.png")

    # 3. Irrigation Method vs Water Efficiency & Profit
    plt.figure(figsize=(10, 5))
    sns.boxplot(data=df, x='Irrigation_Method', y='Water_Efficiency_t_per_1000m3', hue='Season', palette='Set2')
    plt.title("Water Efficiency Across Irrigation Methods by Season", fontsize=12, fontweight='bold')
    plt.ylabel("Water Efficiency (Tonnes / 1000 m³)")
    plt.xlabel("Irrigation Method")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "irrigation_water_efficiency.png"))
    plt.close()
    print("    [3] Saved irrigation_water_efficiency.png")

    # 4. Crop Performance Benchmarking (Yield & Market Price)
    crop_stats = df.groupby('Crop').agg({
        'Yield_Tonnes_Ha': 'mean',
        'Profit_INR': 'mean',
        'Revenue_INR': 'mean'
    }).sort_values('Profit_INR', ascending=False)

    plt.figure(figsize=(11, 5))
    sns.barplot(x=crop_stats.index, y=crop_stats['Profit_INR'], palette='viridis')
    plt.title("Average Net Profit per Crop (INR)", fontsize=13, fontweight='bold')
    plt.xlabel("Crop")
    plt.ylabel("Net Profit (INR)")
    plt.xticks(rotation=20)
    for i, val in enumerate(crop_stats['Profit_INR']):
        plt.text(i, val / 2, f"₹{val:,.0f}", ha='center', va='center', color='white', fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "crop_profit_comparison.png"))
    plt.close()
    print("    [4] Saved crop_profit_comparison.png")

    print("[+] All presentation visuals created successfully in outputs/ directory.")


def main():
    df = load_and_preprocess_data()
    reg_results, X_test, y_test, best_preds, best_reg = train_yield_prediction_models(df)
    clf_results, best_clf = train_profitability_classifier(df)
    generate_presentation_visuals(df)

    summary = {
        'Yield_Regression_Benchmarking': reg_results,
        'Best_Yield_Model': best_reg,
        'Profitability_Classification_Benchmarking': clf_results,
        'Best_Profit_Model': best_clf
    }

    with open(os.path.join(OUTPUT_DIR, "model_benchmark_summary.json"), "w") as f:
        json.dump(summary, f, indent=4)
    print(f"\n[+] Successfully saved benchmark summary to {os.path.join(OUTPUT_DIR, 'model_benchmark_summary.json')}")
    print("\n[+] Machine Learning Pipeline Execution Completed Successfully!\n")


if __name__ == '__main__':
    main()
