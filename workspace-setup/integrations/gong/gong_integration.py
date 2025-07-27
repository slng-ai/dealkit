"""
Gong.io Integration
Analyzes call recordings and transcripts from an individual's Gong library
Supports both direct API access and MCP protocol if available
"""

from ..base_integration import BaseIntegration
import requests
import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import base64

class GongIntegration(BaseIntegration):
    def __init__(self):
        super().__init__("gong")
        self.name = "Gong.io"
        self.config = {
            "auth_type": "oauth2",
            "required_env": ["GONG_API_KEY", "GONG_API_SECRET"],
            "base_url": "https://api.gong.io/v2",
            "integration_type": "hybrid"  # API + URL analysis + MCP
        }
        self.api_key = os.getenv('GONG_API_KEY')
        self.api_secret = os.getenv('GONG_API_SECRET')
        self.headers = {'Content-Type': 'application/json'}
        self.mcp_client = self._init_mcp_client()
    
    def _init_mcp_client(self):
        """Initialize MCP client if Gong MCP server is available"""
        try:
            mcp_url = os.getenv('GONG_MCP_URL', 'http://localhost:3001/gong')
            # In production, would check if MCP server is running
            # For now, return None to use direct API
            return None
        except Exception as e:
            print(f"MCP not available, using direct API: {e}")
            return None
    
    def connect(self):
        """Initialize Gong API connection with basic auth"""
        if not self.api_key or not self.api_secret:
            raise ValueError("Missing Gong API credentials")
        
        # Gong uses basic auth
        credentials = base64.b64encode(f"{self.api_key}:{self.api_secret}".encode()).decode()
        self.headers['Authorization'] = f'Basic {credentials}'
        return True
    
    def analyze_call_url(self, gong_url: str) -> Dict[str, Any]:
        """Analyze a Gong call from URL using WebFetch or extract call ID for API"""
        # Extract call ID from URL if possible
        # Example: https://app.gong.io/call?id=1234567890
        import re
        call_id_match = re.search(r'id=([A-Za-z0-9]+)', gong_url)
        
        if call_id_match and self.api_key:
            # Use API to get full data
            call_id = call_id_match.group(1)
            return self.fetch_call_by_id(call_id)
        else:
            # Fallback to WebFetch analysis
            prompt = """
            Analyze this Gong call and extract:
            1. Participants and their roles
            2. Key topics discussed with timestamps
            3. Customer pain points and challenges
            4. Technical requirements mentioned
            5. Next steps and action items with owners
            6. Competitor mentions and context
            7. Objections raised and responses
            8. Talk time ratio and engagement metrics
            9. Key questions asked by the customer
            10. Risk indicators or concerns
            
            Format the response as structured data.
            """
            return {"url": gong_url, "prompt": prompt, "type": "webfetch_analysis"}
    
    def fetch_call_by_id(self, call_id: str) -> Dict[str, Any]:
        """Fetch complete call data by ID via API"""
        # Use MCP if available
        if self.mcp_client:
            return self._fetch_call_via_mcp(call_id)
        
        try:
            # Get call metadata
            response = requests.get(
                f"{self.config['base_url']}/calls/{call_id}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                call_data = response.json()
                
                # Get transcript
                transcript_response = requests.get(
                    f"{self.config['base_url']}/calls/{call_id}/transcript",
                    headers=self.headers
                )
                
                if transcript_response.status_code == 200:
                    call_data['transcript'] = transcript_response.json()
                
                # Get call stats
                stats_response = requests.get(
                    f"{self.config['base_url']}/calls/{call_id}/stats",
                    headers=self.headers
                )
                
                if stats_response.status_code == 200:
                    call_data['statistics'] = stats_response.json()
                
                return call_data
            else:
                return {"error": f"Failed to fetch call: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Error fetching call: {str(e)}"}
    
    def _fetch_call_via_mcp(self, call_id: str) -> Dict[str, Any]:
        """Fetch call data via MCP protocol"""
        mcp_request = {
            'method': 'gong.getCall',
            'params': {
                'callId': call_id,
                'includeTranscript': True,
                'includeStats': True,
                'includeInsights': True
            }
        }
        # In production, would send to MCP server
        print(f"MCP Request: {mcp_request}")
        return {}
    
    def fetch_my_calls(self, days_back: int = 30) -> List[Dict[str, Any]]:
        """Fetch calls where user is participant"""
        if self.mcp_client:
            return self._fetch_my_calls_via_mcp(days_back)
        
        try:
            from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            user_email = os.getenv('USER_EMAIL', '')
            
            search_params = {
                'fromDateTime': f"{from_date}T00:00:00Z",
                'filter': json.dumps({
                    'participants': [{'email': user_email}]
                })
            }
            
            response = requests.post(
                f"{self.config['base_url']}/calls/search",
                headers=self.headers,
                json=search_params
            )
            
            if response.status_code == 200:
                return response.json().get('calls', [])
            else:
                return []
                
        except Exception as e:
            print(f"Error fetching calls: {e}")
            return []
    
    def _fetch_my_calls_via_mcp(self, days_back: int) -> List[Dict[str, Any]]:
        """Fetch user's calls via MCP"""
        mcp_request = {
            'method': 'gong.getMyCalls',
            'params': {
                'daysBack': days_back,
                'includeSummary': True
            }
        }
        print(f"MCP Request: {mcp_request}")
        return []
    
    def fetch_customer_calls(self, customer_name: str, days_back: int = 30) -> Dict[str, Any]:
        """Fetch all calls related to a specific customer"""
        try:
            from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            
            search_params = {
                'fromDateTime': f"{from_date}T00:00:00Z",
                'filter': json.dumps({
                    'callTitle': {'contains': customer_name}
                })
            }
            
            response = requests.post(
                f"{self.config['base_url']}/calls/search",
                headers=self.headers,
                json=search_params
            )
            
            if response.status_code == 200:
                calls = response.json().get('calls', [])
                return self._analyze_customer_calls(customer_name, calls)
            else:
                return {"error": f"Failed to search calls: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Error searching calls: {str(e)}"}
    
    def _analyze_customer_calls(self, customer_name: str, calls: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns across customer calls"""
        analysis = {
            'customer_name': customer_name,
            'total_calls': len(calls),
            'date_range': {
                'first_call': None,
                'last_call': None
            },
            'engagement_metrics': {
                'total_duration_minutes': 0,
                'average_talk_ratio': 0,
                'call_frequency': 'calculating...'
            },
            'key_themes': {},
            'action_items': [],
            'risks': [],
            'opportunities': [],
            'competitor_mentions': {},
            'deal_progression': []
        }
        
        if not calls:
            return analysis
        
        # Sort calls by date
        calls.sort(key=lambda x: x.get('created', ''))
        
        # Analyze each call
        talk_ratios = []
        for call in calls:
            # Date range
            if not analysis['date_range']['first_call']:
                analysis['date_range']['first_call'] = call.get('created')
            analysis['date_range']['last_call'] = call.get('created')
            
            # Duration
            duration = call.get('duration', 0)
            analysis['engagement_metrics']['total_duration_minutes'] += duration / 60
            
            # Talk ratio
            stats = call.get('statistics', {})
            if 'talkRatio' in stats:
                talk_ratios.append(stats['talkRatio'])
            
            # Themes and topics
            for topic in call.get('topics', []):
                topic_name = topic.get('name', '')
                if topic_name:
                    analysis['key_themes'][topic_name] = \
                        analysis['key_themes'].get(topic_name, 0) + 1
            
            # Call insights
            facts = call.get('facts', {})
            analysis['action_items'].extend(facts.get('actionItems', []))
            analysis['risks'].extend(facts.get('risks', []))
            analysis['opportunities'].extend(facts.get('opportunities', []))
            
            # Competitors
            for comp in facts.get('competitors', []):
                comp_name = comp.get('name', '')
                if comp_name:
                    analysis['competitor_mentions'][comp_name] = \
                        analysis['competitor_mentions'].get(comp_name, 0) + 1
            
            # Deal progression
            analysis['deal_progression'].append({
                'date': call.get('created'),
                'title': call.get('title'),
                'duration_minutes': duration / 60,
                'key_outcome': call.get('summary', 'No summary available')
            })
        
        # Calculate averages
        if talk_ratios:
            analysis['engagement_metrics']['average_talk_ratio'] = \
                sum(talk_ratios) / len(talk_ratios)
        
        # Call frequency analysis
        if len(calls) > 1:
            first_date = datetime.fromisoformat(analysis['date_range']['first_call'].replace('Z', '+00:00'))
            last_date = datetime.fromisoformat(analysis['date_range']['last_call'].replace('Z', '+00:00'))
            days_span = (last_date - first_date).days
            if days_span > 0:
                calls_per_week = len(calls) / (days_span / 7)
                analysis['engagement_metrics']['call_frequency'] = f"{calls_per_week:.1f} calls/week"
        
        return analysis
    
    def search_calls_by_keyword(self, keyword: str, days_back: int = 30) -> List[Dict[str, Any]]:
        """Search transcripts for specific keywords"""
        try:
            from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            
            search_params = {
                'fromDateTime': f"{from_date}T00:00:00Z",
                'filter': json.dumps({
                    'transcript': {'contains': keyword}
                })
            }
            
            response = requests.post(
                f"{self.config['base_url']}/calls/search",
                headers=self.headers,
                json=search_params
            )
            
            if response.status_code == 200:
                return response.json().get('calls', [])
            else:
                return []
                
        except Exception as e:
            print(f"Error searching calls: {e}")
            return []
    
    def push_insights_to_gong(self, call_id: str, insights: Dict[str, Any]) -> bool:
        """Push analyzed insights back to Gong as custom fields or tags"""
        try:
            # Update custom fields
            if 'custom_fields' in insights:
                response = requests.patch(
                    f"{self.config['base_url']}/calls/{call_id}/custom-fields",
                    headers=self.headers,
                    json={'customFields': insights['custom_fields']}
                )
                if response.status_code != 200:
                    return False
            
            # Add tags
            if 'tags' in insights:
                response = requests.post(
                    f"{self.config['base_url']}/calls/{call_id}/tags",
                    headers=self.headers,
                    json={'tags': insights['tags']}
                )
                if response.status_code != 200:
                    return False
            
            return True
            
        except Exception as e:
            print(f"Error pushing insights: {e}")
            return False

# Example usage patterns
if __name__ == "__main__":
    gong = GongIntegration()
    gong.connect()
    
    # Pattern 1: Analyze specific call from URL
    gong_url = "https://app.gong.io/call?id=1234567890"
    result = gong.analyze_call_url(gong_url)
    
    # Pattern 2: Get all calls for a customer
    customer_analysis = gong.fetch_customer_calls("ACME Corp", days_back=90)
    
    # Pattern 3: Search for competitive mentions
    vercel_calls = gong.search_calls_by_keyword("Vercel", days_back=30)
    
    # Pattern 4: Push insights back
    gong.push_insights_to_gong("1234567890", {
        'custom_fields': {'deal_score': 82, 'next_step': 'Contract review'},
        'tags': ['high-value', 'competitor-vercel']
    })