# Pydantic-AI Currency Agent with A2A Protocol

This sample demonstrates a currency conversion agent built with [Pydantic-AI](https://github.com/jxnl/pydantic-ai) and exposed through the A2A protocol. It showcases conversational interactions with support for multi-turn dialogue and streaming responses.

## How It Works

This agent uses Pydantic-AI with LLM (for example Google Gemini..) to provide currency exchange information through a structured tool-based approach. The A2A protocol enables standardized interaction with the agent, allowing clients to send requests and receive real-time updates.

```mermaid
sequenceDiagram
    participant Client as A2A Client
    participant Server as A2A Server
    participant Agent as Pydantic-AI Agent
    participant API as Frankfurter API

    Client->>Server: Send task with currency query
    Server->>Agent: Forward query to currency agent

    alt Complete Information
        Agent->>API: Call get_exchange_rate tool
        API->>Agent: Return exchange rate data
        Agent->>Server: Process data & return result
        Server->>Client: Respond with currency information
    else Incomplete Information
        Agent->>Server: Request additional input
        Server->>Client: Set state to "input-required"
        Client->>Server: Send additional information
        Server->>Agent: Forward additional info
        Agent->>API: Call get_exchange_rate tool
        API->>Agent: Return exchange rate data
        Agent->>Server: Process data & return result
        Server->>Client: Respond with currency information
    end

    alt With Streaming
        Note over Client,Server: Real-time status updates
        Server->>Client: "Looking up exchange rates..."
        Server->>Client: "Processing exchange rates..."
        Server->>Client: Final result
    end
```

## Key Features

- **Multi-turn Conversations**: Agent can request additional information when needed
- **Real-time Streaming**: Provides status updates during processing
- **Push Notifications**: Support for webhook-based notifications
- **Conversational Memory**: Maintains context across interactions
- **Currency Exchange Tool**: Integrates with Frankfurter API for real-time rates
- **Structured Output**: Uses Pydantic models for type-safe responses

## Prerequisites

- Python 3.12 or higher
- [UV](https://docs.astral.sh/uv/)
- Access to an LLM and API Key

## Setup & Running

1. Navigate to the samples directory:

   ```bash
   cd samples/python/agents/pydantic_ai
   ```

2. Create an environment file with your API key:

   ```bash
   If you're using a Google Gemini model (gemini-pro, etc.):
   echo "GOOGLE_API_KEY=your_api_key_here" > .env
  
   
   If you're using OpenAI or any compatible API (e.g., local LLM via Ollama, LM Studio, etc.):

   echo "API_KEY=your_api_key_here" > .env  (not neccessary if have no api key)
   echo "TOOL_LLM_URL=your_llm_url" > .env
   echo "TOOL_LLM_NAME=your_llm_name" > .env

   ```

3. Run the agent:

   ```bash
   # Basic run on default port 10001
   uv run app

   # On custom host/port
   uv run app --host 0.0.0.0 --port 8080
   ```

4. In a separate terminal, run the test client:

   ```bash
   uv run app/test_client.py
   ```

## Build Container Image

Agent can also be built using a container file.

1. Navigate to the `samples/python/agents/pydantic_ai` directory:

  ```bash
  cd samples/python/agents/pydantic_ai
  ```

2. Build the container file

    ```bash
    podman build . -t pydantic-ai-a2a-server
    ```

> [!Tip]  
> Podman is a drop-in replacement for `docker` which can also be used in these commands.

3. Run your container

    ```bash
    podman run -p 10001:10001 -e GOOGLE_API_KEY=your_api_key_here pydantic-ai-a2a-server
    ```

4. Run A2A client (follow step 5 from the section above)

> [!Important]
> * **Access URL:** You must access the A2A client through the URL `0.0.0.0:10001`. Using `localhost` will not work.
> * **Hostname Override:** If you're deploying to an environment where the hostname is defined differently outside the container, use the `HOST_OVERRIDE` environment variable to set the expected hostname on the Agent Card. This ensures proper communication with your client application.

## Technical Implementation

- **Pydantic-AI Agent**: Uses structured tools and response models for type-safe interactions
- **Streaming Support**: Provides incremental updates during processing
- **Tool Integration**: Clean tool definition with Pydantic models
- **Push Notification System**: Webhook-based updates with JWK authentication
- **A2A Protocol Integration**: Full compliance with A2A specifications

## Differences from LangGraph Version

- **Simpler Architecture**: Pydantic-AI provides a more straightforward approach to tool definition
- **Type Safety**: Better type safety with Pydantic models throughout
- **Structured Responses**: Built-in support for structured response formats
- **Cleaner Tool Definition**: Tools are defined as Pydantic models with clear schemas

## Limitations

- Only supports text-based input/output (no multi-modal support)
- Uses Frankfurter API which has limited currency options
- Memory is session-based and not persisted between server restarts

## Examples

**Synchronous request**

Request:

```
POST http://localhost:10001
Content-Type: application/json

{
    "id": "12113c25-b752-473f-977e-c9ad33cf4f56",
    "jsonrpc": "2.0",
    "method": "message/send",
    "params": {
        "message": {
            "kind": "message",
            "messageId": "120ec73f93024993becf954d03a672bc",
            "parts": [
                {
                    "kind": "text",
                    "text": "how much is 10 USD in INR?"
                }
            ],
            "role": "user"
        }
    }
}
```

Response:

```
{
    "id": "12113c25-b752-473f-977e-c9ad33cf4f56",
    "jsonrpc": "2.0",
    "result": {
        "artifacts": [
            {
                "artifactId": "08373241-a745-4abe-a78b-9ca60882bcc6",
                "name": "conversion_result",
                "parts": [
                    {
                        "kind": "text",
                        "text": "10 USD is 856.2 INR."
                    }
                ]
            }
        ],
        "contextId": "e329f200-eaf4-4ae9-a8ef-a33cf9485367",
        "history": [
            {
                "contextId": "e329f200-eaf4-4ae9-a8ef-a33cf9485367",
                "kind": "message",
                "messageId": "120ec73f93024993becf954d03a672bc",
                "parts": [
                    {
                        "kind": "text",
                        "text": "how much is 10 USD in INR?"
                    }
                ],
                "role": "user",
                "taskId": "58124b63-dd3b-46b8-bf1d-1cc1aefd1c8f"
            },
            {
                "contextId": "e329f200-eaf4-4ae9-a8ef-a33cf9485367",
                "kind": "message",
                "messageId": "d8b4d7de-709f-40f7-ae0c-fd6ee398a2bf",
                "parts": [
                    {
                        "kind": "text",
                        "text": "Looking up the exchange rates..."
                    }
                ],
                "role": "agent",
                "taskId": "58124b63-dd3b-46b8-bf1d-1cc1aefd1c8f"
            },
            {
                "contextId": "e329f200-eaf4-4ae9-a8ef-a33cf9485367",
                "kind": "message",
                "messageId": "ee0cb3b6-c3d6-4316-8d58-315c437a2a77",
                "parts": [
                    {
                        "kind": "text",
                        "text": "Processing the exchange rates.."
                    }
                ],
                "role": "agent",
                "taskId": "58124b63-dd3b-46b8-bf1d-1cc1aefd1c8f"
            }
        ],
        "id": "58124b63-dd3b-46b8-bf1d-1cc1aefd1c8f",
        "kind": "task",
        "status": {
            "state": "completed"
        }
    }
}
```

## Learn More

- [A2A Protocol Documentation](https://a2a-protocol.org/)
- [Pydantic-AI Documentation](https://github.com/jxnl/pydantic-ai)
- [Frankfurter API](https://www.frankfurter.app/docs/)
- [Google Gemini API](https://ai.google.dev/gemini-api)

## Disclaimer
Important: The sample code provided is for demonstration purposes and illustrates the mechanics of the Agent-to-Agent (A2A) protocol. When building production applications, it is critical to treat any agent operating outside of your direct control as a potentially untrusted entity.

All data received from an external agent—including but not limited to its AgentCard, messages, artifacts, and task statuses—should be handled as untrusted input. For example, a malicious agent could provide an AgentCard containing crafted data in its fields (e.g., description, name, skills.description). If this data is used without sanitization to construct prompts for a Large Language Model (LLM), it could expose your application to prompt injection attacks.  Failure to properly validate and sanitize this data before use can introduce security vulnerabilities into your application.

Developers are responsible for implementing appropriate security measures, such as input validation and secure handling of credentials to protect their systems and users. 
