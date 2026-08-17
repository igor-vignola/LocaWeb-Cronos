# -*- coding: utf-8 -*-
"""Rotas do painel. Uma por aba, mais os fragmentos que o modal busca."""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.panorama, name='panorama'),
    path('projecao/', views.projecao, name='projecao'),
    path('fila/', views.fila, name='fila'),
    path('saude/', views.saude, name='saude'),
    path('causas/', views.causas, name='causas'),
    path('previsao/', views.previsao, name='previsao'),
    path('detalhe/incidente/<str:codigo>/', views.det_incidente, name='det_incidente'),
    path('detalhe/ativo/<str:codigo>/', views.det_ativo, name='det_ativo'),
    path('detalhe/produto/<str:codigo>/', views.det_produto, name='det_produto'),
    path('detalhe/meta/<str:pri>/', views.det_meta, name='det_meta'),
    path('busca.json', views.busca, name='busca'),
]
