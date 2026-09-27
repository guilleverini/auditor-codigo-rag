# AGENTS.MD: ESPECIFICACIÓN Y CONTEXTO DEL PRODUCTO
> **Inspirado en *AI Product Management* (Aman Khan)**
> Este archivo sirve como la "fuente de verdad" y contexto estructurado para que desarrolladores y asistentes de IA entiendan los objetivos, límites y arquitectura del sistema.

---

## 🎯 1. Visión del Producto
* **Nombre del Sistema:** Auditor Inteligente de Trabajos y Código RAG (Multiagente)
* **Propósito:** Proporcionar una herramienta pedagógica e interactiva que evalúe proyectos de software creados por alumnos comparándolos automáticamente contra una rúbrica o guía de trabajos prácticos (PDF o TXT).
* **Valor Principal:** Automatiza el análisis de cumplimiento de consignas, reduce el tiempo de corrección y entrega retroalimentación detallada al estudiante antes de la entrega final.

---

## 👤 2. Perfil del Usuario
1. **Estudiantes de Programación:** Quieren verificar si su código cumple con las normas y pautas exigidas antes de entregar el trabajo práctico.
2. **Profesor / Evaluador:** Quiere revisar de forma acelerada la coherencia entre las consignas pedagógicas y el proyecto entregado.

---

## 🏗️ 3. Arquitectura del Sistema Multiagente
*Siguiendo los principios de **Building AI Agent Platforms (O'Mahony & Nonnenmacher)**, evitamos el antipatrón de un "Agente Gigante" (God Agent) y dividimos la responsabilidad en 2 agentes especializados:*

1. **Agente 1 - Lector RAG (`AgenteLectorRAG`):**
   * **Función:** Procesar el documento de pautas/rúbrica (PDF o TXT).
   * **Entrada:** Texto o archivo PDF con las reglas del trabajo práctico.
   * **Salida:** Mapeo estructurado de criterios pedagógicos, reglas obligatorias y formato requerido.

2. **Agente 2 - Auditor de Código (`AgenteAuditorCodigo`):**
   * **Función:** Analizar el código fuente del alumno (`.py`, `.js`, etc.) y contrastarlo contra los criterios extraídos por el Agente 1.
   * **Entrada:** Código del usuario + Criterios del Agente Lector.
   * **Salida:** Reporte cuantitativo y cualitativo de auditoría (Puntos cumplidos, faltantes, errores y sugerencias de refactorización).

---

## 🛡️ 4. Reglas de Ingeniería y Calidad (El 30% Humano)
*Inspirado en **Vibe Coding (Addy Osmani)** y **AI-Assisted Programming (Tom Taulli)**:*
* **Manejo de Errores Defensivo:** El sistema no debe colapsar si el alumno sube un archivo vacío, un formato inválido o si no cuenta con una API key.
* **Modo Simulación / Fallback:** Si no se detecta una clave de API válida, el sistema funcionará en modo de evaluación sintética local para permitir pruebas educativas sin costo.
* **Pruebas Unitarias:** Todo el pipeline core de agentes debe ser testeable mediante `pytest`.
