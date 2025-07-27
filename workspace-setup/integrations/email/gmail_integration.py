import os
import sys
sys.path.append('..')

from base_integration import BaseIntegration
from typing import Dict, Any, List
from datetime import datetime, timedelta
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

class GmailIntegration(BaseIntegration):
    def __init__(self):
        super().__init__('../../agents/email_agent.json')
        self.service = None
        self.token_file = '../../config/gmail_token.json'
    
    def authenticate(self) -> bool:
        """Authenticate with Gmail using stored credentials"""
        if not os.path.exists(self.token_file):
            self.logger.error("Gmail not configured. Run setup_gmail.py first.")
            return False
        
        try:
            creds = Credentials.from_authorized_user_file(self.token_file)
            self.service = build('gmail', 'v1', credentials=creds)
            self.logger.info("Gmail authentication successful")
            return True
        except Exception as e:
            self.logger.error(f"Gmail authentication failed: {e}")
            return False
    
    def fetch_data(self, customer_id: str, **kwargs) -> Dict[str, Any]:
        """Fetch emails for a customer"""
        customer_email = kwargs.get('customer_email')
        days_back = kwargs.get('days_back', 30)
        
        if not customer_email:
            self.logger.error("No customer email provided")
            return {'error': 'No customer email'}
        
        results = {
            'customer_id': customer_id,
            'customer_email': customer_email,
            'threads': [],
            'total_emails': 0,
            'date_range': {
                'start': (datetime.now() - timedelta(days=days_back)).isoformat(),
                'end': datetime.now().isoformat()
            }
        }
        
        try:
            # Search for emails to/from customer
            query = f'to:{customer_email} OR from:{customer_email}'
            
            # Get email threads
            threads_result = self.service.users().threads().list(
                userId='me',
                q=query,
                maxResults=50
            ).execute()
            
            threads = threads_result.get('threads', [])
            
            for thread in threads[:20]:  # Limit to 20 most recent threads
                thread_data = self._fetch_thread_details(thread['id'])
                if thread_data:
                    results['threads'].append(thread_data)
                    results['total_emails'] += len(thread_data.get('messages', []))
            
        except Exception as e:
            self.logger.error(f"Error fetching emails: {e}")
            results['error'] = str(e)
        
        return results
    
    def process_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process email data for analysis"""
        processed = {
            'customer_id': raw_data['customer_id'],
            'customer_email': raw_data['customer_email'],
            'summary': {
                'total_threads': len(raw_data.get('threads', [])),
                'total_emails': raw_data.get('total_emails', 0),
                'date_range': raw_data.get('date_range')
            },
            'key_threads': [],
            'action_items': [],
            'sentiment': 'neutral',
            'response_times': []
        }
        
        # Process each thread
        for thread in raw_data.get('threads', []):
            thread_summary = {
                'thread_id': thread['id'],
                'subject': thread.get('subject', 'No Subject'),
                'message_count': len(thread.get('messages', [])),
                'participants': thread.get('participants', []),
                'last_message_date': thread.get('last_message_date'),
                'snippet': thread.get('snippet', ''),
                'has_attachments': thread.get('has_attachments', False)
            }
            
            # Extract key information
            if any(keyword in thread.get('snippet', '').lower() 
                   for keyword in ['contract', 'proposal', 'pricing', 'urgent', 'decision']):
                thread_summary['priority'] = 'high'
            
            processed['key_threads'].append(thread_summary)
            
            # Look for action items in messages
            for msg in thread.get('messages', []):
                body = msg.get('body', '')
                if any(action in body.lower() 
                       for action in ['action:', 'todo:', 'will send', 'please provide', 'need']):
                    processed['action_items'].append({
                        'thread_id': thread['id'],
                        'date': msg.get('date'),
                        'from': msg.get('from'),
                        'snippet': body[:200]
                    })
        
        # Calculate average response time
        response_times = raw_data.get('response_times', [])
        if response_times:
            avg_response = sum(response_times) / len(response_times)
            processed['summary']['avg_response_time'] = f"{avg_response:.1f} hours"
        
        # Sort threads by date
        processed['key_threads'].sort(
            key=lambda x: x.get('last_message_date', ''), 
            reverse=True
        )
        
        return processed
    
    def _fetch_thread_details(self, thread_id: str) -> Dict[str, Any]:
        """Fetch details of a single email thread"""
        try:
            thread = self.service.users().threads().get(
                userId='me',
                id=thread_id
            ).execute()
            
            messages = thread.get('messages', [])
            if not messages:
                return None
            
            # Extract thread info
            thread_data = {
                'id': thread_id,
                'messages': [],
                'participants': set(),
                'has_attachments': False
            }
            
            for msg in messages:
                msg_data = self._parse_message(msg)
                if msg_data:
                    thread_data['messages'].append(msg_data)
                    thread_data['participants'].add(msg_data['from'])
                    thread_data['participants'].add(msg_data['to'])
                    
                    if msg_data.get('has_attachments'):
                        thread_data['has_attachments'] = True
            
            # Get thread metadata from first message
            if thread_data['messages']:
                first_msg = thread_data['messages'][0]
                thread_data['subject'] = first_msg.get('subject', 'No Subject')
                thread_data['snippet'] = first_msg.get('snippet', '')
                thread_data['last_message_date'] = thread_data['messages'][-1].get('date')
            
            thread_data['participants'] = list(thread_data['participants'])
            
            return thread_data
            
        except Exception as e:
            self.logger.error(f"Error fetching thread {thread_id}: {e}")
            return None
    
    def _parse_message(self, msg: Dict[str, Any]) -> Dict[str, Any]:
        """Parse a single email message"""
        try:
            headers = msg['payload'].get('headers', [])
            
            # Extract header info
            msg_data = {
                'id': msg['id'],
                'date': None,
                'from': None,
                'to': None,
                'subject': None,
                'snippet': msg.get('snippet', ''),
                'has_attachments': False
            }
            
            for header in headers:
                name = header['name'].lower()
                if name == 'date':
                    msg_data['date'] = header['value']
                elif name == 'from':
                    msg_data['from'] = self._extract_email(header['value'])
                elif name == 'to':
                    msg_data['to'] = self._extract_email(header['value'])
                elif name == 'subject':
                    msg_data['subject'] = header['value']
            
            # Check for attachments
            if 'parts' in msg['payload']:
                for part in msg['payload']['parts']:
                    if part.get('filename'):
                        msg_data['has_attachments'] = True
                        break
            
            # Extract body (simplified)
            body = self._extract_body(msg['payload'])
            if body:
                msg_data['body'] = body[:1000]  # First 1000 chars
            
            return msg_data
            
        except Exception as e:
            self.logger.error(f"Error parsing message: {e}")
            return None
    
    def _extract_email(self, email_string: str) -> str:
        """Extract email address from string like 'Name <email@example.com>'"""
        import re
        match = re.search(r'<(.+?)>', email_string)
        if match:
            return match.group(1)
        return email_string.strip()
    
    def _extract_body(self, payload: Dict[str, Any]) -> str:
        """Extract body text from email payload"""
        body = ''
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    body += base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        elif payload['body'].get('data'):
            body = base64.urlsafe_b64decode(
                payload['body']['data']
            ).decode('utf-8', errors='ignore')
        
        return body