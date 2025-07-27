#!/usr/bin/env python3
"""
Automated Slack Data Fetcher for Customer Intelligence
Fetches and organizes Slack conversations by customer for sales insights
"""

import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from collections import defaultdict
import re
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SlackMessage:
    """Represents a Slack message with metadata"""
    timestamp: str
    channel: str
    user: str
    text: str
    thread_ts: Optional[str] = None
    reactions: Optional[List[Dict]] = None
    attachments: Optional[List[Dict]] = None
    
@dataclass
class CustomerMention:
    """Represents a customer mention in Slack"""
    customer_name: str
    channel: str
    timestamp: datetime
    context: str
    sentiment: str
    category: str
    importance: str

class SlackCustomerFetcher:
    """Fetches and organizes Slack data by customer"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.customers = self._load_customer_list()
        self.channels = self.config.get('channels', [])
        self.fetch_interval = self.config.get('fetch_interval_hours', 1)
        
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file"""
        if not config_path:
            config_path = 'workspace-setup/integrations/slack/config.json'
        
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found at {config_path}, using defaults")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            'channels': [
                '#sales',
                '#customer-success',
                '#support',
                '#product',
                '#engineering'
            ],
            'fetch_interval_hours': 1,
            'history_days': 30,
            'importance_keywords': {
                'high': ['urgent', 'critical', 'blocker', 'churn', 'cancel'],
                'medium': ['issue', 'problem', 'concern', 'question'],
                'low': ['fyi', 'update', 'info']
            }
        }
    
    def _load_customer_list(self) -> List[Dict[str, Any]]:
        """Load list of customers from customer directory"""
        customers = []
        customer_dir = Path('customers')
        
        for customer_path in customer_dir.iterdir():
            if customer_path.is_dir() and not customer_path.name.startswith('.'):
                profile_path = customer_path / 'profile.json'
                if profile_path.exists():
                    try:
                        with open(profile_path, 'r') as f:
                            profile = json.load(f)
                            customers.append({
                                'id': customer_path.name,
                                'name': profile.get('company_name', customer_path.name),
                                'aliases': profile.get('aliases', []),
                                'domains': profile.get('domains', [])
                            })
                    except Exception as e:
                        logger.error(f"Error loading customer {customer_path.name}: {e}")
        
        return customers
    
    async def fetch_channel_history(self, channel: str, since: datetime) -> List[SlackMessage]:
        """Fetch message history from a Slack channel"""
        # This would integrate with actual Slack API
        # For now, return mock data structure
        messages = []
        
        # Mock implementation - replace with actual Slack API calls
        logger.info(f"Fetching messages from {channel} since {since}")
        
        # Example structure of what real implementation would return
        mock_messages = [
            SlackMessage(
                timestamp="1234567890.123456",
                channel=channel,
                user="U123456",
                text="Had a great call with Acme Corp today. They're interested in our enterprise features.",
                thread_ts=None,
                reactions=[{"name": "thumbsup", "count": 2}]
            ),
            SlackMessage(
                timestamp="1234567891.123456",
                channel=channel,
                user="U234567",
                text="TechStart Inc mentioned they need better API rate limits. Potential upsell opportunity.",
                thread_ts=None
            )
        ]
        
        return mock_messages
    
    def extract_customer_mentions(self, messages: List[SlackMessage]) -> List[CustomerMention]:
        """Extract customer mentions from messages"""
        mentions = []
        
        for message in messages:
            for customer in self.customers:
                # Check customer name and aliases
                patterns = [customer['name']] + customer.get('aliases', [])
                
                for pattern in patterns:
                    if self._is_mentioned(pattern, message.text):
                        mention = CustomerMention(
                            customer_name=customer['name'],
                            channel=message.channel,
                            timestamp=self._parse_timestamp(message.timestamp),
                            context=self._extract_context(message.text, pattern),
                            sentiment=self._analyze_sentiment(message.text),
                            category=self._categorize_mention(message.text),
                            importance=self._assess_importance(message.text)
                        )
                        mentions.append(mention)
                        break
        
        return mentions
    
    def _is_mentioned(self, pattern: str, text: str) -> bool:
        """Check if pattern is mentioned in text"""
        # Case-insensitive word boundary search
        regex = r'\b' + re.escape(pattern.lower()) + r'\b'
        return bool(re.search(regex, text.lower()))
    
    def _extract_context(self, text: str, pattern: str, context_words: int = 50) -> str:
        """Extract context around mention"""
        # Find pattern location and extract surrounding context
        match = re.search(re.escape(pattern), text, re.IGNORECASE)
        if match:
            start = max(0, match.start() - context_words)
            end = min(len(text), match.end() + context_words)
            context = text[start:end]
            
            # Clean up context
            if start > 0:
                context = "..." + context
            if end < len(text):
                context = context + "..."
                
            return context
        return text[:100] + "..."
    
    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis"""
        positive_words = ['great', 'excellent', 'happy', 'pleased', 'excited', 'love']
        negative_words = ['issue', 'problem', 'unhappy', 'frustrated', 'concern', 'disappointed']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _categorize_mention(self, text: str) -> str:
        """Categorize the type of mention"""
        categories = {
            'sales': ['deal', 'opportunity', 'demo', 'proposal', 'contract'],
            'support': ['issue', 'bug', 'problem', 'ticket', 'help'],
            'success': ['onboarding', 'training', 'adoption', 'usage'],
            'product': ['feature', 'request', 'feedback', 'roadmap'],
            'general': []
        }
        
        text_lower = text.lower()
        for category, keywords in categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        
        return 'general'
    
    def _assess_importance(self, text: str) -> str:
        """Assess importance of mention"""
        importance_keywords = self.config.get('importance_keywords', {})
        
        text_lower = text.lower()
        for level, keywords in importance_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return level
        
        return 'medium'
    
    def _parse_timestamp(self, ts: str) -> datetime:
        """Parse Slack timestamp to datetime"""
        try:
            return datetime.fromtimestamp(float(ts))
        except:
            return datetime.now()
    
    async def fetch_all_channels(self) -> Dict[str, List[CustomerMention]]:
        """Fetch data from all configured channels"""
        all_mentions = defaultdict(list)
        since = datetime.now() - timedelta(hours=self.fetch_interval)
        
        for channel in self.channels:
            try:
                messages = await self.fetch_channel_history(channel, since)
                mentions = self.extract_customer_mentions(messages)
                
                for mention in mentions:
                    all_mentions[mention.customer_name].append(mention)
                    
            except Exception as e:
                logger.error(f"Error fetching channel {channel}: {e}")
        
        return dict(all_mentions)
    
    def save_customer_mentions(self, mentions: Dict[str, List[CustomerMention]]):
        """Save mentions to customer folders"""
        for customer_name, customer_mentions in mentions.items():
            # Find customer folder
            customer_folder = None
            for customer in self.customers:
                if customer['name'] == customer_name:
                    customer_folder = Path(f"customers/{customer['id']}/slack")
                    break
            
            if not customer_folder:
                logger.warning(f"No folder found for customer {customer_name}")
                continue
            
            # Create slack folder if it doesn't exist
            customer_folder.mkdir(parents=True, exist_ok=True)
            
            # Save mentions
            mentions_file = customer_folder / f"mentions_{datetime.now().strftime('%Y%m%d')}.json"
            
            mentions_data = []
            for mention in customer_mentions:
                mentions_data.append({
                    'timestamp': mention.timestamp.isoformat(),
                    'channel': mention.channel,
                    'context': mention.context,
                    'sentiment': mention.sentiment,
                    'category': mention.category,
                    'importance': mention.importance
                })
            
            # Append to existing file or create new
            if mentions_file.exists():
                with open(mentions_file, 'r') as f:
                    existing_data = json.load(f)
                mentions_data = existing_data + mentions_data
            
            with open(mentions_file, 'w') as f:
                json.dump(mentions_data, f, indent=2)
            
            logger.info(f"Saved {len(customer_mentions)} mentions for {customer_name}")
            
            # Update customer summary
            self._update_customer_summary(customer_folder.parent, customer_mentions)
    
    def _update_customer_summary(self, customer_folder: Path, mentions: List[CustomerMention]):
        """Update customer Slack summary"""
        summary_file = customer_folder / 'slack_summary.json'
        
        # Load existing summary
        if summary_file.exists():
            with open(summary_file, 'r') as f:
                summary = json.load(f)
        else:
            summary = {
                'total_mentions': 0,
                'sentiment_breakdown': {'positive': 0, 'negative': 0, 'neutral': 0},
                'category_breakdown': {},
                'important_mentions': [],
                'last_updated': None
            }
        
        # Update summary
        summary['total_mentions'] += len(mentions)
        
        for mention in mentions:
            summary['sentiment_breakdown'][mention.sentiment] += 1
            
            if mention.category not in summary['category_breakdown']:
                summary['category_breakdown'][mention.category] = 0
            summary['category_breakdown'][mention.category] += 1
            
            if mention.importance == 'high':
                summary['important_mentions'].append({
                    'timestamp': mention.timestamp.isoformat(),
                    'context': mention.context,
                    'channel': mention.channel
                })
        
        # Keep only last 10 important mentions
        summary['important_mentions'] = summary['important_mentions'][-10:]
        summary['last_updated'] = datetime.now().isoformat()
        
        # Save updated summary
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
    
    async def run_continuous(self):
        """Run continuous fetching"""
        logger.info("Starting continuous Slack data fetching")
        
        while True:
            try:
                logger.info("Fetching latest Slack data...")
                mentions = await self.fetch_all_channels()
                self.save_customer_mentions(mentions)
                
                # Generate alerts for high-importance mentions
                self._generate_alerts(mentions)
                
                logger.info(f"Completed fetch cycle. Next run in {self.fetch_interval} hours")
                await asyncio.sleep(self.fetch_interval * 3600)
                
            except Exception as e:
                logger.error(f"Error in fetch cycle: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error
    
    def _generate_alerts(self, mentions: Dict[str, List[CustomerMention]]):
        """Generate alerts for high-importance mentions"""
        alerts = []
        
        for customer_name, customer_mentions in mentions.items():
            high_importance = [m for m in customer_mentions if m.importance == 'high']
            negative_sentiment = [m for m in customer_mentions if m.sentiment == 'negative']
            
            if high_importance:
                alerts.append({
                    'type': 'high_importance_mention',
                    'customer': customer_name,
                    'count': len(high_importance),
                    'examples': [m.context for m in high_importance[:2]]
                })
            
            if len(negative_sentiment) >= 3:
                alerts.append({
                    'type': 'negative_sentiment_spike',
                    'customer': customer_name,
                    'count': len(negative_sentiment),
                    'examples': [m.context for m in negative_sentiment[:2]]
                })
        
        # Save alerts
        if alerts:
            alerts_file = Path('reporting/pulse/slack_alerts.json')
            alerts_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(alerts_file, 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'alerts': alerts
                }, f, indent=2)
            
            logger.info(f"Generated {len(alerts)} alerts")


def main():
    """Main entry point"""
    fetcher = SlackCustomerFetcher()
    asyncio.run(fetcher.run_continuous())


if __name__ == "__main__":
    main()