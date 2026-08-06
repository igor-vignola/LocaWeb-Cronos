# -*- coding: utf-8 -*-
"""Rotas do projeto."""
from django.urls import include, path

urlpatterns = [path('', include('painel.urls'))]
