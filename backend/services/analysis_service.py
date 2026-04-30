import numpy as np
import random
from typing import Dict, Any, List
from backend.models.user_profile import UserProfile
from backend.services.recommendation_engine import RecommendationEngine

class AnalysisService:
    def __init__(self):
        self.recommendation_engine = RecommendationEngine()
    
    def analyze_opportunity(self, recommendation_id: int, profile: UserProfile, investment_amount: float) -> Dict[str, Any]:
        """Analyze a specific investment opportunity"""
        opportunity = self._get_opportunity_by_id(recommendation_id)
        if not opportunity:
            raise ValueError(f"Opportunity with ID {recommendation_id} not found")
        
        # Calculate investment metrics
        investment_ratio = investment_amount / opportunity['max_investment']
        
        # Profit analysis
        profit_analysis = self._calculate_profit_analysis(opportunity, investment_amount, investment_ratio)
        
        # Risk analysis
        risk_analysis = self._calculate_risk_analysis(opportunity, profile, investment_ratio)
        
        # Sustainability analysis
        sustainability_analysis = self._calculate_sustainability_analysis(opportunity, investment_amount)
        
        # Generate insights
        insights = self._generate_insights(opportunity, profile, profit_analysis, risk_analysis, sustainability_analysis)
        
        return {
            'opportunity': opportunity,
            'investment_amount': investment_amount,
            'profit_analysis': profit_analysis,
            'risk_analysis': risk_analysis,
            'sustainability_analysis': sustainability_analysis,
            'insights': insights,
            'recommendation_score': self._calculate_overall_score(profit_analysis, risk_analysis, sustainability_analysis)
        }
    
    def run_simulation(self, recommendation_id: int, profile: UserProfile, scenarios: List[str]) -> Dict[str, Any]:
        """Run investment simulation for different scenarios"""
        opportunity = self._get_opportunity_by_id(recommendation_id)
        if not opportunity:
            raise ValueError(f"Opportunity with ID {recommendation_id} not found")
        
        simulation_results = {}
        
        for scenario in scenarios:
            scenario_params = self._get_scenario_parameters(scenario)
            results = self._simulate_scenario(opportunity, profile, scenario_params)
            simulation_results[scenario] = results
        
        return {
            'opportunity': opportunity,
            'scenarios': simulation_results,
            'comparison': self._compare_scenarios(simulation_results)
        }
    
    def _get_opportunity_by_id(self, recommendation_id: int) -> Dict[str, Any]:
        """Get opportunity by ID"""
        for opportunity in self.recommendation_engine.opportunities:
            if opportunity['id'] == recommendation_id:
                return opportunity
        return None
    
    def _calculate_profit_analysis(self, opportunity: Dict[str, Any], investment_amount: float, investment_ratio: float) -> Dict[str, Any]:
        """Calculate profit-related metrics"""
        base_return = opportunity['expected_return']
        
        # Adjust returns based on investment size (economies of scale)
        scale_bonus = min(0.05, investment_ratio * 0.1)
        adjusted_return = base_return + scale_bonus
        
        # Calculate projections
        annual_return = investment_amount * adjusted_return
        monthly_return = annual_return / 12
        
        # 5-year projection with compound growth
        years = 5
        projections = []
        cumulative_investment = investment_amount
        
        for year in range(1, years + 1):
            year_return = cumulative_investment * adjusted_return
            cumulative_investment += year_return
            projections.append({
                'year': year,
                'investment': cumulative_investment,
                'annual_return': year_return,
                'total_return': cumulative_investment - investment_amount
            })
        
        # Break-even analysis
        monthly_profit = monthly_return
        break_even_months = 0
        
        return {
            'expected_annual_return': adjusted_return,
            'annual_return_amount': annual_return,
            'monthly_return': monthly_return,
            'projections': projections,
            'roi_percentage': adjusted_return * 100,
            'payback_period_months': int(12 / adjusted_return) if adjusted_return > 0 else 999
        }
    
    def _calculate_risk_analysis(self, opportunity: Dict[str, Any], profile: UserProfile, investment_ratio: float) -> Dict[str, Any]:
        """Calculate risk-related metrics"""
        base_risk = self._risk_level_to_score(opportunity['risk_level'])
        
        # Adjust risk based on user profile
        risk_tolerance = self._risk_level_to_score(profile.risk_level)
        risk_adjustment = (risk_tolerance - base_risk) * 0.3
        adjusted_risk = base_risk + risk_adjustment
        
        # Risk factors
        risk_factors = [
            {'factor': 'Market Volatility', 'score': random.uniform(0.2, 0.8), 'weight': 0.3},
            {'factor': 'Regulatory Risk', 'score': random.uniform(0.1, 0.6), 'weight': 0.2},
            {'factor': 'Technology Risk', 'score': random.uniform(0.1, 0.7), 'weight': 0.2},
            {'factor': 'Competition Risk', 'score': random.uniform(0.2, 0.6), 'weight': 0.15},
            {'factor': 'Execution Risk', 'score': random.uniform(0.1, 0.5), 'weight': 0.15}
        ]
        
        # Calculate weighted risk score
        weighted_risk = sum(r['score'] * r['weight'] for r in risk_factors)
        
        # Risk mitigation strategies
        mitigation_strategies = self._get_risk_mitigation_strategies(opportunity, weighted_risk)
        
        return {
            'overall_risk_score': min(1.0, weighted_risk),
            'risk_level': self._score_to_risk_level(weighted_risk),
            'risk_factors': risk_factors,
            'mitigation_strategies': mitigation_strategies,
            'risk_adjusted_return': opportunity['expected_return'] * (1 - weighted_risk * 0.3)
        }
    
    def _calculate_sustainability_analysis(self, opportunity: Dict[str, Any], investment_amount: float) -> Dict[str, Any]:
        """Calculate sustainability-related metrics"""
        base_sustainability = opportunity['sustainability_score']
        
        # Environmental impact metrics
        environmental_impact = {
            'carbon_reduction': random.uniform(10, 50) * (investment_amount / 100000),  # tons CO2/year
            'water_savings': random.uniform(1000, 10000) * (investment_amount / 100000),  # gallons/year
            'land_efficiency': random.uniform(0.5, 2.0) * (investment_amount / 100000),  # acres equivalent
            'biodiversity_score': random.uniform(0.6, 0.95)
        }
        
        # Social impact metrics
        social_impact = {
            'jobs_created': int(random.uniform(1, 10) * (investment_amount / 100000)),
            'community_benefits': random.uniform(0.5, 0.9),
            'food_security_impact': random.uniform(0.6, 0.95),
            'education_value': random.uniform(0.3, 0.8)
        }
        
        # Economic sustainability
        economic_sustainability = {
            'local_economy_impact': random.uniform(0.6, 0.9),
            'supply_chain_resilience': random.uniform(0.7, 0.95),
            'innovation_contribution': random.uniform(0.5, 0.85)
        }
        
        # Overall sustainability score
        env_weight = 0.4
        social_weight = 0.3
        econ_weight = 0.3
        
        env_score = np.mean(list(environmental_impact.values())[:-1]) / 50  # Normalize
        social_score = np.mean(list(social_impact.values()))
        econ_score = np.mean(list(economic_sustainability.values()))
        
        overall_sustainability = (env_score * env_weight + social_score * social_weight + econ_score * econ_weight)
        
        return {
            'overall_score': min(1.0, overall_sustainability),
            'environmental_impact': environmental_impact,
            'social_impact': social_impact,
            'economic_sustainability': economic_sustainability,
            'sustainability_rating': self._get_sustainability_rating(overall_sustainability)
        }
    
    def _generate_insights(self, opportunity: Dict[str, Any], profile: UserProfile, profit_analysis: Dict, risk_analysis: Dict, sustainability_analysis: Dict) -> List[str]:
        """Generate personalized insights"""
        insights = []
        
        # Profit insights
        if profit_analysis['roi_percentage'] > 15:
            insights.append("This opportunity offers above-average returns compared to traditional agriculture investments.")
        
        # Risk insights
        if risk_analysis['overall_risk_score'] < 0.4:
            insights.append("Lower risk profile makes this suitable for conservative investors.")
        elif risk_analysis['overall_risk_score'] > 0.7:
            insights.append("Higher risk potential requires careful monitoring and diversification.")
        
        # Sustainability insights
        if sustainability_analysis['overall_score'] > 0.8:
            insights.append("Excellent sustainability credentials align with ESG investment goals.")
        
        # Profile-specific insights
        if profile.risk_level == 'low' and opportunity['risk_level'] == 'medium':
            insights.append("Consider starting with minimum investment to test this opportunity.")
        
        if 'sustainability' in profile.interests and sustainability_analysis['overall_score'] > 0.7:
            insights.append("Strong environmental and social impact matches your sustainability interests.")
        
        return insights
    
    def _calculate_overall_score(self, profit_analysis: Dict, risk_analysis: Dict, sustainability_analysis: Dict) -> float:
        """Calculate overall recommendation score"""
        profit_score = min(1.0, profit_analysis['roi_percentage'] / 25)
        risk_score = 1 - risk_analysis['overall_risk_score']
        sustainability_score = sustainability_analysis['overall_score']
        
        # Weighted average
        return (profit_score * 0.4 + risk_score * 0.3 + sustainability_score * 0.3)
    
    def _get_scenario_parameters(self, scenario: str) -> Dict[str, float]:
        """Get parameters for different scenarios"""
        scenarios = {
            'conservative': {'return_multiplier': 0.7, 'risk_multiplier': 1.2, 'volatility': 0.15},
            'moderate': {'return_multiplier': 1.0, 'risk_multiplier': 1.0, 'volatility': 0.25},
            'optimistic': {'return_multiplier': 1.5, 'risk_multiplier': 0.8, 'volatility': 0.35}
        }
        return scenarios.get(scenario, scenarios['moderate'])
    
    def _simulate_scenario(self, opportunity: Dict[str, Any], profile: UserProfile, params: Dict[str, float]) -> Dict[str, Any]:
        """Simulate investment scenario over time"""
        base_return = opportunity['expected_return'] * params['return_multiplier']
        volatility = params['volatility']
        
        # Monte Carlo simulation
        simulations = 1000
        time_horizon = 60  # months
        
        all_paths = []
        for _ in range(simulations):
            path = []
            current_value = profile.budget
            
            for month in range(time_horizon):
                monthly_return = base_return / 12
                random_factor = np.random.normal(1, volatility / 12)
                current_value *= (1 + monthly_return / 12) * random_factor
                path.append(current_value)
            
            all_paths.append(path)
        
        # Calculate statistics
        final_values = [path[-1] for path in all_paths]
        percentiles = np.percentile(final_values, [10, 25, 50, 75, 90])
        
        return {
            'scenario': params,
            'final_values': {
                'p10': percentiles[0],
                'p25': percentiles[1],
                'p50': percentiles[2],
                'p75': percentiles[3],
                'p90': percentiles[4]
            },
            'expected_final_value': np.mean(final_values),
            'probability_of_loss': np.mean([1 for v in final_values if v < profile.budget]) / simulations
        }
    
    def _compare_scenarios(self, simulation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Compare different scenarios"""
        comparison = {}
        
        for scenario_name, results in simulation_results.items():
            comparison[scenario_name] = {
                'expected_return': results['expected_final_value'],
                'risk_level': results['probability_of_loss'],
                'upside_potential': results['final_values']['p90'],
                'downside_protection': results['final_values']['p10']
            }
        
        return comparison
    
    def _risk_level_to_score(self, risk_level: str) -> float:
        """Convert risk level to numeric score"""
        mapping = {'low': 0.2, 'medium': 0.5, 'high': 0.8}
        return mapping.get(risk_level, 0.5)
    
    def _score_to_risk_level(self, score: float) -> str:
        """Convert numeric score to risk level"""
        if score < 0.4:
            return 'low'
        elif score < 0.7:
            return 'medium'
        else:
            return 'high'
    
    def _get_risk_mitigation_strategies(self, opportunity: Dict[str, Any], risk_score: float) -> List[str]:
        """Get risk mitigation strategies"""
        strategies = []
        
        if risk_score > 0.6:
            strategies.append("Consider phased investment approach")
            strategies.append("Diversify across multiple agriculture sectors")
        
        if opportunity['category'] == 'agri-tech':
            strategies.append("Start with pilot project before full investment")
        
        if opportunity['category'] == 'farming':
            strategies.append("Secure insurance coverage for crop failures")
            strategies.append("Establish contracts with buyers before planting")
        
        strategies.append("Regular monitoring of market conditions")
        strategies.append("Maintain emergency reserve fund")
        
        return strategies
    
    def _get_sustainability_rating(self, score: float) -> str:
        """Get sustainability rating"""
        if score > 0.8:
            return 'Excellent'
        elif score > 0.6:
            return 'Good'
        elif score > 0.4:
            return 'Moderate'
        else:
            return 'Needs Improvement'
