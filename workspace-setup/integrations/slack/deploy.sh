#!/bin/bash
# Deployment script for Slack Customer Intelligence Fetcher

set -e

echo "🚀 Deploying Slack Customer Intelligence Fetcher"
echo "=============================================="

# Check if running as root (for systemd setup)
if [[ $EUID -eq 0 ]]; then
   echo "✅ Running as root - will set up systemd service"
   SETUP_SYSTEMD=true
else
   echo "⚠️  Not running as root - will set up user-level process"
   SETUP_SYSTEMD=false
fi

# Check environment variables
if [ -z "$SLACK_API_TOKEN" ]; then
    echo "❌ Error: SLACK_API_TOKEN environment variable not set"
    echo "Please export SLACK_API_TOKEN='xoxb-your-token-here'"
    exit 1
fi

echo "✅ Slack API token found"

# Check Python dependencies
echo "📦 Checking Python dependencies..."
pip install aiohttp asyncio python-dateutil

# Create required directories
echo "📁 Creating directory structure..."
mkdir -p customers/.template/slack
mkdir -p reporting/pulse
mkdir -p logs

# Initialize customer Slack directories
echo "🏢 Initializing customer Slack folders..."
for customer_dir in customers/*/; do
    if [ -d "$customer_dir" ] && [ "$customer_dir" != "customers/templates/" ] && [ "$customer_dir" != "customers/workflows/" ]; then
        mkdir -p "${customer_dir}slack"
        echo "  ✅ Created ${customer_dir}slack/"
    fi
done

# Create systemd service if running as root
if [ "$SETUP_SYSTEMD" = true ]; then
    echo "🔧 Creating systemd service..."
    
    cat > /etc/systemd/system/slack-customer-fetcher.service << EOF
[Unit]
Description=Slack Customer Intelligence Fetcher
After=network.target

[Service]
Type=simple
User=$SUDO_USER
WorkingDirectory=$(pwd)
Environment="SLACK_API_TOKEN=$SLACK_API_TOKEN"
ExecStart=/usr/bin/python3 $(pwd)/workspace-setup/integrations/slack/slack_fetcher.py
Restart=always
RestartSec=300

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable slack-customer-fetcher
    systemctl start slack-customer-fetcher
    
    echo "✅ Systemd service created and started"
    echo "   Check status: systemctl status slack-customer-fetcher"
    echo "   View logs: journalctl -u slack-customer-fetcher -f"
    
else
    # Create user-level launcher
    echo "🔧 Creating user-level launcher..."
    
    cat > start_slack_fetcher.sh << 'EOF'
#!/bin/bash
# Start Slack Customer Fetcher in background

if [ -z "$SLACK_API_TOKEN" ]; then
    echo "Error: SLACK_API_TOKEN not set"
    exit 1
fi

# Check if already running
if pgrep -f "slack_fetcher.py" > /dev/null; then
    echo "Slack fetcher is already running"
    exit 0
fi

# Start in background
nohup python3 workspace-setup/integrations/slack/slack_fetcher.py > logs/slack_fetcher.log 2>&1 &
echo $! > logs/slack_fetcher.pid

echo "✅ Slack fetcher started with PID $(cat logs/slack_fetcher.pid)"
echo "   View logs: tail -f logs/slack_fetcher.log"
EOF

    chmod +x start_slack_fetcher.sh
    
    # Create stop script
    cat > stop_slack_fetcher.sh << 'EOF'
#!/bin/bash
# Stop Slack Customer Fetcher

if [ -f logs/slack_fetcher.pid ]; then
    PID=$(cat logs/slack_fetcher.pid)
    if kill -0 $PID 2>/dev/null; then
        kill $PID
        echo "✅ Slack fetcher stopped (PID $PID)"
        rm logs/slack_fetcher.pid
    else
        echo "⚠️  Process not running"
        rm logs/slack_fetcher.pid
    fi
else
    echo "❌ PID file not found"
fi
EOF

    chmod +x stop_slack_fetcher.sh
    
    echo "✅ Created start/stop scripts"
    echo "   Start: ./start_slack_fetcher.sh"
    echo "   Stop: ./stop_slack_fetcher.sh"
fi

# Create monitoring script
echo "📊 Creating monitoring script..."

cat > monitor_slack_fetcher.sh << 'EOF'
#!/bin/bash
# Monitor Slack Customer Fetcher health

echo "🔍 Slack Customer Fetcher Status"
echo "================================"

# Check if process is running
if pgrep -f "slack_fetcher.py" > /dev/null; then
    echo "✅ Process: Running"
    
    # Get PID
    PID=$(pgrep -f "slack_fetcher.py")
    echo "   PID: $PID"
    
    # Check CPU and memory usage
    ps -p $PID -o %cpu,%mem,etime | tail -1 | while read CPU MEM TIME; do
        echo "   CPU: $CPU%"
        echo "   Memory: $MEM%"
        echo "   Uptime: $TIME"
    done
else
    echo "❌ Process: Not running"
fi

# Check last fetch time
if [ -f reporting/pulse/slack_alerts.json ]; then
    LAST_FETCH=$(jq -r .timestamp reporting/pulse/slack_alerts.json 2>/dev/null || echo "Unknown")
    echo ""
    echo "📅 Last fetch: $LAST_FETCH"
fi

# Check for recent errors
echo ""
echo "🚨 Recent errors (last 10 lines):"
if [ -f logs/slack_fetcher.log ]; then
    grep -i error logs/slack_fetcher.log | tail -10 || echo "   No recent errors"
else
    echo "   Log file not found"
fi

# Customer mention statistics
echo ""
echo "📊 Customer mention statistics:"
for customer_dir in customers/*/slack/; do
    if [ -d "$customer_dir" ]; then
        customer=$(basename $(dirname "$customer_dir"))
        mention_count=$(find "$customer_dir" -name "mentions_*.json" -type f -exec jq length {} + 2>/dev/null | awk '{s+=$1} END {print s}')
        if [ -n "$mention_count" ] && [ "$mention_count" -gt 0 ]; then
            echo "   $customer: $mention_count mentions"
        fi
    fi
done
EOF

chmod +x monitor_slack_fetcher.sh

echo "✅ Created monitoring script: ./monitor_slack_fetcher.sh"

# Test configuration
echo ""
echo "🧪 Testing configuration..."
python3 -c "
import json
config_path = 'workspace-setup/integrations/slack/config.json'
with open(config_path, 'r') as f:
    config = json.load(f)
print(f'✅ Channels to monitor: {len(config[\"channels\"])}')
print(f'✅ Fetch interval: {config[\"fetch_settings\"][\"fetch_interval_hours\"]} hours')
print(f'✅ History window: {config[\"fetch_settings\"][\"history_days\"]} days')
"

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Start the fetcher:"
if [ "$SETUP_SYSTEMD" = true ]; then
    echo "   systemctl start slack-customer-fetcher"
else
    echo "   ./start_slack_fetcher.sh"
fi
echo "2. Monitor status:"
echo "   ./monitor_slack_fetcher.sh"
echo "3. View customer data:"
echo "   ls customers/*/slack/"
echo ""
echo "Happy fetching! 🚀"