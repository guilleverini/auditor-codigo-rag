"""
================================================================================
TEST_APP.PY - SUITE DE PRUEBAS UNITARIAS CON UNITTEST
================================================================================
Inspirado en:
- AI-Assisted Programming (Tom Taulli): Creación de pruebas unitarias para código generado por IA.
- Vibe Coding (Addy Osmani): Control de calidad automatizado sobre el 30% restante del software.
================================================================================
"""

import unittest
import sys
import os

# Aseguramos el path del sistema para importar los agentes
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agent_auditor import AgenteLectorRAG, AgenteAuditorCodigo


class TestAuditorRAG(unittest.TestCase):

    def test_agente_lector_rag_vacio(self):
        """Verifica que el Agente 1 maneje correctamente un documento de rúbrica vacío."""
        agente = AgenteLectorRAG()
        resultado = agente.extraer_criterios("")
        self.assertEqual(resultado["estado"], "error")
        self.assertIn("vacío", resultado["mensaje"].lower())

    def test_agente_lector_rag_local(self):
        """Verifica la extracción de criterios en modo local sintético."""
        agente = AgenteLectorRAG()
        texto = """
        CONSIGNAS DEL TRABAJO PRÁCTICO
        1. El programa debe permitir ingresar el nombre del alumno.
        2. Es obligatorio incluir comentarios en el código.
        3. Se requiere que las funciones no superen las 20 líneas.
        """
        resultado = agente.extraer_criterios(texto)
        self.assertEqual(resultado["estado"], "exito")
        self.assertIn("criterios_raw", resultado)
        self.assertGreaterThan(len(resultado["criterios_raw"]), 0) if hasattr(self, 'assertGreaterThan') else self.assertTrue(len(resultado["criterios_raw"]) > 0)

    def test_agente_auditor_codigo_vacio(self):
        """Verifica que el Agente 2 detecte si se envía un archivo de código vacío."""
        agente = AgenteAuditorCodigo()
        resultado = agente.auditar_codigo("", {})
        self.assertEqual(resultado["estado"], "error")
        self.assertEqual(resultado["score"], 0)

    def test_agente_auditor_codigo_error_sintaxis(self):
        """Verifica que el Agente 2 identifique errores de sintaxis en el código en Python."""
        agente = AgenteAuditorCodigo()
        codigo_con_error = "def funcion_incompleta(: \n    print('Hola')"
        criterios = {"criterios_raw": "Debe incluir funciones de saludo."}
        
        resultado = agente.auditar_codigo(codigo_con_error, criterios)
        self.assertEqual(resultado["estado"], "exito")
        self.assertTrue("Sintaxis" in resultado["reporte_completo"] or "Error" in resultado["reporte_completo"])

    def test_agente_auditor_codigo_valido(self):
        """Verifica la evaluación de un archivo de código estructurado sin errores de sintaxis."""
        agente = AgenteAuditorCodigo()
        codigo_correcto = """
# Proyecto de prueba
def saludar_alumno(nombre: str):
    \"\"\"Saluda al alumno formateando su nombre.\"\"\"
    return f"Hola {nombre}, bienvenido a la clase."

if __name__ == "__main__":
    print(saludar_alumno("Carlos"))
    """
        criterios = {"criterios_raw": "• Debe usar funciones\n• Debe incluir comentarios"}
        resultado = agente.auditar_codigo(codigo_correcto, criterios)
        
        self.assertEqual(resultado["estado"], "exito")
        self.assertTrue("REPORTE DE AUDITORÍA" in resultado["reporte_completo"])


if __name__ == "__main__":
    unittest.main()
