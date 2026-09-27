"""
================================================================================
AGENTE_AUDITOR.PY - NÚCLEO MULTIAGENTE Y RAG
================================================================================
Inspirado en:
- Building AI Agent Platforms (O'Mahony & Nonnenmacher): Separación de responsabilidades en agentes especializados.
- AI-Assisted Programming (Tom Taulli): Prompting estructurado y manejo de contexto.
- Vibe Coding (Addy Osmani): Control del 30% restante con validaciones y fallbacks.
================================================================================
"""

import os
import re
from typing import Dict, Any, List

# Intentamos importar la librería oficial de Google GenAI si está instalada
try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class AgenteLectorRAG:
    """
    AGENTE 1: Lector y Extractor RAG de Pautas
    Especializado en leer el documento de consignas (PDF/TXT) y extraer
    los criterios evaluables en una estructura organizada.
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if self.api_key and GENAI_AVAILABLE:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def extraer_criterios(self, texto_rubrica: str) -> Dict[str, Any]:
        """
        Analiza el texto del manual/rúbrica y extrae reglas clave.
        """
        if not texto_rubrica or len(texto_rubrica.strip()) == 0:
            return {
                "estado": "error",
                "mensaje": "El documento de pautas está vacío.",
                "criterios": []
            }

        # Si tenemos cliente de GenAI activo, procesamos con el modelo
        if self.client:
            try:
                prompt = f"""
                Actúa como un experto en diseño curricular y auditoría técnica.
                Analiza el siguiente texto de consignas/rúbrica y extrae una lista estructurada
                de los requisitos obligatorios que debe cumplir el código entregado por los alumnos.

                TEXTO DE LAS PAUTAS/RÚBRICA:
                ---------------------------
                {texto_rubrica[:4000]}
                ---------------------------

                Escribe tu respuesta con viñetas claras divididas en:
                1. Requisitos de Funcionalidad y Lógica
                2. Normas de Estilo y Buenas Prácticas
                3. Entregables y Formatos requeridos
                """
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                return {
                    "estado": "exito",
                    "modo": "LLM (Gemini 2.5)",
                    "criterios_raw": response.text,
                    "resumen": "Criterios extraídos exitosamente mediante el agente RAG."
                }
            except Exception as e:
                # Fallback defensivo si falla la llamada a la API
                return self._extraer_criterios_local(texto_rubrica, error=str(e))
        else:
            # Modo Simulación / Reglas locales sin API Key
            return self._extraer_criterios_local(texto_rubrica)

    def _extraer_criterios_local(self, texto: str, error: str = None) -> Dict[str, Any]:
        """Extrae criterios localmente cuando no hay API Key disponible."""
        lineas = [l.strip() for l in texto.split('\n') if l.strip()]
        lineas_clave = [l for l in lineas if any(kw in l.lower() for kw in ['debe', 'requiere', 'importante', 'paso', 'nota', 'criterio', 'apa', 'norma'])]
        
        criterios = lineas_clave[:5] if lineas_clave else lineas[:5]
        return {
            "estado": "exito",
            "modo": "Simulación Local (Sin API Key)",
            "error_origen": error,
            "criterios_raw": "\n".join([f"• {c}" for c in criterios]),
            "resumen": f"Se identificaron {len(criterios)} pautas clave en el documento subido."
        }


class AgenteAuditorCodigo:
    """
    AGENTE 2: Auditor de Código
    Compara el código fuente entregado contra los criterios extraídos por el Agente 1.
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if self.api_key and GENAI_AVAILABLE:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def auditar_codigo(self, codigo_alumno: str, criterios_rag: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audita el código comparándolo contra las pautas de RAG.
        """
        if not codigo_alumno or len(codigo_alumno.strip()) == 0:
            return {
                "estado": "error",
                "score": 0,
                "diagnostico": "El archivo de código está vacío."
            }

        # 1. Análisis Sintáctico/Estructural Básico en Python (El 30% de validación humana)
        errores_sintaxis = []
        try:
            compile(codigo_alumno, '<string>', 'exec')
            sintaxis_valida = True
        except SyntaxError as se:
            sintaxis_valida = False
            errores_sintaxis.append(f"Error de sintaxis en línea {se.lineno}: {se.msg}")
        except Exception:
            sintaxis_valida = True  # Para otros lenguajes o fragmentos

        # 2. Evaluación con IA o Modelo Sintético
        if self.client and sintaxis_valida:
            try:
                prompt = f"""
                Actúa como un Auditor Senior de Código y Profesor de Programación.
                Compara el siguiente código de un alumno contra los criterios extraídos de la rúbrica.

                CRITERIOS EXTRAÍDOS DE LA RÚBRICA (RAG):
                ---------------------------------------
                {criterios_rag.get('criterios_raw', 'Sin criterios específicos.')}

                CÓDIGO ENTREGADO POR EL ALUMNO:
                -------------------------------
                {codigo_alumno[:5000]}

                PROPORCIONA UN REPORTE CON ESTE FORMATO:
                1. Puntaje Estimado (0 a 100)
                2. Aspectos Cumplidos Positivamente
                3. Puntos Críticos a Corregir antes de la entrega
                4. Sugerencias de Refactorización y Buenas Prácticas
                """
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                return {
                    "estado": "exito",
                    "modo": "LLM (Gemini 2.5)",
                    "sintaxis_valida": sintaxis_valida,
                    "reporte_completo": response.text
                }
            except Exception as e:
                return self._auditar_local(codigo_alumno, criterios_rag, errores_sintaxis, error_api=str(e))
        else:
            return self._auditar_local(codigo_alumno, criterios_rag, errores_sintaxis)

    def _auditar_local(self, codigo: str, criterios: Dict[str, Any], errores_sintaxis: List[str], error_api: str = None) -> Dict[str, Any]:
        """Auditoría sintética local defensiva."""
        lineas = codigo.split('\n')
        tiene_comentarios = any('#' in l or '//' in l or '"""' in l for l in lineas)
        tiene_funciones = any('def ' in l or 'function ' in l for l in lineas)
        
        cumplidos = []
        corregir = []
        score = 100

        if errores_sintaxis:
            corregir.extend(errores_sintaxis)
            score -= 40
        else:
            cumplidos.append("Sintaxis de código ejecutable sin errores críticos.")

        if tiene_comentarios:
            cumplidos.append("El código incluye documentación y comentarios explicativos.")
        else:
            corregir.append("Falta agregar comentarios explicativos sobre las funciones principales.")
            score -= 15

        if tiene_funciones:
            cumplidos.append("Estructuración modular detectada (uso de funciones o métodos).")
        else:
            corregir.append("Se recomienda modularizar el código dividiéndolo en funciones.")
            score -= 15

        reporte = f"""
### 📊 REPORTE DE AUDITORÍA (Modo Simulación Local)
**Puntaje Estimado:** {max(score, 10)} / 100
**Estado de Sintaxis:** {'✅ VÁLIDA' if not errores_sintaxis else '❌ ERROR DETECTADO'}

#### ✅ Puntos Cumplidos:
""" + "\n".join([f"- {c}" for c in cumplidos]) + """

#### ⚠️ Puntos a Corregir antes de Entregar:
""" + "\n".join([f"- {c}" for c in corregir if corregir] or ["- ¡Ningún error grave detectado!"]) + f"""

---
*Nota: Este reporte fue generado localmente. Para una revisión semántica profunda con IA, ingresa una API Key válida en la barra lateral.*
"""
        return {
            "estado": "exito",
            "modo": "Simulación Local",
            "score": score,
            "reporte_completo": reporte
        }
