"""
================================================================================
APP.PY - INTERFAZ DE USUARIO CON STREAMLIT
================================================================================
Inspirado en:
- Vibe Coding (Addy Osmani): Prototipado veloz de interfaz limpia para el usuario.
- AI Product Management (Aman Khan): Descubrimiento basado en prototipos funcionales.
- AI-Assisted Programming (Tom Taulli): Feedback visual e interactivo.
================================================================================
"""

import streamlit as st
import os
from agent_auditor import AgenteLectorRAG, AgenteAuditorCodigo

# Intentamos importar pypdf para lectura de PDFs si está disponible
try:
    from pypdf import PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False


def extraer_texto_archivo(uploaded_file) -> str:
    """Lee y extrae texto de un archivo subido (PDF o TXT)."""
    if uploaded_file is None:
        return ""
    
    nombre = uploaded_file.name.lower()
    
    if nombre.endswith('.pdf'):
        if not PYPDF_AVAILABLE:
            st.warning("⚠️ La librería `pypdf` no está disponible. Convierte tu PDF a archivo de texto (.txt) o instala pypdf.")
            return ""
        try:
            reader = PdfReader(uploaded_file)
            texto = ""
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    texto += t + "\n"
            return texto
        except Exception as e:
            st.error(f"Error al procesar PDF: {e}")
            return ""
    else:
        # Archivos de texto o código fuente (.txt, .py, .js)
        try:
            return uploaded_file.getvalue().decode("utf-8")
        except Exception:
            return str(uploaded_file.getvalue())


# CONFIGURACIÓN DE LA PÁGINA STREAMLIT
st.set_page_config(
    page_title="Auditor RAG de Código y Trabajos",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Auditor RAG de Código y Trabajos Prácticos")
st.caption("Sistema Multiagente basado en RAG para evaluación y control de calidad de software")

# BARRA LATERAL - CONFIGURACIÓN Y CLAVE DE API
with st.sidebar:
    st.header("⚙️ Configuración del Sistema")
    api_key_input = st.text_input(
        "Google Gemini API Key (Opcional):",
        type="password",
        help="Si no ingresas una clave, el sistema funcionará en modo de simulación local gratuita."
    )
    
    api_key = api_key_input or os.environ.get("GEMINI_API_KEY", "")
    
    if api_key:
        st.success("🔑 API Key detectada / activa.")
    else:
        st.info("💡 Modo Simulación Local activo (Sin costo de API).")

    st.markdown("---")
    st.markdown("### 📚 Principios de los 4 Libros:")
    st.markdown("• **Aman Khan:** Definición de producto en `agents.md`\n"
                "• **Tom Taulli:** Prompting estructurado y testing\n"
                "• **O'Mahony & Nonnenmacher:** Agentes RAG especializados\n"
                "• **Addy Osmani:** Control humano del 30% restante")

# DISEÑO PRINCIPAL DE 2 COLUMNAS
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 1. Documento de Pautas / Rúbrica")
    file_rubrica = st.file_uploader(
        "Sube el archivo de consignas (PDF o TXT):",
        type=["pdf", "txt"],
        key="rubrica"
    )

with col2:
    st.subheader("💻 2. Código Fuente del Alumno")
    file_codigo = st.file_uploader(
        "Sube el archivo de código (.py, .js, .txt):",
        type=["py", "js", "txt", "html", "css"],
        key="codigo"
    )

st.markdown("---")

# BOTÓN PARA EJECUTAR LA AUDITORÍA MULTIAGENTE
if st.button("🚀 Iniciar Auditoría Multiagente", type="primary", use_container_width=True):
    if not file_rubrica or not file_codigo:
        st.error("⚠️ Debes subir ambos archivos (el documento de pautas y el código fuente) para iniciar la auditoría.")
    else:
        with st.spinner("🔄 Agente 1 (Lector RAG) analizando las pautas y extraendo criterios..."):
            texto_rubrica = extraer_texto_archivo(file_rubrica)
            agente_rag = AgenteLectorRAG(api_key=api_key)
            criterios_extraidos = agente_rag.extraer_criterios(texto_rubrica)

        st.success(f"✅ Agente 1 completado ({criterios_extraidos.get('modo', 'Local')})")

        with st.spinner("🔄 Agente 2 (Auditor de Código) evaluando el proyecto contra las pautas..."):
            texto_codigo = extraer_texto_archivo(file_codigo)
            agente_auditor = AgenteAuditorCodigo(api_key=api_key)
            resultado_auditoria = agente_auditor.auditar_codigo(texto_codigo, criterios_extraidos)

        st.success("✅ Auditoría completada con éxito.")

        # PRESENTACIÓN DE RESULTADOS EN PESTAÑAS
        tab1, tab2, tab3 = st.tabs(["📊 Reporte de Auditoría", "🔍 Criterios RAG Extraídos", "💻 Código Analizado"])

        with tab1:
            st.markdown(resultado_auditoria.get("reporte_completo", "Sin reporte generado."))

        with tab2:
            st.markdown("### Criterios Identificados por el Agente 1:")
            st.markdown(criterios_extraidos.get("criterios_raw", "No se encontraron criterios."))

        with tab3:
            st.code(texto_codigo, language="python")
