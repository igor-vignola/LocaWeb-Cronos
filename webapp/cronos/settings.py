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
ALLOWED_HOSTS = [h.strip() for h in os.environ.get('CRONOS_HOSTS', '*').split(',') if h.strip()]

# As origens confiaveis saem dos proprios hosts quando CRONOS_ORIGENS nao vem preenchida:
# em provedor de contêiner o dominio so e conhecido depois do primeiro deploy, e obrigar duas
# variaveis para a mesma informacao e um passo a mais para errar. `*` nao gera origem porque
# curinga nao e origem valida, e host sem ponto (localhost) nao precisa constar.
_ORIGENS_ENV = [o.strip() for o in os.environ.get('CRONOS_ORIGENS', '').split(',') if o.strip()]
CSRF_TRUSTED_ORIGINS = _ORIGENS_ENV or [
    f'https://{h.lstrip(".")}' for h in ALLOWED_HOSTS if h != '*' and '.' in h
]

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
# Numero em template NAO pode ser localizado: coordenada de SVG com virgula
# decimal quebra path e rect sem avisar. Data continua em pt-BR pelo LANGUAGE_CODE.
USE_THOUSAND_SEPARATOR = False
DECIMAL_SEPARATOR = '.'
NUMBER_GROUPING = 0
USE_TZ = True

STATIC_URL = 'estatico/'
STATIC_ROOT = BASE_DIR / 'estatico'
# O whitenoise serve o estatico no processo da aplicacao. E o que dispensa nginx e volume no
# provedor: com DEBUG=False o Django nao serve estatico, e sem isto a pagina sobe sem CSS.
# So `STORAGES` e lido — a chave STATICFILES_STORAGE saiu do Django na versao 5.1.
STORAGES = {
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if not DEBUG:
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = 'same-origin'
    X_FRAME_OPTIONS = 'DENY'
    # O TLS termina no proxy do provedor, que repassa a requisicao em http e sinaliza o
    # esquema original neste cabecalho. Sem ele o Django trata a conexao como insegura.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
