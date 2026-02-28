-- Script para crear tabla e insertar datos de prueba
-- Ejecutar después de conectarse con: gcloud sql connect demo-db --user=postgres --database=mydb

-- Crear tabla de estudiantes
CREATE TABLE IF NOT EXISTS estudiantes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    carrera VARCHAR(100) NOT NULL,
    semestre INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Limpiar datos existentes (opcional)
TRUNCATE TABLE estudiantes RESTART IDENTITY;

-- Insertar datos de prueba
INSERT INTO estudiantes (nombre, carrera, semestre) VALUES
    ('Ana García', 'Ingeniería de Sistemas', 7),
    ('Carlos Ruiz', 'Ingeniería de Sistemas', 8),
    ('María López', 'Ingeniería Industrial', 6),
    ('Pedro Martínez', 'Ingeniería de Sistemas', 7),
    ('Laura Rodríguez', 'Ingeniería Electrónica', 5),
    ('Juan Pérez', 'Ingeniería de Sistemas', 9),
    ('Sofia González', 'Ingeniería Civil', 4),
    ('Diego Torres', 'Ingeniería de Sistemas', 8),
    ('Valentina Morales', 'Ingeniería Ambiental', 3),
    ('Andrés Silva', 'Ingeniería Mecánica', 6);

-- Verificar inserción
SELECT * FROM estudiantes ORDER BY nombre;

-- Mostrar estadísticas
SELECT 
    carrera, 
    COUNT(*) as total_estudiantes,
    ROUND(AVG(semestre), 1) as semestre_promedio
FROM estudiantes 
GROUP BY carrera 
ORDER BY total_estudiantes DESC;