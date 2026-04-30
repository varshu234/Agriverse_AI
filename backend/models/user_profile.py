from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class UserProfile:
    budget: float
    risk_level: str  # 'low', 'medium', 'high'
    interests: List[str]
    investment_horizon: str = 'medium'  # 'short', 'medium', 'long'
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'budget': self.budget,
            'risk_level': self.risk_level,
            'interests': self.interests,
            'investment_horizon': self.investment_horizon
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfile':
        return cls(
            budget=data.get('budget', 0),
            risk_level=data.get('risk_level', 'medium'),
            interests=data.get('interests', []),
            investment_horizon=data.get('investment_horizon', 'medium')
        )
