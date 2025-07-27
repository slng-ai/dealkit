#!/bin/bash
# Sales Workspace Navigation Helper
# Provides quick navigation and discovery commands

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Base directory (script location)
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function show_help() {
    echo -e "${BLUE}Sales Workspace Navigator${NC}"
    echo "========================="
    echo ""
    echo "Usage: ./navigate.sh [command] [args]"
    echo ""
    echo "Commands:"
    echo "  structure    - Show workspace structure"
    echo "  find         - Find files by pattern"
    echo "  customer     - Navigate to customer folder"
    echo "  report       - Navigate to report type"
    echo "  template     - Find and display templates"
    echo "  audit        - Run workspace audit"
    echo "  search       - Search across all files"
    echo "  recent       - Show recently modified files"
    echo "  help         - Show this help message"
    echo ""
    echo "Quick Navigation:"
    echo "  ./navigate.sh customer acme     - Go to ACME customer folder"
    echo "  ./navigate.sh report personal   - Go to personal reports"
    echo "  ./navigate.sh template email    - Find email templates"
    echo "  ./navigate.sh find '*.json'     - Find all JSON files"
}

function show_structure() {
    echo -e "${BLUE}Sales Workspace Structure${NC}"
    echo "========================"
    echo ""
    
    # Show main directories with descriptions
    echo -e "${GREEN}Main Sections:${NC}"
    echo "├── customers/        - Customer profiles and data"
    echo "├── reporting/        - Analytics and performance tracking"
    echo "│   ├── personal/    - Individual contributor reports"
    echo "│   ├── team/        - Management and leadership reports"
    echo "│   └── pulse/       - Real-time alerts and notifications"
    echo "├── sales-toolkit/    - Sales resources and materials"
    echo "│   ├── templates/   - Email, demo, proposal templates"
    echo "│   ├── battlecards/ - Competitive intelligence"
    echo "│   └── playbooks/   - Sales methodologies"
    echo "├── workspace-setup/  - Internal configuration"
    echo "│   ├── integrations/ - External tool connections"
    echo "│   └── processes/   - Internal workflows"
    echo "├── personal/        - Individual workspaces"
    echo "└── .claude/         - AI agent configurations"
    echo ""
    
    # Show key files
    echo -e "${GREEN}Key Files:${NC}"
    echo "• MASTER_CONTEXT.md  - Complete system overview"
    echo "• QUICK_REFERENCE.md - Common tasks and shortcuts"
    echo "• SEARCH_INDEX.md    - Comprehensive search guide"
    echo "• PROJECT_AUDIT.md   - Governance framework"
}

function find_files() {
    local pattern=$1
    echo -e "${BLUE}Finding files matching: ${NC}$pattern"
    echo "========================"
    
    find "$BASE_DIR" -name "$pattern" -type f | while read -r file; do
        relative_path=${file#$BASE_DIR/}
        echo -e "${GREEN}→${NC} $relative_path"
    done
}

function navigate_customer() {
    local customer=$1
    
    if [ -z "$customer" ]; then
        echo -e "${BLUE}Available Customers:${NC}"
        echo "==================="
        ls -1 "$BASE_DIR/customers" | grep -v -E "^(templates|workflows)$" | while read -r dir; do
            if [ -d "$BASE_DIR/customers/$dir" ]; then
                echo -e "${GREEN}→${NC} $dir"
            fi
        done
        return
    fi
    
    # Find matching customer (case-insensitive)
    local found=$(find "$BASE_DIR/customers" -maxdepth 1 -type d -iname "*$customer*" | head -1)
    
    if [ -n "$found" ]; then
        echo -e "${GREEN}Found:${NC} $found"
        cd "$found" && pwd
        echo ""
        echo "Contents:"
        ls -la
    else
        echo -e "${RED}Customer not found:${NC} $customer"
    fi
}

function navigate_report() {
    local category=$1
    
    if [ -z "$category" ]; then
        echo -e "${BLUE}Report Categories:${NC}"
        echo "=================="
        echo -e "${GREEN}→${NC} personal - Individual contributor reports"
        echo -e "${GREEN}→${NC} team     - Management and leadership reports"
        echo -e "${GREEN}→${NC} pulse    - Real-time alerts and notifications"
        return
    fi
    
    local report_dir="$BASE_DIR/reporting/$category"
    
    if [ -d "$report_dir" ]; then
        cd "$report_dir" && pwd
        echo ""
        echo -e "${BLUE}Available Reports:${NC}"
        ls -1 *.py 2>/dev/null | grep -v "__" | while read -r report; do
            echo -e "${GREEN}→${NC} $report"
        done
    else
        echo -e "${RED}Invalid category:${NC} $category"
    fi
}

function find_template() {
    local type=$1
    
    if [ -z "$type" ]; then
        echo -e "${BLUE}Template Types:${NC}"
        echo "==============="
        echo -e "${GREEN}→${NC} email    - Email templates"
        echo -e "${GREEN}→${NC} demo     - Demo scripts"
        echo -e "${GREEN}→${NC} proposal - Proposal templates"
        echo -e "${GREEN}→${NC} objection - Objection handling"
        return
    fi
    
    echo -e "${BLUE}Templates matching '${NC}$type${BLUE}':${NC}"
    echo "========================"
    
    find "$BASE_DIR/sales-toolkit/templates" -name "*$type*.md" -type f | while read -r file; do
        relative_path=${file#$BASE_DIR/}
        filename=$(basename "$file")
        echo -e "${GREEN}→${NC} $filename"
        echo "   Path: $relative_path"
        
        # Show first few lines
        echo -e "   ${YELLOW}Preview:${NC}"
        head -3 "$file" | sed 's/^/   /'
        echo ""
    done
}

function run_audit() {
    echo -e "${BLUE}Running Workspace Audit...${NC}"
    echo "=========================="
    
    if [ -f "$BASE_DIR/audit_workspace.py" ]; then
        python3 "$BASE_DIR/audit_workspace.py"
    else
        echo -e "${RED}Audit script not found!${NC}"
    fi
}

function search_workspace() {
    local term=$1
    
    if [ -z "$term" ]; then
        echo -e "${RED}Please provide a search term${NC}"
        return
    fi
    
    echo -e "${BLUE}Searching for '${NC}$term${BLUE}'...${NC}"
    echo "===================="
    
    # Use ripgrep if available, otherwise grep
    if command -v rg &> /dev/null; then
        rg "$term" "$BASE_DIR" --type-add 'sales:*.{md,json,py}' -t sales
    else
        grep -r "$term" "$BASE_DIR" --include="*.md" --include="*.json" --include="*.py" | head -20
    fi
}

function show_recent() {
    local days=${1:-7}
    
    echo -e "${BLUE}Recently Modified Files (last $days days):${NC}"
    echo "======================================="
    
    find "$BASE_DIR" -type f -mtime -"$days" -not -path "*/\.*" | \
        xargs ls -lt 2>/dev/null | head -20 | while read -r line; do
        echo -e "${GREEN}→${NC} $line"
    done
}

# Main command dispatcher
case "$1" in
    structure)
        show_structure
        ;;
    find)
        find_files "$2"
        ;;
    customer)
        navigate_customer "$2"
        ;;
    report)
        navigate_report "$2"
        ;;
    template)
        find_template "$2"
        ;;
    audit)
        run_audit
        ;;
    search)
        search_workspace "$2"
        ;;
    recent)
        show_recent "$2"
        ;;
    help|"")
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command:${NC} $1"
        echo "Use './navigate.sh help' for usage information"
        ;;
esac