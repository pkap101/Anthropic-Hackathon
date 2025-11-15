from typing import Any, Dict
from gradio.themes import Base
from gradio.themes.utils import colors, fonts, sizes
import time
import httpx
from config import CONFIG
import gradio as gr
import logging
import json

BOLD = "\033[1m"
gr.ChatMessage
RED = "\033[91m"
RESET = "\033[0m"
BLUE = "\033[94m"
CYAN = "\033[96m"

def build_tool_content(used_tools: Dict[str, Dict[str, Any]]):
    content = ""
    for tool in used_tools.values():
        duration = "Pending"
        if "start_time" in tool and "end_time" in tool:
            duration = f"{round(tool["end_time"] - tool["start_time"], 2)}s"
        content += f"Task: {tool["description"]} ({duration})\n" \
            f"Args: {tool["args"]}\n\n"
        
    return content

def get_api_response(message, history):
    """
    Async version using httpx for better streaming support
    """
    headers = {
        "accept": "text/plain",
        "Content-Type": "application/json"
    }
    payload = {
        "user_message": message,
        "history": history,
    }
    url = f"{CONFIG.API_PROTOCOL}://{CONFIG.API_HOST}:{CONFIG.API_PORT}/api/v1/chat"
    msgs = []
    try:
        logging.info(f"Posting to URL {url}")
        with httpx.Client() as client:
            with client.stream(
                "POST",
                url,
                headers=headers,
                json=payload,  # httpx can handle json directly
                timeout=30.0
            ) as response:
                response.raise_for_status()
                content = ""
                # hold reference to th final content dict
                gathered_response = {
                    "role": "assistant",
                    "content": "",
                }
                # hold reference to the final tool dict
                gathered_tools = {
                    "role": "assistant",
                    "content": "",
                    "metadata": {
                        "title": "Processing...",
                        "status": "pending",
                    },
                }
                used_tools: Dict[str, Dict[str, Any]] = {}
                for chunk in response.iter_text():
                    content += chunk
                    find_start_i = 0
                    while True:
                        close_msg_i = content.find("}", find_start_i)
                        if close_msg_i == -1:
                            yield msgs
                            break
                        find_start_i = close_msg_i + 1
                        try:
                            parsed = json.loads(content[0:close_msg_i + 1])
                            content = content[close_msg_i + 1:]
                            if "tool_start" in parsed:
                                used_tools[parsed["id"]] = parsed
                                used_tools[parsed["id"]]["start_time"] = time.time()
                                if gathered_tools not in msgs:
                                    msgs.append(gathered_tools)
                                gathered_tools["content"] = build_tool_content(used_tools)
                                gathered_tools["metadata"]["status"] = "pending"
                                yield msgs
                            if "tool_end" in parsed:
                                # iterate through the msgs, searching for the tool start
                                # item (filtering by tool_id)
                                used_tools[parsed["id"]]["end_time"] = time.time()
                                gathered_tools["content"] = build_tool_content(used_tools)
                                gathered_tools["metadata"]["status"] = "done" if all("end_time" in inner_dict for inner_dict in used_tools.values()) else "pending"
                                gathered_tools["metadata"]["title"] = "Processed" if all("end_time" in inner_dict for inner_dict in used_tools.values()) else "Processing..."
                                print(all("end_time" in inner_dict for inner_dict in used_tools.values()))
                                print(used_tools.values())
                                print(f"{BLUE}{gathered_tools["metadata"]["status"]}{RESET}")
                                yield msgs
                            if "response" in parsed:
                                if gathered_response not in msgs:
                                    msgs.append(gathered_response)
                                gathered_response["content"] += parsed["response"]
                                yield msgs
                        except json.JSONDecodeError:
                            # if there's a JSON decode error, assume we're attempting to parse an
                            # incomplete JSON (ie. '{"x": {}')
                            pass
                yield msgs
    except httpx.RequestError as e:
        logging.error(f"Error calling API: {e}")
        yield f"Sorry, I couldn't connect to the backend service. Please check if the API is running at {url}."

# Simple custom theme - just colors, no layout changes
class OpsCopilotTheme(Base):
    def __init__(self):
        super().__init__(
            primary_hue=colors.indigo,
            secondary_hue=colors.slate,
            neutral_hue=colors.slate,
        )
        # Only change colors, don't mess with layout
        self.set(
            # Dark backgrounds
            body_background_fill="#0f172a",
            body_background_fill_dark="#0f172a",
            background_fill_primary="#1e293b",
            background_fill_primary_dark="#1e293b",
            # Better text contrast
            body_text_color="#f1f5f9",
            body_text_color_dark="#f1f5f9",
            # Nice accent color
            button_primary_background_fill="#4f46e5",
            button_primary_background_fill_dark="#4f46e5",
        )

app = gr.Blocks(theme=OpsCopilotTheme())

with app:
    # Just add fonts, minimal CSS
    google_fonts = gr.HTML("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    
    <style>
    /* Just apply fonts, don't change layout */
    .gradio-container {
        font-family: 'Inter', system-ui, sans-serif !important;
    }
    
    .gradio-container h1,
    .gradio-container h2,
    .gradio-container h3 {
        font-family: 'Space Grotesk', system-ui, sans-serif !important;
        font-weight: 600 !important;
    }
    
    .bot-row {
        min-width: 70%;
    }
    
    #component-7 {
        height: 800px !important;
    }
    #component-9 .bubble-wrap {
        background-color: black;
    }
    .input-container textarea {
        background: color-mix(in srgb, var(--input-background-fill) 20%, transparent) !important;
        margin-right: 10px !important;
        border-radius: var(--block-radius) !important;
    }
    .message-row .user {
        background: var(--background-fill-secondary) !important;
    }
    </style>
    """)    
    
    gr.ChatInterface(
        fn=get_api_response,
        type="messages",
        title="OpsCopilot",
        examples=["📝 Check the status for AI Gateway", "🚨 What are the most recent AI Platform issues?"],
    )

if __name__ == "__main__":
    logging.info(f"Launching Gradio chat on host {CONFIG.APP_HOST} with port {CONFIG.APP_PORT}")
    app.launch(server_name=CONFIG.APP_HOST, server_port=CONFIG.APP_PORT)
