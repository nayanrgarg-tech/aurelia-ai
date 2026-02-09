#!/bin/bash
# Auto-restart stuck downloads

log_file="/tmp/ollama_downloads.log"
max_idle_time=120  # Restart if no progress for 2 minutes

echo "🤖 Aurelia - Auto Download Watchdog"
echo "Starting continuous model pull..."
echo ""

while true; do
    # Check if process is running
    if ! pgrep -f "ollama pull" > /dev/null; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting mistral download..."
        nohup ollama pull mistral >> "$log_file" 2>&1 &
    fi
    
    # Check for progress
    if [ -f "$log_file" ]; then
        current_time=$(date +%s)
        last_update=$(stat -f %m "$log_file" 2>/dev/null || stat -c %Y "$log_file" 2>/dev/null || echo 0)
        time_since_update=$((current_time - last_update))
        
        if [ $time_since_update -gt $max_idle_time ]; then
            echo "$(date '+%Y-%m-%d %H:%M:%S') - No progress detected, restarting..."
            pkill -f "ollama pull"
            sleep 2
            nohup ollama pull mistral >> "$log_file" 2>&1 &
        fi
    fi
    
    sleep 30
done
