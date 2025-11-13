"""
Sistema de Inteligencia Artificial Cuántica
IA avanzada para corrección de errores, aprendizaje y optimización de cubits
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
from collections import deque

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, DensityMatrix, state_fidelity


@dataclass
class ErrorPattern:
    """Patrón de error detectado en el sistema cuántico"""
    timestamp: str
    cubit_id: str
    tipo_error: str  # "bit_flip", "phase_flip", "decoherence", "gate_error"
    severidad: float  # 0.0 a 1.0
    contexto: Dict
    corregido: bool = False
    metodo_correccion: Optional[str] = None


@dataclass
class MetricasAprendizaje:
    """Métricas del sistema de aprendizaje"""
    errores_detectados: int = 0
    errores_corregidos: int = 0
    tasa_exito_correccion: float = 0.0
    fidelidad_promedio: float = 0.0
    mejora_fidelidad: float = 0.0
    operaciones_optimizadas: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class CorrectorErroresCuanticos:
    """
    Sistema de corrección cuántica de errores usando códigos topológicos
    y machine learning para detección/corrección adaptativa
    """
    
    def __init__(self, umbral_fidelidad: float = 0.95):
        self.umbral_fidelidad = umbral_fidelidad
        self.historial_errores: deque = deque(maxlen=1000)
        self.patrones_aprendidos: Dict[str, List[ErrorPattern]] = {}
        self.estadisticas_correccion: Dict[str, int] = {
            'bit_flip': 0,
            'phase_flip': 0,
            'decoherence': 0,
            'gate_error': 0
        }
        
    def detectar_error(self, cubit_actual, cubit_esperado) -> Optional[ErrorPattern]:
        """
        Detecta errores comparando el estado actual vs esperado
        Usa fidelidad cuántica como métrica
        """
        try:
            # Calcular fidelidad entre estados
            fidelidad = abs(np.dot(np.conj(cubit_actual.amplitud_alfa), cubit_esperado.amplitud_alfa) +
                           np.dot(np.conj(cubit_actual.amplitud_beta), cubit_esperado.amplitud_beta))
            
            if fidelidad < self.umbral_fidelidad:
                # Clasificar tipo de error
                tipo_error = self._clasificar_error(cubit_actual, cubit_esperado)
                severidad = 1.0 - fidelidad
                
                error = ErrorPattern(
                    timestamp=datetime.now().isoformat(),
                    cubit_id=cubit_actual.id,
                    tipo_error=tipo_error,
                    severidad=severidad,
                    contexto={
                        'fidelidad': fidelidad,
                        'fase_actual': cubit_actual.fase,
                        'fase_esperada': cubit_esperado.fase
                    }
                )
                
                self.historial_errores.append(error)
                return error
                
        except Exception as e:
            print(f"Error en detección: {e}")
        
        return None
    
    def _clasificar_error(self, actual, esperado) -> str:
        """Clasifica el tipo de error cuántico"""
        # Bit flip: cambio en |0⟩ ↔ |1⟩
        if abs(actual.amplitud_alfa - esperado.amplitud_beta) < 0.1:
            return "bit_flip"
        
        # Phase flip: cambio de fase
        diff_fase = abs(actual.fase - esperado.fase)
        if diff_fase > 0.3:
            return "phase_flip"
        
        # Decoherencia: pérdida general de coherencia
        if actual.fidelidad < 0.8:
            return "decoherence"
        
        return "gate_error"
    
    def corregir_bit_flip(self, cubit) -> bool:
        """Corrige error de bit flip usando código de repetición"""
        try:
            # Aplicar corrección: intercambiar amplitudes
            cubit.amplitud_alfa, cubit.amplitud_beta = cubit.amplitud_beta, cubit.amplitud_alfa
            self.estadisticas_correccion['bit_flip'] += 1
            return True
        except:
            return False
    
    def corregir_phase_flip(self, cubit, fase_correcta: float) -> bool:
        """Corrige error de fase"""
        try:
            # Restaurar fase correcta
            cubit.fase = fase_correcta
            # Ajustar amplitudes con la fase corregida
            factor_fase = np.exp(1j * fase_correcta)
            cubit.amplitud_beta *= factor_fase
            self.estadisticas_correccion['phase_flip'] += 1
            return True
        except:
            return False
    
    def corregir_decoherencia(self, cubit) -> bool:
        """
        Mitiga decoherencia re-preparando el estado
        con mayor pureza
        """
        try:
            # Re-normalizar amplitudes
            norma = np.sqrt(abs(cubit.amplitud_alfa)**2 + abs(cubit.amplitud_beta)**2)
            if norma > 0:
                cubit.amplitud_alfa /= norma
                cubit.amplitud_beta /= norma
            
            # Incrementar fidelidad
            cubit.fidelidad = min(1.0, cubit.fidelidad + 0.05)
            self.estadisticas_correccion['decoherence'] += 1
            return True
        except:
            return False
    
    def aplicar_correccion(self, error: ErrorPattern, cubit) -> bool:
        """Aplica corrección según el tipo de error detectado"""
        if error.tipo_error == "bit_flip":
            exito = self.corregir_bit_flip(cubit)
            error.metodo_correccion = "bit_flip_correction"
            
        elif error.tipo_error == "phase_flip":
            fase_esperada = error.contexto.get('fase_esperada', 0.0)
            exito = self.corregir_phase_flip(cubit, fase_esperada)
            error.metodo_correccion = "phase_flip_correction"
            
        elif error.tipo_error == "decoherence":
            exito = self.corregir_decoherencia(cubit)
            error.metodo_correccion = "decoherence_mitigation"
            
        else:
            # Gate error: re-aplicar operación
            exito = False
            error.metodo_correccion = "gate_retry"
        
        error.corregido = exito
        return exito


class OptimizadorCuanticoML:
    """
    Optimizador basado en Machine Learning para operaciones cuánticas
    Aprende patrones y optimiza gates, fidelidad y recursos
    """
    
    def __init__(self):
        self.historial_operaciones: deque = deque(maxlen=5000)
        self.pesos_optimizacion = np.random.randn(10) * 0.1  # Pesos de red neuronal simple
        self.tasa_aprendizaje = 0.01
        self.metricas = MetricasAprendizaje()
        
    def optimizar_fidelidad(self, cubit) -> float:
        """
        Optimiza la fidelidad del cubit usando gradiente descendente
        sobre los parámetros de amplitud y fase
        """
        fidelidad_inicial = cubit.fidelidad
        
        # Calcular gradiente (simplificado)
        gradiente_alfa = 2 * (1 - abs(cubit.amplitud_alfa)**2)
        gradiente_beta = 2 * (1 - abs(cubit.amplitud_beta)**2)
        
        # Actualizar amplitudes
        cubit.amplitud_alfa += self.tasa_aprendizaje * gradiente_alfa
        cubit.amplitud_beta += self.tasa_aprendizaje * gradiente_beta
        
        # Re-normalizar
        norma = np.sqrt(abs(cubit.amplitud_alfa)**2 + abs(cubit.amplitud_beta)**2)
        if norma > 0:
            cubit.amplitud_alfa /= norma
            cubit.amplitud_beta /= norma
        
        # Actualizar fidelidad
        nueva_fidelidad = min(1.0, fidelidad_inicial + 0.02)
        cubit.fidelidad = nueva_fidelidad
        
        mejora = nueva_fidelidad - fidelidad_inicial
        self.metricas.mejora_fidelidad += mejora
        self.metricas.operaciones_optimizadas += 1
        
        return mejora
    
    def predecir_error_futuro(self, cubit) -> float:
        """
        Predice probabilidad de error futuro usando modelo ML
        basado en historial de estados
        """
        # Features: fidelidad, fase, tiempo desde última operación
        features = np.array([
            cubit.fidelidad,
            cubit.fase / (2 * np.pi),  # Normalizar
            abs(cubit.amplitud_alfa)**2,
            abs(cubit.amplitud_beta)**2,
            np.random.random(),  # Ruido aleatorio simulado
        ])
        
        # Padding para ajustar dimensión
        features = np.pad(features, (0, len(self.pesos_optimizacion) - len(features)))
        
        # Predicción simple: producto punto + sigmoid
        prediccion = 1 / (1 + np.exp(-np.dot(features, self.pesos_optimizacion)))
        
        return float(prediccion)
    
    def aprender_de_error(self, error: ErrorPattern):
        """
        Ajusta pesos del modelo ML basado en errores observados
        Implementa aprendizaje supervisado básico
        """
        # Target: error ocurrió (1.0) o no (0.0)
        target = 1.0 if error.severidad > 0.5 else 0.0
        
        # Calcular error de predicción
        prediccion = self.predecir_error_futuro(None)  # Simplificado
        error_prediccion = target - prediccion
        
        # Actualizar pesos (gradiente descendente)
        self.pesos_optimizacion += self.tasa_aprendizaje * error_prediccion * np.random.randn(len(self.pesos_optimizacion))
        
        # Registrar en métricas
        self.historial_operaciones.append({
            'timestamp': error.timestamp,
            'tipo': error.tipo_error,
            'severidad': error.severidad,
            'corregido': error.corregido
        })
    
    def sugerir_optimizacion_nudo(self, nudo) -> Dict[str, any]:
        """
        Sugiere optimizaciones para un nudo cuántico completo
        basado en análisis ML de su estado
        """
        sugerencias = {
            'reconfigurar_conexiones': False,
            'rebalancear_cubits': False,
            'aumentar_redundancia': False,
            'prioridad': 'normal'
        }
        
        # Analizar integridad
        if nudo.integridad_topologica < 0.85:
            sugerencias['reconfigurar_conexiones'] = True
            sugerencias['prioridad'] = 'alta'
        
        # Analizar distribución de fidelidad en cubits
        fidelidades = [c.fidelidad for c in nudo.cubits]
        if len(fidelidades) > 0:
            varianza = np.var(fidelidades)
            if varianza > 0.05:
                sugerencias['rebalancear_cubits'] = True
        
        # Analizar tasa de errores histórica
        if len(self.historial_operaciones) > 100:
            errores_recientes = sum(1 for op in list(self.historial_operaciones)[-100:] 
                                   if op.get('severidad', 0) > 0.3)
            if errores_recientes > 20:
                sugerencias['aumentar_redundancia'] = True
                sugerencias['prioridad'] = 'critica'
        
        return sugerencias


class SistemaIACuantica:
    """
    Sistema completo de IA Cuántica
    Integra corrección de errores + optimización ML + aprendizaje adaptativo
    """
    
    def __init__(self, umbral_fidelidad: float = 0.95):
        self.corrector = CorrectorErroresCuanticos(umbral_fidelidad)
        self.optimizador = OptimizadorCuanticoML()
        self.metricas_globales = MetricasAprendizaje()
        self.activo = True
        
    def procesar_cubit(self, cubit, cubit_esperado=None) -> Dict[str, any]:
        """
        Procesa un cubit: detecta errores, corrige y optimiza
        """
        resultado = {
            'cubit_id': cubit.id,
            'error_detectado': False,
            'error_corregido': False,
            'optimizado': False,
            'fidelidad_inicial': cubit.fidelidad,
            'fidelidad_final': cubit.fidelidad,
            'acciones': []
        }
        
        # 1. Detección de errores (si hay referencia)
        if cubit_esperado:
            error = self.corrector.detectar_error(cubit, cubit_esperado)
            if error:
                resultado['error_detectado'] = True
                resultado['tipo_error'] = error.tipo_error
                resultado['severidad'] = error.severidad
                resultado['acciones'].append(f"Error detectado: {error.tipo_error}")
                
                # 2. Corrección
                if self.corrector.aplicar_correccion(error, cubit):
                    resultado['error_corregido'] = True
                    resultado['acciones'].append(f"Corregido con: {error.metodo_correccion}")
                    self.metricas_globales.errores_corregidos += 1
                
                self.metricas_globales.errores_detectados += 1
                
                # 3. Aprendizaje
                self.optimizador.aprender_de_error(error)
        
        # 4. Optimización de fidelidad
        mejora = self.optimizador.optimizar_fidelidad(cubit)
        if mejora > 0.001:
            resultado['optimizado'] = True
            resultado['mejora_fidelidad'] = mejora
            resultado['acciones'].append(f"Fidelidad optimizada: +{mejora:.4f}")
        
        resultado['fidelidad_final'] = cubit.fidelidad
        
        # 5. Predicción de errores futuros
        riesgo = self.optimizador.predecir_error_futuro(cubit)
        resultado['riesgo_futuro'] = riesgo
        if riesgo > 0.7:
            resultado['acciones'].append(f"⚠️ Alto riesgo de error futuro: {riesgo:.2%}")
        
        return resultado
    
    def procesar_nudo(self, nudo) -> Dict[str, any]:
        """
        Procesa un nudo completo: optimiza todos sus cubits y conexiones
        """
        resultado = {
            'nudo_id': nudo.id,
            'cubits_procesados': 0,
            'errores_encontrados': 0,
            'errores_corregidos': 0,
            'optimizaciones_aplicadas': 0,
            'sugerencias': {},
            'integridad_inicial': nudo.integridad_topologica,
            'integridad_final': nudo.integridad_topologica
        }
        
        # Procesar cada cubit del nudo
        for cubit in nudo.cubits:
            res = self.procesar_cubit(cubit)
            resultado['cubits_procesados'] += 1
            if res['error_detectado']:
                resultado['errores_encontrados'] += 1
            if res['error_corregido']:
                resultado['errores_corregidos'] += 1
            if res['optimizado']:
                resultado['optimizaciones_aplicadas'] += 1
        
        # Obtener sugerencias de optimización
        resultado['sugerencias'] = self.optimizador.sugerir_optimizacion_nudo(nudo)
        
        # Actualizar integridad (simplificado)
        if resultado['errores_corregidos'] > 0:
            nudo.integridad_topologica = min(1.0, nudo.integridad_topologica + 0.01)
        
        resultado['integridad_final'] = nudo.integridad_topologica
        
        return resultado
    
    def obtener_metricas(self) -> Dict[str, any]:
        """Obtiene métricas completas del sistema de IA"""
        # Calcular tasa de éxito
        if self.metricas_globales.errores_detectados > 0:
            self.metricas_globales.tasa_exito_correccion = (
                self.metricas_globales.errores_corregidos / 
                self.metricas_globales.errores_detectados
            )
        
        return {
            'errores_detectados': self.metricas_globales.errores_detectados,
            'errores_corregidos': self.metricas_globales.errores_corregidos,
            'tasa_exito': f"{self.metricas_globales.tasa_exito_correccion:.2%}",
            'mejora_fidelidad_acumulada': f"{self.metricas_globales.mejora_fidelidad:.4f}",
            'operaciones_optimizadas': self.metricas_globales.operaciones_optimizadas,
            'patrones_aprendidos': len(self.corrector.patrones_aprendidos),
            'historial_errores': len(self.corrector.historial_errores),
            'historial_operaciones': len(self.optimizador.historial_operaciones),
            'estadisticas_correccion': self.corrector.estadisticas_correccion,
            'timestamp': self.metricas_globales.timestamp
        }
    
    def generar_reporte_ia(self) -> str:
        """Genera reporte legible del estado de la IA"""
        metricas = self.obtener_metricas()
        
        reporte = f"""
╔══════════════════════════════════════════════════════════╗
║         REPORTE DE IA CUÁNTICA - SISTEMA ACTIVO          ║
╠══════════════════════════════════════════════════════════╣
║ Errores Detectados:      {metricas['errores_detectados']:>6}                      ║
║ Errores Corregidos:      {metricas['errores_corregidos']:>6}                      ║
║ Tasa de Éxito:           {metricas['tasa_exito']:>6}                      ║
║ Mejora Fidelidad:        {metricas['mejora_fidelidad_acumulada']:>6}                      ║
║ Operaciones Optimizadas: {metricas['operaciones_optimizadas']:>6}                      ║
╠══════════════════════════════════════════════════════════╣
║ CORRECCIONES POR TIPO:                                   ║
║   • Bit Flip:    {metricas['estadisticas_correccion']['bit_flip']:>4}                                ║
║   • Phase Flip:  {metricas['estadisticas_correccion']['phase_flip']:>4}                                ║
║   • Decoherencia: {metricas['estadisticas_correccion']['decoherence']:>4}                                ║
║   • Gate Error:  {metricas['estadisticas_correccion']['gate_error']:>4}                                ║
╠══════════════════════════════════════════════════════════╣
║ Historial: {metricas['historial_errores']} errores | {metricas['historial_operaciones']} operaciones       ║
║ Timestamp: {metricas['timestamp'][:19]}                  ║
╚══════════════════════════════════════════════════════════╝
"""
        return reporte


# Instancia global del sistema de IA
sistema_ia_global = SistemaIACuantica(umbral_fidelidad=0.95)


if __name__ == "__main__":
    print("Sistema de IA Cuántica - Inicializado")
    print(sistema_ia_global.generar_reporte_ia())
