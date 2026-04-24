import pickle
import numpy as np
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from .models import LoanPrediction
from .services import generate_credit_explanation
from django.contrib import messages
from django.http import JsonResponse
import os
from django.conf import settings
import google.generativeai as genai

# Load model globally to avoid reloading on each request
MODEL_PATH = os.path.join(settings.BASE_DIR, 'modele_regression_logistique_le_plus_performant.pkl')

def load_ml_model():
    try:
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Erreur chargement modèle : {e}")
        return None

model = load_ml_model()

def landing_page(request):
    """Page de présentation de l'application."""
    return render(request, 'prediction/landing.html')

def dashboard(request):
    predictions = LoanPrediction.objects.all().order_by('-created_at')
    total_count = predictions.count()
    approved_count = predictions.filter(prediction_result=True).count()
    denied_count = predictions.filter(prediction_result=False).count()
    
    context = {
        'predictions': predictions[:15], # Top 15 for display
        'total_count': total_count,
        'approved_count': approved_count,
        'denied_count': denied_count,
    }
    return render(request, 'prediction/dashboard.html', context)

def predict_view(request):
    if request.method == 'POST':
        try:
            full_name = request.POST.get('full_name')
            applicant_income = float(request.POST.get('applicant_income'))
            coapplicant_income = float(request.POST.get('coapplicant_income', 0))
            loan_amount = float(request.POST.get('loan_amount'))
            loan_amount_term = float(request.POST.get('loan_amount_term'))
            credit_history = float(request.POST.get('credit_history'))
            gender = request.POST.get('gender')
            married = request.POST.get('married')
            dependents = request.POST.get('dependents')
            education = request.POST.get('education')
            self_employed = request.POST.get('self_employed')
            property_area = request.POST.get('property_area')

            # Mapping for model
            mapping = {
                'Gender': 1 if gender == 'Male' else 0,
                'Married': 1 if married == 'Yes' else 0,
                'Dependents': 3 if dependents == '3+' else int(dependents),
                'Education': 1 if education == 'Graduate' else 0,
                'Self_Employed': 1 if self_employed == 'Yes' else 0,
                'Property_Area': {'Rural': 0, 'Semiurban': 1, 'Urban': 2}[property_area]
            }

            # Create feature array
            features = np.array([[
                applicant_income, coapplicant_income, loan_amount, loan_amount_term, credit_history,
                mapping['Gender'], mapping['Married'], mapping['Dependents'], 
                mapping['Education'], mapping['Self_Employed'], mapping['Property_Area']
            ]])

            # ML Prediction
            prediction = model.predict(features)[0]
            probability = model.predict_proba(features)[0][1]

            # Initial object
            obj = LoanPrediction(
                full_name=full_name,
                applicant_income=applicant_income,
                coapplicant_income=coapplicant_income,
                loan_amount=loan_amount,
                loan_amount_term=loan_amount_term,
                credit_history=credit_history,
                gender=gender,
                married=married,
                dependents=dependents,
                education=education,
                self_employed=self_employed,
                property_area=property_area,
                prediction_result=bool(prediction),
                prediction_probability=probability
            )

            # Generate Gemini Explanation
            explanation = generate_credit_explanation(obj)
            obj.explanation = explanation
            obj.save()

            return render(request, 'prediction/result.html', {'prediction': obj})

        except Exception as e:
            messages.error(request, f"Erreur lors de la prédiction : {e}")
            return redirect('predict_form')

    return render(request, 'prediction/predict_form.html')

def prediction_detail(request, pk):
    prediction = get_object_or_404(LoanPrediction, pk=pk)
    return render(request, 'prediction/result.html', {'prediction': prediction})

def delete_prediction(request, pk):
    prediction = get_object_or_404(LoanPrediction, pk=pk)
    prediction.delete()
    messages.success(request, "L'analyse a été supprimée avec succès.")
    return redirect('dashboard')

def delete_all_predictions(request):
    if request.method == 'POST':
        LoanPrediction.objects.all().delete()
        messages.success(request, "Tout l'historique a été vidé.")
    return redirect('dashboard')

def chat_api(request):
    """API pour le chatbot AideBanque utilisant Gemini 2.5 Flash."""
    if request.method == 'POST':
        user_message = request.POST.get('message')
        if not user_message:
            return JsonResponse({'error': 'Message vide'}, status=400)
        
        try:
            api_key = os.environ.get('GEMINI_API_KEY')
            genai.configure(api_key=api_key)
            # Utilisation de gemini-1.5-flash pour un meilleur quota
            model_gemini = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Tu es l'assistant IA de l'application AideBanque, une plateforme de scoring de crédit.
            Ton but est d'aider les conseillers bancaires et les clients.
            Sois professionnel, expert en finance, et chaleureux.
            L'utilisateur dit : "{user_message}"
            Réponds de manière concise.
            """
            
            response = model_gemini.generate_content(prompt)
            return JsonResponse({'reply': response.text})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
