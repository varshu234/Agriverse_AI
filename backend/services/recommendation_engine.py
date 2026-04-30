import random
import numpy as np
from typing import List, Dict, Any
from backend.models.user_profile import UserProfile

class RecommendationEngine:
    def __init__(self):
        self.opportunities = self._load_opportunities()
    
    def _load_opportunities(self) -> List[Dict[str, Any]]:
        """Load agriculture investment opportunities"""
        return [
            {
                'id': 1,
                'title': 'Precision Farming Technology',
                'category': 'agri-tech',
                'description': 'Invest in IoT sensors and AI-driven crop monitoring systems that optimize water usage and increase yield by up to 30%.',
                'min_investment': 830000,
                'max_investment': 41500000,
                'risk_level': 'medium',
                'expected_return': 0.15,
                'sustainability_score': 0.85,
                'time_horizon': 'medium',
                'tags': ['technology', 'iot', 'ai', 'sustainability'],
                'market_size': '₹996 billion',
                'growth_rate': '22% annually'
            },
            {
                'id': 2,
                'title': 'Organic Vertical Farming',
                'category': 'farming',
                'description': 'Urban vertical farming using hydroponics to grow organic vegetables year-round with 90% less water usage.',
                'min_investment': 2075000,
                'max_investment': 83000000,
                'risk_level': 'low',
                'expected_return': 0.12,
                'sustainability_score': 0.95,
                'time_horizon': 'long',
                'tags': ['organic', 'urban', 'hydroponics', 'sustainability'],
                'market_size': '₹664 billion',
                'growth_rate': '25% annually'
            },
            {
                'id': 3,
                'title': 'Agricultural Supply Chain Platform',
                'category': 'supply-chain',
                'description': 'Blockchain-based platform connecting farmers directly with buyers, reducing middlemen costs by 40%.',
                'min_investment': 1245000,
                'max_investment': 24900000,
                'risk_level': 'high',
                'expected_return': 0.25,
                'sustainability_score': 0.75,
                'time_horizon': 'short',
                'tags': ['blockchain', 'platform', 'supply-chain', 'fintech'],
                'market_size': '₹1,245 billion',
                'growth_rate': '30% annually'
            },
            {
                'id': 4,
                'title': 'Sustainable Livestock Management',
                'category': 'farming',
                'description': 'Invest in regenerative grazing practices and methane reduction technology for sustainable meat production.',
                'min_investment': 4150000,
                'max_investment': 166000000,
                'risk_level': 'medium',
                'expected_return': 0.18,
                'sustainability_score': 0.80,
                'time_horizon': 'long',
                'tags': ['livestock', 'sustainability', 'regenerative'],
                'market_size': '₹1,660 billion',
                'growth_rate': '15% annually'
            },
            {
                'id': 5,
                'title': 'Agri-Tech Education Platform',
                'category': 'agri-tech',
                'description': 'Online learning platform teaching modern farming techniques and digital agriculture to farmers worldwide.',
                'min_investment': 664000,
                'max_investment': 12450000,
                'risk_level': 'low',
                'expected_return': 0.20,
                'sustainability_score': 0.90,
                'time_horizon': 'short',
                'tags': ['education', 'digital', 'platform', 'scalable'],
                'market_size': '₹415 billion',
                'growth_rate': '35% annually'
            },
            {
                'id': 6,
                'title': 'Cold Chain Logistics',
                'category': 'supply-chain',
                'description': 'Solar-powered cold storage facilities reducing food waste by 60% in developing regions.',
                'min_investment': 6225000,
                'max_investment': 249000000,
                'risk_level': 'medium',
                'expected_return': 0.14,
                'sustainability_score': 0.88,
                'time_horizon': 'medium',
                'tags': ['logistics', 'renewable-energy', 'infrastructure'],
                'market_size': '₹2,075 billion',
                'growth_rate': '18% annually'
            }
        ]
    
    def _calculate_match_score(self, opportunity: Dict[str, Any], profile: UserProfile) -> float:
        """Calculate how well an opportunity matches the user profile"""
        score = 0.0
        
        # Risk alignment (30% weight)
        risk_match = 0
        if opportunity['risk_level'] == profile.risk_level:
            risk_match = 1.0
        elif profile.risk_level == 'medium':
            risk_match = 0.7
        elif (profile.risk_level == 'low' and opportunity['risk_level'] == 'medium') or \
             (profile.risk_level == 'high' and opportunity['risk_level'] == 'medium'):
            risk_match = 0.5
        score += risk_match * 0.3
        
        # Budget alignment (25% weight)
        if profile.budget >= opportunity['min_investment']:
            budget_match = min(1.0, profile.budget / opportunity['max_investment'])
        else:
            budget_match = 0.0
        score += budget_match * 0.25
        
        # Interest alignment (25% weight)
        interest_match = 0
        for interest in profile.interests:
            if interest.lower() in [tag.lower() for tag in opportunity['tags']]:
                interest_match += 1
        interest_match = min(1.0, interest_match / max(1, len(profile.interests)))
        score += interest_match * 0.25
        
        # Time horizon alignment (20% weight)
        horizon_match = 1.0 if opportunity['time_horizon'] == profile.investment_horizon else 0.5
        score += horizon_match * 0.2
        
        return score
    
    def get_recommendations(self, profile: UserProfile, limit: int = 5) -> List[Dict[str, Any]]:
        """Get personalized recommendations based on user profile"""
        scored_opportunities = []
        
        for opportunity in self.opportunities:
            match_score = self._calculate_match_score(opportunity, profile)
            
            # Add some randomness for variety
            match_score += random.uniform(-0.05, 0.05)
            match_score = max(0, min(1, match_score))
            
            opportunity_copy = opportunity.copy()
            opportunity_copy['match_score'] = match_score
            scored_opportunities.append(opportunity_copy)
        
        # Sort by match score and return top recommendations
        scored_opportunities.sort(key=lambda x: x['match_score'], reverse=True)
        return scored_opportunities[:limit]
