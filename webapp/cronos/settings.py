# -*- coding: utf-8 -*-
"""Configuracao do Cronos.

Aplicacao de leitura: nao ha banco, nao ha login, nao ha escrita. Os dados vem de
arquivos gerados pelos notebooks. Por isso nao existe app de sessao nem migracao.
Agnostica de provedor: nada aqui amarra a AWS, GCP ou Azure.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Em producao a chave vem do ambiente. O valor abaixo so serve para rodar local.
SECRET_KEY = os.environ.get('CRONOS_SECRET_KEY', 'apenas-para-desenvolvimento-local')
DEBUG = os.environ.get('CRONOS_DEBUG', '1') == '1'

# Aceita o host que o provedor injetar, sem precisar reconstruir a imagem
ALLOWED_HOSTS = [h for h in os.environ.get('CRONOS_HOSTS', '*').split(',') if h]
CSRF_TRUSTED_ORIGINS = [o for o in os.environ.get('CRONOS_ORIGENS', '').split(',') if o]

# Onde estao painel.json e fila.parquet
DADOS_DIR = os.environ.get('CRONOS_DADOS', str(BASE_DIR.parent / 'data' / 'app'))

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'painel',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'cronos.urls'
WSGI_APPLICATION = 'cronos.wsgi.application'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'painel' / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': ['django.template.context_processors.request']},
}]

DATABASES = {}          # sem banco: a aplicacao so le arquivo

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'estatico/'
STATIC_ROOT = BASE_DIR / 'estatico'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STORAGES = {
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if not DEBUG:
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = 'same-origin'
    X_FRAME_OPTIONS = 'DENY'
