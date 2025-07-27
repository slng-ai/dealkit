"""
Keyword-based triggers for sales automation
"""

import re
from typing import Dict, Any, List
from .base_trigger import BaseTrigger, TriggerResult, TriggerCondition


class KeywordTrigger(BaseTrigger):
    """Base class for keyword-based triggers"""
    
    def __init__(self,
                 trigger_id: str,
                 name: str,
                 description: str,
                 priority: str,
                 keywords: List[str],
                 patterns: List[str] = None,
                 context_window: int = 50,
                 enabled: bool = True):
        super().__init__(trigger_id, name, description, priority, enabled)
        self.keywords = [k.lower() for k in keywords]
        self.patterns = patterns or []
        self.context_window = context_window
    
    def evaluate(self, data: Dict[str, Any]) -> TriggerResult:
        """Evaluate keyword trigger conditions"""
        matched_conditions = []
        suggested_actions = []
        context = {}
        
        text = data.get("text", "").lower()
        subject = data.get("subject", "").lower()
        
        # Check keywords in text
        matched_keywords = []
        for keyword in self.keywords:
            if keyword in text or keyword in subject:
                matched_keywords.append(keyword)
                matched_conditions.append(f"keyword_match_{keyword}")
        
        # Check regex patterns
        matched_patterns = []
        for pattern in self.patterns:
            if re.search(pattern, text, re.IGNORECASE) or re.search(pattern, subject, re.IGNORECASE):
                matched_patterns.append(pattern)
                matched_conditions.append(f"pattern_match")
        
        if matched_keywords or matched_patterns:
            context["matched_keywords"] = matched_keywords
            context["matched_patterns"] = matched_patterns
            context["text_snippet"] = self._extract_context(text, matched_keywords + matched_patterns)
        
        triggered = len(matched_conditions) > 0
        confidence = self.calculate_confidence(matched_conditions, len(self.keywords) + len(self.patterns))
        
        return TriggerResult(
            triggered=triggered,
            confidence=confidence,
            matched_conditions=matched_conditions,
            suggested_actions=suggested_actions,
            context=context
        )
    
    def _extract_context(self, text: str, matches: List[str]) -> str:
        """Extract context around matched keywords/patterns"""
        if not matches:
            return ""
        
        # Find the first match
        first_match_pos = len(text)
        for match in matches:
            pos = text.lower().find(match.lower())
            if pos != -1 and pos < first_match_pos:
                first_match_pos = pos
        
        # Extract context window
        start = max(0, first_match_pos - self.context_window)
        end = min(len(text), first_match_pos + self.context_window)
        
        return text[start:end].strip()
    
    def get_conditions(self) -> Dict[str, Any]:
        """Get trigger conditions"""
        return {
            "keywords": self.keywords,
            "patterns": self.patterns,
            "context_window": self.context_window
        }


class BuyingSignalTrigger(KeywordTrigger):
    """Trigger for detecting buying signals"""
    
    def __init__(self,
                 trigger_id: str = "buying_signals",
                 name: str = "Buying Signal Detection",
                 description: str = "Detects when prospects show buying intent",
                 priority: str = "high",
                 enabled: bool = True):
        
        buying_keywords = [
            "budget approved",
            "looking for a solution",
            "need something by",
            "ready to purchase",
            "when can we start",
            "what would it take",
            "can acme handle",
            "timeline for implementation",
            "contract terms",
            "pricing proposal",
            "next steps",
            "decision by",
            "approve this",
            "move forward",
            "sign up",
            "get started"
        ]
        
        buying_patterns = [
            r"budget\s+of\s+\$?\d+",
            r"need\s+this\s+by\s+\w+",
            r"timeline\s+is\s+\w+",
            r"decision\s+maker\s+is",
            r"ready\s+to\s+(sign|commit|proceed)",
            r"what\s+(would|will)\s+it\s+take",
            r"can\s+you\s+(deliver|provide|support)",
            r"(urgent|asap|immediately)\s+need"
        ]
        
        super().__init__(
            trigger_id=trigger_id,
            name=name,
            description=description,
            priority=priority,
            keywords=buying_keywords,
            patterns=buying_patterns,
            enabled=enabled
        )
    
    def evaluate(self, data: Dict[str, Any]) -> TriggerResult:
        """Evaluate buying signal trigger conditions"""
        result = super().evaluate(data)
        
        if result.triggered:
            # Add buying signal specific actions
            result.suggested_actions.extend([
                "notify_ae_immediately",
                "schedule_demo",
                "prepare_proposal",
                "update_opportunity_stage"
            ])
            
            # Boost confidence for strong buying signals
            strong_signals = ["budget approved", "ready to purchase", "sign up", "get started"]
            for signal in strong_signals:
                if signal in result.context.get("matched_keywords", []):
                    result.confidence = min(result.confidence + 0.2, 1.0)
        
        return result


class ChurnRiskTrigger(KeywordTrigger):
    """Trigger for detecting churn risk signals"""
    
    def __init__(self,
                 trigger_id: str = "churn_risk",
                 name: str = "Churn Risk Detection",
                 description: str = "Detects when customers show signs of leaving",
                 priority: str = "critical",
                 enabled: bool = True):
        
        churn_keywords = [
            "cancel",
            "terminate",
            "disappointed",
            "frustrated",
            "switching",
            "alternative",
            "competitor",
            "not meeting needs",
            "considering options",
            "poor performance",
            "unreliable",
            "expensive",
            "cheaper option",
            "end contract",
            "not renewing",
            "unsatisfied",
            "problems with",
            "issues with",
            "complaints about"
        ]
        
        churn_patterns = [
            r"considering\s+(other\s+)?alternatives",
            r"not\s+meeting\s+.*\s+needs",
            r"shopping\s+around",
            r"price\s+is\s+too\s+high",
            r"found\s+(a\s+)?cheaper",
            r"having\s+issues\s+with",
            r"problems\s+with\s+.*\s+(service|platform|support)",
            r"thinking\s+about\s+(leaving|switching)",
            r"(downtime|outage)\s+issues"
        ]
        
        super().__init__(
            trigger_id=trigger_id,
            name=name,
            description=description,
            priority=priority,
            keywords=churn_keywords,
            patterns=churn_patterns,
            enabled=enabled
        )
    
    def evaluate(self, data: Dict[str, Any]) -> TriggerResult:
        """Evaluate churn risk trigger conditions"""
        result = super().evaluate(data)
        
        if result.triggered:
            # Add churn risk specific actions
            result.suggested_actions.extend([
                "immediate_escalation",
                "notify_csm",
                "schedule_emergency_call",
                "prepare_retention_offer",
                "alert_management"
            ])
            
            # Critical churn signals get maximum confidence
            critical_signals = ["cancel", "terminate", "switching", "not renewing"]
            for signal in critical_signals:
                if signal in result.context.get("matched_keywords", []):
                    result.confidence = 1.0
                    result.priority = "critical"
        
        return result


class CompetitiveTrigger(KeywordTrigger):
    """Trigger for detecting competitive mentions"""
    
    def __init__(self,
                 trigger_id: str = "competitive_mention",
                 name: str = "Competitive Mention Detection",
                 description: str = "Detects when competitors are mentioned",
                 priority: str = "high",
                 enabled: bool = True):
        
        competitor_keywords = [
            "vercel",
            "netlify",
            "aws amplify",
            "cloudflare pages",
            "github pages",
            "heroku",
            "firebase hosting",
            "azure static web apps"
        ]
        
        competitive_patterns = [
            r"comparing\s+with\s+\w+",
            r"vs\.?\s+\w+",
            r"better\s+than\s+\w+",
            r"cheaper\s+than\s+\w+",
            r"(competitor|alternative)\s+offers",
            r"their\s+platform\s+(has|offers|provides)"
        ]
        
        super().__init__(
            trigger_id=trigger_id,
            name=name,
            description=description,
            priority=priority,
            keywords=competitor_keywords,
            patterns=competitive_patterns,
            enabled=enabled
        )
    
    def evaluate(self, data: Dict[str, Any]) -> TriggerResult:
        """Evaluate competitive trigger conditions"""
        result = super().evaluate(data)
        
        if result.triggered:
            # Add competitive specific actions
            result.suggested_actions.extend([
                "notify_competitive_team",
                "prepare_battlecard",
                "schedule_competitive_demo",
                "gather_competitive_intel"
            ])
            
            # Identify specific competitor mentioned
            for keyword in result.context.get("matched_keywords", []):
                if keyword in self.keywords:
                    result.context["competitor"] = keyword
                    result.suggested_actions.append(f"load_{keyword}_battlecard")
        
        return result


class SecurityComplianceTrigger(KeywordTrigger):
    """Trigger for security and compliance inquiries"""
    
    def __init__(self,
                 trigger_id: str = "security_compliance",
                 name: str = "Security/Compliance Inquiry",
                 description: str = "Detects security and compliance questions",
                 priority: str = "high",
                 enabled: bool = True):
        
        security_keywords = [
            "security",
            "compliance",
            "hipaa",
            "gdpr",
            "soc2",
            "penetration test",
            "vulnerability",
            "encryption",
            "data protection",
            "privacy policy",
            "audit",
            "certification",
            "iso 27001",
            "pci dss",
            "data residency",
            "access control",
            "authentication",
            "authorization"
        ]
        
        security_patterns = [
            r"security\s+(audit|assessment|review)",
            r"compliance\s+with\s+\w+",
            r"data\s+(protection|privacy|security)",
            r"(penetration|pen)\s+test",
            r"vulnerability\s+(scan|assessment)",
            r"security\s+(controls|measures)",
            r"(encrypt|decrypt)\w*",
            r"access\s+(control|management)"
        ]
        
        super().__init__(
            trigger_id=trigger_id,
            name=name,
            description=description,
            priority=priority,
            keywords=security_keywords,
            patterns=security_patterns,
            enabled=enabled
        )
    
    def evaluate(self, data: Dict[str, Any]) -> TriggerResult:
        """Evaluate security/compliance trigger conditions"""
        result = super().evaluate(data)
        
        if result.triggered:
            # Add security/compliance specific actions
            result.suggested_actions.extend([
                "notify_security_team",
                "prepare_compliance_docs",
                "schedule_security_review",
                "provide_certifications"
            ])
            
            # Healthcare compliance gets special handling
            healthcare_terms = ["hipaa", "baa", "phi", "healthcare"]
            for term in healthcare_terms:
                if term in result.context.get("matched_keywords", []):
                    result.suggested_actions.append("prepare_hipaa_materials")
                    result.context["compliance_type"] = "healthcare"
        
        return result