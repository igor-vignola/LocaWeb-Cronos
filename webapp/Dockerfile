# Cronos · imagem da aplicação.
# Agnóstica de provedor: roda em qualquer lugar que aceite um contêiner escutando $PORT.
#
# O contexto de build é a RAIZ do repositório, porque a imagem precisa de webapp/ e de
# data/app/ ao mesmo tempo:
#     docker build -f webapp/Dockerfile -t cronos .
#     docker run --rm -p 8000:8000 cronos
#
# Prophet, scikit-learn e xgboost ficam de fora de propósito: eles rodam nos notebooks,
# gravam parquet, e o contêiner apenas lê. É isso que mantém a imagem pequena e permite
# a entrega rodar em plano gratuito.
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CRONOS_DEBUG=0 \
    CRONOS_DADOS=/app/dados

WORKDIR /app

COPY webapp/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY webapp/ /app/
# o pacote agregado pelos notebooks: painel.json e fila.parquet, cerca de 295 kB
COPY data/app/ /app/dados/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Um processo, varias threads. A aplicacao le arquivo e guarda o pacote em lru_cache, entao
# cada worker extra duplica os 130 MB do parquet e dos JSON em memoria — em plano gratuito de
# 512 MB isso derruba o contêiner por falta de memoria. Thread compartilha o mesmo cache e
# atende concorrencia de leitura sem pagar essa copia.
#
# ${PORT:-8000} porque o provedor injeta a porta em variavel de ambiente; o 8000 e o padrao
# de quem roda a imagem na mao.
CMD ["sh", "-c", "gunicorn cronos.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 1 --threads 8 --timeout 120 --access-logfile - --error-logfile -"]
