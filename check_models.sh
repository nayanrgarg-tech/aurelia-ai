#!/bin/bash
# Monitor Aurelia model downloads and auto-launch when ready

echo "🤖 Aurelia - Model Download Monitor"
echo "======================================"

# Check download progress
if [ -f /tmp/ollama_downloads.log ]; then
    echo ""
    echo "📥 Download Progress:"
    tail -3 /tmp/ollama_downloads.log | grep -E "pulling|%"
fi

echo ""
echo "🔄 Checking available models..."

# Try to query available models
models=$(curl -s http://localhost:11434/api/tags 2>/dev/null | grep -o '"name":"[^"]*"' | cut -d'"' -f4 | tr '\n' ', ')

if [ -z "$models" ]; then
    echo "⏳ Waiting for models to finish downloading..."
    echo "   This may take a few minutes..."
else
    echo "✅ Available models: $models"
    echo ""
    echo "🚀 Ready! Launch Aurelia with: aurelia"
fi
