let userProfile = null;
let recommendations = [];

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadUserProfile();
    loadRecommendations();
});

function loadUserProfile() {
    const storedProfile = localStorage.getItem('userProfile');
    if (storedProfile) {
        userProfile = JSON.parse(storedProfile);
        updateProfileDisplay();
    } else {
        window.location.href = '/profile';
    }
}

function loadRecommendations() {
    const storedRecommendations = localStorage.getItem('recommendations');
    if (storedRecommendations) {
        recommendations = JSON.parse(storedRecommendations);
        displayRecommendations();
        createCharts();
    } else {
        window.location.href = '/profile';
    }
}

function updateProfileDisplay() {
    if (!userProfile) return;

    // Update profile summary
    const profileSummary = document.getElementById('profileSummary');
    profileSummary.textContent = `Budget: ₹${userProfile.budget.toLocaleString('en-IN')} | Risk Level: ${userProfile.risk_level} | Interests: ${userProfile.interests.join(', ') || 'None selected'}`;

    // Update metrics
    document.getElementById('budgetDisplay').textContent = `₹${userProfile.budget.toLocaleString('en-IN')}`;
    document.getElementById('riskDisplay').textContent = userProfile.risk_level.charAt(0).toUpperCase() + userProfile.risk_level.slice(1);
    document.getElementById('horizonDisplay').textContent = userProfile.investment_horizon.charAt(0).toUpperCase() + userProfile.investment_horizon.slice(1);
    document.getElementById('opportunitiesCount').textContent = recommendations.length;
}

function displayRecommendations() {
    const container = document.getElementById('recommendationsContainer');
    
    if (recommendations.length === 0) {
        container.innerHTML = `
            <div class="text-center py-5">
                <i class="fas fa-search fa-3x text-muted mb-3"></i>
                <h5>No recommendations found</h5>
                <p class="text-muted">Try adjusting your profile criteria</p>
            </div>
        `;
        return;
    }

    const recommendationsHTML = recommendations.map(rec => createRecommendationCard(rec)).join('');
    container.innerHTML = recommendationsHTML;
}

function createRecommendationCard(recommendation) {
    const riskClass = `risk-${recommendation.risk_level}`;
    const matchPercentage = Math.round(recommendation.match_score * 100);
    
    return `
        <div class="recommendation-card card mb-4 fade-in">
            <div class="card-body">
                <div class="row align-items-start">
                    <div class="col-md-8">
                        <div class="d-flex justify-content-between align-items-start mb-3">
                            <div>
                                <h5 class="card-title mb-1">${recommendation.title}</h5>
                                <span class="badge bg-secondary me-2">${recommendation.category}</span>
                                <span class="badge ${riskClass}">${recommendation.risk_level} risk</span>
                            </div>
                            <div class="match-score">
                                ${matchPercentage}% Match
                            </div>
                        </div>
                        
                        <p class="card-text text-muted mb-3">${recommendation.description}</p>
                        
                        <div class="row g-3 mb-3">
                            <div class="col-md-4">
                                <small class="text-muted d-block">Min Investment</small>
                                <strong>₹${recommendation.min_investment.toLocaleString('en-IN')}</strong>
                            </div>
                            <div class="col-md-4">
                                <small class="text-muted d-block">Expected Return</small>
                                <strong>${(recommendation.expected_return * 100).toFixed(1)}%</strong>
                            </div>
                            <div class="col-md-4">
                                <small class="text-muted d-block">Sustainability</small>
                                <strong>${(recommendation.sustainability_score * 100).toFixed(0)}%</strong>
                            </div>
                        </div>
                        
                        <div class="d-flex gap-2 flex-wrap">
                            ${recommendation.tags.map(tag => `<span class="badge bg-light text-dark">${tag}</span>`).join('')}
                        </div>
                    </div>
                    
                    <div class="col-md-4">
                        <div class="d-grid gap-2">
                            <button class="btn btn-primary" onclick="analyzeOpportunity(${recommendation.id})">
                                <i class="fas fa-chart-line me-2"></i>Analyze
                            </button>
                            <button class="btn btn-outline-success" onclick="runSimulation(${recommendation.id})">
                                <i class="fas fa-calculator me-2"></i>Simulate
                            </button>
                            <button class="btn btn-outline-info" onclick="viewDetails(${recommendation.id})">
                                <i class="fas fa-info-circle me-2"></i>Details
                            </button>
                        </div>
                        
                        <div class="mt-3">
                            <small class="text-muted">Market Size: ${recommendation.market_size}</small><br>
                            <small class="text-muted">Growth: ${recommendation.growth_rate}</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function createCharts() {
    createRiskReturnChart();
    createCategoryChart();
}

function createRiskReturnChart() {
    const trace = {
        x: recommendations.map(r => r.risk_level),
        y: recommendations.map(r => r.expected_return * 100),
        mode: 'markers',
        type: 'scatter',
        text: recommendations.map(r => r.title),
        textposition: 'top center',
        marker: {
            size: 12,
            color: recommendations.map(r => {
                switch(r.risk_level) {
                    case 'low': return '#28a745';
                    case 'medium': return '#ffc107';
                    case 'high': return '#dc3545';
                    default: return '#6c757d';
                }
            }),
            line: {
                color: 'rgba(0,0,0,0.2)',
                width: 1
            }
        }
    };

    const layout = {
        title: 'Risk vs Return Analysis',
        xaxis: { title: 'Risk Level' },
        yaxis: { title: 'Expected Return (%)' },
        showlegend: false,
        height: 300,
        margin: { l: 50, r: 50, t: 50, b: 50 }
    };

    Plotly.newPlot('riskReturnChart', [trace], layout, {responsive: true});
}

function createCategoryChart() {
    const categories = {};
    recommendations.forEach(rec => {
        categories[rec.category] = (categories[rec.category] || 0) + 1;
    });

    const data = [{
        values: Object.values(categories),
        labels: Object.keys(categories),
        type: 'pie',
        marker: {
            colors: ['#28a745', '#ffc107', '#dc3545', '#17a2b8', '#6f42c1']
        }
    }];

    const layout = {
        title: 'Investment Categories',
        height: 250,
        margin: { l: 10, r: 10, t: 40, b: 10 },
        showlegend: true,
        legend: {
            x: 0,
            y: 0,
            xanchor: 'left',
            yanchor: 'bottom'
        }
    };

    Plotly.newPlot('categoryChart', data, layout, {responsive: true});
}

async function analyzeOpportunity(recommendationId) {
    const investmentAmount = prompt('Enter investment amount:', userProfile.budget);
    if (!investmentAmount || isNaN(investmentAmount)) return;

    try {
        const response = await fetch('/api/analyze/' + recommendationId, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                profile: userProfile,
                investment_amount: parseFloat(investmentAmount)
            })
        });

        const result = await response.json();
        if (result.success) {
            displayAnalysis(result.analysis);
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

function displayAnalysis(analysis) {
    const content = document.getElementById('analysisContent');
    
    const profitAnalysis = analysis.profit_analysis;
    const riskAnalysis = analysis.risk_analysis;
    const sustainabilityAnalysis = analysis.sustainability_analysis;
    
    content.innerHTML = `
        <div class="row">
            <div class="col-md-12 mb-4">
                <h5>${analysis.opportunity.title}</h5>
                <p class="text-muted">${analysis.opportunity.description}</p>
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-4">
                <div class="analysis-card">
                    <h6>Profit Analysis</h6>
                    <div class="value">${(profitAnalysis.expected_annual_return * 100).toFixed(1)}%</div>
                    <small class="text-muted">Annual Return</small>
                    <div class="mt-3">
                        <small class="text-muted d-block">Monthly Return</small>
                        <strong>₹${profitAnalysis.monthly_return.toLocaleString('en-IN')}</strong>
                    </div>
                    <div class="mt-2">
                        <small class="text-muted d-block">Payback Period</small>
                        <strong>${profitAnalysis.payback_period_months} months</strong>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="analysis-card">
                    <h6>Risk Analysis</h6>
                    <div class="value">${riskAnalysis.risk_level}</div>
                    <small class="text-muted">Risk Level</small>
                    <div class="mt-3">
                        <small class="text-muted d-block">Risk Score</small>
                        <div class="progress">
                            <div class="progress-bar bg-warning" style="width: ${riskAnalysis.overall_risk_score * 100}%"></div>
                        </div>
                    </div>
                    <div class="mt-3">
                        <h6 class="text-muted small">Risk Mitigation:</h6>
                        <ul class="small">
                            ${riskAnalysis.mitigation_strategies.map(s => `<li>${s}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="analysis-card">
                    <h6>Sustainability Analysis</h6>
                    <div class="value">${sustainabilityAnalysis.sustainability_rating}</div>
                    <small class="text-muted">Rating</small>
                    <div class="mt-3">
                        <small class="text-muted d-block">Overall Score</small>
                        <div class="sustainability-meter">
                            <div class="sustainability-fill" style="width: ${sustainabilityAnalysis.overall_score * 100}%"></div>
                        </div>
                    </div>
                    <div class="mt-3">
                        <small class="text-muted d-block">Carbon Reduction</small>
                        <strong>${sustainabilityAnalysis.environmental_impact.carbon_reduction.toFixed(1)} tons/year</strong>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row mt-4">
            <div class="col-md-12">
                <div class="analysis-card">
                    <h6>Key Insights</h6>
                    <ul>
                        ${analysis.insights.map(insight => `<li>${insight}</li>`).join('')}
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="row mt-4">
            <div class="col-md-12">
                <div id="projectionChart" style="height: 400px;"></div>
            </div>
        </div>
    `;
    
    // Create projection chart
    createProjectionChart(profitAnalysis.projections);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('analysisModal'));
    modal.show();
}

function createProjectionChart(projections) {
    const trace = {
        x: projections.map(p => `Year ${p.year}`),
        y: projections.map(p => p.investment),
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Total Investment Value',
        line: {color: '#28a745', width: 3},
        marker: {size: 8}
    };

    const returnTrace = {
        x: projections.map(p => `Year ${p.year}`),
        y: projections.map(p => p.total_return),
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Total Returns',
        line: {color: '#17a2b8', width: 3},
        marker: {size: 8}
    };

    const layout = {
        title: '5-Year Investment Projection',
        xaxis: { title: 'Time Period' },
        yaxis: { title: 'Amount (₹)' },
        height: 400,
        margin: { l: 50, r: 50, t: 50, b: 50 }
    };

    Plotly.newPlot('projectionChart', [trace, returnTrace], layout, {responsive: true});
}

async function runSimulation(recommendationId) {
    try {
        const response = await fetch('/api/simulate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                profile: userProfile,
                recommendation_id: recommendationId,
                scenarios: ['conservative', 'moderate', 'optimistic']
            })
        });

        const result = await response.json();
        if (result.success) {
            displaySimulation(result.simulation);
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

function displaySimulation(simulation) {
    const content = document.getElementById('simulationContent');
    
    const scenarios = Object.keys(simulation.scenarios);
    const comparison = simulation.comparison;
    
    content.innerHTML = `
        <div class="row">
            <div class="col-md-12 mb-4">
                <h5>Investment Simulation</h5>
                <p class="text-muted">${simulation.opportunity.title}</p>
            </div>
        </div>
        
        <div class="row">
            ${scenarios.map(scenario => {
                const data = simulation.scenarios[scenario];
                return `
                    <div class="col-md-4">
                        <div class="analysis-card">
                            <h6>${scenario.charAt(0).toUpperCase() + scenario.slice(1)} Scenario</h6>
                            <div class="value">₹${data.expected_final_value.toLocaleString('en-IN')}</div>
                            <small class="text-muted">Expected Final Value</small>
                            <div class="mt-3">
                                <small class="text-muted d-block">Best Case (90th percentile)</small>
                                <strong>₹${data.final_values.p90.toLocaleString('en-IN')}</strong>
                            </div>
                            <div class="mt-2">
                                <small class="text-muted d-block">Worst Case (10th percentile)</small>
                                <strong>₹${data.final_values.p10.toLocaleString('en-IN')}</strong>
                            </div>
                            <div class="mt-2">
                                <small class="text-muted d-block">Probability of Loss</small>
                                <strong>${(data.probability_of_loss * 100).toFixed(1)}%</strong>
                            </div>
                        </div>
                    </div>
                `;
            }).join('')}
        </div>
        
        <div class="row mt-4">
            <div class="col-md-12">
                <div id="simulationChart" style="height: 400px;"></div>
            </div>
        </div>
    `;
    
    // Create simulation comparison chart
    createSimulationChart(simulation.scenarios);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('simulationModal'));
    modal.show();
}

function createSimulationChart(scenarios) {
    const traces = Object.keys(scenarios).map(scenario => {
        const data = scenarios[scenario];
        return {
            x: ['P10', 'P25', 'P50', 'P75', 'P90'],
            y: [
                data.final_values.p10,
                data.final_values.p25,
                data.final_values.p50,
                data.final_values.p75,
                data.final_values.p90
            ],
            type: 'scatter',
            mode: 'lines+markers',
            name: scenario.charAt(0).toUpperCase() + scenario.slice(1),
            line: {width: 3},
            marker: {size: 8}
        };
    });

    const layout = {
        title: 'Scenario Comparison - Investment Outcomes',
        xaxis: { title: 'Percentile' },
        yaxis: { title: 'Final Investment Value (₹)' },
        height: 400,
        margin: { l: 50, r: 50, t: 50, b: 50 }
    };

    Plotly.newPlot('simulationChart', traces, layout, {responsive: true});
}

function viewDetails(recommendationId) {
    const recommendation = recommendations.find(r => r.id === recommendationId);
    if (!recommendation) return;
    
    const details = `
        <h5>${recommendation.title}</h5>
        <p><strong>Category:</strong> ${recommendation.category}</p>
        <p><strong>Description:</strong> ${recommendation.description}</p>
        <p><strong>Investment Range:</strong> ₹${recommendation.min_investment.toLocaleString('en-IN')} - ₹${recommendation.max_investment.toLocaleString('en-IN')}</p>
        <p><strong>Expected Return:</strong> ${(recommendation.expected_return * 100).toFixed(1)}%</p>
        <p><strong>Risk Level:</strong> ${recommendation.risk_level}</p>
        <p><strong>Sustainability Score:</strong> ${(recommendation.sustainability_score * 100).toFixed(0)}%</p>
        <p><strong>Time Horizon:</strong> ${recommendation.time_horizon}</p>
        <p><strong>Market Size:</strong> ${recommendation.market_size}</p>
        <p><strong>Growth Rate:</strong> ${recommendation.growth_rate}</p>
        <p><strong>Tags:</strong> ${recommendation.tags.join(', ')}</p>
    `;
    
    alert(details);
}
