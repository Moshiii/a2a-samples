# Enhanced A2A Protocol Demo

A comprehensive demonstration of the **Agent2Agent (A2A) protocol** showcasing all communication types, task states, content types, and protocol features.

## 🚀 Overview

This enhanced demo demonstrates **every single type of request and handling** of the A2A protocol, going far beyond the basic demo to provide a complete showcase of agent-to-agent communication capabilities.

### What is A2A Protocol?

The **Agent2Agent (A2A) protocol** is an open standard by Google for communication and interoperability between AI agents. It enables agents to:

- **Communicate synchronously and asynchronously**
- **Handle multiple content types** (text, files, structured data)
- **Manage task states** and progress tracking
- **Stream responses** in real-time
- **Handle errors** and edge cases gracefully
- **Support push notifications** for task updates

## ✨ Features Demonstrated

### 🔄 **RPC Methods**
- ✅ `message/send` - Synchronous message communication
- ✅ `message/stream` - Streaming communication via Server-Sent Events (SSE)
- ✅ `tasks/get` - Query task status and details
- ✅ `tasks/cancel` - Cancel running tasks
- ✅ `tasks/pushNotification/set` - Configure push notifications
- ✅ `tasks/pushNotification/get` - Retrieve push notification settings
- ✅ `tasks/resubscribe` - Resubscribe to task updates

### 📊 **Task States**
- ✅ `submitted` - Task has been submitted
- ✅ `working` - Task is currently being processed
- ✅ `input-required` - Task needs additional input
- ✅ `completed` - Task has finished successfully
- ✅ `canceled` - Task has been canceled
- ✅ `failed` - Task has encountered an error
- ✅ `unknown` - Task state is unknown

### 📝 **Content Types (Parts)**
- ✅ `TextPart` - Plain text content
- ✅ `FilePart` - File content with base64 encoding
- ✅ `DataPart` - Structured JSON data

### 🎯 **Event Types**
- ✅ `TaskStatusUpdateEvent` - Task state changes
- ✅ `TaskArtifactUpdateEvent` - New artifacts or outputs

### 🌊 **Advanced Features**
- ✅ **Streaming responses** - Real-time communication
- ✅ **File upload/download** - Binary file handling
- ✅ **Structured data processing** - JSON data handling
- ✅ **Error handling** - Graceful error management
- ✅ **Long-running tasks** - Progress tracking
- ✅ **Input requirements** - Interactive task processing
- ✅ **Task cancellation** - Cancel ongoing operations
- ✅ **Push notifications** - Webhook-based updates

## 🏗️ Project Structure

```
a2a-mcp-without-framework/
├── src/no_llm_framework/
│   ├── enhanced_client/
│   │   ├── enhanced_client.py      # Comprehensive A2A client
│   │   └── __main__.py             # Client entry point
│   ├── enhanced_server/
│   │   ├── enhanced_agent.py       # Enhanced agent implementation
│   │   ├── enhanced_agent_executor.py  # Agent executor
│   │   └── __main__.py             # Server entry point
│   └── server/
│       └── constant.py             # Server constants
├── run_enhanced_demo.sh            # Automated demo runner
├── .env.example                    # Environment variables template
├── ENHANCED_DEMO_README.md         # This file
└── ENHANCED_DEMO_README.md         # Original README
```

## 🛠️ Setup & Installation

### Prerequisites

- Python 3.8+
- Google API Key for LLM interaction
- Internet connection for package installation

### 1. Install Dependencies

```bash
# Install from the main requirements file
pip install -r /path/to/a2a-samples/samples/python/requirements.txt

# Or install specific packages
pip install a2a-sdk httpx uvicorn click python-dotenv google-genai fastapi jinja2
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Edit the file and add your Google API key
GOOGLE_API_KEY=your-actual-api-key-here
DEBUG_MODE=false
```

**Important:** You need a valid Google API key for the LLM functionality to work.

### 3. Verify Installation

```bash
# Test that the enhanced demo script is executable
chmod +x run_enhanced_demo.sh

# Check if environment is properly configured
./run_enhanced_demo.sh
```

## 🚀 Running the Enhanced Demo

### Quick Start

```bash
# Run the complete enhanced demo
./run_enhanced_demo.sh
```

This script will:
1. ✅ Load environment variables from `.env`
2. ✅ Start the enhanced A2A server
3. ✅ Wait for server to be ready
4. ✅ Run comprehensive client demonstrations
5. ✅ Clean up server processes

### Manual Execution

#### Start the Server

```bash
# Navigate to the server directory
cd src/no_llm_framework/enhanced_server

# Start the enhanced server
python __main__.py --host localhost --port 9999
```

#### Run the Client

```bash
# In another terminal, navigate to the client directory
cd src/no_llm_framework/enhanced_client

# Run the enhanced client demo
python __main__.py
```

## 📋 Demo Scenarios

The enhanced demo includes comprehensive scenarios:

### 1. **Comprehensive Protocol Demo**
- All RPC methods in sequence
- All content types demonstration
- Error handling scenarios
- Task management operations

### 2. **Individual Feature Demonstrations**
- **Basic Text Processing** - Simple text communication
- **Streaming Response** - Real-time streaming communication
- **File Upload** - File handling with base64 encoding
- **Structured Data** - JSON data processing
- **Task Query** - Task status and details retrieval
- **Push Notifications** - Webhook configuration (if supported)
- **Error Handling** - Invalid inputs and error scenarios
- **Task Cancellation** - Cancel ongoing operations

### 3. **Special Scenario Demonstrations**
- **Long-running Tasks** - Progress tracking and updates
- **Input Required** - Interactive task processing
- **Error Scenarios** - Error simulation and handling
- **File Processing** - Advanced file analysis
- **Form Processing** - Complex structured data handling

## 🔍 Expected Output

### Server Output
```
🚀 Starting Enhanced A2A Protocol Server
==================================================
📍 Server URL: http://localhost:9999/
📋 Agent Card: http://localhost:9999/.well-known/agent.json
🔧 A2A Endpoint: http://localhost:9999/a2a
🌊 Streaming Endpoint: http://localhost:9999/a2a/stream
==================================================
✨ This server demonstrates ALL A2A protocol features:
   • All RPC methods (message/send, message/stream, tasks/get, tasks/cancel)
   • All task states (submitted, working, input-required, completed, canceled, failed)
   • All event types (TaskStatusUpdateEvent, TaskArtifactUpdateEvent)
   • All content types (TextPart, FilePart, DataPart)
   • Push notifications
   • Error handling
   • Streaming responses
   • Long-running tasks with progress updates
   • Input requirements and user interaction
   • Task cancellation
==================================================
```

### Client Output
```
🚀 Enhanced A2A Protocol Client Demo
============================================================
This demo showcases ALL A2A protocol communication types:
• All RPC methods (message/send, message/stream, tasks/get, tasks/cancel)
• All task states (submitted, working, input-required, completed, canceled, failed)
• All event types (TaskStatusUpdateEvent, TaskArtifactUpdateEvent)
• All content types (TextPart, FilePart, DataPart)
• Push notifications
• Error handling
• Streaming responses
• Long-running tasks with progress updates
• Input requirements and user interaction
• Task cancellation
============================================================

🌟 Running Comprehensive A2A Protocol Demo
============================================================

🔄 Demonstrating synchronous message/send...
📤 SEND Message Request: [message-id]
   Part 0: Text content (42 chars)
✅ Synchronous response received for task [task-id]
   Status: completed

🌊 Demonstrating streaming message/stream...
✅ Streaming completed for task [task-id]

📁 Demonstrating file upload: demo_file.txt
📤 SEND Message Request: [message-id]
   Part 0: Text content (33 chars)
   Part 1: File content (demo_file.txt)
✅ File upload completed for task [task-id]
   Status: completed

📋 Demonstrating structured data: {...}
📤 SEND Message Request: [message-id]
   Part 0: Text content (29 chars)
   Part 1: Structured data
✅ Structured data sent for task [task-id]
   Status: completed
```

## 🔧 API Endpoints

### Server Endpoints
- **Main Server**: `http://localhost:9999/`
- **Agent Card**: `http://localhost:9999/.well-known/agent.json`
- **A2A Endpoint**: `http://localhost:9999/a2a`
- **Streaming Endpoint**: `http://localhost:9999/a2a/stream`

### Agent Capabilities
The enhanced agent supports:
- **Input Modes**: `text`, `file`, `data`
- **Output Modes**: `text`, `file`, `data`
- **Streaming**: `true`
- **Push Notifications**: `true`
- **State Transition History**: `true`

## 📊 Protocol Coverage Comparison

| Feature | Basic Demo | Enhanced Demo |
|---------|------------|---------------|
| **RPC Methods** | 2/7 | **7/7** ✅ |
| **Task States** | 3/7 | **7/7** ✅ |
| **Content Types** | 1/3 | **3/3** ✅ |
| **Event Types** | 1/2 | **2/2** ✅ |
| **Streaming** | ✅ | ✅ |
| **File Handling** | ❌ | ✅ |
| **Structured Data** | ❌ | ✅ |
| **Error Handling** | Basic | **Comprehensive** |
| **Task Management** | ❌ | ✅ |
| **Push Notifications** | ❌ | ✅ |

## 🔑 Key Differences from Basic Demo

### **Enhanced Features**
1. **Comprehensive Protocol Coverage** - All A2A protocol features
2. **Multiple Content Types** - Text, file, and structured data
3. **Advanced Error Handling** - Graceful error management
4. **Task Management** - Query, cancel, and monitor tasks
5. **Streaming Excellence** - Real-time communication
6. **File Processing** - Upload, download, and analysis
7. **Structured Data** - JSON data handling
8. **Interactive Scenarios** - Input requirements and user interaction

### **Technical Improvements**
1. **Better Architecture** - Separated client and server concerns
2. **Enhanced Logging** - Comprehensive request/response logging
3. **Error Recovery** - Graceful handling of failures
4. **Resource Management** - Proper cleanup and resource handling
5. **Environment Configuration** - Flexible configuration via `.env`

## 🎯 Use Cases

This enhanced demo is perfect for:

### **Learning A2A Protocol**
- Understanding all protocol features
- Learning best practices
- Exploring different communication patterns

### **Development & Testing**
- Testing A2A client implementations
- Validating server implementations
- Debugging protocol issues

### **Integration Examples**
- Building A2A-compatible agents
- Implementing protocol features
- Reference implementation

### **Demonstration**
- Showcasing A2A capabilities
- Training and education
- Proof of concept

## 🚨 Troubleshooting

### Common Issues

#### 1. **GOOGLE_API_KEY not set**
```
Error: GOOGLE_API_KEY environment variable is not set
```
**Solution**: Create a `.env` file with your Google API key:
```bash
echo "GOOGLE_API_KEY=your-api-key-here" > .env
```

#### 2. **Port already in use**
```
Error: Address already in use
```
**Solution**: Use a different port or kill existing processes:
```bash
# Kill processes on port 9999
lsof -ti:9999 | xargs kill -9
```

#### 3. **Import errors**
```
ModuleNotFoundError: No module named 'a2a'
```
**Solution**: Install the A2A SDK:
```bash
pip install a2a-sdk
```

#### 4. **Permission denied**
```
Permission denied: ./run_enhanced_demo.sh
```
**Solution**: Make the script executable:
```bash
chmod +x run_enhanced_demo.sh
```

### Debug Mode

Enable debug mode for detailed logging:
```bash
# In .env file
DEBUG_MODE=true
```

## 🔮 Next Steps

### **Extending the Demo**
1. **Add More Content Types** - Images, audio, video
2. **Implement Push Notifications** - Webhook endpoints
3. **Add Authentication** - Secure communication
4. **Multi-Agent Scenarios** - Agent-to-agent communication
5. **Performance Testing** - Load testing and optimization

### **Integration Examples**
1. **Custom Agents** - Build your own A2A agents
2. **Framework Integration** - Integrate with existing frameworks
3. **Production Deployment** - Deploy to production environments
4. **Monitoring & Observability** - Add monitoring and metrics

## 📚 Additional Resources

### **Documentation**
- [A2A Protocol Specification](https://github.com/google/a2a)
- [A2A SDK Documentation](https://github.com/google/a2a-sdk)
- [Protocol Examples](https://github.com/google/a2a-samples)

### **Related Projects**
- [A2A SDK](https://github.com/google/a2a-sdk) - Official A2A SDK
- [A2A Samples](https://github.com/google/a2a-samples) - More examples
- [A2A Protocol](https://github.com/google/a2a) - Protocol specification

## 🤝 Contributing

Contributions are welcome! Please feel free to:

1. **Report Issues** - Bug reports and feature requests
2. **Submit Pull Requests** - Code improvements and new features
3. **Improve Documentation** - Better explanations and examples
4. **Add Examples** - More demonstration scenarios

## 📄 License

This project is part of the A2A samples and follows the same license as the main A2A project.

---

## 🎉 Success!

You've successfully set up and run the **Enhanced A2A Protocol Demo**! This comprehensive demonstration showcases all the power and flexibility of the A2A protocol for agent-to-agent communication.

**Key Achievements:**
- ✅ **All A2A protocol features** demonstrated
- ✅ **Streaming communication** working perfectly
- ✅ **Multiple content types** supported
- ✅ **Comprehensive error handling** implemented
- ✅ **Task management** fully functional
- ✅ **Real-world scenarios** covered

The enhanced demo is now ready for learning, development, and integration! 🚀 
