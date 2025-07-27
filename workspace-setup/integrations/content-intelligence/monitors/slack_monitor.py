#!/usr/bin/env python3
"""
Slack Monitor for Content Intelligence
Monitors specified Slack channels for insights to improve sales content
"""

import os
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class ContentInsight:
    """Represents an insight that could improve sales content"""
    source: str
    channel: str
    timestamp: datetime
    insight_type: str
    confidence: float
    content: str
    suggested_action: str
    affected_files: List[str]
    evidence: Dict[str, Any]

class SlackContentMonitor:
    """Monitors Slack for content improvement opportunities"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.insights = []
        
    def monitor_channels(self) -> List[ContentInsight]:
        """Monitor configured Slack channels for insights"""
        insights = []
        
        for channel_config in self.config['slack']['channels']:
            channel_insights = self._analyze_channel(channel_config)
            insights.extend(channel_insights)
        
        return insights
    
    def _analyze_channel(self, channel_config: Dict) -> List[ContentInsight]:
        """Analyze a specific channel for insights"""
        channel_name = channel_config['name']
        patterns = channel_config['patterns']
        
        # In production, this would fetch real messages
        # For now, we'll use example patterns
        
        insights = []
        
        if channel_name == 'sales-wins':
            insights.extend(self._analyze_wins_channel(channel_config))
        elif channel_name == 'competitive-intel':
            insights.extend(self._analyze_competitive_channel(channel_config))
        elif channel_name == 'lost-deals':
            insights.extend(self._analyze_losses_channel(channel_config))
        
        return insights
    
    def _analyze_wins_channel(self, config: Dict) -> List[ContentInsight]:
        """Analyze sales wins for successful patterns"""
        insights = []
        
        # Example: Detect winning email patterns
        winning_pattern = {
            'pattern': 'ROI-focused subject line',
            'occurrences': 5,
            'success_rate': 0.8,
            'examples': [
                "Reducing infrastructure costs by 40%",
                "Quick question about your AWS bill",
                "Found 30% cost savings for similar companies"
            ]
        }
        
        if winning_pattern['occurrences'] >= 3 and winning_pattern['success_rate'] > 0.7:
            insight = ContentInsight(
                source='slack',
                channel='#sales-wins',
                timestamp=datetime.now(),
                insight_type='winning_pattern',
                confidence=0.85,
                content=f"ROI-focused email subjects driving {winning_pattern['success_rate']*100:.0f}% success rate",
                suggested_action="Add ROI-focused subject line variants to email templates",
                affected_files=[
                    'sales-toolkit/templates/email_sequence_enterprise.md',
                    'sales-toolkit/templates/email_cold_outreach.md'
                ],
                evidence={
                    'examples': winning_pattern['examples'],
                    'success_metrics': {
                        'open_rate': '45%',
                        'response_rate': '18%',
                        'meetings_booked': 5
                    }
                }
            )
            insights.append(insight)
        
        return insights
    
    def _analyze_competitive_channel(self, config: Dict) -> List[ContentInsight]:
        """Analyze competitive intelligence"""
        insights = []
        
        # Example: New competitor feature detected
        competitor_intel = {
            'competitor': 'CompetitorX',
            'new_feature': 'Auto-scaling API',
            'mentions': 4,
            'lost_deals': 2
        }
        
        if competitor_intel['mentions'] >= 3:
            insight = ContentInsight(
                source='slack',
                channel='#competitive-intel',
                timestamp=datetime.now(),
                insight_type='competitor_update',
                confidence=0.9,
                content=f"{competitor_intel['competitor']} launched {competitor_intel['new_feature']}",
                suggested_action=f"Update battlecard with counter-positioning for {competitor_intel['new_feature']}",
                affected_files=[
                    f"sales-toolkit/battlecards/{competitor_intel['competitor'].lower()}_battlecard.md"
                ],
                evidence={
                    'feature_details': 'Auto-scaling API with 5-minute response time',
                    'our_advantage': 'Our auto-scaling responds in 30 seconds',
                    'suggested_talk_track': 'While they offer auto-scaling, our sub-minute response time means...'
                }
            )
            insights.append(insight)
        
        return insights
    
    def _analyze_losses_channel(self, config: Dict) -> List[ContentInsight]:
        """Analyze lost deals for improvement opportunities"""
        insights = []
        
        # Example: Recurring objection pattern
        objection_pattern = {
            'objection': 'Security concerns about data residency',
            'occurrences': 6,
            'lost_revenue': 450000
        }
        
        if objection_pattern['occurrences'] >= 5:
            insight = ContentInsight(
                source='slack',
                channel='#lost-deals',
                timestamp=datetime.now(),
                insight_type='recurring_objection',
                confidence=0.95,
                content=f"Security/data residency objection causing losses (${objection_pattern['lost_revenue']:,})",
                suggested_action="Create comprehensive security objection handling guide",
                affected_files=[
                    'sales-toolkit/templates/objection_handling_playbook.md',
                    'sales-toolkit/security-compliance/data_residency_guide.md'
                ],
                evidence={
                    'specific_concerns': [
                        'GDPR compliance for EU data',
                        'Data sovereignty requirements',
                        'Multi-region deployment options'
                    ],
                    'successful_responses': [
                        'We offer region-specific deployments',
                        'Full GDPR compliance with DPA',
                        'Customer-controlled encryption keys'
                    ]
                }
            )
            insights.append(insight)
        
        return insights
    
    def generate_suggestions(self, insights: List[ContentInsight]) -> List[Dict[str, Any]]:
        """Convert insights into actionable suggestions"""
        suggestions = []
        
        for insight in insights:
            suggestion = {
                'id': f"suggestion_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'created_at': datetime.now().isoformat(),
                'source': {
                    'platform': insight.source,
                    'channel': insight.channel
                },
                'type': insight.insight_type,
                'confidence': insight.confidence,
                'priority': self._calculate_priority(insight),
                'title': insight.content,
                'description': insight.suggested_action,
                'affected_content': insight.affected_files,
                'implementation': self._generate_implementation(insight),
                'expected_impact': self._estimate_impact(insight)
            }
            suggestions.append(suggestion)
        
        return suggestions
    
    def _calculate_priority(self, insight: ContentInsight) -> str:
        """Calculate priority based on confidence and impact"""
        if insight.confidence > 0.8:
            if 'lost_revenue' in insight.evidence:
                return 'critical'
            return 'high'
        elif insight.confidence > 0.6:
            return 'medium'
        return 'low'
    
    def _generate_implementation(self, insight: ContentInsight) -> Dict[str, Any]:
        """Generate specific implementation details"""
        if insight.insight_type == 'winning_pattern':
            return {
                'action': 'update',
                'changes': [
                    {
                        'file': insight.affected_files[0],
                        'section': 'Subject Lines',
                        'add': insight.evidence['examples']
                    }
                ]
            }
        elif insight.insight_type == 'competitor_update':
            return {
                'action': 'update',
                'changes': [
                    {
                        'file': insight.affected_files[0],
                        'section': 'Competitive Advantages',
                        'add': {
                            'their_feature': insight.evidence['feature_details'],
                            'our_response': insight.evidence['our_advantage'],
                            'talk_track': insight.evidence['suggested_talk_track']
                        }
                    }
                ]
            }
        elif insight.insight_type == 'recurring_objection':
            return {
                'action': 'create',
                'new_content': {
                    'title': 'Security & Data Residency Objection Handling',
                    'sections': {
                        'common_concerns': insight.evidence['specific_concerns'],
                        'proven_responses': insight.evidence['successful_responses'],
                        'supporting_materials': ['security whitepaper', 'compliance certs']
                    }
                }
            }
        return {}
    
    def _estimate_impact(self, insight: ContentInsight) -> Dict[str, Any]:
        """Estimate the potential impact of implementing the suggestion"""
        if insight.insight_type == 'winning_pattern':
            return {
                'metric': 'email_response_rate',
                'current': '10%',
                'projected': '18%',
                'revenue_impact': '+$200K/quarter'
            }
        elif insight.insight_type == 'competitor_update':
            return {
                'metric': 'competitive_win_rate',
                'current': '35%',
                'projected': '45%',
                'deals_impacted': '~5/quarter'
            }
        elif insight.insight_type == 'recurring_objection':
            return {
                'metric': 'objection_overcome_rate',
                'current': '20%',
                'projected': '60%',
                'revenue_recovery': f"${insight.evidence.get('lost_revenue', 0)*0.4:,.0f}"
            }
        return {}
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration"""
        if not config_path:
            config_path = 'config.json'
        
        with open(config_path, 'r') as f:
            return json.load(f)['data_sources']


def main():
    """Run the Slack content monitor"""
    monitor = SlackContentMonitor()
    
    # Gather insights
    insights = monitor.monitor_channels()
    
    # Generate suggestions
    suggestions = monitor.generate_suggestions(insights)
    
    # Output suggestions
    print(f"\n🔍 Content Intelligence Report")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Found {len(suggestions)} improvement suggestions\n")
    
    for suggestion in suggestions:
        print(f"{'='*60}")
        print(f"📌 {suggestion['title']}")
        print(f"Priority: {suggestion['priority'].upper()}")
        print(f"Confidence: {suggestion['confidence']*100:.0f}%")
        print(f"\nAction: {suggestion['description']}")
        print(f"Files to update: {', '.join(suggestion['affected_content'])}")
        print(f"\nExpected Impact:")
        impact = suggestion['expected_impact']
        print(f"  {impact['metric']}: {impact['current']} → {impact['projected']}")
        if 'revenue_impact' in impact:
            print(f"  Revenue Impact: {impact['revenue_impact']}")
        print()


if __name__ == "__main__":
    main()