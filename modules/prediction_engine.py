import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Definisi path model dan scaler
MODELS_CONFIG = {
    "KNN": {
        "model_path": "models/knn/knn_model.pkl",
        "scaler_path": "models/knn/scaler.pkl"
    },
    "SVM": {
        "model_path": "models/svm/svm_model.pkl",
        "scaler_path": "models/svm/scaler.pkl"
    },
    "Decision Tree": {
        "model_path": "models/decision_tree/decesiontree_model.pkl",
        "scaler_path": "models/decision_tree/scaler.pkl"
    },
    "Neural Network": {
        "model_path": "models/neural_network/nn_model.pkl",
        "scaler_path": "models/neural_network/scalernn.pkl"
    }
}

@st.cache_resource
def load_all_models():
    """Memuat semua model dan scaler ke dalam memory dengan cache Streamlit."""
    loaded = {}
    for name, config in MODELS_CONFIG.items():
        try:
            model = joblib.load(config["model_path"])
            scaler = joblib.load(config["scaler_path"])
            loaded[name] = {
                "model": model,
                "scaler": scaler,
                "status": "success"
            }
        except Exception as e:
            loaded[name] = {
                "model": None,
                "scaler": None,
                "status": f"Gagal memuat model: {e}"
            }
    return loaded

def predict_single(model_name, features_df):
    """
    Melakukan prediksi menggunakan model tunggal.
    features_df: DataFrame pandas berisi 13 kolom fitur pasien
    """
    models = load_all_models()
    if model_name not in models or models[model_name]["status"] != "success":
        raise ValueError(f"Model {model_name} tidak tersedia atau gagal dimuat.")
    
    scaler = models[model_name]["scaler"]
    model = models[model_name]["model"]
    
    # Scale data
    scaled_data = scaler.transform(features_df)
    
    # Predict
    predictions = model.predict(scaled_data)
    
    # Try to get prediction probability if available
    probabilities = None
    if hasattr(model, "predict_proba"):
        try:
            probabilities = model.predict_proba(scaled_data)[:, 1]
        except:
            pass
            
    return predictions, probabilities

def predict_all(features_df):
    """
    Melakukan prediksi menggunakan seluruh model yang tersedia.
    Mengembalikan dictionary hasil prediksi masing-masing model.
    """
    results = {}
    for name in MODELS_CONFIG.keys():
        try:
            preds, probs = predict_single(name, features_df)
            results[name] = {
                "status": "success",
                "prediction": preds,
                "probability": probs
            }
        except Exception as e:
            results[name] = {
                "status": "failed",
                "error": str(e)
            }
    return results
