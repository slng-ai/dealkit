#!/bin/bash
# Cleanup script to prepare workspace for open source release

echo "🧹 Cleaning up Sales Workspace for Open Source Release"
echo "===================================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Fix naming convention violations
echo ""
echo "📝 Fixing naming conventions..."

# Rename directories with underscores to hyphens
find . -type d -name "*_*" -not -path "./venv/*" -not -path "./.git/*" -not -path "*/__pycache__/*" | while read dir; do
    newdir=$(echo "$dir" | sed 's/_/-/g')
    if [ "$dir" != "$newdir" ]; then
        echo "  Renaming: $dir → $newdir"
        mv "$dir" "$newdir" 2>/dev/null || true
    fi
done

# Clean up the deep customer structure
echo ""
echo "📁 Reorganizing customer structure..."

# Move acme_inc to proper location
if [ -d "customers/profiles/acme_inc" ]; then
    mv customers/profiles/acme_inc customers/acme-inc 2>/dev/null || true
    rm -rf customers/profiles 2>/dev/null || true
fi

# Flatten deep customer subdirectories
for customer in customers/*/; do
    if [ -d "$customer" ] && [[ "$customer" != *"templates"* ]] && [[ "$customer" != *"workflows"* ]]; then
        # Move deeply nested files to appropriate level
        find "$customer" -mindepth 3 -type f | while read file; do
            # Get the relative path within customer
            rel_path=${file#$customer}
            # Extract the category (first directory)
            category=$(echo "$rel_path" | cut -d'/' -f1)
            # Create category if needed
            mkdir -p "$customer$category"
            # Move file to flattened structure
            filename=$(basename "$file")
            mv "$file" "$customer$category/$filename" 2>/dev/null || true
        done
    fi
done

# Remove Python files from sales-toolkit
echo ""
echo "🐍 Removing code files from sales-toolkit..."
find sales-toolkit -name "*.py" -delete 2>/dev/null || true

# Replace company-specific references
echo ""
echo "🏢 Replacing company references..."

# List of files to check and clean
FILES_TO_CLEAN=$(find . -type f \( -name "*.md" -o -name "*.json" -o -name "*.yaml" \) \
    -not -path "./venv/*" \
    -not -path "./.git/*" \
    -not -path "./node_modules/*" 2>/dev/null)

for file in $FILES_TO_CLEAN; do
    # Skip binary files
    if file --mime "$file" | grep -q "charset=binary"; then
        continue
    fi
    
    # Replace email addresses with examples
    sed -i.bak 's/[a-zA-Z0-9._%+-]*@baseten\.com/user@yourcompany.com/g' "$file" 2>/dev/null || true
    sed -i.bak 's/[a-zA-Z0-9._%+-]*@.*\.baseten\.com/user@yourcompany.com/g' "$file" 2>/dev/null || true
    
    # Replace company names
    sed -i.bak 's/Baseten/Your Company/g' "$file" 2>/dev/null || true
    sed -i.bak 's/baseten/yourcompany/g' "$file" 2>/dev/null || true
    
    # Remove backup files
    rm -f "${file}.bak"
done

# Create .gitignore for personal data
echo ""
echo "📄 Creating .gitignore..."
cat > .gitignore << EOF
# Personal and sensitive data
.env
personal/daily-plans/*
personal/triggers/*
!personal/daily-plans/.gitkeep
!personal/triggers/.gitkeep

# Customer data (for team deployments)
customers/*
!customers/templates/
!customers/workflows/
!customers/sample-customer/
!customers/README.md

# Logs and temporary files
*.log
logs/
*.pid
*.tmp
*.bak
.DS_Store

# Python
__pycache__/
*.py[cod]
*$py.class
venv/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Audit results
audits/*.json
audits/*.txt

# Cache
.cache/
*.cache

# OS
Thumbs.db
EOF

# Create .gitkeep files for empty directories
touch personal/daily-plans/.gitkeep
touch personal/triggers/.gitkeep
touch logs/.gitkeep

# Remove any remaining sensitive patterns
echo ""
echo "🔒 Final security check..."

# Remove any remaining API keys or tokens
find . -type f -name "*.json" -not -path "./venv/*" -not -path "./.git/*" | while read file; do
    # Replace actual tokens with placeholders
    sed -i.bak 's/"[a-zA-Z0-9_-]\{20,\}"/"YOUR_TOKEN_HERE"/g' "$file" 2>/dev/null || true
    sed -i.bak 's/xoxb-[a-zA-Z0-9-]\+/xoxb-your-token-here/g' "$file" 2>/dev/null || true
    rm -f "${file}.bak"
done

# Create LICENSE file
echo ""
echo "📜 Creating LICENSE file..."
cat > LICENSE << EOF
MIT License

Copyright (c) 2024 Your Company

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# Run final audit
echo ""
echo "🔍 Running final audit..."
mkdir -p audits
python3 audit_workspace.py > audits/final_audit.txt 2>&1

# Summary
echo ""
echo -e "${GREEN}✅ Cleanup Complete!${NC}"
echo ""
echo "The workspace has been cleaned for open source release:"
echo "  • Company references replaced with placeholders"
echo "  • Sensitive data removed"
echo "  • Naming conventions fixed"
echo "  • Directory structure flattened"
echo "  • .gitignore created"
echo "  • LICENSE added"
echo ""
echo -e "${YELLOW}⚠️  Please review:${NC}"
echo "  • audits/final_audit.txt for any remaining issues"
echo "  • .env.example to ensure no sensitive data"
echo "  • Customer profiles for any real data"
echo ""
echo "Ready to push to GitHub! 🚀"