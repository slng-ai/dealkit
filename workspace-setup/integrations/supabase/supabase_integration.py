"""
Supabase Integration for Customer Data

Pulls customer-specific data from Supabase database using customer ID.
Provides unified access to customer information stored in Supabase.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import sys
sys.path.append('..')
from base_integration import BaseIntegration

try:
    from supabase import create_client, Client
except ImportError:
    print("supabase package not installed. Run: pip install supabase")
    sys.exit(1)


class SupabaseIntegration(BaseIntegration):
    """Integration for pulling customer data from Supabase database."""
    
    def __init__(self, config_path: str = "../config/supabase_config.json"):
        super().__init__(config_path)
        self.client = self._setup_supabase_client()
        
    def _setup_supabase_client(self) -> Client:
        """Initialize Supabase client with credentials."""
        try:
            supabase_url = self.config.get('url')
            supabase_key = self.config.get('service_role_key')
            
            if not supabase_url or not supabase_key:
                raise ValueError("Missing Supabase URL or service role key in config")
                
            return create_client(supabase_url, supabase_key)
            
        except Exception as e:
            self.logger.error(f"Failed to setup Supabase client: {e}")
            raise

    def fetch_customer_data(self, customer_id: str) -> Dict[str, Any]:
        """
        Fetch comprehensive customer data by customer ID.
        
        Args:
            customer_id: Unique identifier for the customer
            
        Returns:
            Dictionary containing all customer data
        """
        try:
            self.logger.info(f"Fetching data for customer: {customer_id}")
            
            # Get main customer record
            customer_profile = self._get_customer_profile(customer_id)
            
            # Get related data
            customer_data = {
                'profile': customer_profile,
                'usage_metrics': self._get_usage_metrics(customer_id),
                'billing_info': self._get_billing_information(customer_id),
                'support_tickets': self._get_support_tickets(customer_id),
                'feature_usage': self._get_feature_usage(customer_id),
                'api_usage': self._get_api_usage(customer_id),
                'user_activity': self._get_user_activity(customer_id),
                'subscription_details': self._get_subscription_details(customer_id)
            }
            
            # Cache the result
            self._cache_data(f"customer_{customer_id}", customer_data)
            
            return customer_data
            
        except Exception as e:
            self.logger.error(f"Error fetching customer data for {customer_id}: {e}")
            return {}

    def _get_customer_profile(self, customer_id: str) -> Dict[str, Any]:
        """Get basic customer profile information."""
        try:
            response = (self.client.table('customers')
                       .select('*')
                       .eq('id', customer_id)
                       .execute())
            
            if response.data:
                profile = response.data[0]
                return {
                    'customer_id': profile.get('id'),
                    'company_name': profile.get('company_name'),
                    'industry': profile.get('industry'),
                    'company_size': profile.get('company_size'),
                    'plan_type': profile.get('plan_type'),
                    'signup_date': profile.get('created_at'),
                    'last_login': profile.get('last_login'),
                    'status': profile.get('status'),
                    'primary_contact': profile.get('primary_contact'),
                    'account_manager': profile.get('account_manager')
                }
            return {}
            
        except Exception as e:
            self.logger.error(f"Error fetching customer profile for {customer_id}: {e}")
            return {}

    def _get_usage_metrics(self, customer_id: str, days: int = 30) -> Dict[str, Any]:
        """Get customer usage metrics for specified period."""
        try:
            start_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            response = (self.client.table('usage_metrics')
                       .select('*')
                       .eq('customer_id', customer_id)
                       .gte('date', start_date)
                       .order('date', desc=True)
                       .execute())
            
            if response.data:
                metrics = response.data
                
                # Calculate aggregated metrics
                total_api_calls = sum(m.get('api_calls', 0) for m in metrics)
                total_models_deployed = len(set(m.get('model_id') for m in metrics if m.get('model_id')))
                avg_response_time = sum(m.get('avg_response_time', 0) for m in metrics) / len(metrics)
                
                return {
                    'period_days': days,
                    'total_api_calls': total_api_calls,
                    'total_models_deployed': total_models_deployed,
                    'average_response_time': round(avg_response_time, 2),
                    'daily_metrics': metrics,
                    'peak_usage_day': max(metrics, key=lambda x: x.get('api_calls', 0)) if metrics else None
                }
                
            return {'period_days': days, 'no_data': True}
            
        except Exception as e:
            self.logger.error(f"Error fetching usage metrics for {customer_id}: {e}")
            return {}

    def _get_billing_information(self, customer_id: str) -> Dict[str, Any]:
        """Get customer billing and payment information."""
        try:
            # Get current billing info
            billing_response = (self.client.table('billing')
                               .select('*')
                               .eq('customer_id', customer_id)
                               .order('created_at', desc=True)
                               .limit(1)
                               .execute())
            
            # Get recent invoices
            invoices_response = (self.client.table('invoices')
                                .select('*')
                                .eq('customer_id', customer_id)
                                .order('invoice_date', desc=True)
                                .limit(12)
                                .execute())
            
            billing_info = billing_response.data[0] if billing_response.data else {}
            invoices = invoices_response.data if invoices_response.data else []
            
            return {
                'current_plan': billing_info.get('plan_name'),
                'monthly_spend': billing_info.get('current_monthly_spend'),
                'billing_cycle': billing_info.get('billing_cycle'),
                'payment_method': billing_info.get('payment_method'),
                'next_billing_date': billing_info.get('next_billing_date'),
                'credit_balance': billing_info.get('credit_balance', 0),
                'recent_invoices': invoices[:5],  # Last 5 invoices
                'total_invoices': len(invoices),
                'payment_status': billing_info.get('payment_status', 'unknown')
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching billing info for {customer_id}: {e}")
            return {}

    def _get_support_tickets(self, customer_id: str, days: int = 90) -> Dict[str, Any]:
        """Get customer support tickets and interaction history."""
        try:
            start_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            response = (self.client.table('support_tickets')
                       .select('*')
                       .eq('customer_id', customer_id)
                       .gte('created_at', start_date)
                       .order('created_at', desc=True)
                       .execute())
            
            tickets = response.data if response.data else []
            
            # Analyze ticket patterns
            open_tickets = [t for t in tickets if t.get('status') != 'closed']
            priority_breakdown = {}
            for ticket in tickets:
                priority = ticket.get('priority', 'normal')
                priority_breakdown[priority] = priority_breakdown.get(priority, 0) + 1
            
            return {
                'total_tickets': len(tickets),
                'open_tickets': len(open_tickets),
                'closed_tickets': len(tickets) - len(open_tickets),
                'priority_breakdown': priority_breakdown,
                'recent_tickets': tickets[:10],  # Last 10 tickets
                'avg_resolution_time': self._calculate_avg_resolution_time(tickets),
                'escalated_tickets': [t for t in tickets if t.get('escalated', False)]
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching support tickets for {customer_id}: {e}")
            return {}

    def _get_feature_usage(self, customer_id: str) -> Dict[str, Any]:
        """Get customer feature adoption and usage patterns."""
        try:
            response = (self.client.table('feature_usage')
                       .select('*')
                       .eq('customer_id', customer_id)
                       .order('last_used', desc=True)
                       .execute())
            
            features = response.data if response.data else []
            
            # Analyze feature adoption
            active_features = [f for f in features if f.get('last_used') and 
                             (datetime.now() - datetime.fromisoformat(f['last_used'].replace('Z', '+00:00'))).days <= 30]
            
            most_used_features = sorted(features, key=lambda x: x.get('usage_count', 0), reverse=True)[:5]
            
            return {
                'total_features_available': len(features),
                'active_features_30d': len(active_features),
                'feature_adoption_rate': round(len(active_features) / len(features) * 100, 1) if features else 0,
                'most_used_features': most_used_features,
                'unused_features': [f for f in features if not f.get('usage_count', 0)],
                'feature_details': features
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching feature usage for {customer_id}: {e}")
            return {}

    def _get_api_usage(self, customer_id: str, days: int = 30) -> Dict[str, Any]:
        """Get detailed API usage statistics."""
        try:
            start_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            response = (self.client.table('api_logs')
                       .select('endpoint, method, response_time, status_code, timestamp')
                       .eq('customer_id', customer_id)
                       .gte('timestamp', start_date)
                       .execute())
            
            api_calls = response.data if response.data else []
            
            if not api_calls:
                return {'period_days': days, 'no_data': True}
            
            # Analyze API patterns
            endpoint_usage = {}
            error_count = 0
            total_response_time = 0
            
            for call in api_calls:
                endpoint = call.get('endpoint', 'unknown')
                endpoint_usage[endpoint] = endpoint_usage.get(endpoint, 0) + 1
                
                if call.get('status_code', 200) >= 400:
                    error_count += 1
                    
                total_response_time += call.get('response_time', 0)
            
            return {
                'period_days': days,
                'total_api_calls': len(api_calls),
                'unique_endpoints': len(endpoint_usage),
                'error_rate': round(error_count / len(api_calls) * 100, 2),
                'avg_response_time': round(total_response_time / len(api_calls), 2),
                'top_endpoints': sorted(endpoint_usage.items(), key=lambda x: x[1], reverse=True)[:10],
                'calls_per_day': round(len(api_calls) / days, 1)
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching API usage for {customer_id}: {e}")
            return {}

    def _get_user_activity(self, customer_id: str, days: int = 30) -> Dict[str, Any]:
        """Get user activity and engagement metrics."""
        try:
            start_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            # Get user sessions
            sessions_response = (self.client.table('user_sessions')
                                .select('*')
                                .eq('customer_id', customer_id)
                                .gte('session_start', start_date)
                                .execute())
            
            # Get active users
            users_response = (self.client.table('customer_users')
                             .select('*')
                             .eq('customer_id', customer_id)
                             .execute())
            
            sessions = sessions_response.data if sessions_response.data else []
            users = users_response.data if users_response.data else []
            
            # Calculate engagement metrics
            active_users = set(s.get('user_id') for s in sessions)
            total_session_time = sum(s.get('duration_minutes', 0) for s in sessions)
            
            return {
                'period_days': days,
                'total_users': len(users),
                'active_users': len(active_users),
                'user_engagement_rate': round(len(active_users) / len(users) * 100, 1) if users else 0,
                'total_sessions': len(sessions),
                'avg_session_duration': round(total_session_time / len(sessions), 1) if sessions else 0,
                'sessions_per_day': round(len(sessions) / days, 1),
                'most_active_users': self._get_most_active_users(sessions)[:5]
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching user activity for {customer_id}: {e}")
            return {}

    def _get_subscription_details(self, customer_id: str) -> Dict[str, Any]:
        """Get subscription and contract information."""
        try:
            response = (self.client.table('subscriptions')
                       .select('*')
                       .eq('customer_id', customer_id)
                       .order('created_at', desc=True)
                       .execute())
            
            if response.data:
                subscription = response.data[0]  # Most recent subscription
                
                # Calculate days until renewal
                renewal_date = subscription.get('renewal_date')
                days_to_renewal = None
                if renewal_date:
                    renewal_dt = datetime.fromisoformat(renewal_date.replace('Z', '+00:00'))
                    days_to_renewal = (renewal_dt - datetime.now()).days
                
                return {
                    'subscription_id': subscription.get('id'),
                    'plan_name': subscription.get('plan_name'),
                    'subscription_status': subscription.get('status'),
                    'start_date': subscription.get('start_date'),
                    'renewal_date': renewal_date,
                    'days_to_renewal': days_to_renewal,
                    'auto_renewal': subscription.get('auto_renewal', False),
                    'contract_value': subscription.get('contract_value'),
                    'seat_count': subscription.get('seat_count'),
                    'usage_limits': subscription.get('usage_limits'),
                    'add_ons': subscription.get('add_ons', [])
                }
                
            return {'no_subscription': True}
            
        except Exception as e:
            self.logger.error(f"Error fetching subscription details for {customer_id}: {e}")
            return {}

    def _calculate_avg_resolution_time(self, tickets: List[Dict]) -> Optional[float]:
        """Calculate average ticket resolution time in hours."""
        resolved_tickets = [t for t in tickets if t.get('resolved_at') and t.get('created_at')]
        
        if not resolved_tickets:
            return None
            
        total_hours = 0
        for ticket in resolved_tickets:
            created = datetime.fromisoformat(ticket['created_at'].replace('Z', '+00:00'))
            resolved = datetime.fromisoformat(ticket['resolved_at'].replace('Z', '+00:00'))
            total_hours += (resolved - created).total_seconds() / 3600
            
        return round(total_hours / len(resolved_tickets), 1)

    def _get_most_active_users(self, sessions: List[Dict]) -> List[Dict]:
        """Get most active users by session count and duration."""
        user_activity = {}
        
        for session in sessions:
            user_id = session.get('user_id')
            if user_id:
                if user_id not in user_activity:
                    user_activity[user_id] = {'sessions': 0, 'total_duration': 0}
                
                user_activity[user_id]['sessions'] += 1
                user_activity[user_id]['total_duration'] += session.get('duration_minutes', 0)
        
        # Sort by total activity (sessions + duration)
        return sorted(
            [{'user_id': uid, **data} for uid, data in user_activity.items()],
            key=lambda x: x['sessions'] + (x['total_duration'] / 60),  # Sessions + hours
            reverse=True
        )

    def get_customer_health_score(self, customer_id: str) -> Dict[str, Any]:
        """
        Calculate comprehensive customer health score based on multiple factors.
        
        Returns:
            Dictionary with health score and contributing factors
        """
        try:
            customer_data = self.fetch_customer_data(customer_id)
            
            if not customer_data:
                return {'error': 'No customer data available'}
            
            health_factors = {}
            
            # Usage health (30% weight)
            usage = customer_data.get('usage_metrics', {})
            if usage and not usage.get('no_data'):
                usage_score = min(100, (usage.get('total_api_calls', 0) / 10000) * 100)
                health_factors['usage'] = {'score': usage_score, 'weight': 0.3}
            
            # Support health (20% weight) - inverse relationship with ticket count
            support = customer_data.get('support_tickets', {})
            open_tickets = support.get('open_tickets', 0)
            support_score = max(0, 100 - (open_tickets * 10))
            health_factors['support'] = {'score': support_score, 'weight': 0.2}
            
            # Feature adoption health (25% weight)
            features = customer_data.get('feature_usage', {})
            adoption_rate = features.get('feature_adoption_rate', 0)
            health_factors['feature_adoption'] = {'score': adoption_rate, 'weight': 0.25}
            
            # User engagement health (25% weight)
            activity = customer_data.get('user_activity', {})
            engagement_rate = activity.get('user_engagement_rate', 0)
            health_factors['user_engagement'] = {'score': engagement_rate, 'weight': 0.25}
            
            # Calculate weighted average
            total_score = sum(factor['score'] * factor['weight'] for factor in health_factors.values())
            
            # Determine health status
            if total_score >= 80:
                status = 'Excellent'
                color = 'green'
            elif total_score >= 60:
                status = 'Good'
                color = 'yellow'
            elif total_score >= 40:
                status = 'At Risk'
                color = 'orange'
            else:
                status = 'Critical'
                color = 'red'
            
            return {
                'customer_id': customer_id,
                'overall_score': round(total_score, 1),
                'status': status,
                'status_color': color,
                'factors': health_factors,
                'recommendations': self._get_health_recommendations(health_factors),
                'calculated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating health score for {customer_id}: {e}")
            return {'error': str(e)}

    def _get_health_recommendations(self, factors: Dict) -> List[str]:
        """Generate recommendations based on health factors."""
        recommendations = []
        
        for factor_name, data in factors.items():
            score = data['score']
            
            if factor_name == 'usage' and score < 50:
                recommendations.append("Increase platform usage through targeted training")
            elif factor_name == 'support' and score < 70:
                recommendations.append("Address open support tickets to improve satisfaction")
            elif factor_name == 'feature_adoption' and score < 60:
                recommendations.append("Drive feature adoption through demos and onboarding")
            elif factor_name == 'user_engagement' and score < 50:
                recommendations.append("Improve user engagement with regular check-ins")
        
        if not recommendations:
            recommendations.append("Customer health is strong - focus on expansion opportunities")
            
        return recommendations

    def get_recent_customer_changes(self, customer_id: str, days: int = 7) -> Dict[str, Any]:
        """Get summary of recent changes for a customer."""
        try:
            # This would query change logs or audit tables in a real implementation
            # For now, return recent activity summary
            customer_data = self.fetch_customer_data(customer_id)
            
            changes = {
                'period_days': days,
                'changes_detected': [],
                'summary': f"Customer activity summary for last {days} days"
            }
            
            # Check for significant changes in usage
            usage = customer_data.get('usage_metrics', {})
            if usage.get('total_api_calls', 0) > 0:
                changes['changes_detected'].append({
                    'type': 'usage_increase',
                    'description': f"API usage: {usage['total_api_calls']} calls",
                    'significance': 'medium'
                })
            
            return changes
            
        except Exception as e:
            self.logger.error(f"Error getting recent changes for {customer_id}: {e}")
            return {'error': str(e)}


def main():
    """Example usage of Supabase integration."""
    try:
        # Initialize integration
        supabase = SupabaseIntegration()
        
        # Example customer ID (replace with actual ID)
        customer_id = "customer_123"
        
        print(f"Fetching data for customer: {customer_id}")
        
        # Get comprehensive customer data
        customer_data = supabase.fetch_customer_data(customer_id)
        print(f"Customer Profile: {customer_data.get('profile', {}).get('company_name', 'Unknown')}")
        
        # Get health score
        health_score = supabase.get_customer_health_score(customer_id)
        print(f"Health Score: {health_score.get('overall_score', 'N/A')} ({health_score.get('status', 'Unknown')})")
        
        # Get recent changes
        recent_changes = supabase.get_recent_customer_changes(customer_id)
        print(f"Recent Changes: {len(recent_changes.get('changes_detected', []))} detected")
        
    except Exception as e:
        print(f"Error running Supabase integration: {e}")


if __name__ == "__main__":
    main()