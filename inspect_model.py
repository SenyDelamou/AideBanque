import pickle
import os

model_path = r'c:\Users\DELAMOU_Samaké\Desktop\AideBanque\modele_regression_logistique_le_plus_performant.pkl'

try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    print(f"Type de modèle: {type(model)}")
    
    if hasattr(model, 'feature_names_in_'):
        print(f"Features: {model.feature_names_in_}")
    elif hasattr(model, 'n_features_in_'):
        print(f"Nombre de features: {model.n_features_in_}")
    else:
        print("Impossible de déterminer les features automatiquement.")

    # Tentative d'accès aux classes de sortie
    if hasattr(model, 'classes_'):
        print(f"Classes de sortie: {model.classes_}")

except Exception as e:
    print(f"Erreur lors du chargement du modèle: {e}")
