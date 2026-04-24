from django.db import models

class LoanPrediction(models.Model):
    GENDER_CHOICES = [('Male', 'Homme'), ('Female', 'Femme')]
    MARRIED_CHOICES = [('Yes', 'Oui'), ('No', 'Non')]
    DEPENDENTS_CHOICES = [('0', '0'), ('1', '1'), ('2', '2'), ('3+', '3+')]
    EDUCATION_CHOICES = [('Graduate', 'Diplômé'), ('Not Graduate', 'Non Diplômé')]
    SELF_EMPLOYED_CHOICES = [('Yes', 'Oui'), ('No', 'Non')]
    PROPERTY_AREA_CHOICES = [('Urban', 'Urbain'), ('Semiurban', 'Semi-urbain'), ('Rural', 'Rural')]

    full_name = models.CharField(max_length=100, verbose_name="Nom Complet")
    applicant_income = models.FloatField(verbose_name="Revenu du Demandeur")
    coapplicant_income = models.FloatField(default=0, verbose_name="Revenu du Co-demandeur")
    loan_amount = models.FloatField(verbose_name="Montant du Prêt (en k$)")
    loan_amount_term = models.FloatField(default=360, verbose_name="Durée du Prêt (en jours)")
    credit_history = models.FloatField(choices=[(1.0, 'Bon'), (0.0, 'Mauvais')], verbose_name="Historique de Crédit")
    
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Genre")
    married = models.CharField(max_length=10, choices=MARRIED_CHOICES, verbose_name="Marié")
    dependents = models.CharField(max_length=10, choices=DEPENDENTS_CHOICES, verbose_name="Personnes à charge")
    education = models.CharField(max_length=20, choices=EDUCATION_CHOICES, verbose_name="Éducation")
    self_employed = models.CharField(max_length=10, choices=SELF_EMPLOYED_CHOICES, verbose_name="Travailleur indépendant")
    property_area = models.CharField(max_length=20, choices=PROPERTY_AREA_CHOICES, verbose_name="Zone de propriété")

    # Result fields
    prediction_result = models.BooleanField(null=True, blank=True)
    prediction_probability = models.FloatField(null=True, blank=True)
    explanation = models.TextField(null=True, blank=True, verbose_name="Analyse Détaillée")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {'Approuvé' if self.prediction_result else 'Refusé'}"
