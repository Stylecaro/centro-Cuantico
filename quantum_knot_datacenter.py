"""
Sistema de Centro de Datos Cuántico con Nudos
Almacenamiento cúbico cuántico para cristales con conectividad de red
"""

import numpy as np
import hashlib
import json
import socket
import threading
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix, Statevector, partial_trace


class EstadoCuantico(Enum):
    """Estados cuánticos posibles para los cubits"""
    SUPERPOSICION = "superposicion"
    ENTRELAZADO = "entrelazado"
    COLAPSADO = "colapsado"
    COHERENTE = "coherente"


class TipoNudo(Enum):
    """Tipos de nudos topológicos para almacenamiento"""
    TREBOL = "trebol"
    FIGURA_OCHO = "figura_ocho"
    TOROIDAL = "toroidal"
    BORROMEO = "borromeo"
    HOPF = "hopf"


@dataclass
class Cubit:
    """Representación de un cubit cuántico"""
    id: str
    estado: EstadoCuantico
    amplitud_alfa: complex
    amplitud_beta: complex
    fase: float
    fidelidad: float
    timestamp: str
    circuito_preparacion: Optional[QuantumCircuit] = None
    statevector: Optional[Statevector] = None
    
    def medir(self) -> int:
        """Simula la medición del cubit"""
        probabilidad_cero = abs(self.amplitud_alfa) ** 2
        return 0 if np.random.random() < probabilidad_cero else 1
    
    def to_dict(self) -> dict:
        """Convierte el cubit a diccionario"""
        return {
            'id': self.id,
            'estado': self.estado.value,
            'amplitud_alfa': f"{self.amplitud_alfa.real}+{self.amplitud_alfa.imag}j",
            'amplitud_beta': f"{self.amplitud_beta.real}+{self.amplitud_beta.imag}j",
            'fase': self.fase,
            'fidelidad': self.fidelidad,
            'timestamp': self.timestamp
        }


@dataclass
class NudoCuantico:
    """Estructura de nudo cuántico para almacenamiento topológico"""
    id: str
    tipo: TipoNudo
    cubits: List[Cubit]
    conexiones: List[int]  # Índices de otros nudos conectados
    integridad_topologica: float
    matriz_entrelazamiento: np.ndarray
    circuito: Optional[QuantumCircuit]
    statevector: Optional[Statevector]
    
    def calcular_invariante_topologico(self) -> complex:
        """Calcula el invariante topológico del nudo"""
        if len(self.cubits) == 0:
            return 0 + 0j
        
        suma = sum(c.amplitud_alfa * c.amplitud_beta for c in self.cubits)
        return suma * np.exp(1j * self.integridad_topologica)
    
    def verificar_coherencia(self) -> bool:
        """Verifica la coherencia cuántica del nudo"""
        return all(c.fidelidad > 0.85 for c in self.cubits)


class CristalCuantico:
    """Estructura cristalina para almacenar nudos cuánticos"""
    
    def __init__(self, dimensiones: Tuple[int, int, int], nombre: str):
        self.dimensiones = dimensiones
        self.nombre = nombre
        self.red_nudos: Dict[Tuple[int, int, int], NudoCuantico] = {}
        self.capacidad_total = dimensiones[0] * dimensiones[1] * dimensiones[2]
        self.capacidad_usada = 0
        self.timestamp_creacion = datetime.now().isoformat()
        
    def agregar_nudo(self, posicion: Tuple[int, int, int], nudo: NudoCuantico) -> bool:
        """Agrega un nudo a una posición específica del cristal"""
        x, y, z = posicion
        
        if not (0 <= x < self.dimensiones[0] and 
                0 <= y < self.dimensiones[1] and 
                0 <= z < self.dimensiones[2]):
            return False
        
        if posicion in self.red_nudos:
            return False
        
        self.red_nudos[posicion] = nudo
        self.capacidad_usada += 1
        return True
    
    def obtener_nudo(self, posicion: Tuple[int, int, int]) -> Optional[NudoCuantico]:
        """Obtiene un nudo de una posición específica"""
        return self.red_nudos.get(posicion)
    
    def obtener_vecinos(self, posicion: Tuple[int, int, int]) -> List[NudoCuantico]:
        """Obtiene los nudos vecinos en la red cristalina"""
        x, y, z = posicion
        vecinos = []
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    if dx == dy == dz == 0:
                        continue
                    
                    pos_vecino = (x + dx, y + dy, z + dz)
                    nudo = self.obtener_nudo(pos_vecino)
                    if nudo:
                        vecinos.append(nudo)
        
        return vecinos
    
    def calcular_energia_cristal(self) -> float:
        """Calcula la energía total del cristal"""
        energia = 0.0
        for nudo in self.red_nudos.values():
            invariante = nudo.calcular_invariante_topologico()
            energia += abs(invariante) ** 2
        return energia
    
    def get_estado(self) -> dict:
        """Retorna el estado actual del cristal"""
        return {
            'nombre': self.nombre,
            'dimensiones': self.dimensiones,
            'capacidad_total': self.capacidad_total,
            'capacidad_usada': self.capacidad_usada,
            'ocupacion': f"{(self.capacidad_usada/self.capacidad_total)*100:.2f}%",
            'energia_total': self.calcular_energia_cristal(),
            'timestamp': self.timestamp_creacion
        }


class CentroDatosNudos:
    """Centro de datos principal para gestionar cristales cuánticos con nudos"""
    
    def __init__(self, nombre: str, puerto_red: int = 5555):
        self.nombre = nombre
        self.cristales: Dict[str, CristalCuantico] = {}
        self.puerto_red = puerto_red
        self.servidor_activo = False
        self.conexiones_red: List[socket.socket] = []
        self.lock = threading.Lock()
        
    def crear_cristal(self, nombre: str, dimensiones: Tuple[int, int, int]) -> CristalCuantico:
        """Crea un nuevo cristal cuántico"""
        cristal = CristalCuantico(dimensiones, nombre)
        self.cristales[nombre] = cristal
        print(f"✓ Cristal '{nombre}' creado con dimensiones {dimensiones}")
        return cristal
    
    def generar_cubit(self, id_cubit: str) -> Cubit:
        """Genera un nuevo cubit con estado cuántico aleatorio"""
        theta = np.random.uniform(0, np.pi)
        phi = np.random.uniform(0, 2 * np.pi)
        lam = np.random.uniform(0, 2 * np.pi)

        circuito = QuantumCircuit(1, name=f"prep_{id_cubit}")
        circuito.u(theta, phi, lam, 0)

        estado = Statevector.from_instruction(circuito)
        alfa, beta = estado.data

        return Cubit(
            id=id_cubit,
            estado=EstadoCuantico.COHERENTE,
            amplitud_alfa=complex(alfa),
            amplitud_beta=complex(beta),
            fase=float(lam),
            fidelidad=np.random.uniform(0.88, 0.99),
            timestamp=datetime.now().isoformat(),
            circuito_preparacion=circuito,
            statevector=estado
        )
    
    def crear_nudo(self, id_nudo: str, tipo: TipoNudo, num_cubits: int,
                   payload: Optional[bytes] = None) -> NudoCuantico:
        """Crea un nuevo nudo cuántico con cubits"""
        cubits = [self.generar_cubit(f"{id_nudo}_q{i}") for i in range(num_cubits)]
        circuito, statevector, matriz = self._generar_circuito_nudo(id_nudo, tipo, num_cubits, payload)

        return NudoCuantico(
            id=id_nudo,
            tipo=tipo,
            cubits=cubits,
            conexiones=[],
            integridad_topologica=np.random.uniform(0.9, 1.0),
            matriz_entrelazamiento=matriz,
            circuito=circuito,
            statevector=statevector
        )

    def _generar_circuito_nudo(self, id_nudo: str, tipo: TipoNudo, num_cubits: int,
                               payload: Optional[bytes]) -> Tuple[Optional[QuantumCircuit], Optional[Statevector], np.ndarray]:
        """Construye el circuito cuántico del nudo y calcula su matriz de entrelazamiento"""
        if num_cubits <= 0:
            return None, None, np.zeros((0, 0), dtype=np.float64)

        circuito = QuantumCircuit(num_cubits, name=id_nudo)

        bits = self._extraer_bits_payload(payload, num_cubits)
        for idx, bit in enumerate(bits):
            if bit:
                circuito.x(idx)

        self._aplicar_patron_nudo(circuito, tipo)

        statevector = Statevector.from_instruction(circuito)
        matriz_entrelazamiento = self._calcular_matriz_entrelazamiento(statevector)

        return circuito, statevector, matriz_entrelazamiento

    def _extraer_bits_payload(self, payload: Optional[bytes], num_cubits: int) -> List[int]:
        """Obtiene los bits iniciales a codificar en el circuito"""
        if not payload:
            return [0] * num_cubits

        bitstream = "".join(f"{byte:08b}" for byte in payload)
        bits = [int(bitstream[i]) for i in range(min(len(bitstream), num_cubits))]
        if len(bits) < num_cubits:
            bits.extend([0] * (num_cubits - len(bits)))
        return bits

    def _aplicar_patron_nudo(self, circuito: QuantumCircuit, tipo: TipoNudo):
        """Aplica las compuertas cuánticas que representan el nudo topológico"""
        n = circuito.num_qubits
        if n == 0:
            return

        if tipo == TipoNudo.TREBOL:
            circuito.h(0)
            for i in range(1, n):
                circuito.cx(i - 1, i)

        elif tipo == TipoNudo.FIGURA_OCHO:
            for i in range(n):
                circuito.ry(np.pi / 3, i)
                circuito.rz(np.pi / 4, i)
            for i in range(n - 1):
                circuito.cx(i, i + 1)

        elif tipo == TipoNudo.TOROIDAL:
            for i in range(n):
                circuito.h(i)
            for i in range(n):
                circuito.cx(i, (i + 1) % n)

        elif tipo == TipoNudo.BORROMEO:
            for i in range(n):
                circuito.rx(np.pi / 3, i)
            for i in range(n - 1):
                circuito.cz(i, i + 1)
            if n >= 3:
                circuito.ccx(0, 1, 2)

        elif tipo == TipoNudo.HOPF:
            circuito.h(0)
            for i in range(1, n):
                circuito.ry(np.pi / 4, i)
                circuito.cz(0, i)

        else:
            for i in range(n):
                circuito.h(i)

    def _calcular_matriz_entrelazamiento(self, statevector: Statevector) -> np.ndarray:
        """Calcula una matriz simétrica de entrelazamiento utilizando trazas parciales"""
        densidad = DensityMatrix(statevector)
        n = densidad.num_qubits
        matriz = np.zeros((n, n), dtype=np.float64)

        for i in range(n):
            resto = [q for q in range(n) if q != i]
            reducido = partial_trace(densidad, resto) if resto else densidad
            matriz[i, i] = max(0.0, 1.0 - reducido.purity())

        for i in range(n):
            for j in range(i + 1, n):
                resto = [q for q in range(n) if q not in (i, j)]
                reducido = partial_trace(densidad, resto) if resto else densidad
                pureza = reducido.purity()
                medida = max(0.0, 1.0 - pureza)
                matriz[i, j] = matriz[j, i] = medida

        return matriz
    
    def almacenar_datos(self, nombre_cristal: str, datos: bytes, 
                        tipo_nudo: TipoNudo = TipoNudo.TREBOL) -> bool:
        """Almacena datos en el cristal especificado usando nudos cuánticos"""
        if nombre_cristal not in self.cristales:
            print(f"✗ Cristal '{nombre_cristal}' no encontrado")
            return False
        
        cristal = self.cristales[nombre_cristal]
        
        # Generar hash de los datos
        hash_datos = hashlib.sha256(datos).hexdigest()
        
        # Crear nudo para almacenar
        # Limitar cubits por nudo para evitar estados gigantes (memoria ~2^n)
        num_cubits = max(1, min(len(datos), 8))
        nudo = self.crear_nudo(
            f"nudo_{hash_datos[:8]}",
            tipo_nudo,
            num_cubits,
            payload=datos
        )
        
        # Encontrar posición libre en el cristal
        for x in range(cristal.dimensiones[0]):
            for y in range(cristal.dimensiones[1]):
                for z in range(cristal.dimensiones[2]):
                    posicion = (x, y, z)
                    if cristal.agregar_nudo(posicion, nudo):
                        print(f"✓ Datos almacenados en posición {posicion}")
                        print(f"  Hash: {hash_datos[:16]}...")
                        print(f"  Tipo nudo: {tipo_nudo.value}")
                        print(f"  Cubits: {num_cubits}")
                        return True
        
        print("✗ No hay espacio disponible en el cristal")
        return False
    
    def iniciar_servidor_red(self):
        """Inicia el servidor de red para conexiones remotas"""
        def servidor_thread():
            try:
                servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                servidor.bind(('localhost', self.puerto_red))
                servidor.listen(5)
                self.servidor_activo = True
                
                print(f"✓ Servidor de red activo en puerto {self.puerto_red}")
                
                while self.servidor_activo:
                    servidor.settimeout(1.0)
                    try:
                        cliente, direccion = servidor.accept()
                        with self.lock:
                            self.conexiones_red.append(cliente)
                        print(f"✓ Nueva conexión desde {direccion}")
                        
                        # Manejar cliente en thread separado
                        threading.Thread(target=self.manejar_cliente, 
                                       args=(cliente,), daemon=True).start()
                    except socket.timeout:
                        continue
                    except Exception as e:
                        if self.servidor_activo:
                            print(f"✗ Error en servidor: {e}")
                
                servidor.close()
                
            except Exception as e:
                print(f"✗ Error al iniciar servidor: {e}")
                self.servidor_activo = False
        
        thread = threading.Thread(target=servidor_thread, daemon=True)
        thread.start()
    
    def manejar_cliente(self, cliente: socket.socket):
        """Maneja las peticiones de un cliente conectado"""
        try:
            while True:
                datos = cliente.recv(4096)
                if not datos:
                    break
                
                # Procesar comando
                comando = datos.decode('utf-8').strip()
                respuesta = self.procesar_comando(comando)
                
                cliente.send(respuesta.encode('utf-8'))
                
        except Exception as e:
            print(f"✗ Error con cliente: {e}")
        finally:
            cliente.close()
            with self.lock:
                if cliente in self.conexiones_red:
                    self.conexiones_red.remove(cliente)
    
    def procesar_comando(self, comando: str) -> str:
        """Procesa comandos recibidos por la red"""
        partes = comando.split()
        
        if not partes:
            return "ERROR: Comando vacío"
        
        cmd = partes[0].upper()
        
        if cmd == "STATUS":
            return self.obtener_estado_json()
        
        elif cmd == "LIST":
            return "\n".join(self.cristales.keys())
        
        elif cmd == "INFO" and len(partes) > 1:
            nombre_cristal = partes[1]
            if nombre_cristal in self.cristales:
                return json.dumps(self.cristales[nombre_cristal].get_estado(), indent=2)
            return f"ERROR: Cristal '{nombre_cristal}' no encontrado"
        
        return "ERROR: Comando no reconocido"
    
    def obtener_estado_json(self) -> str:
        """Obtiene el estado completo del centro de datos en JSON"""
        estado = {
            'centro_datos': self.nombre,
            'cristales': len(self.cristales),
            'servidor_red': {
                'activo': self.servidor_activo,
                'puerto': self.puerto_red,
                'conexiones': len(self.conexiones_red)
            },
            'cristales_detalle': {
                nombre: cristal.get_estado() 
                for nombre, cristal in self.cristales.items()
            }
        }
        return json.dumps(estado, indent=2)
    
    def detener_servidor(self):
        """Detiene el servidor de red"""
        self.servidor_activo = False
        with self.lock:
            for conexion in self.conexiones_red:
                try:
                    conexion.close()
                except:
                    pass
            self.conexiones_red.clear()
        print("✓ Servidor de red detenido")
    
    def mostrar_estado(self):
        """Muestra el estado actual del centro de datos"""
        print("\n" + "="*60)
        print(f"CENTRO DE DATOS CUÁNTICO: {self.nombre}")
        print("="*60)
        print(f"Cristales activos: {len(self.cristales)}")
        print(f"Servidor de red: {'ACTIVO' if self.servidor_activo else 'INACTIVO'}")
        print(f"Puerto: {self.puerto_red}")
        print(f"Conexiones activas: {len(self.conexiones_red)}")
        print("\nCristales:")
        
        for nombre, cristal in self.cristales.items():
            estado = cristal.get_estado()
            print(f"\n  • {nombre}")
            print(f"    Dimensiones: {estado['dimensiones']}")
            print(f"    Ocupación: {estado['ocupacion']}")
            print(f"    Energía: {estado['energia_total']:.4f}")


def main():
    """Función principal de demostración"""
    print("Inicializando Centro de Datos Cuántico con Nudos...")
    print("="*60)
    
    # Crear centro de datos
    centro = CentroDatosNudos("QUANTUM_KNOT_DC_001", puerto_red=5555)
    
    # Crear cristales cuánticos
    cristal1 = centro.crear_cristal("Cristal_Alpha", (4, 4, 4))
    cristal2 = centro.crear_cristal("Cristal_Beta", (3, 3, 3))
    cristal3 = centro.crear_cristal("Cristal_Gamma", (5, 5, 5))
    
    print("\n" + "-"*60)
    print("Almacenando datos en cristales...")
    print("-"*60)
    
    # Almacenar diferentes tipos de datos
    datos_ejemplos = [
        (b"Datos secretos nivel 1", TipoNudo.TREBOL),
        (b"Informacion clasificada", TipoNudo.FIGURA_OCHO),
        (b"Quantum encryption key", TipoNudo.TOROIDAL),
        (b"Entangled state data", TipoNudo.BORROMEO),
        (b"Cristal coherence info", TipoNudo.HOPF),
    ]
    
    for i, (datos, tipo_nudo) in enumerate(datos_ejemplos):
        cristal_nombre = ["Cristal_Alpha", "Cristal_Beta", "Cristal_Gamma"][i % 3]
        centro.almacenar_datos(cristal_nombre, datos, tipo_nudo)
    
    # Iniciar servidor de red
    print("\n" + "-"*60)
    print("Iniciando conectividad de red...")
    print("-"*60)
    centro.iniciar_servidor_red()
    
    # Mostrar estado final
    import time
    time.sleep(0.5)  # Dar tiempo al servidor para iniciar
    centro.mostrar_estado()
    
    print("\n" + "="*60)
    print("Sistema listo. Servidor escuchando en puerto", centro.puerto_red)
    print("Usa 'STATUS', 'LIST', 'INFO <cristal>' para consultar")
    print("="*60)
    
    return centro


if __name__ == "__main__":
    centro = main()
    
    # Mantener el programa ejecutándose
    try:
        print("\nPresiona Ctrl+C para detener el servidor...\n")
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nDeteniendo sistema...")
        centro.detener_servidor()
        print("✓ Sistema detenido correctamente")
