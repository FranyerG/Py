from flask import Flask, render_template_string, request, redirect, url_for
import random

app = Flask(__name__)

# Base de datos simple en memoria (lista de diccionarios)
tareas = []
contador_id = 1

# Template HTML como string
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Mi Página Web con Python</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f0f0f0;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .mensaje {
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            margin: 10px 0;
        }
        form {
            display: flex;
            gap: 10px;
            margin: 20px 0;
        }
        input[type="text"] {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #45a049;
        }
        ul {
            list-style: none;
            padding: 0;
        }
        li {
            padding: 10px;
            background-color: #f9f9f9;
            margin: 5px 0;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .completada {
            text-decoration: line-through;
            color: #888;
        }
        .eliminar {
            background-color: #f44336;
            padding: 5px 10px;
            font-size: 14px;
        }
        .eliminar:hover {
            background-color: #da190b;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 Mi Lista de Tareas</h1>
        
        {% if mensaje %}
        <div class="mensaje">{{ mensaje }}</div>
        {% endif %}
        
        <form method="POST" action="/agregar">
            <input type="text" name="tarea" placeholder="Escribe una nueva tarea..." required>
            <button type="submit">Agregar Tarea</button>
        </form>
        
        <ul>
            {% for tarea in tareas %}
            <li>
                <span class="{% if tarea.completada %}completada{% endif %}">
                    {{ tarea.texto }}
                </span>
                <div>
                    <form method="POST" action="/completar/{{ tarea.id }}" style="display: inline;">
                        <button type="submit" class="{% if tarea.completada %}eliminar{% endif %}">
                            {% if tarea.completada %}Desmarcar{% else %}Completar{% endif %}
                        </button>
                    </form>
                    <form method="POST" action="/eliminar/{{ tarea.id }}" style="display: inline;">
                        <button type="submit" class="eliminar">Eliminar</button>
                    </form>
                </div>
            </li>
            {% endfor %}
        </ul>
        
        <div class="footer">
            <p>Total de tareas: {{ tareas|length }}</p>
            <p>Hechas: {{ tareas|selectattr('completada', 'equalto', true)|list|length }}</p>
            <p>Pendientes: {{ tareas|rejectattr('completada', 'equalto', true)|list|length }}</p>
            <hr>
            <p>💡 Dato curioso: Hoy es {{ fecha }}</p>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    mensaje = request.args.get('mensaje', '')
    from datetime import datetime
    fecha = datetime.now().strftime("%d/%m/%Y")
    return render_template_string(HTML_TEMPLATE, tareas=tareas, mensaje=mensaje, fecha=fecha)

@app.route('/agregar', methods=['POST'])
def agregar():
    global contador_id
    texto_tarea = request.form['tarea']
    
    nueva_tarea = {
        'id': contador_id,
        'texto': texto_tarea,
        'completada': False
    }
    tareas.append(nueva_tarea)
    contador_id += 1
    
    return redirect(url_for('index', mensaje=f'✅ Tarea "{texto_tarea}" agregada con éxito!'))

@app.route('/completar/<int:tarea_id>', methods=['POST'])
def completar(tarea_id):
    for tarea in tareas:
        if tarea['id'] == tarea_id:
            tarea['completada'] = not tarea['completada']
            estado = "completada" if tarea['completada'] else "pendiente"
            return redirect(url_for('index', mensaje=f'📌 Tarea marcada como {estado}'))
    return redirect(url_for('index', mensaje='❌ Tarea no encontrada'))

@app.route('/eliminar/<int:tarea_id>', methods=['POST'])
def eliminar(tarea_id):
    global tareas
    tarea_eliminada = None
    for tarea in tareas:
        if tarea['id'] == tarea_id:
            tarea_eliminada = tarea['texto']
            tareas = [t for t in tareas if t['id'] != tarea_id]
            break
    
    if tarea_eliminada:
        return redirect(url_for('index', mensaje=f'🗑️ Tarea "{tarea_eliminada}" eliminada'))
    return redirect(url_for('index', mensaje='❌ Tarea no encontrada'))

if __name__ == '__main__':
    # Agregar algunas tareas de ejemplo
    tareas.append({'id': 1, 'texto': 'Aprender Python', 'completada': True})
    tareas.append({'id': 2, 'texto': 'Hacer una página web', 'completada': False})
    tareas.append({'id': 3, 'texto': 'Compartir el código', 'completada': False})
    contador_id = 4
    
    print("🚀 Servidor web iniciado!")
    print("🌐 Abre tu navegador en: http://localhost:5000")
    print("🔧 Presiona CTRL+C para detener el servidor")
    app.run(debug=True)
