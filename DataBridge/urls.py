from django.contrib import admin
from django.urls import path, include
from converter.views import index

urlpatterns = [
    # Page d'accueil
    path('', index, name='home'),
    # Outils
    path('tools/', include('converter.urls', namespace='converter')),
]
