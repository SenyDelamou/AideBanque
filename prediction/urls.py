from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('presentation/', views.landing_page, name='landing'),
    path('predict/', views.predict_view, name='predict_form'),
    path('detail/<int:pk>/', views.prediction_detail, name='prediction_detail'),
    path('delete/<int:pk>/', views.delete_prediction, name='delete_prediction'),
    path('delete-all/', views.delete_all_predictions, name='delete_all'),
    path('api/chat/', views.chat_api, name='chat_api'),
]
