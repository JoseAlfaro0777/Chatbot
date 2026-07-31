# 🤖 Chatbot con OpenAI API

API de chatbot construida con **FastAPI** y **OpenAI GPT-4o**, con soporte de streaming en tiempo real, historial de conversación y despliegue con Docker.

## Tecnologías

| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.12 | Lenguaje base |
| FastAPI | 0.111 | Framework web |
| OpenAI SDK | 1.30 | Integración con GPT-4o |
| Uvicorn | 0.29 | Servidor ASGI |
| Docker | latest | Contenedorización |

## Estructura del proyecto

```
chatbot/
├── main.py              # Aplicación FastAPI + endpoints
├── requirements.txt     # Dependencias Python
├── Dockerfile           # Imagen Docker
├── .env.example         # Variables de entorno de ejemplo
└── README.md
```

## Instalación y uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/chatbot-openai.git
cd chatbot-openai
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita el archivo `.env`:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Instalar dependencias

```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
# venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

### 4. Ejecutar el servidor

```bash
uvicorn main:app --reload --port 8000
```

La API estará disponible en `http://localhost:8000`.  
Documentación interactiva: `http://localhost:8000/docs`

### Con Docker

```bash
docker build -t chatbot-api .
docker run -p 8000:8000 --env-file .env chatbot-api
```

## Endpoints

### `POST /chat` — Respuesta estándar

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "¿Qué es la inteligencia artificial?"}
    ],
    "system_prompt": "Eres un asistente experto en tecnología.",
    "model": "gpt-4o",
    "temperature": 0.7
  }'
```

Respuesta:

```json
{
  "reply": "La inteligencia artificial es...",
  "tokens_used": 142,
  "model": "gpt-4o-2024-05-13"
}
```

### `POST /chat/stream` — Streaming en tiempo real (SSE)

```bash
curl -N -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Explica qué es Python"}]
  }'
```

Retorna eventos `text/event-stream`:

```
data: {"delta": "Python"}
data: {"delta": " es un"}
data: {"delta": " lenguaje..."}
data: [DONE]
```

### `GET /health` — Health check

```bash
curl http://localhost:8000/health
# {"status": "ok"}
```

## Enviar historial de conversación

Para mantener contexto entre turnos, incluye todos los mensajes anteriores:

```json
{
  "messages": [
    {"role": "user",      "content": "Hola, ¿cómo te llamas?"},
    {"role": "assistant", "content": "Soy un asistente de IA."},
    {"role": "user",      "content": "¿Qué puedes hacer?"}
  ]
}
```

## Variables de entorno

| Variable | Requerida | Descripción |
|---|---|---|
| `OPENAI_API_KEY` | ✅ Sí | Clave de API de OpenAI |

## Notas de desarrollo

- El endpoint `/chat/stream` usa **Server-Sent Events (SSE)** para transmitir tokens a medida que el modelo los genera.
- El campo `system_prompt` permite personalizar el comportamiento del modelo sin modificar el código.
- `temperature` controla la creatividad: `0.0` = determinista, `1.0` = más creativo.

## Licencia

MIT
