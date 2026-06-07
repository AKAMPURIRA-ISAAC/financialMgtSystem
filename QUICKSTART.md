# QUICK START GUIDE - Finance Pro 2.0

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
cd c:\Users\akamp\Desktop\selfPython\my_financial_mgt
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python main.py
```

The app will launch with a modern dashboard showing:
- Financial summary cards
- AI-powered insights
- Quick action buttons
- Health score

### Step 3: Start Tracking
1. Click **"➕ Expense"** to log your spending
2. Click **"💵 Income"** to record income
3. Click **"📊 Analytics"** to view insights
4. Click **"⚙️ Settings"** for configuration

---

## 🤖 AI Features Explained

### Automatic Categorization
- Describe your expense in plain text
- App learns and auto-categorizes
- Example: "Lunch at pizza place" → Food

### Spending Predictions
- Based on 90 days of history
- Predicts next month's spending
- Shows trends and patterns

### Anomaly Detection
- Detects unusual spending
- Alerts you to potential fraud
- Customizable sensitivity

### Financial Health Score
- A-F grading system
- Based on 5 metrics
- Actionable recommendations

---

## 📊 Sample Data

App comes with sample transactions:
- Groceries: 50,000 UGX
- Transport: 15,000 UGX
- Monthly Salary: 500,000 UGX

Replace with your actual data for accurate predictions!

---

## 🔗 API Server (Optional)

To run the backend API:
```bash
python api_server.py
```

API available at: **http://localhost:8000**

### Test Endpoints
```bash
# Get dashboard
curl http://localhost:8000/api/dashboard

# Add expense
curl -X POST http://localhost:8000/api/expenses \
  -H "Content-Type: application/json" \
  -d '{"category":"Food","amount":50000,"description":"Lunch"}'

# Get predictions
curl http://localhost:8000/api/ml/predictions
```

---

## ⚙️ Configuration

Edit `.env` file to customize:

```env
# Currency Settings
DEFAULT_CURRENCY=UGX

# ML Settings
ENABLE_ML_FEATURES=True
ANOMALY_SENSITIVITY=0.15

# Budget Alerts
ENABLE_BUDGET_ALERTS=True
BUDGET_ALERT_THRESHOLD=80
```

---

## 💾 Data Management

### Backup
Data is stored in: `finance_pro_advanced.db`
- Manual backup: Copy this file
- Auto-backup: Configure in settings

### Export
- Dashboard shows export options
- Supports CSV and JSON formats

---

## 🐛 Common Issues

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"Database locked"**
- Close the app completely
- Remove any stray Python processes

**"No predictions shown"**
- Add more transactions (min 10)
- Wait 24 hours for model to train

---

## 📚 File Overview

| File | Purpose |
|------|---------|
| `main.py` | Desktop app (Kivy) |
| `api_server.py` | Backend API (FastAPI) |
| `ml_engine.py` | AI/ML features |
| `enhanced_database.py` | Database management |
| `analytics.py` | Financial reports |
| `integrations.py` | External services |
| `config.py` | Configuration |

---

## 🎓 Next Steps

1. **Add Your Data** - Log real expenses and income
2. **Set Budgets** - Define spending limits
3. **Create Goals** - Set financial targets
4. **Track Investments** - Add portfolio items
5. **Review Reports** - Check monthly analytics
6. **Optimize** - Use insights to improve finances

---

## 💡 Pro Tips

1. **Categories** - Use consistent category names
2. **Descriptions** - Detailed descriptions help AI learn
3. **Regular Input** - Add transactions daily
4. **Review Insights** - Check insights weekly
5. **Adjust Budgets** - Based on actual spending

---

## 🆘 Need Help?

1. Check README.md for detailed documentation
2. Review configuration in config.py
3. Check .env.example for available settings
4. Review error messages in terminal

---

**Happy tracking! Let Finance Pro 2.0 help you master your finances! 💰**
