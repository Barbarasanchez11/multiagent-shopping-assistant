# Multiagent Shopping Assistant

Este proyecto es un asistente de compras multiagente. A continuación, se detallan los pasos necesarios para instalar y ejecutar el proyecto en tu máquina local.

## Clonar el Repositorio

Primero, clona el repositorio desde GitHub:

```bash
git clone https://github.com/Barbarasanchez11/multiagent-shopping-assistant.git
```

## Entrar en el Directorio del Proyecto

Accede al directorio del proyecto:

```bash
cd multiagent-shopping-assistant
```

## Instalación de Dependencias

Instala las siguientes librerías utilizando Poetry:

```bash
poetry add pydantic@2.11.7
poetry add tenacity@9.1.2
poetry add langsmith@0.3.45
poetry add langchain-core@0.3.65
poetry add langgraph-prebuilt@0.2.2
poetry add langgraph@0.4.8
poetry add langgraph-api@0.2.51
poetry add langchain-groq@0.3.2
poetry add langchain@0.3.25
```

## Configuración del Entorno

Crea un archivo `.env` en la raíz del proyecto con la siguiente variable:

```plaintext
GROQ_API_KEY=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
```

> **Nota:** Este paso es exclusivamente para pruebas de un repositorio privado. Bajo ninguna otra circunstancia se debe compartir esta clave.

## Ejecución del Proyecto

Para ejecutar el proyecto localmente, utiliza el siguiente comando:

```bash
poetry run python main.py
```

## Ejecución en Langgraph Studio

Para correr el proyecto en Langgraph Studio, utiliza:

```bash
poetry run langgraph dev --config=langgraph.config.json
```

## Interfaz Gráfica con Streamlit

Para ver la interfaz gráfica de Streamlit, ejecuta:

```bash
poetry run streamlit run app.py
```

## Video de Demostración

Puedes ver un video de demostración del proyecto en el siguiente enlace: [Video Demo](https://drive.google.com/file/d/1PUEliao7GZgfDvu9xkDh_rseVvrtWO0e/view)

---

Este README proporciona las instrucciones necesarias para configurar y ejecutar el proyecto en diferentes entornos. Asegúrate de seguir cada paso cuidadosamente para garantizar una instalación y ejecución correctas.