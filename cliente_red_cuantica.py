"""
Cliente de Red para conectarse al Centro de Datos Cuántico
Permite consultar estado y gestionar cristales remotamente
"""

import socket
import json
import sys


class ClienteRedCuantica:
    """Cliente para conectarse al centro de datos cuántico"""
    
    def __init__(self, host: str = 'localhost', puerto: int = 5555):
        self.host = host
        self.puerto = puerto
        self.socket = None
        self.conectado = False
    
    def conectar(self) -> bool:
        """Establece conexión con el servidor"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.puerto))
            self.conectado = True
            print(f"✓ Conectado a {self.host}:{self.puerto}")
            return True
        except Exception as e:
            print(f"✗ Error al conectar: {e}")
            return False
    
    def enviar_comando(self, comando: str) -> str:
        """Envía un comando al servidor y retorna la respuesta"""
        if not self.conectado:
            return "ERROR: No conectado al servidor"
        
        try:
            self.socket.send(comando.encode('utf-8'))
            respuesta = self.socket.recv(8192).decode('utf-8')
            return respuesta
        except Exception as e:
            return f"ERROR: {e}"
    
    def obtener_estado(self):
        """Obtiene el estado completo del centro de datos"""
        respuesta = self.enviar_comando("STATUS")
        try:
            estado = json.loads(respuesta)
            self.mostrar_estado(estado)
        except:
            print(respuesta)
    
    def listar_cristales(self):
        """Lista todos los cristales disponibles"""
        respuesta = self.enviar_comando("LIST")
        print("\nCristales disponibles:")
        print("-" * 40)
        if respuesta:
            for cristal in respuesta.split('\n'):
                if cristal:
                    print(f"  • {cristal}")
        else:
            print("  (No hay cristales)")
    
    def info_cristal(self, nombre: str):
        """Obtiene información detallada de un cristal"""
        respuesta = self.enviar_comando(f"INFO {nombre}")
        try:
            info = json.loads(respuesta)
            print(f"\nInformación del cristal '{nombre}':")
            print("-" * 40)
            for clave, valor in info.items():
                print(f"  {clave}: {valor}")
        except:
            print(respuesta)
    
    def mostrar_estado(self, estado: dict):
        """Muestra el estado del centro de datos de forma formateada"""
        print("\n" + "="*60)
        print(f"ESTADO DEL CENTRO DE DATOS: {estado.get('centro_datos', 'N/A')}")
        print("="*60)
        
        print(f"\nCristales totales: {estado.get('cristales', 0)}")
        
        servidor = estado.get('servidor_red', {})
        print(f"\nServidor de red:")
        print(f"  Estado: {'ACTIVO' if servidor.get('activo') else 'INACTIVO'}")
        print(f"  Puerto: {servidor.get('puerto', 'N/A')}")
        print(f"  Conexiones: {servidor.get('conexiones', 0)}")
        
        cristales_detalle = estado.get('cristales_detalle', {})
        if cristales_detalle:
            print(f"\nDetalle de cristales:")
            for nombre, detalle in cristales_detalle.items():
                print(f"\n  • {nombre}")
                print(f"    Dimensiones: {detalle.get('dimensiones')}")
                print(f"    Ocupación: {detalle.get('ocupacion')}")
                print(f"    Capacidad: {detalle.get('capacidad_usada')}/{detalle.get('capacidad_total')}")
                print(f"    Energía: {detalle.get('energia_total', 0):.4f}")
    
    def desconectar(self):
        """Cierra la conexión con el servidor"""
        if self.socket:
            self.socket.close()
            self.conectado = False
            print("✓ Desconectado del servidor")
    
    def menu_interactivo(self):
        """Menú interactivo para el cliente"""
        while True:
            print("\n" + "="*60)
            print("CLIENTE CUÁNTICO - MENÚ PRINCIPAL")
            print("="*60)
            print("1. Obtener estado completo")
            print("2. Listar cristales")
            print("3. Info de cristal específico")
            print("4. Enviar comando personalizado")
            print("5. Salir")
            print("-"*60)
            
            opcion = input("Selecciona una opción: ").strip()
            
            if opcion == "1":
                self.obtener_estado()
            
            elif opcion == "2":
                self.listar_cristales()
            
            elif opcion == "3":
                nombre = input("Nombre del cristal: ").strip()
                if nombre:
                    self.info_cristal(nombre)
            
            elif opcion == "4":
                comando = input("Comando: ").strip()
                if comando:
                    respuesta = self.enviar_comando(comando)
                    print("\nRespuesta:")
                    print(respuesta)
            
            elif opcion == "5":
                print("\nCerrando cliente...")
                break
            
            else:
                print("✗ Opción no válida")


def main():
    """Función principal del cliente"""
    print("Cliente de Red Cuántica")
    print("="*60)
    
    # Configuración
    host = input("Host (default: localhost): ").strip() or "localhost"
    puerto_str = input("Puerto (default: 5555): ").strip()
    puerto = int(puerto_str) if puerto_str else 5555
    
    # Crear cliente
    cliente = ClienteRedCuantica(host, puerto)
    
    # Conectar
    if cliente.conectar():
        try:
            # Menú interactivo
            cliente.menu_interactivo()
        finally:
            cliente.desconectar()
    else:
        print("\n✗ No se pudo establecer conexión")
        sys.exit(1)


if __name__ == "__main__":
    main()
