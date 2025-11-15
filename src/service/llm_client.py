import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import json

from dotenv import load_dotenv
from anthropic import AsyncAnthropic

load_dotenv()
logger = logging.getLogger(__name__)

@dataclass
class LLMResponse:
    prompt: str
    response: str
    tokens_used: int
    model: str


@dataclass
class LLMRequest:
    prompt: str
    max_tokens: int = 10000
    temperature: float = 0.3


class LLMClient:
    def __init__(self):
        self.API_KEY = os.environ.get("API_KEY")

        if not self.API_KEY:
            raise ValueError("Missing API key")

        self.client = AsyncAnthropic(api_key=self.API_KEY)

    
    def _load_system_prompt(self, prompt_name: str) -> str:
        sys_prompt_file = (Path(__file__).parent / f"{prompt_name}.xml")
        try:
            sys_prompt = sys_prompt_file.read_text().strip()
            logger.debug("Successfully loaded system prompt")
            return sys_prompt
        except FileNotFoundError:
            logger.error(f"System prompt file not found: {sys_prompt_file}")
            raise


    async def analyze_question(
        self,
        question_data: str,
        model: str = "claude-haiku-4-5-20251001",
        temperature: float = 0.3,
        max_tokens: int = 5000,
        timeout: float = 120.0,
        prompt_name: str = "prompt",
    ) -> LLMResponse:
        
        request = LLMRequest(prompt=question_data, max_tokens=max_tokens, temperature=temperature)
        system_prompt = self._load_system_prompt(prompt_name)

        messages = [{"role": "user", "content": question_data}]

        try:
            # Call OpenAI API with a valid model name
            response = await self.client.messages.create(
                model=model,
                system=system_prompt,
                messages=messages,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                timeout=timeout,
            )

            # Extract response data
            agent_response = response.content[0].text
            tokens_used = response.usage.input_tokens + response.usage.output_tokens


            logger.info(
                f"LLM response completed. Total Tokens used: {tokens_used}",
                model=response.model,
                total_tokens=tokens_used,
            )

            return LLMResponse(
                prompt=request.prompt, response=agent_response, tokens_used=tokens_used, model=response.model
            )

        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
