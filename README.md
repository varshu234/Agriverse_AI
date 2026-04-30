# Agriverse AI - Smart Agriculture Investment Platform

A comprehensive web application that helps corporates explore agriculture as an investment and business opportunity using AI-powered recommendations and analysis.

## 🌟 Features

- **User Profile System**: Input budget, risk level, and investment interests
- **AI-Powered Recommendations**: Personalized agriculture investment opportunities
- **Comprehensive Analysis**: Profit, risk, and sustainability analysis for each recommendation
- **Interactive Dashboard**: Clean, modern UI with real-time data visualization
- **Investment Simulation**: Scenario analysis with conservative, moderate, and optimistic projections
- **Data Visualizations**: Interactive charts using Plotly.js
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🏗️ Project Structure

```
agriverse-ai/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                      # Project documentation
├── static/
│   ├── css/
│   │   └── style.css             # Custom styles
│   ├── js/
│   │   ├── main.js               # Main JavaScript functionality
│   │   └── dashboard.js          # Dashboard-specific JavaScript
│   └── images/                   # Static images (if needed)
├── templates/
│   ├── index.html                # Landing page
│   ├── profile.html              # User profile setup
│   └── dashboard.html            # Main dashboard
└── backend/
    ├── models/
    │   └── user_profile.py       # User profile data model
    └── services/
        ├── recommendation_engine.py  # AI recommendation system
        └── analysis_service.py      # Investment analysis service
```

## 🚀 Technology Stack

### Backend
- **Flask**: Python web framework
- **NumPy**: Numerical computing
- **Pandas**: Data manipulation
- **Scikit-learn**: Machine learning utilities

### Frontend
- **HTML5/CSS3**: Modern web standards
- **JavaScript**: Interactive functionality
- **Bootstrap 5**: Responsive UI framework
- **Font Awesome**: Icon library
- **Plotly.js**: Interactive charts and visualizations

### Additional Libraries
- **Flask-CORS**: Cross-origin resource sharing
- **Matplotlib/Seaborn**: Data visualization (backend)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🛠️ Installation & Setup

### Step 1: Clone or Download the Project

If you have the project files, navigate to the project directory:

```bash
cd agriverse-ai
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app.py
```

The application will start running on:
- **Local URL**: http://localhost:5000
- **Network URL**: http://0.0.0.0:5000

## 🎯 How to Use the Application

### 1. Landing Page
- Open http://localhost:5000 in your web browser
- Explore the features and investment categories
- Click "Get Started" to begin

### 2. Create Your Investment Profile
- **Budget**: Enter your investment budget (minimum $1,000)
- **Risk Tolerance**: Choose between Conservative, Moderate, or Aggressive
- **Investment Horizon**: Select Short-term (1-2 years), Medium-term (3-5 years), or Long-term (5+ years)
- **Interests**: Select areas that interest you (Technology, Sustainability, Innovation, etc.)

### 3. View Your Dashboard
- See personalized recommendations based on your profile
- Each recommendation shows:
  - Match percentage with your profile
  - Investment requirements and expected returns
  - Risk level and sustainability score
  - Market size and growth rate

### 4. Analyze Investment Opportunities
- Click "Analyze" on any recommendation to see:
  - Detailed profit analysis with projections
  - Risk assessment with mitigation strategies
  - Sustainability impact metrics
  - Personalized insights

### 5. Run Investment Simulations
- Click "Simulate" to explore different scenarios:
  - Conservative, Moderate, and Optimistic projections
  - Monte Carlo simulation results
  - Probability analysis for different outcomes

## 📊 Investment Categories

The platform covers three main agriculture investment categories:

### 🚜 Agri-Tech
- Precision farming technology
- IoT sensors and monitoring
- AI-driven crop management
- Agricultural robotics

### 🌾 Farming
- Organic and vertical farming
- Sustainable livestock management
- Regenerative agriculture
- Hydroponics and aquaponics

### 🚚 Supply Chain
- Cold storage logistics
- Blockchain traceability
- Distribution platforms
- Market access solutions

## 🔧 Customization

### Adding New Investment Opportunities

Edit `backend/services/recommendation_engine.py` and add new opportunities to the `_load_opportunities()` method:

```python
{
    'id': 7,
    'title': 'Your New Opportunity',
    'category': 'agri-tech',
    'description': 'Description of the investment opportunity',
    'min_investment': 10000,
    'max_investment': 500000,
    'risk_level': 'medium',
    'expected_return': 0.15,
    'sustainability_score': 0.85,
    'time_horizon': 'medium',
    'tags': ['technology', 'innovation'],
    'market_size': '$10 billion',
    'growth_rate': '20% annually'
}
```

### Modifying Recommendation Algorithm

The recommendation logic is in `_calculate_match_score()` method in `recommendation_engine.py`. You can adjust the weights and scoring criteria based on your requirements.

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find and kill the process using port 5000
   # On Windows:
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   
   # On macOS/Linux:
   lsof -ti:5000 | xargs kill -9
   ```

2. **Module Import Errors**
   ```bash
   # Ensure all dependencies are installed
   pip install -r requirements.txt
   
   # If using virtual environment, make sure it's activated
   ```

3. **Browser Cache Issues**
   - Clear browser cache and reload
   - Try incognito/private browsing mode

### Performance Tips

- Use a virtual environment to isolate dependencies
- For production deployment, consider using a production WSGI server like Gunicorn
- Enable browser caching for static assets in production

## 🚀 Deployment

### For Development
The built-in Flask development server is sufficient for testing and development.

### For Production
Consider using:

1. **Gunicorn** as WSGI server:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Docker** for containerization:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 5000
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
   ```

3. **Cloud Platforms**:
   - Heroku
   - AWS Elastic Beanstalk
   - Google Cloud Platform
   - Azure App Service

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For questions or support:
- Check the troubleshooting section above
- Review the code comments for detailed explanations
- Test with different browser profiles if encountering UI issues

## 🎉 Happy Investing!

Explore the future of agriculture investment with AI-powered insights and make informed decisions for sustainable growth.

---

**Note**: This is a demonstration project. For real investment decisions, please consult with qualified financial advisors and conduct thorough due diligence.
