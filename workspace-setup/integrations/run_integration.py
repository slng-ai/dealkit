#!/usr/bin/env python3

import argparse
import json
import os
from datetime import datetime

# Import all integrations
import sys
sys.path.append('slack')
from slack_integration import SlackIntegration
# from gong.gong_integration import GongIntegration
# from email.email_integration import EmailIntegration
# from granola.granola_integration import GranolaIntegration

INTEGRATIONS = {
    'slack': SlackIntegration,
    # 'gong': GongIntegration,
    # 'email': EmailIntegration,
    # 'granola': GranolaIntegration
}

def run_single_integration(integration_name: str, customer_id: str, force_refresh: bool = False, **kwargs):
    if integration_name not in INTEGRATIONS:
        print(f"Unknown integration: {integration_name}")
        return None
    
    print(f"Running {integration_name} integration for customer {customer_id}...")
    
    try:
        integration = INTEGRATIONS[integration_name]()
        
        # Load customer data to get specific channels if defined
        customer_file = f"../customers/{customer_id}.json"
        if os.path.exists(customer_file):
            with open(customer_file, 'r') as f:
                customer_data = json.load(f)
                
            # Check for specific Slack channels
            if integration_name == 'slack' and 'slack_channels' in customer_data.get('interactions', {}):
                kwargs['channels'] = customer_data['interactions']['slack_channels']
                print(f"  Fetching from channels: {', '.join(kwargs['channels'])}")
        else:
            customer_data = {'customer_id': customer_id}
        
        data = integration.sync_customer_data(customer_id, force_refresh=force_refresh, **kwargs)
        
        if 'interactions' not in customer_data:
            customer_data['interactions'] = {}
        
        customer_data['interactions'][integration_name] = data
        customer_data['updated_at'] = datetime.now().isoformat()
        
        with open(customer_file, 'w') as f:
            json.dump(customer_data, f, indent=2)
        
        print(f"✓ {integration_name} data synced successfully")
        return data
        
    except Exception as e:
        print(f"✗ Error running {integration_name}: {e}")
        import traceback
        traceback.print_exc()
        return None

def run_all_integrations(customer_id: str, force_refresh: bool = False):
    results = {}
    for integration_name in INTEGRATIONS:
        data = run_single_integration(integration_name, customer_id, force_refresh)
        if data:
            results[integration_name] = data
    return results

def main():
    parser = argparse.ArgumentParser(description='Run integrations to sync customer data')
    parser.add_argument('customer_id', help='Customer ID to sync data for')
    parser.add_argument('--integration', '-i', choices=list(INTEGRATIONS.keys()) + ['all'],
                       default='all', help='Which integration to run')
    parser.add_argument('--force', '-f', action='store_true',
                       help='Force refresh, ignore cache')
    parser.add_argument('--customer-name', '-n', help='Customer name (for search)')
    
    args = parser.parse_args()
    
    if args.integration == 'all':
        results = run_all_integrations(args.customer_id, args.force)
    else:
        kwargs = {}
        if args.customer_name:
            kwargs['customer_name'] = args.customer_name
        results = run_single_integration(args.integration, args.customer_id, args.force, **kwargs)
    
    if results:
        print(f"\nSync complete. Data saved to customers/{args.customer_id}.json")

if __name__ == '__main__':
    main()