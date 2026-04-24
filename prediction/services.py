import google.generativeai as genai
import os

def generate_credit_explanation(prediction_obj):
    """
    Utilise Gemini 2.5 Flash pour générer une explication diplomatique et experte
    basée sur les résultats de la prédiction ML.
    """
    try:
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            return "Note de l'analyste : Erreur de configuration API (Clé manquante)."

        genai.configure(api_key=api_key)
        
        # Mise à jour vers le modèle stable : gemini-1.5-flash (meilleur quota)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        status = "approuvé" if prediction_obj.prediction_result else "refusé"
        confidence = f"{prediction_obj.prediction_probability * 100:.2f}%"
        
        prompt = f"""
        Tu es un expert en analyse de crédit bancaire pour la plateforme AideBanque.
        Un dossier client vient d'être traité par notre algorithme de Machine Learning.
        
        RÉSULTAT DU DOSSIER :
        - Statut : {status}
        - Score de confiance : {confidence}
        - Client : {prediction_obj.full_name}
        - Revenu mensuel : {prediction_obj.applicant_income} $
        - Montant demandé : {prediction_obj.loan_amount} k$
        - Historique de crédit : {"Favorable" if prediction_obj.credit_history == 1.0 else "Défavorable"}
        - Niveau d'éducation : {prediction_obj.education}
        
        TA MISSION :
        Rédige une note de synthèse professionnelle (5 à 10 lignes) destinée au conseiller bancaire.
        - Si le crédit est approuvé, souligne les points forts.
        - Si le crédit est refusé, explique avec diplomatie les facteurs de risque et donne des conseils pour le futur.
        - Ton ton doit être expert, précis et institutionnel.
        """
        
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"Erreur Gemini : {e}")
        return f"Note de l'analyste : L'analyse automatisée a conclu à un profil {'à risque' if not prediction_obj.prediction_result else 'favorable'} basé sur les données fournies. (Service IA indisponible actuellement)"
