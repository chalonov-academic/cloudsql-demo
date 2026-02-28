#!/bin/bash

# Script de despliegue automático
# Uso: ./deploy.sh

set -e

echo "=========================================="
echo "Desplegando Demo Cloud SQL"
echo "=========================================="

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "Error: No se encuentra app.py"
    echo "Asegúrate de estar en el directorio cloudsql-demo"
    exit 1
fi

# Obtener PROJECT_ID
PROJECT_ID=$(gcloud config get-value project)
if [ -z "$PROJECT_ID" ]; then
    echo "Error: No hay proyecto configurado"
    echo "Ejecuta: gcloud config set project TU-PROJECT-ID"
    exit 1
fi

echo "Proyecto: $PROJECT_ID"

# Verificar que Cloud SQL existe
if ! gcloud sql instances describe demo-db &>/dev/null; then
    echo "Error: La instancia demo-db no existe"
    echo "Ejecuta primero:"
    echo "  gcloud sql instances create demo-db --database-version=POSTGRES_15 --tier=db-f1-micro --region=us-central1 --root-password=Demo123456"
    exit 1
fi

# Obtener connection name
CONNECTION_NAME=$(gcloud sql instances describe demo-db --format='value(connectionName)')
echo "Connection Name: $CONNECTION_NAME"

# Build
echo ""
echo "Construyendo imagen..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/demo-sql

# Deploy
echo ""
echo "Desplegando en Cloud Run..."
gcloud run deploy demo-sql \
    --image gcr.io/$PROJECT_ID/demo-sql \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 256Mi \
    --add-cloudsql-instances=$CONNECTION_NAME \
    --set-env-vars="CLOUD_SQL_CONNECTION=$CONNECTION_NAME,DB_NAME=mydb,DB_USER=postgres,DB_PASSWORD=Demo123456"

# Obtener URL
SERVICE_URL=$(gcloud run services describe demo-sql --region us-central1 --format='value(status.url)')

echo ""
echo "=========================================="
echo "Despliegue completado exitosamente!"
echo "=========================================="
echo "URL: $SERVICE_URL"
echo ""
echo "Abre esta URL en tu navegador para ver la app"
echo "=========================================="