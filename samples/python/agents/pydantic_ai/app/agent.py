import os
from collections.abc import AsyncIterable
from typing import Any, Literal

import httpx
from pydantic import BaseModel, Field
from pydantic_ai import Agent, Tool

# Define the tool for currency conversion
def get_exchange_rate(
    currency_from: str,
    currency_to: str,
    currency_date: str = "latest"
) -> dict[str, Any]:
    """Get current exchange rate between two currencies.
    
    Args:
        currency_from: The currency to convert from (e.g., 'USD')
        currency_to: The currency to convert to (e.g., 'EUR')
        currency_date: The date for the exchange rate or 'latest'
    """
    try:
        response = httpx.get(
            f'https://api.frankfurter.app/{currency_date}',
            params={'from': currency_from, 'to': currency_to},
        )
        response.raise_for_status()

        data = response.json()
        if 'rates' not in data:
            return {'error': 'Invalid API response format.'}
        return data
    except httpx.HTTPError as e:
        return {'error': f'API request failed: {e}'}
    except ValueError:
        return {'error': 'Invalid JSON response from API.'}





class CurrencyAgent:
    """CurrencyAgent - a specialized assistant for currency conversions using Pydantic-AI."""

    SYSTEM_INSTRUCTION = (
        'You are a specialized assistant for currency conversions. '
        "Your sole purpose is to use the 'get_exchange_rate' tool to answer questions about currency exchange rates. "
        'If the user asks about anything other than currency conversion or exchange rates, '
        'politely state that you cannot help with that topic and can only assist with currency-related queries. '
        'Do not attempt to answer unrelated questions or use tools for other purposes.'
    )

    FORMAT_INSTRUCTION = (
        'Set response status to input_required if the user needs to provide more information to complete the request. '
        'Set response status to error if there is an error while processing the request. '
        'Set response status to completed if the request is complete.'
    )

    def __init__(self):
        model_source = os.getenv('model_source', 'google')
        if model_source == 'google':
            self.agent = Agent(
                model="gemini-2.0-flash",
                tools=[get_exchange_rate],
                system_prompt=self.SYSTEM_INSTRUCTION
            )
        else:
            # For OpenAI or other models
            self.agent = Agent(
                model=os.getenv('TOOL_LLM_NAME', 'gpt-4'),
                tools=[get_exchange_rate],
                system_prompt=self.SYSTEM_INSTRUCTION
            )

    async def stream(self, query: str, context_id: str) -> AsyncIterable[dict[str, Any]]:
        """Stream the agent response."""
        try:
            # First yield a status update
            yield {
                'is_task_complete': False,
                'require_user_input': False,
                'content': 'Looking up the exchange rates...',
            }
            
            # Process the query
            response = await self.agent.run(query)
            
            # Yield processing status
            yield {
                'is_task_complete': False,
                'require_user_input': False,
                'content': 'Processing the exchange rates..',
            }
            
            # Return the final response
            yield self.get_agent_response(response)
            
        except Exception as e:
            yield {
                'is_task_complete': False,
                'require_user_input': True,
                'content': f'Error processing request: {str(e)}',
            }

    def get_agent_response(self, response) -> dict[str, Any]:
        """Process the agent response and return appropriate format."""
        # Extract the string content from AgentRunResult
        if hasattr(response, 'output'):
            content = response.output
        else:
            content = str(response)
            
        return {
            'is_task_complete': True,
            'require_user_input': False,
            'content': content,
        }



    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain'] 
