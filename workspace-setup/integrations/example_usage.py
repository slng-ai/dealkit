#!/usr/bin/env python3
"""
Example usage of integrations with ACME Inc sample data
Shows how to pull data from various sources and aggregate it
"""

import os
import json
from datetime import datetime
from slack.slack_integration import SlackIntegration
from gong.gong_integration import GongIntegration
from granola.granola_integration import GranolaIntegration
from email.gmail_integration import GmailIntegration

def demonstrate_slack_integration():
    """Show how to use Slack integration"""
    print("\n=== Slack Integration Demo ===")
    
    slack = SlackIntegration()
    
    # Method 1: API-based fetching
    if slack.authenticate():
        # Fetch conversations about ACME Corp
        data = slack.fetch_data(
            customer_id='acme-corp',
            customer_name='ACME Corp',
            days_back=30
        )
        
        # Process the data
        processed = slack.process_data(data)
        
        print(f"Found {processed['summary']['total_messages']} messages")
        print(f"Engagement level: {processed['engagement_level']}")
        print(f"Action items found: {len(processed['action_items'])}")
        
        # Save to file system
        save_slack_data('acme_inc', data)
    else:
        print("Using sample data fallback...")
        # Load from sample data
        with open('../../customers/profiles/acme_inc/slack/2024-03-15_poc_planning.json', 'r') as f:
            sample_data = json.load(f)
        print(f"Sample shows excitement about POC in #{sample_data['channel']}")

def demonstrate_gong_integration():
    """Show how to use Gong integration"""
    print("\n=== Gong Integration Demo ===")
    
    gong = GongIntegration()
    
    # Method 1: URL-based analysis
    gong_url = "https://app.gong.io/call?id=1234567890"
    print(f"Analyzing Gong URL: {gong_url}")
    
    result = gong.analyze_call_url(gong_url)
    
    if result.get('type') == 'webfetch_analysis':
        print("Would use WebFetch to analyze the call recording")
    else:
        print(f"Fetched call data via API")
    
    # Method 2: Customer call analysis
    if gong.connect():
        customer_analysis = gong.fetch_customer_calls("ACME Corp", days_back=90)
        
        print(f"Total calls analyzed: {customer_analysis['total_calls']}")
        print(f"Engagement metrics: {customer_analysis['engagement_metrics']}")
        print(f"Key themes: {list(customer_analysis['key_themes'].keys())[:5]}")
        
        # Push insights back to Gong
        gong.push_insights_to_gong("1234567890", {
            'custom_fields': {
                'deal_score': 82,
                'next_step': 'Contract review',
                'competitor': 'Vercel'
            },
            'tags': ['high-value', 'competitive-deal', 'technical-buyer']
        })

def demonstrate_granola_integration():
    """Show how to use Granola integration"""
    print("\n=== Granola Integration Demo ===")
    
    granola = GranolaIntegration()
    
    # Analyze meeting URL
    meeting_url = "https://app.granola.so/meeting/abc123def456"
    print(f"Analyzing Granola meeting: {meeting_url}")
    
    result = granola.analyze_granola_url(meeting_url)
    
    # Fetch all meetings for customer
    if granola.authenticate():
        meetings_data = granola.fetch_data(
            customer_id='acme-corp',
            customer_name='ACME Corp',
            days_back=30
        )
        
        processed = granola.process_data(meetings_data)
        
        print(f"Meeting cadence: {processed['summary']['meeting_cadence']}")
        print(f"Pending actions: {len(processed['pending_actions'])}")
        print(f"Recent decisions: {len(processed['recent_decisions'])}")
        
        # Update action item status
        for action in processed['pending_actions']:
            if 'security review' in action['item'].lower():
                granola.push_data({
                    'action_id': 'sec-review-001',
                    'completed': True
                }, 'action_item_status')
                print("✓ Marked security review as complete")

def demonstrate_email_integration():
    """Show how to use Email integration"""
    print("\n=== Email Integration Demo ===")
    
    gmail = GmailIntegration()
    
    # Search for customer emails
    if gmail.authenticate():
        # Fetch emails with ACME Corp
        emails = gmail.fetch_data(
            customer_id='acme-corp',
            customer_name='ACME Corp',
            email_addresses=['michael.chen@acme.dev', 'sarah.rodriguez@acme.dev']
        )
        
        print(f"Found {len(emails['threads'])} email threads")
        print(f"Key topics: {emails.get('key_topics', [])}")
        
        # Analyze sentiment
        for thread in emails['threads'][:3]:
            print(f"- Thread: {thread['subject']} ({thread['message_count']} messages)")

def demonstrate_context_aggregation():
    """Show how to aggregate data from all sources"""
    print("\n=== Context Aggregation Demo ===")
    
    # Initialize all integrations
    integrations = {
        'slack': SlackIntegration(),
        'gong': GongIntegration(),
        'granola': GranolaIntegration(),
        'email': GmailIntegration()
    }
    
    # Collect data from all sources
    all_data = {}
    
    for name, integration in integrations.items():
        print(f"Fetching from {name}...")
        try:
            if hasattr(integration, 'authenticate') and integration.authenticate():
                data = integration.fetch_data('acme-corp', customer_name='ACME Corp')
                all_data[name] = integration.process_data(data)
        except Exception as e:
            print(f"  Error with {name}: {e}")
            # Load sample data as fallback
            all_data[name] = load_sample_data(name, 'acme_inc')
    
    # Aggregate insights
    context = {
        'customer': 'ACME Corp',
        'deal_stage': 'Negotiation',
        'deal_size': '$600K ACV',
        'key_signals': [],
        'risk_factors': [],
        'next_actions': []
    }
    
    # Extract signals from each source
    if 'slack' in all_data:
        if all_data['slack'].get('engagement_level') == 'high':
            context['key_signals'].append("High Slack engagement - team is excited")
    
    if 'gong' in all_data:
        if all_data['gong'].get('summary', {}).get('deal_score', 0) > 70:
            context['key_signals'].append("Strong Gong deal score indicating high probability")
    
    if 'granola' in all_data:
        pending = all_data['granola'].get('pending_actions', [])
        if pending:
            context['next_actions'].extend([
                f"- {action['item']} (Owner: {action['owner']})"
                for action in pending[:3]
            ])
    
    # Display aggregated context
    print("\n📊 Aggregated Customer Context:")
    print(f"Customer: {context['customer']}")
    print(f"Stage: {context['deal_stage']} | Size: {context['deal_size']}")
    print("\n✅ Key Signals:")
    for signal in context['key_signals']:
        print(f"  - {signal}")
    print("\n📋 Next Actions:")
    for action in context['next_actions']:
        print(f"  {action}")

def save_slack_data(customer_folder: str, data: dict):
    """Save Slack data to file system"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"../../customers/profiles/{customer_folder}/slack/{date_str}_integration_sync.json"
    
    # Create directory if needed
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved Slack data to {filename}")

def load_sample_data(integration: str, customer: str) -> dict:
    """Load sample data for demonstration"""
    sample_files = {
        'slack': f"../../customers/profiles/{customer}/slack/2024-03-15_poc_planning.json",
        'gong': f"../../customers/profiles/{customer}/gong/2024-04-05_poc_results_review.json",
        'granola': f"../../customers/profiles/{customer}/granola/2024-03-22_executive_overview.md"
    }
    
    if integration in sample_files:
        try:
            if integration == 'granola':
                # For markdown files, return parsed structure
                return {
                    'summary': {'meeting_cadence': 'weekly'},
                    'pending_actions': [
                        {'item': 'Security review', 'owner': 'Lisa Thompson'},
                        {'item': 'Migration plan', 'owner': 'Alex Kumar'}
                    ]
                }
            else:
                with open(sample_files[integration], 'r') as f:
                    return json.load(f)
        except:
            pass
    
    return {}

def main():
    """Run all demonstrations"""
    print("Sales Workspace Integration Examples")
    print("=" * 50)
    print("\nThis demonstrates how to use integrations to fetch and aggregate customer data.")
    print("Set environment variables for live API access, or it will use sample data.")
    
    # Run demos
    demonstrate_slack_integration()
    demonstrate_gong_integration()
    demonstrate_granola_integration()
    demonstrate_email_integration()
    demonstrate_context_aggregation()
    
    print("\n✨ Demo complete! Check the sample data in customers/profiles/acme_inc/")
    print("Set up your API credentials to start pulling live data.")

if __name__ == "__main__":
    main()