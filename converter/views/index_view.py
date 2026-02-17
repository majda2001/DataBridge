# views_index.py
from django.shortcuts import render

def index(request):
    """Page d'accueil avec liens vers les outils"""
    return render(request, 'index.html')
