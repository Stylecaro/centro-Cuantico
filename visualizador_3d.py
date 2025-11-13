"""
Visualizador 3D para Nudos Cuánticos
Muestra cristales cuánticos y sus nudos en espacio 3D interactivo
Autor: StyleEvolution
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.patches import FancyBboxPatch
import matplotlib.animation as animation
from typing import Dict, Tuple, List
import socket
import json


class Visualizador3DNudos:
    """Visualizador 3D para cristales y nudos cuánticos"""
    
    def __init__(self):
        self.fig = None
        self.ax = None
        self.datos_cristal = None
        self.angulo_rotacion = 0
        
    def conectar_servidor(self, host: str = 'localhost', puerto: int = 5555) -> bool:
        """Conecta al servidor para obtener datos"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, puerto))
            return True
        except Exception as e:
            print(f"❌ Error al conectar: {e}")
            return False
    
    def obtener_datos_cristal(self, nombre_cristal: str = None) -> Dict:
        """Obtiene datos del cristal del servidor"""
        try:
            # Obtener estado completo
            self.socket.send("STATUS".encode('utf-8'))
            respuesta = self.socket.recv(8192).decode('utf-8')
            estado = json.loads(respuesta)
            
            cristales = estado.get('cristales_detalle', {})
            
            if not cristales:
                print("❌ No hay cristales disponibles")
                return None
            
            # Si no se especifica cristal, tomar el primero
            if nombre_cristal is None:
                nombre_cristal = list(cristales.keys())[0]
            
            if nombre_cristal not in cristales:
                print(f"❌ Cristal '{nombre_cristal}' no encontrado")
                return None
            
            return {
                'nombre': nombre_cristal,
                'datos': cristales[nombre_cristal]
            }
            
        except Exception as e:
            print(f"❌ Error al obtener datos: {e}")
            return None
    
    def crear_figura_3d(self):
        """Crea la figura 3D con configuración"""
        self.fig = plt.figure(figsize=(14, 10))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Configuración estética
        self.ax.set_facecolor('#0a0a0a')
        self.fig.patch.set_facecolor('#1a1a1a')
        
        # Etiquetas
        self.ax.set_xlabel('X', fontsize=12, color='cyan')
        self.ax.set_ylabel('Y', fontsize=12, color='cyan')
        self.ax.set_zlabel('Z', fontsize=12, color='cyan')
        
        # Grid
        self.ax.grid(True, alpha=0.3, color='cyan')
        
    def dibujar_estructura_cristal(self, dimensiones: Tuple[int, int, int]):
        """Dibuja la estructura del cristal (cuadrícula 3D)"""
        x_max, y_max, z_max = dimensiones
        
        # Dibujar aristas del cristal
        # Aristas en X
        for y in range(y_max + 1):
            for z in range(z_max + 1):
                self.ax.plot([0, x_max], [y, y], [z, z], 
                           'c-', alpha=0.2, linewidth=0.5)
        
        # Aristas en Y
        for x in range(x_max + 1):
            for z in range(z_max + 1):
                self.ax.plot([x, x], [0, y_max], [z, z], 
                           'c-', alpha=0.2, linewidth=0.5)
        
        # Aristas en Z
        for x in range(x_max + 1):
            for y in range(y_max + 1):
                self.ax.plot([x, x], [y, y], [0, z_max], 
                           'c-', alpha=0.2, linewidth=0.5)
    
    def generar_nudo_trebol(self, t: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Genera puntos para un nudo de trébol"""
        x = np.sin(t) + 2 * np.sin(2 * t)
        y = np.cos(t) - 2 * np.cos(2 * t)
        z = -np.sin(3 * t)
        return x, y, z
    
    def generar_nudo_figura8(self, t: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Genera puntos para un nudo en forma de 8"""
        x = (2 + np.cos(2 * t)) * np.cos(3 * t)
        y = (2 + np.cos(2 * t)) * np.sin(3 * t)
        z = np.sin(4 * t)
        return x, y, z
    
    def generar_nudo_toroidal(self, t: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Genera puntos para un nudo toroidal"""
        R = 2.0
        r = 0.8
        x = (R + r * np.cos(3 * t)) * np.cos(2 * t)
        y = (R + r * np.cos(3 * t)) * np.sin(2 * t)
        z = r * np.sin(3 * t)
        return x, y, z
    
    def dibujar_nudo(self, posicion: Tuple[int, int, int], tipo_nudo: str, 
                     energia: float, integridad: float, escala: float = 0.3):
        """Dibuja un nudo cuántico en una posición específica"""
        x_pos, y_pos, z_pos = posicion
        
        # Generar puntos del nudo
        t = np.linspace(0, 2 * np.pi, 200)
        
        if tipo_nudo == 'trebol':
            x, y, z = self.generar_nudo_trebol(t)
        elif tipo_nudo == 'figura8':
            x, y, z = self.generar_nudo_figura8(t)
        elif tipo_nudo == 'toroidal':
            x, y, z = self.generar_nudo_toroidal(t)
        else:  # circular por defecto
            x = np.cos(t)
            y = np.sin(t)
            z = 0.2 * np.sin(4 * t)
        
        # Escalar y trasladar
        x = x * escala + x_pos + 0.5
        y = y * escala + y_pos + 0.5
        z = z * escala + z_pos + 0.5
        
        # Color basado en energía e integridad
        color_intensidad = min(1.0, energia / 10.0)
        if integridad > 0.9:
            color = (0, 1 - color_intensidad, color_intensidad)  # Verde-Cyan
        elif integridad > 0.7:
            color = (color_intensidad, 1 - color_intensidad, 0)  # Amarillo
        else:
            color = (1, 0, color_intensidad)  # Rojo-Magenta
        
        # Dibujar el nudo
        self.ax.plot(x, y, z, color=color, linewidth=2.5, alpha=0.9)
        
        # Punto central del nudo
        self.ax.scatter([x_pos + 0.5], [y_pos + 0.5], [z_pos + 0.5], 
                       c=[color], s=100, alpha=0.8, edgecolors='white', linewidth=1)
        
        # Etiqueta con información
        label = f"{tipo_nudo[:3]}\nE:{energia:.2f}"
        self.ax.text(x_pos + 0.5, y_pos + 0.5, z_pos + 0.5 + 0.5, 
                    label, fontsize=8, color='white', 
                    bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.7))
    
    def visualizar_cristal(self, nombre_cristal: str = None, host: str = 'localhost', 
                          puerto: int = 5555, modo_demo: bool = False):
        """
        Visualiza un cristal cuántico en 3D
        
        Args:
            nombre_cristal: Nombre del cristal a visualizar
            host: Host del servidor
            puerto: Puerto del servidor
            modo_demo: Si es True, genera datos de demostración sin conectar al servidor
        """
        
        if modo_demo:
            # Modo demostración con datos simulados
            self.datos_cristal = {
                'nombre': 'Demo_Crystal',
                'datos': {
                    'dimensiones': [4, 4, 4],
                    'capacidad_usada': 8,
                    'capacidad_total': 64,
                    'energia_total': 45.6,
                    'ocupacion': '12.5%'
                }
            }
            # Generar nudos de demostración
            nudos_demo = []
            tipos = ['trebol', 'figura8', 'toroidal', 'circular']
            for i in range(8):
                x, y, z = np.random.randint(0, 4), np.random.randint(0, 4), np.random.randint(0, 4)
                nudos_demo.append({
                    'posicion': (x, y, z),
                    'tipo': tipos[i % 4],
                    'energia': np.random.uniform(3, 8),
                    'integridad': np.random.uniform(0.7, 1.0)
                })
            self.nudos = nudos_demo
        else:
            # Conectar al servidor y obtener datos reales
            if not self.conectar_servidor(host, puerto):
                print("💡 Iniciando modo demostración...")
                return self.visualizar_cristal(nombre_cristal, host, puerto, modo_demo=True)
            
            self.datos_cristal = self.obtener_datos_cristal(nombre_cristal)
            
            if not self.datos_cristal:
                print("💡 Iniciando modo demostración...")
                self.socket.close()
                return self.visualizar_cristal(nombre_cristal, host, puerto, modo_demo=True)
            
            # Simular posiciones de nudos (en producción, vendrían del servidor)
            self.nudos = self._generar_nudos_desde_servidor()
            self.socket.close()
        
        # Crear visualización
        self.crear_figura_3d()
        
        # Obtener dimensiones
        dims = self.datos_cristal['datos']['dimensiones']
        if isinstance(dims, str):
            dims = eval(dims)
        
        # Dibujar estructura del cristal
        self.dibujar_estructura_cristal(dims)
        
        # Dibujar nudos
        for nudo in self.nudos:
            self.dibujar_nudo(
                nudo['posicion'],
                nudo['tipo'],
                nudo['energia'],
                nudo['integridad']
            )
        
        # Configurar límites
        self.ax.set_xlim([0, dims[0]])
        self.ax.set_ylim([0, dims[1]])
        self.ax.set_zlim([0, dims[2]])
        
        # Título con información
        titulo = f"🔮 Cristal Cuántico: {self.datos_cristal['nombre']}\n"
        titulo += f"Dimensiones: {dims[0]}×{dims[1]}×{dims[2]} | "
        titulo += f"Nudos: {len(self.nudos)} | "
        titulo += f"Energía Total: {self.datos_cristal['datos'].get('energia_total', 0):.2f}"
        
        self.ax.set_title(titulo, fontsize=14, color='white', pad=20, 
                         bbox=dict(boxstyle='round,pad=0.8', facecolor='#2a2a2a', alpha=0.9))
        
        # Ángulo de vista inicial
        self.ax.view_init(elev=20, azim=45)
        
        # Leyenda de colores
        self._agregar_leyenda()
        
        plt.tight_layout()
        plt.show()
    
    def _generar_nudos_desde_servidor(self) -> List[Dict]:
        """Genera representación de nudos desde datos del servidor"""
        # En esta versión, generamos nudos de ejemplo
        # En producción, el servidor debería enviar las posiciones reales
        nudos = []
        capacidad = self.datos_cristal['datos'].get('capacidad_usada', 0)
        
        if capacidad > 0:
            tipos = ['trebol', 'figura8', 'toroidal', 'circular']
            dims = self.datos_cristal['datos']['dimensiones']
            if isinstance(dims, str):
                dims = eval(dims)
            
            for i in range(min(capacidad, 20)):  # Máximo 20 para rendimiento
                x = np.random.randint(0, dims[0])
                y = np.random.randint(0, dims[1])
                z = np.random.randint(0, dims[2])
                
                nudos.append({
                    'posicion': (x, y, z),
                    'tipo': tipos[i % 4],
                    'energia': np.random.uniform(2, 8),
                    'integridad': np.random.uniform(0.7, 1.0)
                })
        
        return nudos
    
    def _agregar_leyenda(self):
        """Agrega leyenda de colores y tipos de nudos"""
        from matplotlib.lines import Line2D
        
        elementos_leyenda = [
            Line2D([0], [0], color=(0, 1, 1), lw=3, label='Alta integridad (>90%)'),
            Line2D([0], [0], color=(1, 1, 0), lw=3, label='Media integridad (70-90%)'),
            Line2D([0], [0], color=(1, 0, 1), lw=3, label='Baja integridad (<70%)'),
        ]
        
        legend = self.ax.legend(handles=elementos_leyenda, loc='upper left', 
                               framealpha=0.9, facecolor='#2a2a2a', 
                               edgecolor='cyan', fontsize=9)
        plt.setp(legend.get_texts(), color='white')


def visualizar_desde_cliente():
    """Función para visualizar desde el cliente"""
    print("\n" + "="*60)
    print("🔮 VISUALIZADOR 3D DE NUDOS CUÁNTICOS")
    print("="*60)
    
    vis = Visualizador3DNudos()
    
    print("\n1. Conectar a servidor")
    print("2. Modo demostración (sin servidor)")
    
    opcion = input("\nSelecciona modo: ").strip()
    
    if opcion == "1":
        host = input("Host (default: localhost): ").strip() or "localhost"
        puerto_str = input("Puerto (default: 5555): ").strip()
        puerto = int(puerto_str) if puerto_str else 5555
        nombre = input("Nombre del cristal (Enter para primero disponible): ").strip() or None
        
        vis.visualizar_cristal(nombre, host, puerto, modo_demo=False)
    else:
        print("\n🎨 Generando visualización de demostración...")
        vis.visualizar_cristal(modo_demo=True)


if __name__ == "__main__":
    visualizar_desde_cliente()
