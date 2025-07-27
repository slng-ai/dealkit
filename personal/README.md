# Personal Workspace

Your individual workspace for personal organization, automation rules, and customizations.

## Overview

The personal workspace is your private area within the sales workspace system. It's designed to store your individual preferences, daily plans, personal triggers, and custom configurations without affecting the shared team resources.

## Directory Structure

```
personal/
├── daily-plans/         # Your daily planning and notes
├── triggers/            # Personal automation rules
└── README.md           # This file
```

## Features

### Daily Plans
Store your personal daily planning documents, to-do lists, and notes. These are private to you and help organize your individual workflow.

Example structure:
```
daily-plans/
├── 2024-03-15.md
├── 2024-03-16.md
└── templates/
    └── daily-template.md
```

### Personal Triggers
Define automation rules specific to your workflow. These triggers can:
- Alert you about specific customer mentions
- Notify you of deals meeting your criteria
- Create personalized morning briefs
- Track keywords important to you

Example trigger:
```yaml
trigger_name: "My High-Value Deals"
conditions:
  - deal_size: "> 100000"
  - assigned_to: "me"
  - stage: "negotiation"
actions:
  - notify: "email"
  - priority: "high"
```

## Best Practices

1. **Keep it Organized**: Use consistent naming for daily plans
2. **Regular Cleanup**: Archive old daily plans monthly
3. **Document Triggers**: Add comments to explain trigger logic
4. **Backup Important**: Keep copies of critical personal configurations
5. **Don't Store Secrets**: Never store passwords or API keys here

## Privacy

- This directory is meant to be user-specific
- In a team deployment, each user would have their own personal space
- Contents should not be shared in the main repository
- Add `personal/*` to `.gitignore` for team deployments

## Getting Started

1. Create your first daily plan:
   ```bash
   echo "# Daily Plan - $(date +%Y-%m-%d)" > personal/daily-plans/$(date +%Y-%m-%d).md
   ```

2. Set up a personal trigger:
   ```bash
   cp workspace-setup/integrations/triggers/trigger_template.yaml personal/triggers/my_first_trigger.yaml
   ```

3. Customize your workspace:
   - Add personal shortcuts
   - Create custom report views
   - Define your notification preferences

## Tips

- Use markdown for daily plans for better formatting
- Leverage triggers to reduce manual checking
- Keep sensitive information encrypted
- Regularly review and update your triggers
- Share useful triggers with the team (after sanitizing)

Remember: This is YOUR space - organize it in a way that makes you most productive!