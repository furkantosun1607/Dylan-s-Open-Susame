# 🎸 Dylan Door AI

## Project Summary & Artistic Vision

**Dylan Door AI** is an interactive web experience that invites users to *knock* on a virtual door.  By speaking into their microphone the app captures an audio snippet, transcribes it, and then, through a **Bob Dylan‑style AI persona**, generates:

- A short philosophical poem (3 lines) echoing the spirit of Dylan’s 1973 *‘Knockin’ on Heaven’s Door’*.
- An evocative emotion / transition description.
- A **Stable‑Diffusion** prompt that creates a cinematic image of a door that visualizes the user’s metaphorical threshold.

The result is displayed as a stylised, dark‑mode UI that feels like a 1970s western film poster – the perfect blend of art and AI.

---

## Technical Architecture

```
└─ dylan_ai/
   ├─ backend/                # FastAPI server (Python)
   │   ├─ src/
   │   │   ├─ api/            # HTTP routes (knock endpoint)
   │   │   ├─ core/           # Agent & config
   │   │   └─ services/       # STT, TTS, Image generation
   │   └─ requirements.txt    # Python deps
   ├─ frontend/               # React app (Vite) – modern UI
   │   └─ src/App.jsx          # Main component
   └─ .env                    # Secrets (Groq API key, etc.)
```

- **Speech‑to‑Text (STT)** – `faster-whisper` transcribes the audio file.
- **LLM (Groq API)** – `langchain_groq.ChatGroq` produces a structured `DylanResponse` (emotion, poem, image_prompt).
- **Stable Diffusion** – `diffusers` generates the door image based on the prompt.
- **Text‑to‑Speech (TTS)** – optional service that turns the poem into audio.
- **Frontend** – fetches the `/knock` endpoint, displays the image, poem, and plays the generated audio.

---

## Setup Instructions

### Prerequisites
- Python 3.10+ and `pip`
- Node.js 20+ and `npm`
- A **Groq API key** (sign up at https://groq.com)
- (Optional) **Stable Diffusion** model files if you run the image service locally.

### Backend
```bash
# Clone the repo (assuming you have a remote – replace with your URL)
git clone <your‑repo‑url>
cd dylan_ai/backend

# Create virtual environment
python -m venv venv
source venv/Scripts/activate   # Windows PowerShell

# Install deps
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and set GROQ_API_KEY=<your‑key>

# Run the server
uvicorn src.main:app --reload
```

### Frontend
```bash
cd ../frontend
npm install
npm run dev   # Vite dev server on http://localhost:5173
```

Visit the web UI, click **KNOCK**, record your voice, and watch the Dylan‑inspired magic happen!

---

## Used AI Techniques
1. **Large Language Model (LLM) – Groq (llama‑3.3‑70b‑versatile)**
   - Prompt engineering creates a Bob Dylan persona.
   - Structured output (`DylanResponse`) is enforced via LangChain’s `with_structured_output`.
2. **Text‑to‑Image – Stable Diffusion (Diffusers)**
   - The LLM‑generated `image_prompt` drives the diffusion model to render a cinematic door.
   - The image is served back to the frontend as a static asset.

(We also have a **STT** service using `faster‑whisper` and a **TTS** service based on `edge‑tts`, but the two items above satisfy the requirement.)

---

## Dependencies
| Category | Library / Service | Version |
|----------|-------------------|---------|
| **Backend** | fastapi | ^0.115.0 |
| | uvicorn | ^0.30.1 |
| | langchain‑groq | ^0.2.0 |
| | pydantic | ^2.8.2 |
| | faster‑whisper | ^1.0.2 |
| | diffusers | ^0.30.0 |
| | torch | >=2.0 |
| | edge‑tts | ^6.1.12 |
| **Frontend** | react | ^18.3.0 |
| | vite | ^5.4.0 |
| | tailwindcss (optional for styling) | ^3.4.0 |
| **Dev / Ops** | python‑dotenv | ^1.0.1 |
| | python‑dotenv | ^1.0.1 |

---

## Example Outputs
Below is a mock‑up of the result page showing the generated door image on the left and the Dylan‑style poem on the right.

![Example output](file:///C:/Users/Furkan/.gemini/antigravity/brain/c6baaf12-de81-4412-a1e5-96f5528f9df2/example_output_1777797958840.png)

*The poem (example):*
> "When the wind whispers the final chord,\
>  Shadows stretch across the fading road,\
>  I stand before the night‑kissed door."

---

## License & Credits
This project is open‑source under the **MIT License**.  It leverages the following open‑source components:
- **LangChain** – orchestration of LLM calls.
- **FastAPI** – lightweight backend framework.
- **Diffusers** – Stable Diffusion implementation.
- **faster‑whisper** – speech‑to‑text.
- **React** – modern UI.
- **Bob Dylan** – cultural inspiration (fair‑use for artistic parody).

---

*Happy knocking!*
