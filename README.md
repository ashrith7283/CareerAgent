---
title: CareerAgent
emoji: 💼
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: "5.22"
python_version: "3.12"
app_file: app.py
pinned: false
---

# CareerAgent

**An AI-powered career assistant that represents you—answering questions about your background, skills, and experience, and helping visitors get in touch.**

CareerAgent is a conversational AI agent that runs on your resume and a short summary. It stays in character, answers professional and career-related questions, and can capture leads (email, name, notes) and log questions it couldn’t answer—all through a simple chat interface.

---

## Features

- **Career Q&A** — Answers questions about your experience, skills, and background using your resume and summary.
- **Lead capture** — Records visitor email, name, and notes when they want to stay in touch.
- **Unknown-question logging** — Sends questions the agent couldn’t answer to you (e.g. via Pushover) for follow-up.
- **Chat interface** — Clean Gradio chat UI, easy to embed or share.
- **Tool use** — Uses OpenAI function calling for structured actions (record details, log questions).

---

## How It Works

1. **Context** — On startup, the app loads your resume (PDF) and a text summary from `assets/`.
2. **Chat** — Visitors talk to an AI that is prompted to act as you and use only that context.
3. **Tools** — The model can call:
   - `record_user_details` — Store email, name, and notes (e.g. trigger a notification).
   - `record_unknown_question` — Log questions it couldn’t answer (e.g. push to Pushover).
4. **UI** — Gradio’s ChatInterface handles the conversation and display.

---

## Tech Stack

| Layer        | Technology        |
|-------------|--------------------|
| **UI**      | Gradio             |
| **LLM**     | OpenAI (GPT-4o-mini) |
| **Tools**   | OpenAI function calling |
| **Notifications** | Pushover (optional) |
| **Python**  | 3.12+              |

---

## Prerequisites

- **Python** 3.12 or higher  
- **OpenAI API key**  
- (Optional) **Pushover** account and credentials for lead/unknown-question notifications  

---

## Installation

**With [uv](https://docs.astral.sh/uv/):**

```bash
git clone <your-repo-url>
cd CareerAgent
uv sync
```

**With pip:**

```bash
git clone <your-repo-url>
cd CareerAgent
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
PUSHOVER_TOKEN=your_pushover_token    # optional
PUSHOVER_USER=your_pushover_user      # optional
```

Without Pushover keys, the app still runs; tool calls for recording leads or unknown questions will no-op unless you add your own notification logic.

---

## Running the App

```bash
uv run app.py
```

Or, if using pip:

```bash
python app.py
```

The Gradio app will start (with `share=True` you get a temporary public link). Open the URL shown in the terminal (e.g. `http://127.0.0.1:7860`) to use the chat interface.

---

## Project Structure

```
CareerAgent/
├── app.py              # Gradio app, OpenAI client, tools, and agent logic
├── assets/
│   ├── Ashrith_Resume.pdf   # Resume PDF (replace with your own)
│   ├── summary.txt          # Enhanced career summary
│   ├── achievements.txt     # Key achievements
│   ├── skills.txt           # Detailed skills breakdown
│   └── preferences.txt      # Career preferences
├── .env                 # API keys and optional Pushover config (do not commit)
├── pyproject.toml       # Project metadata and dependencies
├── requirements.txt    # Pip-installable dependencies
└── README.md           # This file
```

**Customization:**
- Put your resume PDF in `assets/` and update `assets/summary.txt`, `assets/achievements.txt`, `assets/skills.txt`, and `assets/preferences.txt` with your own information.
- In `app.py`, update the `Me` class (e.g. `self.name`, file paths) to match your name and files.

---

## License

Use and modify as you like. If you use or extend this project, attribution is appreciated.
