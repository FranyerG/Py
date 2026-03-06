import sys
import os
import random
from datetime import datetime

# Detectar el entorno
def es_entorno_web():
    """Detecta si estamos en un entorno que espera una aplicación web"""
    return any([
        'REPL_ID' in os.environ,  # Replit
        'FLASK_ENV' in os.environ,
        'PORT' in os.environ,
        'DYNO' in os.environ,  # Heroku
        'K_SERVICE' in os.environ,  # Google Cloud Run
        'WEBSITE_HOSTNAME' in os.environ,  # Azure
    ])

# Modo Web (usando Flask)
if es_entorno_web() or len(sys.argv) > 1 and sys.argv[1] == 'web':
    try:
        from flask import Flask, render_template_string, request, redirect, url_for
        
        app = Flask(__name__)
        
        # Base de datos simple
        tareas = []
        contador_id = 1
        
        HTML_TEMPLATE = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Mi Página Web</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }
                .container {
                    background: white;
                    padding: 30px;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                }
                h1 {
                    color: #333;
                    text-align: center;
                    margin-bottom: 30px;
                }
                .mensaje {
                    background: #4CAF50;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                    text-align: center;
                    margin: 10px 0;
                    animation: slideIn 0.5s;
                }
                @keyframes slideIn {
                    from { transform: translateY(-20px); opacity: 0; }
                    to { transform: translateY(0); opacity: 1; }
                }
                form {
                    display: flex;
                    gap: 10px;
                    margin: 20px 0;
                }
                input[type="text"] {
                    flex: 1;
                    padding: 12px;
                    border: 2px solid #ddd;
                    border-radius: 8px;
                    font-size: 16px;
                    transition: border-color 0.3s;
                }
                input[type="text"]:focus {
                    border-color: #667eea;
                    outline: none;
                }
                button {
                    padding: 12px 24px;
                    background: #667eea;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 16px;
                    transition: transform 0.3s, background 0.3s;
                }
                button:hover {
                    background: #764ba2;
                    transform: translateY(-2px);
                }
                ul {
                    list-style: none;
                    padding: 0;
                }
                li {
                    padding: 15px;
                    background: #f9f9f9;
                    margin: 10px 0;
                    border-radius: 8px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    animation: fadeIn 0.5s;
                }
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateX(-20px); }
                    to { opacity: 1; transform: translateX(0); }
                }
                .completada {
                    text-decoration: line-through;
                    color: #888;
                }
                .btn-eliminar {
                    background: #f44336;
                    padding: 8px 16px;
                }
                .btn-eliminar:hover {
                    background: #da190b;
                }
                .stats {
                    display: flex;
                    justify-content: space-around;
                    margin-top: 30px;
                    padding: 20px;
                    background: #f0f0f0;
                    border-radius: 8px;
                }
                .stat-item {
                    text-align: center;
                }
                .stat-value {
                    font-size: 24px;
                    font-weight: bold;
                    color: #667eea;
                }
                .stat-label {
                    color: #666;
                    font-size: 14px;
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
                <h1>📝 Lista de Tareas</h1>
                
                {% if mensaje %}
                <div class="mensaje">{{ mensaje }}</div>
                {% endif %}
                
                <form method="POST" action="/agregar">
                    <input type="text" name="tarea" placeholder="¿Qué necesitas hacer?" required>
                    <button type="submit">Agregar</button>
                </form>
                
                <ul>
                    {% for tarea in tareas %}
                    <li>
                        <span class="{% if tarea.completada %}completada{% endif %}">
                            {{ tarea.texto }}
                        </span>
                        <div>
                            <form method="POST" action="/completar/{{ tarea.id }}" style="display: inline;">
                                <button type="submit" style="background: #4CAF50;">
                                    {% if tarea.completada %}↩️{% else %}✅{% endif %}
                                </button>
                            </form>
                            <form method="POST" action="/eliminar/{{ tarea.id }}" style="display: inline;">
                                <button type="submit" class="btn-eliminar">🗑️</button>
                            </form>
                        </div>
                    </li>
                    {% endfor %}
                </ul>
                
                <div class="stats">
                    <div class="stat-item">
                        <div class="stat-value">{{ tareas|length }}</div>
                        <div class="stat-label">Total</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{{ tareas|selectattr('completada', 'equalto', true)|list|length }}</div>
                        <div class="stat-label">Completadas</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{{ tareas|rejectattr('completada', 'equalto', true)|list|length }}</div>
                        <div class="stat-label">Pendientes</div>
                    </div>
                </div>
                
                <div class="footer">
                    <p>🕒 {{ fecha }} • 🌐 Modo Web</p>
                </div>
            </div>
        </body>
        </html>
        '''
        
        @app.route('/')
        def index():
            mensaje = request.args.get('mensaje', '')
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
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
            
            return redirect(url_for('index', mensaje=f'✅ "{texto_tarea}" agregada'))
        
        @app.route('/completar/<int:tarea_id>', methods=['POST'])
        def completar(tarea_id):
            for tarea in tareas:
                if tarea['id'] == tarea_id:
                    tarea['completada'] = not tarea['completada']
                    estado = "completada" if tarea['completada'] else "pendiente"
                    return redirect(url_for('index', mensaje=f'📌 Tarea marcada como {estado}'))
            return redirect(url_for('index', mensaje='❌ Error'))
        
        @app.route('/eliminar/<int:tarea_id>', methods=['POST'])
        def eliminar(tarea_id):
            global tareas
            tareas = [t for t in tareas if t['id'] != tarea_id]
            return redirect(url_for('index', mensaje='🗑️ Tarea eliminada'))
        
        if __name__ == '__main__':
            # Tareas de ejemplo
            tareas.append({'id': 1, 'texto': 'Aprender Python', 'completada': True})
            tareas.append({'id': 2, 'texto': 'Crear una app web', 'completada': False})
            tareas.append({'id': 3, 'texto': 'Compartir el código', 'completada': False})
            contador_id = 4
            
            print("\n" + "="*50)
            print("🚀 MODO WEB ACTIVADO")
            print("🌐 Servidor iniciado en http://localhost:5000")
            print("📝 Presiona CTRL+C para detener")
            print("="*50 + "\n")
            app.run(host='0.0.0.0', port=5000, debug=True)
            
    except ImportError:
        print("❌ Flask no está instalado. Ejecuta: pip install flask")
        print("💡 Ejecutando en modo consola en su lugar...\n")
        modo_consola()

# Modo Consola
else:
    def juego_adivinanza():
        print("\n" + "="*50)
        print("🎮 JUEGO DE ADIVINANZA")
        print("="*50)
        print("Estoy pensando en un número entre 1 y 100.")
        
        numero_secreto = random.randint(1, 100)
        intentos = 0
        adivinado = False
        
        while not adivinado:
            try:
                guess = int(input("\n🔢 Tu adivinanza: "))
                intentos += 1
                
                if guess < numero_secreto:
                    print("📉 ¡Demasiado bajo!")
                elif guess > numero_secreto:
                    print("📈 ¡Demasiado alto!")
                else:
                    print(f"\n🎉 ¡FELICIDADES! Adivinaste en {intentos} intentos.")
                    
                    if intentos == 1:
                        print("✨ ¡Increíble! ¡A la primera!")
                    elif intentos <= 5:
                        print("🌟 ¡Muy bien!")
                    elif intentos <= 10:
                        print("👍 Bien hecho")
                    else:
                        print("💪 ¡Lo lograste!")
                    
                    adivinado = True
                    
            except ValueError:
                print("❌ Por favor, introduce un número válido.")
        
        jugar_again = input("\n¿Quieres jugar de nuevo? (s/n): ").lower()
        if jugar_again == 's':
            juego_adivinanza()
        else:
            print("\n👋 ¡Gracias por jugar! ¡Hasta luego!")
            print("="*50)

    if __name__ == "__main__":
        print("\n" + "🌟"*20)
        print("BIENVENIDO AL PROGRAMA")
        print("🌟"*20 + "\n")
        
        print("Selecciona el modo:")
        print("1️⃣  Modo Consola (Juego de Adivinanza)")
        print("2️⃣  Modo Web (Lista de Tareas)")
        print("3️⃣  Detectar automáticamente")
        
        opcion = input("\nElige (1/2/3): ")
        
        if opcion == '2':
            print("\n🔄 Cambiando a modo web...")
            print("💡 Ejecuta con 'python main.py web' para modo web directo")
            os.system(f'{sys.executable} "{__file__}" web')
        elif opcion == '1':
            juego_adivinanza()
        else:
            juego_adivinanza()
