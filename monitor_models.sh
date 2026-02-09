#!/bin/bash
# Continuous Aurelia model download monitor

clear
echo "🤖 AURELIA MODEL DOWNLOAD MONITOR"
echo "=================================="
echo ""

# Monitor every 5 seconds
while true; do
    clear
    echo "🤖 AURELIA MODEL DOWNLOAD MONITOR"
    echo "=================================="
    echo ""
    
    # Show last download line
    if [ -f /tmp/ollama_downloads.log ]; then
        echo "📥 Current Progress:"
        tail -3 /tmp/ollama_downloads.log | grep -E "pulling|%" | tail -1
        echo ""
        
        # Check if complete
        if grep -q "success" /tmp/ollama_downloads.log 2>/dev/null; then
            echo "✅ DOWNLOAD COMPLETE!"
            echo ""
            ollama list 2>/dev/null | tail -5
            break
        fi
    fi
    
    # Show available models
    echo "📦 Models checking..."
    timeout 2 curl -s http://localhost:11434/api/tags 2>/dev/null | grep -o '"name":"[^"]*"' | cut -d'"' -f4 && echo "" || echo "   (Ollama still starting...)"
    
    # Show status
    echo ""
    echo "🔄 Auto-restart enabled: If download stops, it will restart"
    echo "⏰ Updates every 5 seconds... Press Ctrl+C to exit"
    echo ""
    
    sleep 5
done
