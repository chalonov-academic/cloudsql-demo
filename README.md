# Demo: Cloud SQL PostgreSQL + Cloud Run

Aplicación de demostración que conecta Cloud Run con Cloud SQL PostgreSQL.

## Qué hace esta app

- Se conecta a una base de datos PostgreSQL en Cloud SQL
- Muestra información de la base de datos
- Lista estudiantes de una tabla de ejemplo

## Requisitos

- Cuenta de Google Cloud Platform
- gcloud CLI instalado

## Paso 1: Crear Cloud SQL PostgreSQL
```bash
# Crear instancia (tarda 5-10 minutos)
gcloud sql instances create demo-db \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=us-central1 \
    --root-password=Demo123456

# Crear base de datos
gcloud sql databases create mydb --instance=demo-db

# Obtener connection name
gcloud sql instances describe demo-db --format='value(connectionName)'
# Guarda este valor, lo necesitarás después
```

## Paso 2: Crear Tabla e Insertar Datos
```bash
# Conectarse a la base de datos
gcloud sql connect demo-db --user=postgres --database=mydb

# Dentro de psql, ejecutar:
```
```sql
-- Crear tabla
CREATE TABLE estudiantes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    carrera VARCHAR(100),
    semestre INTEGER
);

-- Insertar datos de prueba
INSERT INTO estudiantes (nombre, carrera, semestre) VALUES
    ('Ana García', 'Ingeniería de Sistemas', 7),
    ('Carlos Ruiz', 'Ingeniería de Sistemas', 8),
    ('María López', 'Ingeniería Industrial', 6),
    ('Pedro Martínez', 'Ingeniería de Sistemas', 7),
    ('Laura Rodríguez', 'Ingeniería Electrónica', 5),
    ('Juan Pérez', 'Ingeniería de Sistemas', 9),
    ('Sofia González', 'Ingeniería Civil', 4),
    ('Diego Torres', 'Ingeniería de Sistemas', 8);

-- Verificar
SELECT * FROM estudiantes;

-- Salir
\q
```

## Paso 3: Desplegar en Cloud Run
```bash
# Clonar repositorio
git clone https://github.com/chalonov-academic/cloudsql-demo.git
cd cloudsql-demo

# Configurar proyecto
PROJECT_ID=$(gcloud config get-value project)

# Obtener connection name
CONNECTION_NAME=$(gcloud sql instances describe demo-db --format='value(connectionName)')

# Build
gcloud builds submit --tag gcr.io/$PROJECT_ID/demo-sql

# Deploy
gcloud run deploy demo-sql \
    --image gcr.io/$PROJECT_ID/demo-sql \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 256Mi \
    --add-cloudsql-instances=$CONNECTION_NAME \
    --set-env-vars="CLOUD_SQL_CONNECTION=$CONNECTION_NAME,DB_NAME=mydb,DB_USER=postgres,DB_PASSWORD=Demo123456"

# Ver URL
gcloud run services describe demo-sql --region us-central1 --format='value(status.url)'
```

## Paso 4: Verificar

Abre la URL en tu navegador. Deberías ver:
- Mensaje de conexión exitosa
- Versión de PostgreSQL
- Lista de 8 estudiantes

## Costos

- Cloud SQL (db-f1-micro): ~$8/mes
- Cloud Run: ~$0/mes (dentro del free tier)

## Limpiar Recursos
```bash
# Eliminar servicio Cloud Run
gcloud run services delete demo-sql --region us-central1

# Eliminar instancia Cloud SQL
gcloud sql instances delete demo-db
```

## Estructura del Proyecto
```
cloudsql-demo/
├── app.py              # Aplicación Flask
├── requirements.txt    # Dependencias Python
├── Dockerfile         # Configuración del contenedor
└── README.md          # Esta documentación
```

## Troubleshooting

### Error: Cannot connect to Cloud SQL

Verifica que:
1. La instancia Cloud SQL está en estado RUNNABLE
2. El connection name es correcto
3. Las variables de entorno están configuradas

### Error: Table doesn't exist

Asegúrate de haber ejecutado los comandos SQL del Paso 2.

### Error: Authentication failed

Verifica que la contraseña en `--set-env-vars` sea correcta (Demo123456).
