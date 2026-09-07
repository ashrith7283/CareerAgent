# CareerAgent

An AI-powered career assistant that represents you—answering questions about your background, skills, and experience, and helping visitors get in touch.

## Tech Stack

- **UI**: Gradio (`gradio.ChatInterface`)
- **LLM**: OpenAI GPT-4o-mini via `openai` SDK
- **Tools**: OpenAI function calling (`record_user_details`, `record_unknown_question`)
- **Notifications**: Pushover (optional)
- **Python**: 3.12+

## Project Structure

```
CareerAgent/
├── app.py              # Main Gradio app with Me class, tools, and chat logic
├── assets/
│   ├── Ashrith_Resume.pdf   # Resume PDF (full details)
│   ├── summary.txt          # Enhanced career summary
│   ├── achievements.txt     # Key achievements with metrics
│   ├── skills.txt           # Detailed skills breakdown
│   └── preferences.txt      # Career preferences for recruiters
├── pyproject.toml       # uv/pip dependencies
├── requirements.txt     # Pip-installable deps
└── README.md           # User-facing docs
```

## Key Files

### `app.py`

- **`Me` class** (line 76): Core agent logic
  - Loads resume PDF via `pypdf.PdfReader`
  - Loads all context files from `assets/` (summary, achievements, skills, preferences)
  - `system_prompt()` (line 108): Builds comprehensive system prompt with all context
  - `chat()` (line 124): Handles OpenAI chat completions with tool calls
  - `handle_tool_call()` (line 97): Dispatches tool calls to actual functions

- **Tool functions**:
  - `record_user_details(email, name, notes)` (line 23): Calls Pushover to notify of lead capture
  - `record_unknown_question(question)` (line 27): Logs questions agent couldn't answer

- **Tools schema** (lines 31-73): OpenAI function definitions for `record_user_details` and `record_unknown_question`

- **Entry point** (line 151): `gr.ChatInterface(me.chat).launch(share=True)`

### `assets/` Files

| File | Purpose |
|------|---------|
| `summary.txt` | Enhanced career summary with who you are, approach, expertise, and what you're looking for |
| `achievements.txt` | Key achievements with context (add specific metrics where noted) |
| `skills.txt` | Detailed skills breakdown by category with proficiency levels |
| `preferences.txt` | Career preferences: role type, work arrangement, location, compensation notes |
| `Ashrith_Resume.pdf` | Full resume with complete work history |

## Running

```bash
uv run app.py
# or
python app.py
```

Gradio launches on `http://127.0.0.1:7860` (with `share=True` creates a temporary public link).

## Environment Variables

```env
OPENAI_API_KEY=sk-...       # Required
PUSHOVER_TOKEN=...          # Optional
PUSHOVER_USER=...           # Optional
```

## Customization

To personalize for a different person:

1. Replace `assets/Ashrith_Resume.pdf` with their resume
2. Update `assets/summary.txt` with their career summary
3. Update `assets/achievements.txt` with their key achievements
4. Update `assets/skills.txt` with their skills breakdown
5. Update `assets/preferences.txt` with their career preferences
6. Change `self.name` in the `Me.__init__` method (line 80)

## Dependencies

Installed via `uv sync` or `pip install -r requirements.txt`:
- `gradio>=5.22.0`
- `openai>=1.68.2`
- `pypdf>=5.4.0`
- `python-dotenv>=1.0.1`
- `requests>=2.32.3`
