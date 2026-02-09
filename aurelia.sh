#!/bin/bash
# Aurelia Launcher - Simple one-command startup

cd /Users/nayangarg/code/GemmaAI_Deployment

# Kill any existing Aurelia instances
pkill -f "gemma_ultra.py" 2>/dev/null || true

# Start Ollama if not running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "🔧 Starting Ollama..."
    ollama serve > /tmp/ollama.log 2>&1 &
    sleep 2
else
    echo "✅ Ollama already running"
fi

# Start Aurelia
echo "🌟 Starting Aurelia..."
/Users/nayangarg/code/.venv/bin/python gemma_ultra.py
