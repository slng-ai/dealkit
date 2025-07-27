"""
Granola integration for extracting meeting notes and insights
Supports URL-based analysis, API access, and MCP protocol
"""

from ..base_integration import BaseIntegration
from typing import Dict, Any, List, Optional
import requests
import os
import json
from datetime import datetime, timedelta
import re


class GranolaIntegration(BaseIntegration):
    """
    Integration with Granola for meeting notes analysis
    Granola captures meeting notes and action items from video calls
    """
    
    def __init__(self):
        super().__init__("granola")
        self.name = "Granola"
        self.config = {
            "auth_type": "api_key",
            "required_env": ["GRANOLA_API_KEY"],
            "base_url": "https://api.granola.so/v1",
            "integration_type": "hybrid"  # URL analysis + API + MCP
        }
        self.api_key = os.getenv('GRANOLA_API_KEY')
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        self.mcp_client = self._init_mcp_client()
    
    def _init_mcp_client(self):
        """Initialize MCP client if Granola MCP server is available"""
        try:
            mcp_url = os.getenv('GRANOLA_MCP_URL', 'http://localhost:3001/granola')
            # In production, would check if MCP server is running
            return None
        except Exception as e:
            print(f"MCP not available, using direct methods: {e}")
            return None
    
    def authenticate(self) -> bool:
        """
        Authenticate with Granola API
        """
        if not self.api_key:
            print("No Granola API key found")
            return False
        
        try:
            # Test authentication with a simple API call
            response = requests.get(
                f"{self.config['base_url']}/user",
                headers=self.headers
            )
            
            if response.status_code == 200:
                print("Granola authentication successful")
                return True
            else:
                print(f"Granola authentication failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Authentication error: {e}")
            return False
    
    def analyze_granola_url(self, url: str) -> Dict[str, Any]:
        """
        Analyze a specific Granola meeting notes URL
        """
        # Extract meeting ID from URL if possible
        # Example: https://app.granola.so/meeting/abc123def456
        meeting_id_match = re.search(r'/meeting/([A-Za-z0-9]+)', url)
        
        if meeting_id_match and self.api_key:
            # Use API to get full data
            meeting_id = meeting_id_match.group(1)
            return self.fetch_meeting_by_id(meeting_id)
        else:
            # Fallback to WebFetch analysis
            prompt = """
            Analyze these Granola meeting notes and extract:
            1. Meeting title and date
            2. Attendees and their roles
            3. Meeting agenda items
            4. Key discussion points with context
            5. Decisions made during the meeting
            6. Action items with owners and deadlines
            7. Notable quotes or important statements
            8. Follow-up items or next meeting plans
            9. Any blockers or concerns raised
            10. Overall meeting sentiment and productivity
            
            Format the response as structured data.
            """
            return {"url": url, "prompt": prompt, "type": "webfetch_analysis"}
    
    def fetch_meeting_by_id(self, meeting_id: str) -> Dict[str, Any]:
        """Fetch complete meeting data by ID via API"""
        if self.mcp_client:
            return self._fetch_meeting_via_mcp(meeting_id)
        
        try:
            response = requests.get(
                f"{self.config['base_url']}/meetings/{meeting_id}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to fetch meeting: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Error fetching meeting: {str(e)}"}
    
    def _fetch_meeting_via_mcp(self, meeting_id: str) -> Dict[str, Any]:
        """Fetch meeting data via MCP protocol"""
        mcp_request = {
            'method': 'granola.getMeeting',
            'params': {
                'meetingId': meeting_id,
                'includeTranscript': True,
                'includeActionItems': True
            }
        }
        print(f"MCP Request: {mcp_request}")
        return {}
    
    def fetch_data(self, customer_id: str, **kwargs) -> Dict[str, Any]:
        """
        Fetch meeting notes related to a customer
        """
        customer_name = kwargs.get('customer_name', customer_id)
        days_back = kwargs.get('days_back', 30)
        meeting_ids = kwargs.get('meeting_ids', [])
        
        if self.mcp_client:
            return self._fetch_via_mcp(customer_id, customer_name, days_back)
        
        results = {
            "customer_id": customer_id,
            "customer_name": customer_name,
            "meetings": [],
            "insights": {
                "total_meetings": 0,
                "total_duration_minutes": 0,
                "action_items_count": 0,
                "decisions_made": [],
                "key_themes": {},
                "participant_engagement": {}
            }
        }
        
        # If specific meeting IDs provided
        if meeting_ids:
            for meeting_id in meeting_ids:
                meeting_data = self.fetch_meeting_by_id(meeting_id)
                if 'error' not in meeting_data:
                    results['meetings'].append(meeting_data)
        else:
            # Search for meetings by customer name
            meetings = self.search_meetings_by_customer(customer_name, days_back)
            results['meetings'] = meetings
        
        # Calculate insights
        if results['meetings']:
            results['insights'] = self._calculate_insights(results['meetings'])
        
        return results
    
    def _fetch_via_mcp(self, customer_id: str, customer_name: str, days_back: int) -> Dict[str, Any]:
        """Fetch data via MCP protocol"""
        mcp_request = {
            'method': 'granola.getCustomerMeetings',
            'params': {
                'customerName': customer_name,
                'daysBack': days_back,
                'includeNotes': True
            }
        }
        print(f"MCP Request: {mcp_request}")
        return {}
    
    def search_meetings_by_customer(self, customer_name: str, days_back: int = 30) -> List[Dict[str, Any]]:
        """Search for meetings related to a customer"""
        try:
            from_date = (datetime.now() - timedelta(days=days_back)).isoformat()
            
            params = {
                'query': customer_name,
                'from_date': from_date,
                'limit': 100
            }
            
            response = requests.get(
                f"{self.config['base_url']}/meetings/search",
                headers=self.headers,
                params=params
            )
            
            if response.status_code == 200:
                return response.json().get('meetings', [])
            else:
                return []
                
        except Exception as e:
            print(f"Error searching meetings: {e}")
            return []
    
    def fetch_my_recent_meetings(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """Fetch user's recent meetings"""
        try:
            from_date = (datetime.now() - timedelta(days=days_back)).isoformat()
            
            params = {
                'from_date': from_date,
                'limit': 50
            }
            
            response = requests.get(
                f"{self.config['base_url']}/meetings",
                headers=self.headers,
                params=params
            )
            
            if response.status_code == 200:
                return response.json().get('meetings', [])
            else:
                return []
                
        except Exception as e:
            print(f"Error fetching meetings: {e}")
            return []
    
    def _calculate_insights(self, meetings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate insights from meetings"""
        insights = {
            "total_meetings": len(meetings),
            "total_duration_minutes": 0,
            "action_items_count": 0,
            "decisions_made": [],
            "key_themes": {},
            "participant_engagement": {},
            "meeting_effectiveness": []
        }
        
        for meeting in meetings:
            # Duration
            duration = meeting.get('duration_minutes', 0)
            insights['total_duration_minutes'] += duration
            
            # Action items
            action_items = meeting.get('action_items', [])
            insights['action_items_count'] += len(action_items)
            
            # Decisions
            decisions = meeting.get('decisions', [])
            insights['decisions_made'].extend(decisions)
            
            # Themes from tags or topics
            for tag in meeting.get('tags', []):
                insights['key_themes'][tag] = insights['key_themes'].get(tag, 0) + 1
            
            # Participant engagement
            for participant in meeting.get('participants', []):
                name = participant.get('name', 'Unknown')
                if name not in insights['participant_engagement']:
                    insights['participant_engagement'][name] = {
                        'meetings_attended': 0,
                        'action_items_owned': 0
                    }
                insights['participant_engagement'][name]['meetings_attended'] += 1
                
                # Count action items owned
                for item in action_items:
                    if item.get('owner') == name:
                        insights['participant_engagement'][name]['action_items_owned'] += 1
            
            # Meeting effectiveness
            effectiveness = self._calculate_meeting_effectiveness(meeting)
            insights['meeting_effectiveness'].append({
                'meeting_id': meeting.get('id'),
                'title': meeting.get('title'),
                'effectiveness_score': effectiveness
            })
        
        return insights
    
    def _calculate_meeting_effectiveness(self, meeting: Dict[str, Any]) -> int:
        """Calculate meeting effectiveness score"""
        score = 50  # Base score
        
        # Positive indicators
        if meeting.get('agenda'):
            score += 10
        if meeting.get('action_items'):
            score += len(meeting['action_items']) * 5
        if meeting.get('decisions'):
            score += len(meeting['decisions']) * 10
        if meeting.get('duration_minutes', 60) <= 30:
            score += 10  # Bonus for short meetings
        
        # Negative indicators
        if meeting.get('duration_minutes', 0) > 60:
            score -= 10  # Penalty for long meetings
        if not meeting.get('next_steps'):
            score -= 5
        
        return max(0, min(100, score))
    
    def process_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process Granola meeting data into actionable insights
        """
        processed = {
            "customer_id": raw_data['customer_id'],
            "customer_name": raw_data['customer_name'],
            "summary": {
                "meeting_cadence": "calculating...",
                "engagement_trend": "stable",
                "action_completion_rate": 0,
                "decision_velocity": "normal"
            },
            "key_insights": [],
            "pending_actions": [],
            "recent_decisions": [],
            "collaboration_health": "good"
        }
        
        insights = raw_data.get('insights', {})
        meetings = raw_data.get('meetings', [])
        
        # Calculate meeting cadence
        if len(meetings) > 1:
            # Sort by date
            sorted_meetings = sorted(meetings, key=lambda x: x.get('date', ''))
            days_between = []
            
            for i in range(1, len(sorted_meetings)):
                date1 = datetime.fromisoformat(sorted_meetings[i-1]['date'].replace('Z', '+00:00'))
                date2 = datetime.fromisoformat(sorted_meetings[i]['date'].replace('Z', '+00:00'))
                days_between.append((date2 - date1).days)
            
            if days_between:
                avg_days = sum(days_between) / len(days_between)
                if avg_days <= 7:
                    processed['summary']['meeting_cadence'] = 'weekly'
                elif avg_days <= 14:
                    processed['summary']['meeting_cadence'] = 'bi-weekly'
                else:
                    processed['summary']['meeting_cadence'] = 'monthly'
        
        # Extract pending actions
        for meeting in meetings:
            for action in meeting.get('action_items', []):
                if not action.get('completed', False):
                    processed['pending_actions'].append({
                        'item': action.get('description'),
                        'owner': action.get('owner'),
                        'due_date': action.get('due_date', 'TBD'),
                        'from_meeting': meeting.get('title')
                    })
        
        # Recent decisions
        all_decisions = insights.get('decisions_made', [])
        processed['recent_decisions'] = all_decisions[-5:]  # Last 5 decisions
        
        # Key insights
        if insights.get('action_items_count', 0) > 10 and len(processed['pending_actions']) > 5:
            processed['key_insights'].append({
                'type': 'action_overload',
                'insight': 'High number of pending action items',
                'recommendation': 'Review and prioritize action items in next meeting'
            })
        
        # Collaboration health
        participant_count = len(insights.get('participant_engagement', {}))
        if participant_count < 3:
            processed['collaboration_health'] = 'limited'
        elif participant_count > 6:
            processed['collaboration_health'] = 'complex'
        
        return processed
    
    def push_data(self, data: Dict[str, Any], destination: str) -> bool:
        """
        Push data back to Granola (e.g., update action items, add notes)
        """
        try:
            if destination == 'action_item_status':
                # Update action item completion status
                action_id = data.get('action_id')
                completed = data.get('completed', False)
                
                response = requests.patch(
                    f"{self.config['base_url']}/action-items/{action_id}",
                    headers=self.headers,
                    json={'completed': completed}
                )
                
                return response.status_code == 200
            
            elif destination == 'meeting_notes':
                # Add additional notes to a meeting
                meeting_id = data.get('meeting_id')
                notes = data.get('notes', '')
                
                response = requests.post(
                    f"{self.config['base_url']}/meetings/{meeting_id}/notes",
                    headers=self.headers,
                    json={'notes': notes}
                )
                
                return response.status_code == 200
            
            return False
            
        except Exception as e:
            print(f"Error pushing data: {e}")
            return False
    
    def create_meeting_summary(self, meeting_id: str) -> Dict[str, Any]:
        """Generate AI summary of a meeting"""
        try:
            response = requests.post(
                f"{self.config['base_url']}/meetings/{meeting_id}/summary",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to create summary: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Error creating summary: {str(e)}"}

# Example usage patterns
if __name__ == "__main__":
    granola = GranolaIntegration()
    granola.authenticate()
    
    # Pattern 1: Analyze specific meeting from URL
    meeting_url = "https://app.granola.so/meeting/abc123def456"
    result = granola.analyze_granola_url(meeting_url)
    
    # Pattern 2: Get all meetings for a customer
    customer_meetings = granola.fetch_data(
        'acme-corp', 
        customer_name='ACME Corp',
        days_back=30
    )
    processed = granola.process_data(customer_meetings)
    
    # Pattern 3: Get my recent meetings
    my_meetings = granola.fetch_my_recent_meetings(days_back=7)
    
    # Pattern 4: Update action item status
    granola.push_data({
        'action_id': '12345',
        'completed': True
    }, 'action_item_status')
    
    # Pattern 5: Generate meeting summary
    summary = granola.create_meeting_summary('abc123def456')