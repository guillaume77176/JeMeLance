import json
import pandas as pd
import numpy
import joblib

def load_model():
    
    model1 = joblib.load("xgb_radié1.pkl")
    model2 = joblib.load("xgb_radié2.pkl")
    model3 = joblib.load("xgb_radié3.pkl")
    model4 = joblib.load("xgb_radié4.pkl")
    model5 = joblib.load("xgb_radié5.pkl")

    return model1,model2,model3,model4,model5

def load_threshold():

    with open("seuils_proba_xgb.json", "r") as f:
        liste_th = json.load(f)
        
    return liste_th

