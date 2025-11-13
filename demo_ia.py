"""
Demo rápida del Sistema de IA Cuántica
Muestra las capacidades de corrección y optimización
"""

from quantum_ai import SistemaIACuantica, ErrorPattern
from quantum_knot_datacenter import CentroDatosNudos, TipoNudo
from datetime import datetime

print("="*60)
print("🤖 DEMO DEL SISTEMA DE IA CUÁNTICA")
print("="*60)

# 1. Crear sistema de IA
print("\n1️⃣ Inicializando sistema de IA...")
ia = SistemaIACuantica(umbral_fidelidad=0.95)
print("   ✓ Sistema IA inicializado")

# 2. Crear centro de datos
print("\n2️⃣ Creando centro de datos cuántico...")
centro = CentroDatosNudos("Demo_DataCenter")
print("   ✓ Centro creado")

# 3. Crear cristales
print("\n3️⃣ Creando cristales...")
centro.crear_cristal("Cristal_Test", dimensiones=(3, 3, 3))
print("   ✓ Cristal_Test creado (3x3x3)")

# 4. Almacenar datos (genera nudo con cubits)
print("\n4️⃣ Almacenando datos (genera nudos automáticamente)...")
datos_prueba = b"Test IA Cuantica 2025"
centro.almacenar_datos("Cristal_Test", datos_prueba, TipoNudo.TREBOL)
print("   ✓ Datos almacenados con procesamiento de IA")

# 5. Procesar cristal completo con IA
print("\n5️⃣ Optimizando cristal completo con IA...")
cristal = centro.cristales["Cristal_Test"]
total_procesados = 0
total_optimizados = 0

for posicion, nudo in cristal.red_nudos.items():
    resultado = ia.procesar_nudo(nudo)
    total_procesados += 1
    total_optimizados += resultado['optimizaciones_aplicadas']
    
    print(f"   🤖 Nudo {nudo.id}:")
    print(f"      - Cubits procesados: {resultado['cubits_procesados']}")
    print(f"      - Optimizaciones: {resultado['optimizaciones_aplicadas']}")
    print(f"      - Integridad: {resultado['integridad_inicial']:.4f} → {resultado['integridad_final']:.4f}")

print(f"\n   ✓ Total nudos procesados: {total_procesados}")
print(f"   ✓ Total optimizaciones: {total_optimizados}")

# 6. Mostrar métricas finales
print("\n6️⃣ Métricas del Sistema de IA:")
print("="*60)
print(ia.generar_reporte_ia())

print("\n✅ Demo completada!")
print("="*60)
print("\n💡 Próximo paso: Ejecuta 'python quantum_knot_datacenter.py'")
print("   para iniciar el servidor completo con IA integrada.")

