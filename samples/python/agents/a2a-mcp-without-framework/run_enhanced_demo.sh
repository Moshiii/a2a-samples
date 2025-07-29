#!/bin/bash

# Enhanced A2A Protocol Demo Runner
# This script runs the comprehensive A2A protocol demonstration

echo "🚀 Enhanced A2A Protocol Demo"
echo "=================================================="
echo "This demo showcases ALL A2A protocol communication types"
echo "=================================================="

# Load environment variables from .env file if it exists
if [ -f ".env" ]; then
    echo "📄 Loading environment variables from .env file..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check if GOOGLE_API_KEY is set
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "❌ Error: GOOGLE_API_KEY environment variable is not set"
    echo "Please create a .env file with your Google API key:"
    echo "echo 'GOOGLE_API_KEY=your-api-key-here' > .env"
    echo ""
    echo "Or set it directly:"
    echo "export GOOGLE_API_KEY='your-api-key-here'"
    exit 1
fi

echo "✅ Google API key is configured"

# Function to cleanup background processes
cleanup() {
    echo "🛑 Stopping enhanced demo..."
    if [ ! -z "$SERVER_PID" ]; then
        kill $SERVER_PID 2>/dev/null
    fi
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start the enhanced server in the background
echo "🔧 Starting Enhanced A2A Server..."
cd src/no_llm_framework/enhanced_server
python __main__.py --host localhost --port 9999 &
SERVER_PID=$!

# Wait for server to start
echo "⏳ Waiting for server to start..."
sleep 3

# Check if server is running
if ! curl -s http://localhost:9999/.well-known/agent.json > /dev/null; then
    echo "❌ Error: Server failed to start"
    cleanup
fi

echo "✅ Enhanced A2A Server is running on http://localhost:9999"

# Run the enhanced client demo
echo "🎯 Starting Enhanced A2A Client Demo..."
cd ../enhanced_client
python __main__.py

# Cleanup
cleanup 
