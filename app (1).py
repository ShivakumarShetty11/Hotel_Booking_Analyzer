# streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pyspark.sql import SparkSession, Row
from pyspark.ml import PipelineModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# Start Spark session
spark = SparkSession.builder.appName("HotelCancellationApp").getOrCreate()

# Define model paths
models = {
    "Logistic Regression": "hdfs://namenode:9000/models/LogisticRegression_model",
    "Decision Tree": "hdfs://namenode:9000/models/DecisionTree_model",
    "Random Forest": "hdfs://namenode:9000/models/RandomForest_model",
    "Gradient Boosted Trees": "hdfs://namenode:9000/models/GBTClassifier_model"
}

# Load and prepare data
df = spark.read.csv("hdfs://namenode:9000/data.csv", header=True, inferSchema=True).na.drop()
df = df.select("hotel", "lead_time", "adr", "total_of_special_requests", "is_canceled")
train_data, test_data = df.randomSplit([0.8, 0.2], seed=42)

# Page selection
st.sidebar.title("📚 Menu")
page = st.sidebar.radio("Choose Page", ["🧠 Prediction Inference", "📊 Model Evaluation"])

# ---------------------------
# 🧠 PAGE 1: PREDICTION INFERENCE
# ---------------------------
if page == "🧠 Prediction Inference":
    st.title("🧠 Hotel Booking Cancellation Prediction")

    with st.sidebar:
        st.header("🔧 Input Booking Features")
        hotel = st.selectbox("Hotel", ["City Hotel", "Resort Hotel"])
        lead_time = st.slider("Lead Time (days)", 0, 500, 100)
        adr = st.number_input("Average Daily Rate (ADR)", min_value=0.0, value=120.0)
        special_requests = st.slider("Total Special Requests", 0, 5, 1)
        selected_model = st.selectbox("Select Model", list(models.keys()))
        run_button = st.button("🚀 Predict")

    if run_button:
        model = PipelineModel.load(models[selected_model])
        input_df = spark.createDataFrame([Row(hotel=hotel, lead_time=lead_time, adr=adr, total_of_special_requests=special_requests)])
        result = model.transform(input_df).select("prediction", "probability").collect()[0]

        pred = int(result["prediction"])
        prob = result["probability"][1]  # Probability of cancellation

        st.subheader("📈 Prediction Result")
        st.write(f"**Prediction:** {'❌ Will Cancel' if pred else '✅ Will Not Cancel'}")
        st.write(f"**Probability of Cancellation:** `{prob*100:.2f}%`")

# ---------------------------
# 📊 PAGE 2: MODEL EVALUATION
# ---------------------------
elif page == "📊 Model Evaluation":
    st.title("📊 Model Evaluation & Comparison")

    evaluator = MulticlassClassificationEvaluator(labelCol="is_canceled", metricName="accuracy")
    results = []
    confusion_data = {}

    # Loop through all models
    for name, path in models.items():
        m = PipelineModel.load(path)
        preds = m.transform(test_data)
        acc = evaluator.evaluate(preds)
        results.append((name, acc))

        # Build confusion matrix
        matrix = preds.groupBy("is_canceled", "prediction").count().toPandas().pivot(
            index="is_canceled", columns="prediction", values="count"
        ).fillna(0)
        confusion_data[name] = matrix

    # Show accuracy table
    df_results = pd.DataFrame(results, columns=["Model", "Accuracy"]).sort_values("Accuracy", ascending=False)
    st.subheader("📋 Accuracy Comparison")
    st.dataframe(df_results.style.background_gradient(cmap="Greens"), use_container_width=True)

    # Show confusion matrices
    st.subheader("📉 Confusion Matrices")
    cols = st.columns(len(models))
    for i, (name, matrix) in enumerate(confusion_data.items()):
        with cols[i]:
            fig, ax = plt.subplots()
            ax.imshow(matrix.values, cmap='Blues')
            ax.set_title(name, fontsize=10)
            ax.set_xticks([0, 1])
            ax.set_yticks([0, 1])
            ax.set_xlabel("Prediction")
            ax.set_ylabel("Actual")
            for x in range(2):
                for y in range(2):
                    ax.text(y, x, int(matrix.iat[x, y]), ha='center', va='center', color='black')
            st.pyplot(fig)
