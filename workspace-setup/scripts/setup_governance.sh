#!/bin/bash
# Setup governance and structure protection for sales workspace

echo "🛡️ Setting up Sales Workspace Governance"
echo "========================================"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "⚠️  Warning: Not in a git repository. Git hooks will not be active."
    echo "Initialize with 'git init' to enable pre-commit validation."
else
    # Set up git hooks
    echo "🔧 Configuring git hooks..."
    git config core.hooksPath .githooks
    echo "✅ Git hooks configured"
fi

# Create audit directory
mkdir -p audits
echo "📁 Created audits directory"

# Run initial audit
echo ""
echo "🔍 Running initial workspace audit..."
python3 audit_workspace.py

# Create cron job for regular audits (optional)
echo ""
read -p "Would you like to set up daily automated audits? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Create audit script
    cat > run_daily_audit.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
python3 audit_workspace.py > audits/daily_$(date +%Y%m%d).log 2>&1

# Keep only last 30 days of audits
find audits -name "daily_*.log" -mtime +30 -delete
EOF
    chmod +x run_daily_audit.sh
    
    # Add to crontab
    (crontab -l 2>/dev/null; echo "0 9 * * * $(pwd)/run_daily_audit.sh") | crontab -
    echo "✅ Daily audit scheduled for 9 AM"
fi

# Create quick access aliases
echo ""
echo "📝 Add these aliases to your shell configuration for quick access:"
echo ""
echo "# Sales Workspace Navigation"
echo "alias ws='cd $(pwd)'"
echo "alias ws-audit='$(pwd)/audit_workspace.py'"
echo "alias ws-nav='$(pwd)/navigate.sh'"
echo "alias ws-customer='$(pwd)/navigate.sh customer'"
echo "alias ws-report='$(pwd)/navigate.sh report'"
echo "alias ws-template='$(pwd)/navigate.sh template'"

# Display governance summary
echo ""
echo "✅ Governance Setup Complete!"
echo ""
echo "🛡️ Protection Enabled:"
echo "  • Structure validation on git commit"
echo "  • Naming convention enforcement"
echo "  • Cross-boundary violation detection"
echo "  • Automated audit trail"
echo ""
echo "📋 Key Commands:"
echo "  ./audit_workspace.py  - Run structure audit"
echo "  ./navigate.sh        - Navigate workspace"
echo "  ./navigate.sh help   - Show navigation help"
echo ""
echo "📚 Documentation:"
echo "  PROJECT_AUDIT.md     - Governance rules"
echo "  MASTER_CONTEXT.md    - System overview"
echo "  QUICK_REFERENCE.md   - Common tasks"

# Final check
echo ""
echo "🎯 Next Steps:"
echo "1. Review PROJECT_AUDIT.md for governance rules"
echo "2. Run './navigate.sh structure' to explore"
echo "3. Use './audit_workspace.py' regularly"
echo ""
echo "Happy selling! 🚀"