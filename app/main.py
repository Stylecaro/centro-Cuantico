"""
App de monitoreo y análisis cuántico con IA avanzada
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import json

app = FastAPI(title="Centro de Datos Cuántico - Analítica & IA")

# Cargar estado simulado desde el servidor cuántico
ESTADO_PATH = os.path.join(os.path.dirname(__file__), "estado_simulado.json")

def cargar_estado():
    if os.path.exists(ESTADO_PATH):
        with open(ESTADO_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Centro de Datos Cuántico</title>
        <link rel='stylesheet' href='/static/style.css'>
    </head>
    <body>
        <h1>Centro de Datos Cuántico</h1>
        <div id='panel'></div>
        <script src='/static/app.js'></script>
    </body>
    </html>
    """

@app.get("/estado")
def estado():
    estado = cargar_estado()
    return JSONResponse(content=estado)

@app.get("/analisis")
def analisis():
    estado = cargar_estado()
    # IA simulada: alerta si ocupación > 90% o energía > 900
    alertas = []
    for nombre, cristal in estado.get("cristales_detalle", {}).items():
        ocupacion = float(cristal.get("ocupacion", "0").replace("%", ""))
        energia = float(cristal.get("energia_total", 0))
        if ocupacion > 90:
            alertas.append(f"Cristal '{nombre}' con ocupación crítica: {ocupacion}%")
        if energia > 900:
            alertas.append(f"Cristal '{nombre}' con energía elevada: {energia}")
    return {"alertas": alertas, "cristales": estado.get("cristales_detalle", {})}

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
