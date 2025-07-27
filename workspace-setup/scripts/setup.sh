#!/bin/bash
# Sales Workspace Setup Script
# Prepares the workspace for first use

set -e

echo "🚀 Sales Workspace Setup Wizard"
echo "=============================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check Python version
echo "🔍 Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed.${NC}"
    echo "Please install Python 3.8 or higher and try again."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo ""
echo "📚 Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -q -r requirements.txt
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    # Create requirements.txt if it doesn't exist
    cat > requirements.txt << EOF
# Core dependencies
python-dotenv==1.0.0
pyyaml==6.0.1
requests==2.31.0
aiohttp==3.9.1
asyncio==3.4.3
python-dateutil==2.8.2

# Data processing
pandas==2.1.4
numpy==1.24.3
jinja2==3.1.2

# Integrations
slack-sdk==3.23.0
salesforce-bulk==2.2.0
hubspot-api-client==8.2.1

# Monitoring
prometheus-client==0.19.0
structlog==23.2.0

# Development
pytest==7.4.3
black==23.12.1
flake8==6.1.0
EOF
    pip install -q -r requirements.txt
    echo -e "${GREEN}✅ Requirements file created and dependencies installed${NC}"
fi

# Create .env template
if [ ! -f ".env" ]; then
    echo ""
    echo "🔐 Creating environment configuration..."
    cat > .env.example << EOF
# Company Settings
COMPANY_NAME="Your Company Name"
WORKSPACE_ADMIN_EMAIL="admin@yourcompany.com"
TEAM_SIZE=10

# Slack Integration (Optional)
SLACK_API_TOKEN=""
SLACK_WORKSPACE=""

# CRM Integration (Choose One)
# Salesforce
SALESFORCE_CLIENT_ID=""
SALESFORCE_CLIENT_SECRET=""
SALESFORCE_USERNAME=""
SALESFORCE_PASSWORD=""
SALESFORCE_SECURITY_TOKEN=""
SALESFORCE_INSTANCE_URL="https://yourinstance.salesforce.com"

# HubSpot
HUBSPOT_API_KEY=""

# Email Integration
EMAIL_PROVIDER="gmail"  # gmail or outlook
EMAIL_ADDRESS=""
EMAIL_APP_PASSWORD=""

# AI Configuration
AI_PROVIDER="claude"
AI_MODEL="claude-3-opus-20240229"
AI_TEMPERATURE=0.7

# Monitoring (Optional)
ENABLE_MONITORING=false
GRAFANA_API_KEY=""
GRAFANA_URL=""
EOF
    cp .env.example .env
    echo -e "${GREEN}✅ Created .env file (please edit with your settings)${NC}"
fi

# Clean up any references to specific companies
echo ""
echo "🧹 Cleaning up example data..."
# Replace Baseten references with generic placeholders
find . -type f \( -name "*.md" -o -name "*.json" -o -name "*.py" \) -exec grep -l "baseten\|Baseten" {} \; 2>/dev/null | while read file; do
    if [[ "$file" != *"venv"* ]] && [[ "$file" != *".git"* ]]; then
        sed -i.bak 's/baseten\.com/yourcompany.com/g' "$file"
        sed -i.bak 's/Baseten/Your Company/g' "$file"
        sed -i.bak 's/baseten/yourcompany/g' "$file"
        rm "${file}.bak"
    fi
done
echo -e "${GREEN}✅ Cleaned up example references${NC}"

# Create missing directories
echo ""
echo "📁 Setting up directory structure..."
mkdir -p personal/{daily-plans,triggers}
mkdir -p customers/sample-customer/{notes,emails,slack,meetings}
mkdir -p audits
mkdir -p logs
echo -e "${GREEN}✅ Directory structure created${NC}"

# Create sample customer
if [ ! -f "customers/sample-customer/profile.json" ]; then
    cat > customers/sample-customer/profile.json << EOF
{
  "company_name": "Sample Customer Inc",
  "industry": "Technology",
  "size": "Mid-Market",
  "location": "San Francisco, CA",
  "website": "https://samplecustomer.com",
  "status": "prospect",
  "stage": "discovery",
  "deal_size": 75000,
  "probability": 30,
  "expected_close_date": "2024-06-30",
  "assigned_to": "john.doe@yourcompany.com",
  "created_at": "2024-03-01T10:00:00Z",
  "last_interaction": "2024-03-15T14:30:00Z",
  "next_meeting": "2024-03-20T15:00:00Z",
  "primary_contact": {
    "name": "Jane Smith",
    "title": "VP of Engineering",
    "email": "jane.smith@samplecustomer.com",
    "phone": "+1-555-123-4567"
  },
  "use_case": "Infrastructure automation and scaling",
  "competitors": ["Competitor A", "Competitor B"],
  "notes": "Strong technical team, looking for Q2 implementation"
}
EOF
    echo -e "${GREEN}✅ Created sample customer profile${NC}"
fi

# Initialize git hooks
if [ -d ".git" ]; then
    echo ""
    echo "🔗 Setting up git hooks..."
    git config core.hooksPath .githooks
    echo -e "${GREEN}✅ Git hooks configured${NC}"
fi

# Create startup script
cat > start_workspace.sh << 'EOF'
#!/bin/bash
# Start Sales Workspace Services

echo "🚀 Starting Sales Workspace..."

# Activate virtual environment
source venv/bin/activate

# Start Slack monitoring (if configured)
if [ -n "$SLACK_API_TOKEN" ]; then
    echo "Starting Slack monitor..."
    nohup python workspace-setup/integrations/slack/slack_fetcher.py > logs/slack.log 2>&1 &
    echo $! > logs/slack.pid
fi

# Start report scheduler
echo "Starting report scheduler..."
nohup python reporting/scheduler.py > logs/scheduler.log 2>&1 &
echo $! > logs/scheduler.pid

echo "✅ Sales Workspace is running!"
echo ""
echo "View logs:"
echo "  tail -f logs/slack.log"
echo "  tail -f logs/scheduler.log"
echo ""
echo "Stop services:"
echo "  ./stop_workspace.sh"
EOF
chmod +x start_workspace.sh

# Create stop script
cat > stop_workspace.sh << 'EOF'
#!/bin/bash
# Stop Sales Workspace Services

echo "🛑 Stopping Sales Workspace..."

# Stop Slack monitor
if [ -f logs/slack.pid ]; then
    kill $(cat logs/slack.pid) 2>/dev/null
    rm logs/slack.pid
    echo "✅ Slack monitor stopped"
fi

# Stop scheduler
if [ -f logs/scheduler.pid ]; then
    kill $(cat logs/scheduler.pid) 2>/dev/null
    rm logs/scheduler.pid
    echo "✅ Report scheduler stopped"
fi

echo "✅ All services stopped"
EOF
chmod +x stop_workspace.sh

# Run initial audit
echo ""
echo "🔍 Running initial workspace audit..."
python3 audit_workspace.py > audits/initial_audit.txt 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Workspace audit passed${NC}"
else
    echo -e "${YELLOW}⚠️ Workspace audit found issues (see audits/initial_audit.txt)${NC}"
fi

# Create quick start guide
cat > QUICK_START.txt << EOF
🚀 SALES WORKSPACE QUICK START
=============================

1. Edit .env file with your settings:
   vi .env

2. Start the workspace:
   ./start_workspace.sh

3. View your morning brief:
   python reporting/pulse/morning_brief.py

4. Navigate the workspace:
   ./navigate.sh help

5. Add a customer:
   python create_customer.py

6. Run reports:
   python reporting/personal/ae_report.py

For full documentation, see GETTING_STARTED.md
EOF

# Display success message
echo ""
echo -e "${GREEN}✨ Setup Complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Edit ${BLUE}.env${NC} with your API credentials"
echo "2. Run ${BLUE}./start_workspace.sh${NC} to start services"
echo "3. Use ${BLUE}./navigate.sh help${NC} to explore"
echo ""
echo "For detailed instructions, see:"
echo "  • ${BLUE}GETTING_STARTED.md${NC} - Step-by-step guide"
echo "  • ${BLUE}QUICK_REFERENCE.md${NC} - Common commands"
echo "  • ${BLUE}PROJECT_AUDIT.md${NC} - Structure rules"
echo ""
echo "Happy selling! 🎯"