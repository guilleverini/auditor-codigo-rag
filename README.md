# 🎓 AUDITOR RAG DE CÓDIGO Y TRABAJOS PRÁCTICOS (MULTIAGENTE)

> **Desarrollado como Sistema de Conocimiento Integrado** combinando los principios de:
> - **AI Product Management (Aman Khan):** Especificación de producto en `agents.md` y prototipado rápido.
> - **AI-Assisted Programming (Tom Taulli):** Prompting estructurado y pruebas unitarias con `pytest`.
> - **Building AI Agent Platforms (Ben O'Mahony & Fabian Nonnenmacher):** Arquitectura RAG multiagente sin "God Agents".
> - **Vibe Coding (Addy Osmani):** Control humano del 30% restante (sintaxis, validaciones y calidad).

---

## 🚀 1. CÓMO EJECUTAR EL PROYECTO EN LOCAL

### Paso 1: Instalar las dependencias
Abre la terminal en la carpeta del proyecto y ejecuta:
```bash
pip install -r requirements.txt
```

### Paso 2: Ejecutar la aplicación web
Para abrir la interfaz interactiva en tu navegador:
```bash
streamlit run app.py
```
Se abrirá automáticamente la dirección `http://localhost:8501`.

### Paso 3: Ejecutar la suite de pruebas unitarias
Para validar que los agentes y el código no tengan errores:
```bash
pytest test_app.py
```

---

## 🌐 2. CÓMO PUBLICAR TU APP GRATIS EN INTERNET (Sin servidor propio)

Si tienes un hosting tradicional (PHP/HTML), no necesitas usarlo para Python. La forma moderna, estándar y **100% GRATUITA** de publicar aplicaciones de Streamlit con Python es usar **Streamlit Community Cloud** conectado a **GitHub**.

### Guía en 3 Pasos para Publicar Online:

1. **Crear un Repositorio en GitHub:**
   * Ve a [github.com](https://github.com) y crea una cuenta gratuita si no tienes una.
   * Crea un nuevo repositorio público (ejemplo: `auditor-rag-codigo`).
   * Sube todos los archivos de esta carpeta (`app.py`, `agent_auditor.py`, `agents.md`, `requirements.txt`, etc.).

2. **Conectar con Streamlit Cloud:**
   * Ve a [share.streamlit.io](https://share.streamlit.io/) e inicia sesión con tu cuenta de GitHub.
   * Haz clic en **"New app"** (Nueva aplicación).
   * Selecciona tu repositorio (`auditor-rag-codigo`), la rama (`main`) y el archivo principal (`app.py`).
   * Haz clic en **"Deploy!"** (Desplegar).

3. **¡Listo! Tu App estará Online:**
   * En 2 minutos obtendrás una URL pública en internet, por ejemplo:
     `https://auditor-rag-codigo.streamlit.app`

---

## 🏷️ 3. CÓMO USAR LA ETIQUETA NFC NTAG213

Las etiquetas **NFC NTAG213** son pequeños adhesivos inteligentes que transmiten información a un teléfono inteligente al acercarlo a menos de 5 cm.

### ¿Qué debes grabar en la etiqueta NFC?
1. Una vez desplegada tu app online (ejemplo: `https://auditor-rag-codigo.streamlit.app`), copia esa dirección URL.
2. Abre en tu celular una aplicación gratuita de grabación NFC (como **NFC Tools** para Android o iOS).
3. Selecciona la opción **Escribir (Write) ➔ Añadir registro (Add record) ➔ URL / Enlace**.
4. Pega la dirección de tu aplicación web (`https://auditor-rag-codigo.streamlit.app`) y presiona **Escribir / Grabar**.
5. Acerca la etiqueta NFC NTAG213 a la parte trasera del teléfono para completar la grabación.

### Casos de Uso Prácticos de la Etiqueta NFC:
* **En el Laboratorio o Aula de Clase:** Pega la etiqueta en la mesa del profesor o en la entrada del laboratorio. Los alumnos solo acercan su celular y acceden instantáneamente al auditor de tareas desde su teléfono o laptop.
* **En la Tapa de las Notebooks Vendidas:** Si vendes una computadora a un cliente o alumno, pega la etiqueta NFC en la esquina de la laptop. Al acercar el teléfono, se abre su portal de soporte, manuales y asistentes técnicos sin tener que memorizar enlaces.
