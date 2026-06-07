# 💰 Finance Pro 2.0 - AI-Powered Financial Management System

## Advanced Financial Management with Machine Learning, Analytics & Multi-Platform Support

## 🚀 Features

### 🤖 AI & Machine Learning

- **Smart Spending Predictions** - ML-based forecasting for next month's expenses
- **Anomaly Detection** - Automatically detect unusual spending patterns
- **Auto-Categorization** - Intelligent expense categorization from descriptions
- **Budget Recommendations** - AI-powered budget suggestions based on history

### 📊 Analytics & Insights

- **Real-time Dashboard** - Comprehensive financial overview
- **Spending Analytics** - Category breakdown, trends, and patterns
- **Financial Health Score** - Overall financial wellness rating (A-F)
- **Monthly/Quarterly Reports** - Detailed financial reports
- **Savings Potential Analysis** - Identify where to cut spending

### 💼 Financial Management

- **Expense Tracking** - Quick expense logging with smart categorization
- **Income Tracking** - Multiple income source support
- **Budget Management** - Set and monitor budgets per category
- **Financial Goals** - Track progress toward financial objectives
- **Investment Portfolio** - Monitor stocks, bonds, and other investments

### 🌐 Integrations

- **Real-time Exchange Rates** - Multi-currency support (UGX, USD, EUR, etc.)
- **Bank Sync Ready** - Plaid integration support (future)
- **Cloud Sync Ready** - Multi-device synchronization (future)
- **Data Export** - CSV, JSON, and PDF export options

### 🎯 Alerts & Notifications

- **Budget Alerts** - Notifications when spending exceeds budget
- **Anomaly Alerts** - Alerts for unusual transactions
- **Recurring Expense Detection** - Identify subscriptions and regular payments
- **Goal Progress Alerts** - Track progress toward financial goals

---

## 📋 System Architecture

```python
Finance Pro 2.0
├── Frontend (Desktop/Mobile)
│   └── Kivy UI (main.py)
├── Backend API
│   └── FastAPI (api_server.py)
├── ML Engine
│   ├── Predictions (ml_engine.py)
│   ├── Anomaly Detection
│   └── Auto-categorization
├── Database
│   └── SQLite (enhanced_database.py)
├── Analytics
│   └── Reporting (analytics.py)
└── Integrations
    ├── Exchange Rates (integrations.py)
    ├── Bank APIs (future)
    └── Cloud Sync (future)
```

---

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- pip or conda

### Quick Start

1. **Clone/Setup Project**

```bash
cd c:\Users\akamp\Desktop\selfPython\my_financial_mgt
```

1. **Install Dependencies**

```bash
pip install -r requirements.txt
```

1. **Configure Environment**

```bash
cp .env.example .env
# Edit .env with your settings
```

1. **Run Application**

### Desktop App (Kivy)

```bash
python main.py
```

### Backend API Server

```bash
python api_server.py
# API available at http://localhost:8000
```

---

## 📱 Usage Guide

### Desktop Application (Kivy)

#### Dashboard

- View financial summary and health score
- See AI-powered insights
- Quick access to main features

#### Add Expense

1. Click "➕ Expense"
2. Enter amount, description, category
3. App auto-categorizes if needed
4. Select payment method
5. Click "Save"

#### Add Income

1. Click "💵 Income"
2. Enter amount and source
3. Select payment method
4. Click "Save"

#### Analytics

- View spending by category
- See next month predictions
- Analyze spending patterns
- Identify savings opportunities

### API Endpoints

#### Expenses

```json
POST   /api/expenses              - Add expense
GET    /api/expenses              - Get expenses
GET    /api/expenses/analytics    - Get analytics & predictions
```

#### Income

```json
POST   /api/income                - Add income
GET    /api/income                - Get income
```

#### Budgets

```json
POST   /api/budgets               - Set budget
GET    /api/budgets               - Get budgets
GET    /api/budgets/recommendations - AI recommendations
```

#### Goals

```json
POST   /api/goals                 - Create goal
```

#### Investments

```json
POST   /api/investments           - Add investment
GET    /api/investments/portfolio - Get portfolio
```

#### Analytics

```json
GET    /api/dashboard             - Dashboard summary
GET    /api/analytics/trends      - Spending trends
GET    /api/ml/predictions        - ML predictions
GET    /api/ml/anomalies          - Detected anomalies
GET    /api/insights              - AI insights
```

---

## 🔧 Configuration

Edit `.env` file to customize:

```env
# ML Features
ENABLE_ML_FEATURES=True
ANOMALY_SENSITIVITY=0.15

# Currency
DEFAULT_CURRENCY=UGX
SUPPORTED_CURRENCIES=UGX,USD,EUR

# API
API_PORT=8000

# Features
ENABLE_ANALYTICS=True
ENABLE_BUDGET_ALERTS=True
ENABLE_ANOMALY_ALERTS=True
```

---

## 📊 Advanced Features

### Machine Learning Models

#### Spending Prediction

- Uses Gradient Boosting Regressor
- Learns from 90 days of history
- Predicts spending by category
- Confidence scoring

#### Anomaly Detection

- Isolation Forest algorithm
- Real-time detection
- Configurable sensitivity
- Multi-feature analysis

#### Auto-Categorization
- Random Forest classifier
- Description-based learning
- Confidence scoring
- Fallback to manual entry

### Financial Health Score

Calculated based on:
- **Savings Rate** (30 points) - Income vs spending ratio
- **Goal Progress** (20 points) - Financial goals completion
- **Category Diversity** (20 points) - Balanced spending
- **Budget Compliance** (15 points) - Staying within budgets
- **Recurring Optimization** (15 points) - Subscription management

Grade: A (90+), B (80-89), C (70-79), D (60-69), F (<60)

---

## 📈 Data & Reports

### Monthly Report
- Income summary
- Expense breakdown by category
- Top transactions
- Daily trends
- Budget vs actual

### Quarterly Report
- Consolidated quarterly data
- YoY comparison
- Trend analysis

### Year-to-Date Summary
- Cumulative income/expenses
- Savings rate
- Average daily spending

---

## 🔐 Security & Privacy

- **Local-First** - All data stored locally by default
- **No Cloud** - Optional cloud sync feature (disabled by default)
- **Encrypted Settings** - Sensitive data encrypted in .env
- **No Tracking** - No telemetry or analytics
- **Backup Ready** - Easy backup/restore functionality

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:** Install missing package
```bash
pip install -r requirements.txt
```

### Issue: "Database locked"
**Solution:** Close other instances
```bash
# Kill any running processes
taskkill /F /IM python.exe
```

### Issue: "ML predictions not working"
**Solution:** Need minimum 10 transactions
```
Add more transactions first, then predictions will be available
```

### Issue: Exchange rates not updating
**Solution:** Check internet connection and API key
```bash
# Test API
curl https://api.exchangerate-api.com/v4/latest/UGX
```

---

## 📦 Project Structure

```
my_financial_mgt/
├── main.py                    # Kivy Desktop App
├── api_server.py             # FastAPI Backend
├── enhanced_database.py       # Advanced Database Layer
├── ml_engine.py              # ML & AI Features
├── analytics.py              # Analytics Engine
├── integrations.py           # External Integrations
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── .env.example              # Environment Template
└── finance_pro_advanced.db   # SQLite Database
```

---

## 🚀 Future Roadmap

- [ ] Web Dashboard (React)
- [ ] Mobile App (React Native)
- [ ] Bank Integration (Plaid API)
- [ ] Cloud Sync (Firebase)
- [ ] Multi-user Support
- [ ] Advanced Charting
- [ ] Budget Categories Customization
- [ ] Receipt Scanning (OCR)
- [ ] Voice Input
- [ ] Dark Mode Toggle
- [ ] Recurring Payment Automation
- [ ] Bill Reminders

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- UI/UX enhancements
- Additional ML models
- Performance optimization
- More integrations
- Documentation

---

## 📝 License

MIT License - See LICENSE file for details

---

## 💬 Support

For issues, questions, or suggestions:
1. Check the troubleshooting section
2. Review existing issues
3. Create a new issue with details
4. Include error messages and steps to reproduce

---

## 🎓 Learning Resources

### ML Models Used
- **Gradient Boosting** - Spending predictions
- **Isolation Forest** - Anomaly detection
- **Random Forest** - Category classification
- **Statistical Analysis** - Trend detection

### Technologies
- **Kivy** - Cross-platform GUI
- **FastAPI** - High-performance API
- **SQLite** - Lightweight database
- **scikit-learn** - Machine learning
- **pandas** - Data analysis

---

## 🎉 Features Highlight

### Smart Insights
```python
# Example: AI-generated insights
"⚠️ Your savings rate is only 12%. Consider reducing expenses."
"✅ Great! You're saving 35% of your income."
"💸 Your biggest spending is Entertainment (42% of total)"
"🚨 You've exceeded your Shopping budget by 25%!"
"📈 'Home Renovation' goal is 45% complete"
```

### Predictions
```python
# Example: Next month predictions
{
    "Groceries": {
        "predicted_amount": 185000,
        "confidence": 0.85,
        "trend": "up"
    },
    "Entertainment": {
        "predicted_amount": 75000,
        "confidence": 0.72,
        "trend": "stable"
    }
}
```

### Health Score
```python
# Example: Financial health
{
    "score": 82,
    "grade": "B",
    "breakdown": {
        "savings": 25,
        "goals": 18,
        "diversity": 20,
        "budget": 12,
        "recurring": 7
    }
}
```

---

## 📞 Contact & Support

- **Issues**: GitHub Issues
- **Email**: Support available via repository
- **Documentation**: See docs/ folder

---

**Finance Pro 2.0** - Making Financial Management Smart, Simple & Secure
