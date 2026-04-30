"""
Skill Gap Analyzer Service for Agriverse AI
Provides personalized learning paths based on agriculture knowledge assessment
"""

from typing import Dict, List, Tuple, Any
from enum import Enum

class SkillLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class SkillGapAnalyzer:
    """Analyzes user agriculture knowledge and provides personalized learning paths"""
    
    def __init__(self):
        self.quiz_questions = self._initialize_quiz_questions()
        self.learning_modules = self._initialize_learning_modules()
    
    def _initialize_quiz_questions(self) -> List[Dict[str, Any]]:
        """Initialize the 3-question agriculture knowledge quiz"""
        return [
            {
                "id": 1,
                "question": "What is the ideal pH range for most agricultural crops?",
                "topic": "soil",
                "options": [
                    {"text": "4.0 - 5.5 (Acidic)", "correct": False},
                    {"text": "6.0 - 7.0 (Slightly acidic to neutral)", "correct": True},
                    {"text": "7.5 - 8.5 (Alkaline)", "correct": False},
                    {"text": "9.0 - 10.0 (Highly alkaline)", "correct": False}
                ],
                "explanation": "Most crops grow best in slightly acidic to neutral soil (pH 6.0-7.0), which optimizes nutrient availability."
            },
            {
                "id": 2,
                "question": "Which crop rotation practice helps break pest cycles and improves soil fertility?",
                "topic": "crop_cycles",
                "options": [
                    {"text": "Monoculture (same crop every season)", "correct": False},
                    {"text": "Legume-cereal rotation", "correct": True},
                    {"text": "Continuous wheat planting", "correct": False},
                    {"text": "No rotation strategy", "correct": False}
                ],
                "explanation": "Legume-cereal rotation fixes nitrogen in soil and breaks pest cycles, improving overall soil health and yields."
            },
            {
                "id": 3,
                "question": "What is the most water-efficient irrigation method for row crops?",
                "topic": "irrigation",
                "options": [
                    {"text": "Flood irrigation", "correct": False},
                    {"text": "Sprinkler irrigation", "correct": False},
                    {"text": "Drip irrigation", "correct": True},
                    {"text": "Manual watering", "correct": False}
                ],
                "explanation": "Drip irrigation delivers water directly to plant roots, reducing evaporation and using up to 50% less water than traditional methods."
            }
        ]
    
    def _initialize_learning_modules(self) -> Dict[SkillLevel, List[Dict[str, Any]]]:
        """Initialize learning modules for different skill levels"""
        return {
            SkillLevel.BEGINNER: [
                {
                    "title": "Agriculture Fundamentals: Soil Science Basics",
                    "description": "Learn the fundamentals of soil composition, pH levels, and nutrient management for successful crop production.",
                    "duration": "2 weeks",
                    "topics": ["Soil types and structure", "pH management", "Organic matter", "Basic nutrients"],
                    "difficulty": "Beginner",
                    "next_module": "Introduction to Crop Selection"
                },
                {
                    "title": "Introduction to Crop Selection",
                    "description": "Understanding how to choose the right crops based on climate, soil, and market conditions.",
                    "duration": "1 week",
                    "topics": ["Climate considerations", "Soil-crop matching", "Market analysis", "Seasonal planning"],
                    "difficulty": "Beginner",
                    "next_module": "Water Management Essentials"
                },
                {
                    "title": "Water Management Essentials",
                    "description": "Basic irrigation principles and water conservation techniques for sustainable farming.",
                    "duration": "2 weeks",
                    "topics": ["Irrigation basics", "Water requirements", "Conservation methods", "Drought planning"],
                    "difficulty": "Beginner",
                    "next_module": "Sustainable Farming Practices"
                }
            ],
            SkillLevel.INTERMEDIATE: [
                {
                    "title": "Advanced Soil Health Management",
                    "description": "Deep dive into soil microbiology, organic amendments, and precision nutrient management.",
                    "duration": "3 weeks",
                    "topics": ["Soil microbiology", "Precision fertilization", "Soil testing", "Organic amendments"],
                    "difficulty": "Intermediate",
                    "next_module": "Integrated Crop Management"
                },
                {
                    "title": "Integrated Crop Management",
                    "description": "Comprehensive approach to crop production combining modern techniques with sustainable practices.",
                    "duration": "4 weeks",
                    "topics": ["IPM strategies", "Crop rotation planning", "Yield optimization", "Quality management"],
                    "difficulty": "Intermediate",
                    "next_module": "Smart Irrigation Systems"
                },
                {
                    "title": "Smart Irrigation Systems",
                    "description": "Modern irrigation technologies including sensors, automation, and water-use efficiency.",
                    "duration": "3 weeks",
                    "topics": ["Sensor technology", "Automated systems", "Water efficiency metrics", "Cost-benefit analysis"],
                    "difficulty": "Intermediate",
                    "next_module": "Data-Driven Agriculture"
                }
            ],
            SkillLevel.ADVANCED: [
                {
                    "title": "Precision Agriculture Technologies",
                    "description": "Cutting-edge technologies including GPS, drones, and AI for farm management optimization.",
                    "duration": "4 weeks",
                    "topics": ["GPS guidance systems", "Drone applications", "AI in agriculture", "Variable rate technology"],
                    "difficulty": "Advanced",
                    "next_module": "Regenerative Agriculture Systems"
                },
                {
                    "title": "Regenerative Agriculture Systems",
                    "description": "Advanced techniques for soil restoration, carbon sequestration, and ecosystem services.",
                    "duration": "6 weeks",
                    "topics": ["Carbon farming", "Soil restoration", "Biodiversity enhancement", "Ecosystem services"],
                    "difficulty": "Advanced",
                    "next_module": "Agri-Tech Innovation"
                },
                {
                    "title": "Agri-Tech Innovation and Investment",
                    "description": "Emerging technologies, startup opportunities, and investment trends in agricultural technology.",
                    "duration": "4 weeks",
                    "topics": ["Agri-tech trends", "Investment analysis", "Startup evaluation", "Technology integration"],
                    "difficulty": "Advanced",
                    "next_module": "Advanced Farm Management"
                }
            ]
        }
    
    def get_quiz_questions(self) -> List[Dict[str, Any]]:
        """Get all quiz questions"""
        return self.quiz_questions
    
    def evaluate_quiz_answers(self, answers: List[int]) -> Tuple[SkillLevel, int]:
        """
        Evaluate quiz answers and determine skill level
        
        Args:
            answers: List of selected option indices for each question
            
        Returns:
            Tuple of (skill_level, correct_answers_count)
        """
        correct_count = 0
        
        for i, answer_index in enumerate(answers):
            if i < len(self.quiz_questions):
                question = self.quiz_questions[i]
                if answer_index < len(question["options"]):
                    if question["options"][answer_index]["correct"]:
                        correct_count += 1
        
        # Determine skill level based on correct answers
        if correct_count <= 1:
            skill_level = SkillLevel.BEGINNER
        elif correct_count == 2:
            skill_level = SkillLevel.INTERMEDIATE
        else:  # correct_count == 3
            skill_level = SkillLevel.ADVANCED
        
        return skill_level, correct_count
    
    def get_recommended_module(self, skill_level: SkillLevel) -> Dict[str, Any]:
        """Get the recommended starting module for a skill level"""
        modules = self.learning_modules.get(skill_level, [])
        return modules[0] if modules else None
    
    def get_learning_path(self, skill_level: SkillLevel) -> List[Dict[str, Any]]:
        """Get the complete learning path for a skill level"""
        return self.learning_modules.get(skill_level, [])
    
    def get_quiz_feedback(self, answers: List[int]) -> Dict[str, Any]:
        """
        Get detailed feedback for quiz answers
        
        Args:
            answers: List of selected option indices for each question
            
        Returns:
            Dictionary containing skill level, score, feedback, and recommendations
        """
        skill_level, correct_count = self.evaluate_quiz_answers(answers)
        recommended_module = self.get_recommended_module(skill_level)
        
        # Generate feedback for each answer
        answer_feedback = []
        for i, answer_index in enumerate(answers):
            if i < len(self.quiz_questions):
                question = self.quiz_questions[i]
                selected_option = question["options"][answer_index] if answer_index < len(question["options"]) else None
                
                answer_feedback.append({
                    "question": question["question"],
                    "topic": question["topic"],
                    "selected_answer": selected_option["text"] if selected_option else "No answer selected",
                    "is_correct": selected_option["correct"] if selected_option else False,
                    "explanation": question["explanation"]
                })
        
        return {
            "skill_level": skill_level.value,
            "correct_answers": correct_count,
            "total_questions": len(self.quiz_questions),
            "score_percentage": (correct_count / len(self.quiz_questions)) * 100,
            "recommended_module": recommended_module,
            "learning_path": self.get_learning_path(skill_level),
            "answer_feedback": answer_feedback,
            "recommendation_text": f"Based on your responses, we recommend starting with: {recommended_module['title'] if recommended_module else 'Agriculture Fundamentals'}"
        }
    
    def get_user_assessment_summary(self, user_answers: List[int]) -> Dict[str, Any]:
        """
        Get a complete assessment summary for a user
        
        Args:
            user_answers: List of selected option indices for each question
            
        Returns:
            Complete assessment summary with personalized recommendations
        """
        feedback = self.get_quiz_feedback(user_answers)
        skill_level = SkillLevel(feedback["skill_level"])
        
        # Add skill level description
        skill_descriptions = {
            SkillLevel.BEGINNER: "You're new to agriculture - perfect! Everyone starts somewhere, and we'll guide you through the fundamentals.",
            SkillLevel.INTERMEDIATE: "You have a good foundation! Let's build on your existing knowledge with advanced techniques.",
            SkillLevel.ADVANCED: "Excellent! You have strong agricultural knowledge. Let's explore cutting-edge technologies and innovations."
        }
        
        feedback["skill_description"] = skill_descriptions.get(skill_level, "")
        
        return feedback
