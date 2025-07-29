# A2A All Requests Demo

A comprehensive demonstration of the **Agent2Agent (A2A) protocol** showcasing **every single type of request and handling** of the A2A protocol.

## 🚀 Overview

This enhanced demo goes far beyond basic A2A demonstrations to provide a **complete showcase** of all agent-to-agent communication capabilities. Unlike other demos that show only a few communication types, this demo demonstrates **100% of the A2A protocol features**.

## ✨ What This Demo Covers

### **Complete Protocol Coverage**
- ✅ **All 7 RPC Methods** - `message/send`, `message/stream`, `tasks/get`, `tasks/cancel`, `tasks/pushNotification/set`, `tasks/pushNotification/get`, `tasks/resubscribe`
- ✅ **All 7 Task States** - `submitted`, `working`, `input-required`, `completed`, `canceled`, `failed`, `unknown`
- ✅ **All 3 Content Types** - `TextPart`, `FilePart`, `DataPart`
- ✅ **All 2 Event Types** - `TaskStatusUpdateEvent`, `TaskArtifactUpdateEvent`

### **Advanced Features**
- 🌊 **Streaming Communication** - Real-time Server-Sent Events (SSE)
- 📁 **File Processing** - Upload, download, and analysis
- 📋 **Structured Data** - JSON data and form processing
- 🔄 **Task Management** - Query, cancel, and monitor tasks
- 🚨 **Error Handling** - Comprehensive error scenarios
- 🔔 **Push Notifications** - Webhook-based updates
- ⏱️ **Long-running Tasks** - Progress tracking and updates
- 🤔 **Input Requirements** - Interactive task processing

## 🏗️ Project Structure

```
a2a-all-requests-without-framwork/
├── src/
│   └── a2a_all_requests/
│       ├── enhanced_client/          # Comprehensive A2A client
│       │   ├── enhanced_client.py    # All protocol features
│       │   └── __main__.py           # Client entry point
│       └── enhanced_server/          # Enhanced A2A server
│           ├── enhanced_agent.py     # Agent implementation
│           ├── enhanced_agent_executor.py  # Agent executor
│           └── __main__.py           # Server entry point
├── run_enhanced_demo.sh              # Automated demo runner
├── .env.example                      # Environment variables template
├── pyproject.toml                    # Project configuration
├── README.md                         # This file
└── ENHANCED_DEMO_README.md           # Detailed documentation
```

## 🛠️ Quick Start

### 1. **Install Dependencies**
```bash
pip install -r /path/to/a2a-samples/samples/python/requirements.txt
```

### 2. **Configure Environment**
```bash
# Copy and edit the environment file
cp .env.example .env
# Add your Google API key to .env
```

### 3. **Run the Demo**
```bash
# Run the complete enhanced demo
./run_enhanced_demo.sh
```

## 🎯 Demo Scenarios

The enhanced demo includes **comprehensive scenarios**:

### **1. Comprehensive Protocol Demo**
- All RPC methods in sequence
- All content types demonstration
- Error handling scenarios
- Task management operations

### **2. Individual Feature Demonstrations**
- **Basic Text Processing** - Simple text communication
- **Streaming Response** - Real-time streaming communication
- **File Upload** - File handling with base64 encoding
- **Structured Data** - JSON data processing
- **Task Query** - Task status and details retrieval
- **Push Notifications** - Webhook configuration
- **Error Handling** - Invalid inputs and error scenarios
- **Task Cancellation** - Cancel ongoing operations

### **3. Special Scenario Demonstrations**
- **Long-running Tasks** - Progress tracking and updates
- **Input Required** - Interactive task processing
- **Error Scenarios** - Error simulation and handling
- **File Processing** - Advanced file analysis
- **Form Processing** - Complex structured data handling

## 📊 Protocol Coverage Comparison

| Feature | Basic Demo | This Demo |
|---------|------------|-----------|
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

## 🔧 API Endpoints

- **Main Server**: `http://localhost:9999/`
- **Agent Card**: `http://localhost:9999/.well-known/agent.json`
- **A2A Endpoint**: `http://localhost:9999/a2a`
- **Streaming Endpoint**: `http://localhost:9999/a2a/stream`

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

#### **GOOGLE_API_KEY not set**
```bash
# Create .env file with your API key
echo "GOOGLE_API_KEY=your-api-key-here" > .env
```

#### **Port already in use**
```bash
# Kill processes on port 9999
lsof -ti:9999 | xargs kill -9
```

#### **Permission denied**
```bash
# Make script executable
chmod +x run_enhanced_demo.sh
```

## 📚 Documentation

For detailed documentation, see:
- **[ENHANCED_DEMO_README.md](ENHANCED_DEMO_README.md)** - Comprehensive setup and usage guide
- **[A2A Protocol Specification](https://github.com/google/a2a)** - Official protocol docs
- **[A2A SDK Documentation](https://github.com/google/a2a-sdk)** - SDK reference

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

You've successfully set up the **A2A All Requests Demo**! This comprehensive demonstration showcases all the power and flexibility of the A2A protocol for agent-to-agent communication.

**Key Achievements:**
- ✅ **All A2A protocol features** demonstrated
- ✅ **Streaming communication** working perfectly
- ✅ **Multiple content types** supported
- ✅ **Comprehensive error handling** implemented
- ✅ **Task management** fully functional
- ✅ **Real-world scenarios** covered

The enhanced demo is now ready for learning, development, and integration! 🚀 
