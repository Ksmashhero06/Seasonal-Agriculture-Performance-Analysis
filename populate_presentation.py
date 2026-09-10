import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def populate_presentation():
    input_ppt = "VOIS_Major_Project_PPT_Submission_Template.pptx"
    output_ppt = "VOIS_Major_Project_PPT_Submission_Completed.pptx"

    prs = pptx.Presentation(input_ppt)
    print(f"Loaded {input_ppt} with {len(prs.slides)} slides.")

    # Colors
    DARK_BLUE = RGBColor(16, 44, 87)
    CHARCOAL = RGBColor(40, 40, 40)
    ACCENT_RED = RGBColor(230, 0, 0)

    # -------------------------------------------------------------
    # Slide 1: Title Slide
    # -------------------------------------------------------------
    s1 = prs.slides[0]
    for shape in s1.shapes:
        if shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                if "Project Title" in p.text:
                    p.text = "Project Title: Seasonal Agriculture Performance Analysis & Predictive Modeling"
                    p.font.bold = True
                    p.font.size = Pt(20)
                    p.font.color.rgb = DARK_BLUE

    # -------------------------------------------------------------
    # Slide 3: Project Description
    # -------------------------------------------------------------
    s3 = prs.slides[2]
    # Add a clean text box with detailed description
    tx_box = s3.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.5), Inches(4.5))
    tf = tx_box.text_frame
    tf.word_wrap = True

    desc_points = [
        ("Overview: ", "Comprehensive data science and machine learning project analyzing 4,000 agricultural farm operations across 8 major Indian states, 8 crops, and 3 distinct agricultural seasons (Kharif, Rabi, and Zaid)."),
        ("Key Investigations: ", "Explores the intricate relationships between seasonal weather patterns (rainfall, temperature, humidity, sunlight), soil nutrient profiles (N-P-K, pH, moisture), agronomic inputs (irrigation technologies, fertilizers, pesticides), and economic outcomes (production, costs, revenue, net profit, and water efficiency)."),
        ("Methodology & Rigor: ", "Implements domain-aware data imputation, multi-season exploratory data analysis (EDA), statistical hypothesis testing (One-way ANOVA), and machine learning regression and classification models."),
        ("Predictive Modeling: ", "Trains and benchmarks multiple algorithms (Linear/Ridge Regression, Random Forest, Gradient Boosting, XGBoost), achieving an outstanding R² score of 0.990 for Crop Yield Prediction and 92.25% accuracy for Farm Profitability Classification."),
        ("Strategic Value: ", "Delivers actionable, data-driven seasonal crop planning and irrigation recommendations to optimize resource efficiency and farmer livelihoods.")
    ]

    for i, (head, body) in enumerate(desc_points):
        p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = "• " + head
        r1.font.bold = True
        r1.font.size = Pt(14)
        r1.font.color.rgb = DARK_BLUE

        r2 = p.add_run()
        r2.text = body
        r2.font.bold = False
        r2.font.size = Pt(13)
        r2.font.color.rgb = CHARCOAL

    # -------------------------------------------------------------
    # Slide 4: End Users
    # -------------------------------------------------------------
    s4 = prs.slides[3]
    tx_box4 = s4.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(11.5), Inches(4.2))
    tf4 = tx_box4.text_frame
    tf4.word_wrap = True

    users = [
        ("1. Farmers & Agricultural Cooperatives: ", "Provides actionable seasonal advisories for optimal crop selection, timing, and irrigation management (Drip vs. Flood) to maximize yield and net profit while minimizing production costs."),
        ("2. Agronomists & Extension Officers: ", "Empowers field officers with diagnostic tools to evaluate pest/disease vulnerabilities, soil nutrient requirements (N-P-K balance), and water efficiency metrics across varying seasons."),
        ("3. Government Agricultural Departments & Policymakers: ", "Enables evidence-based regional production forecasting, drought/flood contingency planning, and targeted water-subsidy resource allocation."),
        ("4. AgTech Companies & Supply Chain Managers: ", "Delivers high-precision pre-harvest yield estimations to stabilize storage, logistics, food processing, and fair market procurement pricing.")
    ]

    for i, (head, body) in enumerate(users):
        p = tf4.add_paragraph() if i > 0 else tf4.paragraphs[0]
        p.space_after = Pt(14)
        r1 = p.add_run()
        r1.text = head
        r1.font.bold = True
        r1.font.size = Pt(14)
        r1.font.color.rgb = DARK_BLUE

        r2 = p.add_run()
        r2.text = body
        r2.font.bold = False
        r2.font.size = Pt(13)
        r2.font.color.rgb = CHARCOAL

    # -------------------------------------------------------------
    # Slide 5: Technology Used
    # -------------------------------------------------------------
    s5 = prs.slides[4]
    tx_box5 = s5.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.5), Inches(4.5))
    tf5 = tx_box5.text_frame
    tf5.word_wrap = True

    techs = [
        ("Programming Language: ", "Python 3.11+ (High performance data science & ML runtime)"),
        ("Data Manipulation & Wrangling: ", "Pandas (DataFrame transformations, grouped aggregations), NumPy (Vectorized numerical computations)"),
        ("Statistical Inference: ", "SciPy Stats (One-Way ANOVA hypothesis testing, p-value calculation, variance analysis)"),
        ("Machine Learning Frameworks: ", "Scikit-Learn (Pipelines, ColumnTransformer, StandardScaler, OneHotEncoder, Ridge Regression, Random Forest, Gradient Boosting), XGBoost (Extreme Gradient Boosting Regressor & Classifier)"),
        ("Data Visualization & Analytics: ", "Matplotlib & Seaborn (High-resolution multi-panel plots, heatmaps, boxplots, residual scatter plots)"),
        ("Model Serialization & Reporting: ", "Joblib (Model persistence .joblib), Python-PPTX, Jupyter Notebook (.ipynb)")
    ]

    for i, (head, body) in enumerate(techs):
        p = tf5.add_paragraph() if i > 0 else tf5.paragraphs[0]
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = "• " + head
        r1.font.bold = True
        r1.font.size = Pt(14)
        r1.font.color.rgb = DARK_BLUE

        r2 = p.add_run()
        r2.text = body
        r2.font.bold = False
        r2.font.size = Pt(13)
        r2.font.color.rgb = CHARCOAL

    # -------------------------------------------------------------
    # Helper to add image and commentary to result slides
    # -------------------------------------------------------------
    def setup_result_slide(slide, title_text, img_path, bullets):
        # Update title if possible
        for shape in slide.shapes:
            if shape.has_text_frame and "RESULTS" in shape.text:
                shape.text = f"RESULTS: {title_text}"
                for p in shape.text_frame.paragraphs:
                    p.font.size = Pt(20)
                    p.font.bold = True
                    p.font.color.rgb = DARK_BLUE
                break

        # Remove existing placeholder text with "[Add screen shots"
        shapes_to_clean = []
        for shape in slide.shapes:
            if shape.has_text_frame and "[Add screen shots" in shape.text:
                shape.text = ""

        # Insert Image
        if os.path.exists(img_path):
            slide.shapes.add_picture(img_path, Inches(0.8), Inches(1.8), Inches(6.0), Inches(4.3))

        # Insert Bullet commentary
        tx_box = slide.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.8), Inches(4.3))
        tf = tx_box.text_frame
        tf.word_wrap = True

        for i, (b_title, b_desc) in enumerate(bullets):
            p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
            p.space_after = Pt(10)
            r1 = p.add_run()
            r1.text = "• " + b_title + ": "
            r1.font.bold = True
            r1.font.size = Pt(13)
            r1.font.color.rgb = DARK_BLUE

            r2 = p.add_run()
            r2.text = b_desc
            r2.font.bold = False
            r2.font.size = Pt(12)
            r2.font.color.rgb = CHARCOAL

    # Slide 6: Seasonal Yield & Profit Overview
    setup_result_slide(
        prs.slides[5],
        "Seasonal Yield & Profitability Dynamics",
        "outputs/seasonal_yield_profit_comparison.png",
        [
            ("Kharif Season", "Exhibits highest overall rainfall and moisture, supporting heavy crops but experiencing elevated disease/pest risks."),
            ("Rabi Season", "Delivers optimal yield consistency and strong net profits, benefiting from controlled irrigation and favorable winter temperatures."),
            ("Zaid Season", "Characterized by high ambient temperatures and dry conditions; profitability depends critically on high-efficiency irrigation methods.")
        ]
    )

    # Slide 7: Crop Yield Regression Benchmarking
    setup_result_slide(
        prs.slides[6],
        "Crop Yield Prediction Model (R² = 0.990)",
        "outputs/model_actual_vs_predicted.png",
        [
            ("Algorithm Benchmarking", "Compared Linear Regression, Ridge, Random Forest, Gradient Boosting, and XGBoost using 5-Fold Cross-Validation."),
            ("Top Performer", "Gradient Boosting achieved an extraordinary R² of 0.9900, MAE of 0.4636 Tonnes/Ha, and RMSE of 1.3899 Tonnes/Ha."),
            ("Validation Quality", "Actual vs. Predicted scatter plot demonstrates tight alignment along the 1:1 diagonal across all yield distributions.")
        ]
    )

    # Slide 8: Feature Importance & Profit Classification
    setup_result_slide(
        prs.slides[7],
        "Feature Drivers & Farm Profitability Model",
        "outputs/feature_importance_yield.png",
        [
            ("Primary Yield Drivers", "Crop variety, Seed Quality Score, and balanced N-P-K soil fertilization emerged as the most critical determinants of yield."),
            ("Profitability Classifier", "XGBoost Classifier predicted farm profitability with 92.25% Accuracy, 0.9242 F1-Score, and 0.9808 ROC-AUC."),
            ("Practical Impact", "Enables pre-season financial feasibility assessments before farmers invest capital in seeds and fertilizers.")
        ]
    )

    # Slide 9: Environmental Correlations & Irrigation Efficiency
    setup_result_slide(
        prs.slides[8],
        "Irrigation Technology & Water Efficiency",
        "outputs/irrigation_water_efficiency.png",
        [
            ("Drip Irrigation Superiority", "Drip irrigation generated significantly higher water productivity (Tonnes/1000m³) across all 3 agricultural seasons."),
            ("Flood Irrigation Waste", "Traditional flood irrigation consumed the highest water volumes with the lowest marginal yield return."),
            ("Correlation Findings", "Strong positive correlation observed between water efficiency, optimized fertilizer usage, and net farm revenue.")
        ]
    )

    # Slide 10: Crop Economic Comparison & Statistical ANOVA
    setup_result_slide(
        prs.slides[9],
        "Crop Economic Breakdown & ANOVA Results",
        "outputs/crop_profit_comparison.png",
        [
            ("Economic Leaders", "Commercial cash crops (Sugarcane, Chilli, Cotton) achieved the highest net profits per hectare."),
            ("Pulse & Grain Value", "Pulses and Wheat provided critical soil nitrogen replenishment and steady seasonal cash flow."),
            ("Hypothesis Testing", "One-Way ANOVA confirmed statistically significant differences (p < 0.001) across seasons for Yield, Rainfall, and Net Profit.")
        ]
    )

    # -------------------------------------------------------------
    # Slide 11: Future Scope
    # -------------------------------------------------------------
    s11 = prs.slides[10]
    for shape in s11.shapes:
        if shape.has_text_frame and "RESULTS" in shape.text:
            shape.text = "Future Scope & Scaling"
            break

    tx_box11 = s11.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.5), Inches(4.5))
    tf11 = tx_box11.text_frame
    tf11.word_wrap = True

    scopes = [
        ("1. Real-Time IoT & Smart Sensor Integration: ", "Integrate on-farm IoT sensors for continuous telemetry streaming of real-time soil moisture, temperature, and electrical conductivity to automate drip irrigation valves."),
        ("2. Satellite Remote Sensing & Computer Vision: ", "Leverage high-resolution Sentinel/Landsat multispectral imagery (NDVI, NDWI) and drone surveys to spot localized crop stress, nutrient deficiencies, and pest infestations."),
        ("3. Deep Learning & Transformer-based Weather Forecasting: ", "Incorporate regional numerical weather prediction and transformer models to predict monsoon onset anomalies, unseasonal rains, and heatwaves."),
        ("4. Mobile Decision Support Platform: ", "Deploy lightweight quantized XGBoost models into a multilingual mobile app offering personalized, voice-assisted advisories for rural farmers without continuous internet access.")
    ]

    for i, (head, body) in enumerate(scopes):
        p = tf11.add_paragraph() if i > 0 else tf11.paragraphs[0]
        p.space_after = Pt(14)
        r1 = p.add_run()
        r1.text = head
        r1.font.bold = True
        r1.font.size = Pt(14)
        r1.font.color.rgb = DARK_BLUE

        r2 = p.add_run()
        r2.text = body
        r2.font.bold = False
        r2.font.size = Pt(13)
        r2.font.color.rgb = CHARCOAL

    prs.save(output_ppt)
    print(f"Successfully saved populated presentation to {output_ppt}!")

if __name__ == "__main__":
    populate_presentation()
