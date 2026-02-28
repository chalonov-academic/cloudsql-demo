from flask import Flask, render_template_string
import psycopg2
import os

app = Flask(__name__)

def get_db():
    """Conectar a PostgreSQL en Cloud SQL"""
    conn = psycopg2.connect(
        host='/cloudsql/' + os.environ.get('CLOUD_SQL_CONNECTION'),
        database=os.environ.get('DB_NAME', 'mydb'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD')
    )
    return conn

@app.route('/')
def index():
    """Página principal con información de la base de datos"""
    try:
        conn = get_db()
        cur = conn.cursor()
        
        # Obtener versión de PostgreSQL
        cur.execute('SELECT version();')
        version = cur.fetchone()[0]
        
        # Contar estudiantes
        cur.execute('SELECT COUNT(*) FROM estudiantes;')
        total_estudiantes = cur.fetchone()[0]
        
        # Obtener lista de estudiantes
        cur.execute('SELECT nombre, carrera, semestre FROM estudiantes ORDER BY nombre;')
        estudiantes = cur.fetchall()
        
        cur.close()
        conn.close()
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Demo Cloud SQL</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }
                .container {
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }
                h1 {
                    color: #333;
                    border-bottom: 3px solid #667eea;
                    padding-bottom: 10px;
                }
                h2 {
                    color: #555;
                    margin-top: 30px;
                }
                .success {
                    background: #d4edda;
                    border: 1px solid #c3e6cb;
                    color: #155724;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }
                th, td {
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }
                th {
                    background-color: #667eea;
                    color: white;
                }
                tr:hover {
                    background-color: #f5f5f5;
                }
                .info {
                    background: #e7f3ff;
                    border-left: 4px solid #2196F3;
                    padding: 15px;
                    margin: 20px 0;
                }
                code {
                    background: #f4f4f4;
                    padding: 2px 6px;
                    border-radius: 3px;
                    font-family: monospace;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Conexión Exitosa a Cloud SQL PostgreSQL</h1>
                
                <div class="success">
                    <strong>Estado:</strong> Conectado correctamente a la base de datos
                </div>
                
                <div class="info">
                    <strong>Versión PostgreSQL:</strong><br>
                    <code>{{ version }}</code>
                </div>
                
                <h2>Estudiantes Registrados ({{ total }})</h2>
                
                <table>
                    <thead>
                        <tr>
                            <th>Nombre</th>
                            <th>Carrera</th>
                            <th>Semestre</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for estudiante in estudiantes %}
                        <tr>
                            <td>{{ estudiante[0] }}</td>
                            <td>{{ estudiante[1] }}</td>
                            <td>{{ estudiante[2] }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </body>
        </html>
        """
        
        return render_template_string(html, 
                                     version=version, 
                                     total=total_estudiantes,
                                     estudiantes=estudiantes)
        
    except Exception as e:
        return f"""
        <html>
        <body style="font-family: Arial; padding: 50px;">
            <h1 style="color: red;">Error de Conexión</h1>
            <p><strong>Detalles:</strong> {str(e)}</p>
            <hr>
            <p>Verifica que:</p>
            <ul>
                <li>Cloud SQL está creado y en ejecución</li>
                <li>Las variables de entorno están configuradas</li>
                <li>Cloud Run tiene permisos para conectarse</li>
            </ul>
        </body>
        </html>
        """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))