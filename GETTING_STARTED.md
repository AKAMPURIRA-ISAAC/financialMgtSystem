# Finance Pro 2.0 - Getting Started Guide

## 🚀 Quick Start (1 minute)

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Run the Desktop Application**
```bash
python main.py
```

The Kivy desktop app will launch with the Finance Pro 2.0 dashboard.

### 3. **Run the API Server** (Optional, in another terminal)
```bash
python api_server.py
```

API available at: `http://localhost:8000`

---

## 📱 Desktop App Features

### Dashboard
- **Financial Health Score**: A-F grade based on 5 metrics
- **Summary Cards**: Balance, Income, Expenses, Monthly totals
- **AI Insights**: Smart recommendations based on spending patterns
- **Quick Actions**: Fast access to core features

### Add Expense
1. Enter amount in Ugandan Shillings (₨)
2. Add description (e.g., "Groceries at Nakumatt")
3. Select category (auto-suggested by AI)
4. Click Save

### Add Income
1. Enter income amount
2. Add source (e.g., "Salary", "Freelance")
3. Click Save

### Analytics
- View spending breakdown by category
- See predictions for next month
- Analyze spending trends
- Identify savings opportunities

### Settings
- View app version and configuration
- Enable/disable ML features
- Set currency and preferences

---

## 🔌 API Endpoints

### Health Check
```
GET /api/health
```

### Expenses
```
POST   /api/expenses              - Add expense
GET    /api/expenses              - Get all expenses
GET    /api/expenses?days=30      - Get last 30 days
```

### Income
```
POST   /api/income                - Add income
GET    /api/income                - Get all income
```

### Analytics
```
GET    /api/dashboard             - Dashboard summary
GET    /api/analytics/trends      - Spending trends
GET    /api/ml/predictions        - Spending predictions
GET    /api/ml/anomalies          - Detected anomalies
```

### Example Requests
```bash
# Add expense
curl -X POST http://localhost:8000/api/expenses \
  -H "Content-Type: application/json" \
  -d '{"category": "Groceries", "amount": 50000, "description": "Shopping"}'

# Get dashboard
curl http://localhost:8000/api/dashboard

# Get health score
curl http://localhost:8000/api/health
```

---

## 📊 Key Features

### 1. **Machine Learning**
- **Spending Predictions**: Forecasts next month expenses by category
- **Anomaly Detection**: Identifies unusual spending patterns
- **Auto-Categorization**: Intelligent expense categorization from descriptions

### 2. **Financial Health Score**
Calculated based on:
- Savings Rate (30%)
- Goal Progress (20%)
- Spending Diversity (20%)
- Budget Compliance (15%)
- Recurring Optimization (15%)

Grade: A (90+), B (80-89), C (70-79), D (60-69), F (<60)

### 3. **Multi-Currency Support**
- UGX (Ugandan Shilling) - Default
- USD, EUR, GBP, KES
- Real-time exchange rates

### 4. **Advanced Analytics**
- Monthly/Quarterly/YTD reports
- Spending by category
- Top transactions
- Daily trends
- Savings potential

---

## ⚙️ Configuration

Create a `.env` file (copy from `.env.example`):

```env
# ML Features
ENABLE_ML_FEATURES=True
ANOMALY_SENSITIVITY=0.15

# Currency
DEFAULT_CURRENCY=UGX

# API
API_PORT=8000

# Features
ENABLE_ANALYTICS=True
ENABLE_BUDGET_ALERTS=True
```

---

## 📁 Project Structure

```
Finance Pro 2.0/
├── main.py                 # Kivy desktop GUI
├── api_server.py           # FastAPI backend
├── enhanced_database.py    # SQLite database layer
├── ml_engine.py            # ML models (predictions, anomalies)
├── analytics.py            # Analytics & reporting
├── integrations.py         # Exchange rates, health score
├── config.py               # Configuration management
├── finance_pro_advanced.db # SQLite database
└── requirements.txt        # Python dependencies
```

---

## 🔧 Troubleshooting

### App won't start
- Check Python version: `python --version` (requires 3.8+)
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

### "No module named 'pandas'"
```bash
pip install pandas numpy scikit-learn
```

### API won't start
- Check if port 8000 is available
- Use different port: `API_PORT=8001 python api_server.py`

### Database errors
- Delete `finance_pro_advanced.db` to reset
- Restart app (new database will be created)

---

## 📈 Sample Workflow

1. **Open Desktop App**
   ```bash
   python main.py
   ```

2. **Add Some Transactions**
   - Add Expenses: Groceries, Transport, Dining
   - Add Income: Salary, Freelance

3. **Check Dashboard**
   - View financial health score
   - See AI insights

4. **View Analytics**
   - Check spending by category
   - See predictions for next month

5. **Optional: Use API**
   ```bash
   python api_server.py
   # In another terminal
   curl http://localhost:8000/api/dashboard
   ```

---

## 🎯 Next Steps

- Explore all features in the desktop app
- Add your actual financial data
- Review analytics and reports
- Set up budgets and financial goals
- Enable anomaly alerts for unusual spending

Enjoy your new financial management system! 💰
