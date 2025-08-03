import asyncio
import logging
from uuid import uuid4

import httpx

from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    AgentCard,
    MessageSendParams,
    SendMessageRequest,
)

async def main() -> None:
    # Configure logging to show INFO level messages
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    base_url = 'http://localhost:10001'

    async with httpx.AsyncClient(timeout=60.0) as httpx_client:
        # Initialize A2ACardResolver
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=base_url,
        )

        # Fetch Public Agent Card
        try:
            logger.info(f'Fetching agent card from: {base_url}')
            public_card = await resolver.get_agent_card()
            logger.info('Successfully fetched agent card')
            logger.info(public_card.model_dump_json(indent=2, exclude_none=True))
        except Exception as e:
            logger.error(f'Failed to fetch agent card: {e}')
            return

        # Initialize client
        client = A2AClient(
            httpx_client=httpx_client, agent_card=public_card
        )
        logger.info('A2AClient initialized.')

        # Send a simple message
        send_message_payload = {
            'message': {
                'role': 'user',
                'parts': [
                    {'kind': 'text', 'text': 'Hello! Can you help me with currency conversion?'}
                ],
                'message_id': uuid4().hex,
            },
        }
        request = SendMessageRequest(
            id=str(uuid4()), params=MessageSendParams(**send_message_payload)
        )

        try:
            logger.info('Sending message...')
            response = await client.send_message(request)
            logger.info('Response received:')
            print(response.model_dump(mode='json', exclude_none=True))
        except Exception as e:
            logger.error(f'Error sending message: {e}')

if __name__ == '__main__':
    asyncio.run(main()) 
