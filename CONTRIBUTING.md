# Contributing to Sales Workspace

Welcome! We're excited you want to contribute to the AI-powered sales workspace. This project is designed to maintain its structure automatically while allowing meaningful contributions.

## 🚀 Quick Start for Contributors

1. **Fork the repository**
2. **Clone your fork**: `git clone https://github.com/yourusername/sales-workspace.git`
3. **Run setup**: `./workspace-setup/scripts/setup.sh`
4. **Create branch**: `git checkout -b feature/amazing-feature`
5. **Make changes** following our guidelines below
6. **Run audit**: `python workspace-setup/scripts/audit_workspace.py`
7. **Commit and push**: Structure validation runs automatically
8. **Open Pull Request**

## 🏗️ Project Governance

### Core Architecture Principles

The workspace follows strict separation of concerns:

#### 🏢 Customer Data (`/customers/`)
**Purpose**: Store all customer-specific information

✅ **Allowed**:
- Individual customer folders with profile.json
- Customer communications (emails, slack, meetings)
- Health metrics and scores
- Context generation templates

❌ **NOT Allowed**:
- Sales methodology documentation
- Internal processes or system configuration
- Report generation code

#### 🛠️ Sales Resources (`/sales-toolkit/`)
**Purpose**: Customer-facing sales materials

✅ **Allowed**:
- Email/demo/proposal templates
- Battlecards and competitive intelligence
- Sales playbooks and training materials
- Customer-facing security/compliance docs

❌ **NOT Allowed**:
- Individual customer data
- Internal security policies
- System integrations

#### 📈 Reporting (`/reporting/`)
**Purpose**: Analytics and performance tracking

✅ **Allowed**:
- Report generation code (Python)
- Three categories: personal/, team/, pulse/
- Base classes for report inheritance

❌ **NOT Allowed**:
- Raw customer data
- Sales templates or configuration files

#### ⚙️ Workspace Setup (`/workspace-setup/`)
**Purpose**: Internal configuration and integrations

✅ **Allowed**:
- Integration connectors (Slack, CRM, etc.)
- Internal compliance and security policies
- Process documentation and system config

❌ **NOT Allowed**:
- Customer data or sales materials
- Report outputs or personal content

## 📝 Contribution Guidelines

### Naming Conventions

#### Folders
- **Lowercase with hyphens**: `sales-toolkit`, `workspace-setup`
- **No underscores** in folder names (except Python modules)
- **Singular for items**: `/customers/acme-corp/`
- **Plural for collections**: `/templates/`, `/battlecards/`

#### Files
- **Python files**: `snake_case.py` (e.g., `sdr_report.py`)
- **Markdown files**: `UPPERCASE.md` for system docs, `lowercase-hyphenated.md` for content
- **JSON files**: `lowercase_underscore.json` (e.g., `profile.json`)
- **Shell scripts**: `lowercase-hyphenated.sh`

### File Organization Rules

#### Customer Structure
```
customers/{customer-name}/
├── profile.json          # Required: Core customer data
├── notes/               # Optional: Meeting notes
├── emails/              # Optional: Communications
├── slack/               # Optional: Mention data
├── meetings/            # Optional: Call recordings
└── health_metrics.json  # Optional: Health scoring
```

#### Report Structure
```
reporting/{category}/
├── README.md            # Required: Documentation
├── base_report.py       # Inherited by reports
├── {role}_report.py     # Role-specific reports
└── __init__.py         # Python module init
```

## 🚦 Change Control Process

### Minor Changes (No Approval Needed)
- Adding new customers to `/customers/`
- Creating templates in existing categories
- Updating report metrics or calculations
- Adding trigger keywords
- Bug fixes and typos

### Major Changes (Approval Required)

#### 1. Structural Changes
- Creating new top-level directories
- Reorganizing existing structures
- Changing naming conventions
- Modifying core architecture

#### 2. Cross-Boundary Changes
- Moving content between major sections
- Merging or splitting categories
- Changing directory purposes
- Modifying separation of concerns

#### 3. System-Wide Changes
- Integration architecture updates
- Report categorization changes
- Data flow modifications
- Security boundary alterations

### Approval Process

```yaml
1. Document Proposal:
   - Current state description
   - Proposed change details
   - Business justification
   - Impact analysis

2. Review Criteria:
   - Maintains separation of concerns
   - Follows naming conventions
   - Preserves data integrity
   - Improves functionality

3. Implementation:
   - Update CONTRIBUTING.md
   - Modify affected components
   - Update documentation
   - Test all integrations
```

## 📝 Code Standards

### Python Code
- Follow PEP 8 style guidelines
- Use type hints for function parameters
- Include docstrings for all classes and functions
- Write unit tests for new functionality

### Documentation
- Update README files for new directories
- Include examples in template files
- Maintain clear, concise language
- Follow markdown formatting standards

### AI Agents
- Define clear purpose and scope
- Specify required tools and integrations
- Include example usage scenarios
- Document expected outputs

## 🗕️ Testing Requirements

### Before Submitting
1. **Run full audit**: `python workspace-setup/scripts/audit_workspace.py`
2. **Check naming**: Ensure all files follow conventions
3. **Test integrations**: Verify connections work
4. **Validate structure**: Confirm proper file placement

### Automated Checks
- Structure validation runs on commit
- Naming convention enforcement
- Documentation completeness
- Security boundary verification

## 🖊️ Types of Contributions

### 📈 Analytics & Reporting
- New report types for different roles
- Enhanced metrics and KPIs
- Visualization improvements
- Performance optimizations

### 🤖 AI Agents
- Customer intelligence agents
- Sales process automation
- Competitive analysis tools
- Communication monitoring

### 🔗 Integrations
- CRM platform connectors
- Communication tool APIs
- Meeting platform integrations
- Analytics service connections

### 📋 Templates & Content
- Email sequences and templates
- Demo scripts and presentations
- Competitive battlecards
- Training materials

### 🛠️ Tools & Utilities
- Automation scripts
- Data migration tools
- Validation utilities
- Performance monitors

## 🚫 Anti-Patterns to Avoid

### ❌ DON'T: Mix Concerns
```
Bad:  /sales-toolkit/reports/customer_health.py
Good: /reporting/pulse/customer_health_alert.py
```

### ❌ DON'T: Duplicate Data
```
Bad:  /customers/acme/emails.json AND /emails/acme/
Good: /customers/acme/emails/ (single location)
```

### ❌ DON'T: Create Deep Nesting
```
Bad:  /sales-toolkit/templates/email/cold/enterprise/tech/v2/
Good: /sales-toolkit/templates/email_cold_enterprise.md
```

### ❌ DON'T: Inconsistent Naming
```
Bad:  /Customer-Data/, /sales_toolkit/, /REPORTING/
Good: /customers/, /sales-toolkit/, /reporting/
```

## 🔍 Pull Request Process

### PR Checklist
- [ ] Follows naming conventions
- [ ] Maintains separation of concerns
- [ ] Includes appropriate documentation
- [ ] Passes automated audit checks
- [ ] Updates relevant README files
- [ ] Tests all affected functionality

### Review Criteria
1. **Architectural Compliance**: Follows established patterns
2. **Code Quality**: Meets style and documentation standards
3. **Security**: Doesn't expose sensitive data
4. **Usability**: Improves user experience
5. **Maintainability**: Easy to understand and modify

## 🎆 Recognition

We celebrate contributors! Significant contributions will be:
- Acknowledged in release notes
- Featured in project documentation
- Recognized in community discussions
- Invited to join the contributor team

## 📞 Getting Help

- **Questions**: Open a GitHub Discussion
- **Bug Reports**: Create an Issue with reproduction steps
- **Feature Requests**: Propose in GitHub Issues
- **Architecture Questions**: Tag maintainers in discussions

## 🔐 Security Guidelines

### Sensitive Data
- Never commit API keys or credentials
- Use environment variables for secrets
- Redact customer information in examples
- Follow data privacy regulations

### Code Security
- Validate all external inputs
- Use secure coding practices
- Regular dependency updates
- Audit third-party integrations

---

**Thank you for contributing to the sales community!** Your efforts help sales teams worldwide operate more efficiently and effectively.

For questions about these guidelines, please open a GitHub Discussion or reach out to the maintainers.