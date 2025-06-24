#!/bin/bash
#
# Heve AI Service Control Script
# Manage the auto-start dictation service
#

SERVICE_NAME="com.heveai.dictation"
PLIST_PATH="$HOME/Library/LaunchAgents/$SERVICE_NAME.plist"

case "$1" in
    start)
        echo "[+] Starting Heve AI service..."
        launchctl load "$PLIST_PATH"
        echo "[✓] Service started"
        ;;
    stop)
        echo "[-] Stopping Heve AI service..."
        launchctl unload "$PLIST_PATH"
        echo "[✓] Service stopped"
        ;;
    restart)
        echo "[~] Restarting Heve AI service..."
        launchctl unload "$PLIST_PATH"
        sleep 1
        launchctl load "$PLIST_PATH"
        echo "[✓] Service restarted"
        ;;
    status)
        echo "[i] Heve AI service status:"
        if launchctl list | grep -q "$SERVICE_NAME"; then
            PID=$(launchctl list | grep "$SERVICE_NAME" | awk '{print $1}')
            echo "[✓] Running (PID: $PID)"
            echo "[*] Ready for dictation - Hold Right Option (⌥) and speak!"
        else
            echo "[X] Not running"
        fi
        ;;
    logs)
        echo "[i] Recent logs:"
        tail -n 20 logs/heve.log 2>/dev/null || echo "No logs found"
        ;;
    disable)
        echo "[-] Disabling auto-start..."
        launchctl unload "$PLIST_PATH"
        rm "$PLIST_PATH"
        echo "[✓] Auto-start disabled"
        ;;
    *)
        echo "Heve AI Service Control"
        echo "Usage: $0 {start|stop|restart|status|logs|disable}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the service"
        echo "  stop    - Stop the service"  
        echo "  restart - Restart the service"
        echo "  status  - Check service status"
        echo "  logs    - Show recent logs"
        echo "  disable - Disable auto-start completely"
        ;;
esac 