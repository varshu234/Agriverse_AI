// Skill Gap Analyzer JavaScript
let currentQuestionIndex = 0;
let quizQuestions = [];
let userAnswers = [];
let quizResults = null;

// Initialize skill quiz
document.addEventListener('DOMContentLoaded', function() {
    checkSkillAssessmentStatus();
});

function checkSkillAssessmentStatus() {
    // Check if user has already completed the quiz
    const completedQuiz = localStorage.getItem('skillAssessmentCompleted');
    const userProfile = localStorage.getItem('userProfile');
    
    // Only show quiz if user has profile and hasn't completed assessment
    if (userProfile && !completedQuiz) {
        // Show quiz after a short delay to let dashboard load
        setTimeout(() => {
            showSkillQuizModal();
        }, 2000);
    } else if (completedQuiz) {
        // Show existing skill path
        displaySkillPath();
    }
    
    // Always show quiz trigger section for testing
    document.getElementById('quizTriggerSection').style.display = 'block';
}

function forceShowQuiz() {
    // Clear any existing quiz data to force show
    localStorage.removeItem('skillAssessmentCompleted');
    localStorage.removeItem('skillAssessmentResults');
    
    // Hide quiz trigger section
    document.getElementById('quizTriggerSection').style.display = 'none';
    
    // Show quiz modal
    showSkillQuizModal();
}

function showSkillQuizModal() {
    const modal = new bootstrap.Modal(document.getElementById('skillQuizModal'));
    modal.show();
}

function startSkillQuiz() {
    // Load quiz questions
    loadQuizQuestions();
}

async function loadQuizQuestions() {
    try {
        const response = await fetch('/api/skill-quiz/questions');
        const result = await response.json();
        
        if (result.success) {
            quizQuestions = result.questions;
            userAnswers = new Array(quizQuestions.length).fill(-1);
            currentQuestionIndex = 0;
            
            // Show questions, hide intro
            document.getElementById('quizIntro').style.display = 'none';
            document.getElementById('quizQuestions').style.display = 'block';
            
            // Load first question
            displayQuestion();
        } else {
            alert('Failed to load quiz questions');
        }
    } catch (error) {
        console.error('Error loading quiz questions:', error);
        alert('Error loading quiz questions');
    }
}

function displayQuestion() {
    if (currentQuestionIndex >= quizQuestions.length) return;
    
    const question = quizQuestions[currentQuestionIndex];
    const container = document.getElementById('questionContainer');
    
    // Update progress
    const progress = ((currentQuestionIndex + 1) / quizQuestions.length) * 100;
    document.getElementById('quizProgress').style.width = progress + '%';
    document.getElementById('quizProgress').textContent = `Question ${currentQuestionIndex + 1} of ${quizQuestions.length}`;
    
    // Generate question HTML
    let questionHTML = `
        <div class="question-card">
            <h5 class="mb-3">
                <span class="badge bg-success me-2">Question ${currentQuestionIndex + 1}</span>
                ${question.question}
            </h5>
            <div class="options-container">
    `;
    
    question.options.forEach((option, index) => {
        const isSelected = userAnswers[currentQuestionIndex] === index;
        questionHTML += `
            <div class="form-check mb-2 option-item ${isSelected ? 'selected' : ''}" onclick="selectOption(${index})">
                <input class="form-check-input" type="radio" name="question${currentQuestionIndex}" 
                       id="option${index}" value="${index}" ${isSelected ? 'checked' : ''}>
                <label class="form-check-label w-100" for="option${index}">
                    <div class="d-flex align-items-center">
                        <span class="option-letter me-3">${String.fromCharCode(65 + index)}.</span>
                        <span>${option.text}</span>
                    </div>
                </label>
            </div>
        `;
    });
    
    questionHTML += `
            </div>
            <small class="text-muted mt-2 d-block">
                <i class="fas fa-info-circle me-1"></i>
                Topic: ${question.topic.charAt(0).toUpperCase() + question.topic.slice(1)}
            </small>
        </div>
    `;
    
    container.innerHTML = questionHTML;
    
    // Update navigation buttons
    updateNavigationButtons();
}

function selectOption(optionIndex) {
    userAnswers[currentQuestionIndex] = optionIndex;
    
    // Update visual selection
    document.querySelectorAll('.option-item').forEach((item, index) => {
        if (index === optionIndex) {
            item.classList.add('selected');
        } else {
            item.classList.remove('selected');
        }
    });
    
    // Update radio button
    document.getElementById(`option${optionIndex}`).checked = true;
    
    // Update navigation buttons to enable next button
    updateNavigationButtons();
}

function updateNavigationButtons() {
    const prevBtn = document.getElementById('prevQuestionBtn');
    const nextBtn = document.getElementById('nextQuestionBtn');
    const submitBtn = document.getElementById('submitQuizBtn');
    
    // Show/hide previous button
    prevBtn.style.display = currentQuestionIndex > 0 ? 'block' : 'none';
    
    // Show next or submit button
    if (currentQuestionIndex === quizQuestions.length - 1) {
        nextBtn.style.display = 'none';
        submitBtn.style.display = 'block';
    } else {
        nextBtn.style.display = 'block';
        submitBtn.style.display = 'none';
    }
    
    // Enable/disable next button based on answer selection
    const hasAnswer = userAnswers[currentQuestionIndex] !== -1;
    nextBtn.disabled = !hasAnswer;
    submitBtn.disabled = !hasAnswer;
}

function nextQuestion() {
    if (currentQuestionIndex < quizQuestions.length - 1) {
        currentQuestionIndex++;
        displayQuestion();
    }
}

function previousQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        displayQuestion();
    }
}

async function submitSkillQuiz() {
    // Validate all answers are provided
    if (userAnswers.includes(-1)) {
        alert('Please answer all questions before submitting.');
        return;
    }
    
    try {
        const response = await fetch('/api/skill-quiz/evaluate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ answers: userAnswers })
        });
        
        const result = await response.json();
        
        if (result.success) {
            quizResults = result.assessment;
            displayQuizResults();
            
            // Store quiz completion
            localStorage.setItem('skillAssessmentCompleted', 'true');
            localStorage.setItem('skillAssessmentResults', JSON.stringify(quizResults));
            
        } else {
            alert('Failed to evaluate quiz: ' + result.error);
        }
    } catch (error) {
        console.error('Error submitting quiz:', error);
        alert('Error submitting quiz');
    }
}

function displayQuizResults() {
    const results = quizResults;
    
    // Hide questions, show results
    document.getElementById('quizQuestions').style.display = 'none';
    document.getElementById('quizResults').style.display = 'block';
    
    // Set result icon based on skill level
    const iconMap = {
        'beginner': '<i class="fas fa-seedling fa-4x text-success"></i>',
        'intermediate': '<i class="fas fa-tree fa-4x text-warning"></i>',
        'advanced': '<i class="fas fa-mountain fa-4x text-info"></i>'
    };
    
    document.getElementById('resultIcon').innerHTML = iconMap[results.skill_level] || iconMap['beginner'];
    
    // Set result title and description
    document.getElementById('resultTitle').textContent = `You're ${results.skill_level} Level!`;
    document.getElementById('resultDescription').textContent = results.skill_description;
    
    // Set recommendation
    document.getElementById('recommendationText').textContent = results.recommendation_text;
    
    // Display recommended module
    if (results.recommended_module) {
        const module = results.recommended_module;
        document.getElementById('recommendedModule').innerHTML = `
            <h6 class="text-success">${module.title}</h6>
            <p class="mb-2">${module.description}</p>
            <div class="row">
                <div class="col-md-6">
                    <small class="text-muted"><i class="fas fa-clock me-1"></i>Duration: ${module.duration}</small>
                </div>
                <div class="col-md-6">
                    <small class="text-muted"><i class="fas fa-signal me-1"></i>Level: ${module.difficulty}</small>
                </div>
            </div>
            <div class="mt-2">
                <small class="text-muted"><strong>Topics:</strong> ${module.topics.join(', ')}</small>
            </div>
        `;
    }
    
    // Set score display
    document.getElementById('scoreDisplay').textContent = `${results.correct_answers}/${results.total_questions}`;
    document.getElementById('skillLevelDisplay').textContent = results.skill_level.charAt(0).toUpperCase() + results.skill_level.slice(1);
    
    // Display answer review
    const answerReviewHTML = results.answer_feedback.map((feedback, index) => `
        <div class="card mb-2">
            <div class="card-body py-2">
                <div class="d-flex align-items-center">
                    <div class="me-3">
                        ${feedback.is_correct ? 
                            '<i class="fas fa-check-circle text-success"></i>' : 
                            '<i class="fas fa-times-circle text-danger"></i>'}
                    </div>
                    <div class="flex-grow-1">
                        <small class="text-muted">Question ${index + 1} (${feedback.topic})</small>
                        <div class="fw-bold">${feedback.selected_answer}</div>
                        ${!feedback.is_correct ? `<small class="text-success d-block mt-1"><i class="fas fa-info-circle me-1"></i>${feedback.explanation}</small>` : ''}
                    </div>
                </div>
            </div>
        </div>
    `).join('');
    
    document.getElementById('answerReview').innerHTML = answerReviewHTML;
    
    // Show close button
    document.getElementById('closeQuizBtn').style.display = 'block';
}

function closeSkillQuiz() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('skillQuizModal'));
    modal.hide();
    
    // Display skill path on dashboard
    displaySkillPath();
}

function displaySkillPath() {
    const storedResults = localStorage.getItem('skillAssessmentResults');
    
    if (storedResults) {
        const results = JSON.parse(storedResults);
        const section = document.getElementById('skillPathSection');
        
        // Set recommendation text
        document.getElementById('pathRecommendation').textContent = results.recommendation_text;
        document.getElementById('pathDescription').textContent = results.skill_description;
        document.getElementById('skillBadge').textContent = results.skill_level.charAt(0).toUpperCase() + results.skill_level.slice(1);
        
        // Show the section
        section.style.display = 'block';
    }
}

function retakeQuiz() {
    // Reset quiz state
    currentQuestionIndex = 0;
    userAnswers = [];
    quizResults = null;
    
    // Clear stored results
    localStorage.removeItem('skillAssessmentCompleted');
    localStorage.removeItem('skillAssessmentResults');
    
    // Hide results, show intro
    document.getElementById('quizResults').style.display = 'none';
    document.getElementById('quizQuestions').style.display = 'none';
    document.getElementById('quizIntro').style.display = 'block';
    
    // Hide close button
    document.getElementById('closeQuizBtn').style.display = 'none';
}

// Add CSS styles for quiz options
const quizStyles = `
<style>
.option-item {
    border: 2px solid #e9ecef;
    border-radius: 8px;
    padding: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.option-item:hover {
    border-color: #28a745;
    background-color: #f8f9fa;
}

.option-item.selected {
    border-color: #28a745;
    background-color: #d4edda;
}

.option-letter {
    font-weight: bold;
    color: #28a745;
    font-size: 1.1em;
}

.question-card {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 24px;
    border: 1px solid #e9ecef;
}

.progress {
    height: 8px;
}

.progress-bar {
    transition: width 0.3s ease;
}
</style>
`;

document.head.insertAdjacentHTML('beforeend', quizStyles);
