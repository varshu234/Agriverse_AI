from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
from backend.services.recommendation_engine import RecommendationEngine
from backend.services.analysis_service import AnalysisService
from backend.services.skill_gap_analyzer import SkillGapAnalyzer
from backend.models.user_profile import UserProfile

app = Flask(__name__)
CORS(app)

# Initialize services
recommendation_engine = RecommendationEngine()
analysis_service = AnalysisService()
skill_analyzer = SkillGapAnalyzer()

@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')

@app.route('/profile')
def profile():
    """User profile setup page"""
    return render_template('profile.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/profile', methods=['POST'])
def create_profile():
    """Create or update user profile"""
    try:
        data = request.get_json()
        profile = UserProfile(
            budget=data.get('budget'),
            risk_level=data.get('risk_level'),
            interests=data.get('interests', []),
            investment_horizon=data.get('investment_horizon', 'medium')
        )
        
        # Generate recommendations
        recommendations = recommendation_engine.get_recommendations(profile)
        
        return jsonify({
            'success': True,
            'profile': profile.to_dict(),
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/analyze/<int:recommendation_id>', methods=['POST'])
def analyze_recommendation(recommendation_id):
    """Analyze a specific recommendation"""
    try:
        data = request.get_json()
        profile_data = data.get('profile')
        investment_amount = data.get('investment_amount')
        
        profile = UserProfile(**profile_data)
        analysis = analysis_service.analyze_opportunity(
            recommendation_id, profile, investment_amount
        )
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/simulate', methods=['POST'])
def simulate_investment():
    """Run investment simulation"""
    try:
        data = request.get_json()
        profile_data = data.get('profile')
        recommendation_id = data.get('recommendation_id')
        scenarios = data.get('scenarios', ['conservative', 'moderate', 'optimistic'])
        
        profile = UserProfile(**profile_data)
        simulation = analysis_service.run_simulation(
            recommendation_id, profile, scenarios
        )
        
        return jsonify({
            'success': True,
            'simulation': simulation
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# Skill Gap Analyzer API Routes
@app.route('/api/skill-quiz/questions')
def get_quiz_questions():
    """Get skill assessment quiz questions"""
    try:
        questions = skill_analyzer.get_quiz_questions()
        return jsonify({
            'success': True,
            'questions': questions
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/skill-quiz/evaluate', methods=['POST'])
def evaluate_quiz():
    """Evaluate quiz answers and provide recommendations"""
    try:
        data = request.get_json()
        answers = data.get('answers', [])
        
        if not answers or len(answers) != 3:
            return jsonify({'success': False, 'error': 'Please answer all 3 questions'}), 400
        
        assessment = skill_analyzer.get_user_assessment_summary(answers)
        
        return jsonify({
            'success': True,
            'assessment': assessment
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/skill-path/<skill_level>')
def get_learning_path(skill_level):
    """Get learning path for a specific skill level"""
    try:
        from backend.services.skill_gap_analyzer import SkillLevel
        
        # Convert string to enum
        try:
            level_enum = SkillLevel(skill_level.lower())
        except ValueError:
            return jsonify({'success': False, 'error': 'Invalid skill level'}), 400
        
        learning_path = skill_analyzer.get_learning_path(level_enum)
        
        return jsonify({
            'success': True,
            'skill_level': skill_level,
            'learning_path': learning_path
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
