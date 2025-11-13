"""
App de monitoreo y análisis cuántico con IA avanzada
Conecta con el sistema de IA cuántica para métricas en tiempo real
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import json
import socket

app = FastAPI(title="Centro de Datos Cuántico - Analítica & IA")

# Cargar estado simulado desde el servidor cuántico
ESTADO_PATH = os.path.join(os.path.dirname(__file__), "estado_simulado.json")

def conectar_servidor(comando: str = "STATUS") -> dict:
    """Conecta al servidor cuántico para obtener datos en tiempo real"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', 5555))
        s.sendall(comando.encode('utf-8'))
        data = s.recv(16384)
        s.close()
        return json.loads(data.decode('utf-8'))
    except Exception as e:
        print(f"Error conectando al servidor: {e}")
        return cargar_estado()

def cargar_estado():
    """Carga estado simulado como fallback"""
    if os.path.exists(ESTADO_PATH):
        with open(ESTADO_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Centro de Datos Cuántico con IA</title>
        <link rel='stylesheet' href='/static/style.css'>
    </head>
    <body>
        <h1>🔮 Centro de Datos Cuántico + 🤖 IA</h1>
        <div id='panel'></div>
        <div id='ia-panel' style='margin-top: 20px;'></div>
        <script src='/static/app.js'></script>
    </body>
    </html>
    """

@app.get("/estado")
def estado():
    """Obtiene estado completo desde el servidor cuántico"""
    estado = conectar_servidor("STATUS")
    return JSONResponse(content=estado)

@app.get("/ia-status")
def ia_status():
    """Obtiene métricas de la IA cuántica"""
    estado = conectar_servidor("AI_STATUS")
    return JSONResponse(content=estado)

@app.get("/ia-optimize")
def ia_optimize():
    """Ejecuta optimización con IA"""
    resultado = conectar_servidor("AI_OPTIMIZE")
    return JSONResponse(content=resultado)

@app.get("/analisis")
def analisis():
    estado = conectar_servidor("STATUS")
    # IA: analizar datos en tiempo real
    alertas = []
    recomendaciones_ia = []
    
    # Analizar métricas de IA si están disponibles
    ia_data = estado.get("ia_cuantica", {})
    if ia_data:
        errores = ia_data.get("errores_detectados", 0)
        tasa_exito = ia_data.get("tasa_exito", "0%")
        if errores > 100:
            alertas.append(f"🤖 IA detectó {errores} errores - revisar integridad del sistema")
        if "%" in str(tasa_exito) and float(tasa_exito.replace("%", "")) < 80:
            recomendaciones_ia.append("🤖 Tasa de corrección baja - considerar recalibración")
    
    # Analizar cristales
    for nombre, cristal in estado.get("cristales_detalle", {}).items():
        ocupacion_str = cristal.get("ocupacion", "0")
        if isinstance(ocupacion_str, str):
            ocupacion = float(ocupacion_str.replace("%", ""))
        else:
            ocupacion = float(ocupacion_str)
        
        energia = float(cristal.get("energia_total", 0))
        
        if ocupacion > 90:
            alertas.append(f"⚠️ Cristal '{nombre}' con ocupación crítica: {ocupacion}%")
            recomendaciones_ia.append(f"🤖 Ejecutar AI_OPTIMIZE en '{nombre}'")
        if energia > 900:
            alertas.append(f"⚡ Cristal '{nombre}' con energía elevada: {energia}")
    
    return {
        "alertas": alertas,
        "recomendaciones_ia": recomendaciones_ia,
        "cristales": estado.get("cristales_detalle", {}),
        "ia_metricas": ia_data
    }

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
