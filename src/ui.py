from typing import Any, Dict
from gradio.themes import Base
from gradio.themes.utils import colors, fonts, sizes
import time
import httpx
from app_config import CONFIG
import gradio as gr
import logging
import json

BOLD = "\033[1m"
RED = "\033[91m"
RESET = "\033[0m"
BLUE = "\033[94m"
CYAN = "\033[96m"

def get_api_response(question, student_answer, rubric):
    """
    Call the grader API with question, student answer, and rubric.
    Returns the grading response.
    """
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    
    # JSON payload
    payload = {
        "question": question,
        "student_answer": student_answer,
        "rubric": rubric,
    }
    
    url = f"{CONFIG.API_PROTOCOL}://{CONFIG.API_HOST}:{CONFIG.API_PORT}/api/grader"
    
    try:
        logging.info(f"Posting to URL {url}")
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                url,
                headers=headers,
                json=payload,  # Using JSON
            )
            response.raise_for_status()
            
            # Parse JSON response
            data = response.json()
            
            # Extract and format the response
            result = data.get("response", "No response received")
            tokens = data.get("tokens_used", "N/A")
            model = data.get("model", "N/A")
            
            # Format with metadata
            formatted_response = f"{result}\n\n---\n📊 Tokens used: {tokens} | Model: {model}"
            
            return formatted_response
            
    except httpx.RequestError as e:
        logging.error(f"Error calling API: {e}")
        return f"Sorry, I couldn't connect to the backend service. Please check if the API is running at {url}."
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error from API: {e}")
        return f"Error from server: {e.response.text}"
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return f"An unexpected error occurred: {str(e)}"

# Simple custom theme - just colors, no layout changes
class GraderTheme(Base):
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

app = gr.Blocks(theme=GraderTheme())

with app:
    # Add fonts and CSS
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
    
    .input-container textarea {
        background: color-mix(in srgb, var(--input-background-fill) 20%, transparent) !important;
        margin-right: 10px !important;
        border-radius: var(--block-radius) !important;
    }
    </style>
    """)
    
    gr.Markdown("# 📝 Auto Grader")
    gr.Markdown("Enter the question, student answer, and rubric to get automated grading feedback.")
    
    with gr.Row():
        with gr.Column(scale=1):
            question_input = gr.Textbox(
                label="Question",
                placeholder="Enter the question here...",
                lines=3,
            )
            student_answer_input = gr.Textbox(
                label="Student Answer",
                placeholder="Enter the student's answer here...",
                lines=5,
            )
            rubric_input = gr.Textbox(
                label="Rubric",
                placeholder="Enter the grading rubric here...",
                lines=5,
            )
            
            submit_btn = gr.Button("Grade", variant="primary")
            clear_btn = gr.ClearButton([question_input, student_answer_input, rubric_input])
        
        with gr.Column(scale=1):
            output = gr.Textbox(
                label="Grading Result",
                lines=15,
                interactive=False,
            )
    
    # Example inputs - Using Accordion instead of Examples table
    with gr.Accordion("💡 Example Questions (Click to expand)", open=False):
        gr.Markdown("""
        ### Example 1: Simple Factual Question
        **Question:** What is the capital of France?  
        **Student Answer:** Paris is the capital of France.  
        **Rubric:** 1 point for correct answer. 0 points for incorrect answer.
        """)
        example1_btn = gr.Button("📋 Use Example 1", size="sm")
        
        gr.Markdown("""
        ### Example 2: Explanation Question
        **Question:** Explain the difference between supervised and unsupervised learning.  
        **Student Answer:** Supervised learning uses labeled data while unsupervised learning finds patterns in unlabeled data.  
        **Rubric:** Full credit (5 pts): Clear explanation of both concepts with examples. Partial credit (3 pts): Mentions key difference but lacks detail. No credit (0 pts): Incorrect or missing explanation.
        """)
        example2_btn = gr.Button("📋 Use Example 2", size="sm")
    
    # Button click handlers to populate fields
    example1_btn.click(
        fn=lambda: [
            "What is the capital of France?",
            "Paris is the capital of France.",
            "1 point for correct answer. 0 points for incorrect answer."
        ],
        outputs=[question_input, student_answer_input, rubric_input],
    )
    
    example2_btn.click(
        fn=lambda: [
            "Explain the difference between supervised and unsupervised learning.",
            "Supervised learning uses labeled data while unsupervised learning finds patterns in unlabeled data.",
            "Full credit (5 pts): Clear explanation of both concepts with examples. Partial credit (3 pts): Mentions key difference but lacks detail. No credit (0 pts): Incorrect or missing explanation."
        ],
        outputs=[question_input, student_answer_input, rubric_input],
    )
    
    submit_btn.click(
        fn=get_api_response,
        inputs=[question_input, student_answer_input, rubric_input],
        outputs=output,
    )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Launching Gradio grader on host {CONFIG.APP_HOST} with port {CONFIG.APP_PORT}")
    app.launch(server_name=CONFIG.APP_HOST, server_port=CONFIG.APP_PORT)