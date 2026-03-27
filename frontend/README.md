# Canva Magic BG Remover 🪄✨

Herramienta local de eliminación de fondos optimizada para diseñadores de Canva. Utiliza el modelo de IA de última generación **BiRefNet** para segmentación de alta precisión.

## 🚀 Características
- **IA de Alta Precisión:** Implementación de BiRefNet sobre PyTorch.
- **Flujo Zero-Friction:** Soporte para Pegar (Ctrl+V) y Copiar al portapapeles.
- **Arquitectura Local:** Backend en FastAPI y Frontend en React (Vite).
- **Persistencia:** Historial de trabajos gestionado con Supabase/PostgreSQL.
- **Optimizado para Windows:** Incluye instalador automático y lanzador invisible.

## 🛠️ Tech Stack
- **Frontend:** React, Framer Motion, Axios, Lucide Icons.
- **Backend:** Python, FastAPI, SQLAlchemy.
- **IA/ML:** PyTorch, BiRefNet, OpenCV (Refinamiento morfológico).
- **DB:** Supabase (PostgreSQL).

## 📦 Instalación
1. Clonar el repositorio.
2. Configurar el archivo `.env` en `/backend` con las credenciales de Supabase.
3. Ejecutar `PASO_1_INSTALADOR.bat` para configurar entornos y descargar el modelo de IA.
4. Usar `INICIAR_APP.bat` para lanzar la aplicación.

---
Desarrollado como una solución local para optimizar flujos de trabajo creativos.