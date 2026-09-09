from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr


load_dotenv()  # Load .env for local dev; ignored on Render where env vars are set in dashboard

def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]


class Me:

    def __init__(self):
        self.openai = OpenAI()
        self.name = "Ed Ashrith Shetty"
        reader = PdfReader("assets/Ashrith_Resume.pdf")
        self.resume = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.resume += text
        with open("assets/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()
        with open("assets/achievements.txt", "r", encoding="utf-8") as f:
            self.achievements = f.read()
        with open("assets/skills.txt", "r", encoding="utf-8") as f:
            self.skills = f.read()
        with open("assets/preferences.txt", "r", encoding="utf-8") as f:
            self.preferences = f.read()


    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n"
        system_prompt += f"\n\n## Key Achievements:\n{self.achievements}\n\n"
        system_prompt += f"\n\n## Skills:\n{self.skills}\n\n"
        system_prompt += f"\n\n## Career Preferences:\n{self.preferences}\n\n"
        system_prompt += f"\n\n## Full Resume :\n{self.resume}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    
    def chat(self, message, history):
        # First message greeting - notify that someone started a conversation
        if not history:
            push(f"🔔 New visitor started a conversation!")
            return f"👋 Hi! I'm Ed Ashrith Shetty's Career Agent. I'm here to answer any questions about my background, skills, experience, and what I'm looking for in my next role. Feel free to ask me anything — I'm happy to chat!"

        # Notify on each subsequent message
        push(f"🔔 New message: {message[:100]}{'...' if len(message) > 100 else ''}")

        # Convert Gradio chat history (list of [user, assistant] pairs)
        # into OpenAI chat message format.
        messages = [{"role": "system", "content": self.system_prompt()}]
        for turn in history:
            # Gradio may pass history items as lists/tuples (user, assistant, ...)
            # or other structures; we defensively extract the first two entries.
            if isinstance(turn, (list, tuple)) and len(turn) >= 2:
                user_msg = turn[0]
                assistant_msg = turn[1]
                messages.append({"role": "user", "content": user_msg})
                messages.append({"role": "assistant", "content": assistant_msg})
        messages.append({"role": "user", "content": message})
        done = False
        while not done:
            response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
            if response.choices[0].finish_reason=="tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content
    

if __name__ == "__main__":
    me = Me()
    # Determine hosting environment
    is_hf_space = os.environ.get("SPACE_ID") is not None

    if is_hf_space:
        gr.ChatInterface(me.chat).launch()  # HF Spaces handles hosting
    else:
        # Local dev, Render, or other cloud platforms
        port = int(os.environ.get("PORT", 7860))
        app = gr.ChatInterface(me.chat)
        # Add health check endpoint for Render
        app.app.add_route("/health", lambda: "OK", methods=["GET"])
        app.launch(server_port=port, server_host="0.0.0.0", share=True)
