import os
import sys
sys.path.append('..')

from base_integration import BaseIntegration
from typing import Dict, Any, List
from datetime import datetime, timedelta
import requests

class SlackIntegration(BaseIntegration):
    def __init__(self):
        super().__init__('../../agents/slack_agent.json')
        self.base_url = "https://slack.com/api"
        self.token = os.getenv('SLACK_TOKEN')
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def authenticate(self) -> bool:
        if not self.token:
            self.logger.error("No Slack token found")
            return False
        
        response = requests.get(
            f"{self.base_url}/auth.test",
            headers=self.headers
        )
        
        if response.status_code == 200 and response.json().get('ok'):
            self.logger.info("Slack authentication successful")
            return True
        
        self.logger.error(f"Slack authentication failed: {response.text}")
        return False
    
    def fetch_data(self, customer_id: str, **kwargs) -> Dict[str, Any]:
        customer_name = kwargs.get('customer_name', customer_id)
        days_back = kwargs.get('days_back', 30)
        
        # Always look for these two channel patterns
        channel_patterns = [
            f"baseten-{customer_id}",  # Customer channel
            f"baseten-{customer_id}-internal"  # Internal discussion channel
        ]
        
        results = {
            'customer_id': customer_id,
            'customer_name': customer_name,
            'messages': [],
            'channels': [],
            'threads': [],
            'channel_history': {},
            'summary': {
                'total_messages': 0,
                'customer_channel_messages': 0,
                'internal_channel_messages': 0
            }
        }
        
        # Fetch data from both channels
        for channel_name in channel_patterns:
            self.logger.info(f"Looking for channel: #{channel_name}")
            channel_id = self._get_channel_id(channel_name)
            
            if channel_id:
                self.logger.info(f"Found channel {channel_name} with ID {channel_id}")
                history = self._get_channel_history(channel_id, days_back)
                
                if history:
                    results['channel_history'][channel_name] = history
                    results['channels'].append({
                        'name': channel_name,
                        'id': channel_id,
                        'message_count': len(history),
                        'is_internal': '-internal' in channel_name
                    })
                    
                    # Update summary
                    results['summary']['total_messages'] += len(history)
                    if '-internal' in channel_name:
                        results['summary']['internal_channel_messages'] = len(history)
                    else:
                        results['summary']['customer_channel_messages'] = len(history)
                    
                    self.logger.info(f"Fetched {len(history)} messages from {channel_name}")
            else:
                self.logger.warning(f"Channel not found: {channel_name}")
        
        return results
    
    def process_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        processed = {
            'customer_id': raw_data['customer_id'],
            'customer_name': raw_data['customer_name'],
            'summary': {},
            'key_discussions': [],
            'action_items': [],
            'sentiment': 'neutral',
            'engagement_level': 'medium'
        }
        
        # Process messages
        for message in raw_data.get('messages', []):
            discussion = {
                'timestamp': message.get('ts'),
                'channel': message.get('channel', {}).get('name'),
                'text': message.get('text'),
                'user': message.get('username')
            }
            processed['key_discussions'].append(discussion)
            
            # Extract action items
            if any(keyword in message.get('text', '').lower() for keyword in ['todo', 'action', 'will do', 'follow up']):
                processed['action_items'].append({
                    'text': message.get('text'),
                    'timestamp': message.get('ts'),
                    'assigned_to': message.get('username')
                })
        
        # Calculate engagement metrics
        message_count = len(raw_data.get('messages', []))
        if message_count > 50:
            processed['engagement_level'] = 'high'
        elif message_count < 10:
            processed['engagement_level'] = 'low'
        
        # Generate summary
        processed['summary'] = {
            'total_messages': message_count,
            'active_channels': len(raw_data.get('channels', [])),
            'thread_count': len(raw_data.get('threads', [])),
            'last_interaction': max([m.get('ts', '0') for m in raw_data.get('messages', [])], default='Never')
        }
        
        return processed
    
    def _search_messages(self, query: str) -> Dict[str, Any]:
        try:
            response = requests.get(
                f"{self.base_url}/search.messages",
                headers=self.headers,
                params={'query': query, 'count': 100}
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            self.logger.error(f"Error searching messages: {e}")
        return {}
    
    def _get_customer_channels(self, customer_name: str) -> List[Dict[str, Any]]:
        # This would search for channels where the customer is discussed
        # For now, returning empty list as this requires channel iteration
        return []
    
    def _get_channel_threads(self, channel_id: str, days_back: int) -> List[Dict[str, Any]]:
        # This would get threads from a specific channel
        # For now, returning empty list
        return []
    
    def _get_channel_id(self, channel_name: str) -> str:
        """Get channel ID from channel name"""
        try:
            # Remove # if present
            channel_name = channel_name.lstrip('#')
            
            # Get list of channels
            response = requests.get(
                f"{self.base_url}/conversations.list",
                headers=self.headers,
                params={'types': 'public_channel,private_channel', 'limit': 1000}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    for channel in data.get('channels', []):
                        if channel.get('name') == channel_name:
                            return channel['id']
            
            self.logger.error(f"Channel not found: {channel_name}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting channel ID: {e}")
            return None
    
    def _get_channel_history(self, channel_id: str, days_back: int) -> List[Dict[str, Any]]:
        """Get message history from a channel"""
        try:
            oldest = (datetime.now() - timedelta(days=days_back)).timestamp()
            
            messages = []
            cursor = None
            
            while True:
                params = {
                    'channel': channel_id,
                    'oldest': oldest,
                    'limit': 100
                }
                
                if cursor:
                    params['cursor'] = cursor
                
                response = requests.get(
                    f"{self.base_url}/conversations.history",
                    headers=self.headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('ok'):
                        messages.extend(data.get('messages', []))
                        
                        # Check if there are more messages
                        if not data.get('has_more'):
                            break
                        cursor = data.get('response_metadata', {}).get('next_cursor')
                    else:
                        self.logger.error(f"Error fetching history: {data.get('error')}")
                        break
                else:
                    self.logger.error(f"HTTP error: {response.status_code}")
                    break
            
            return messages
            
        except Exception as e:
            self.logger.error(f"Error getting channel history: {e}")
            return []