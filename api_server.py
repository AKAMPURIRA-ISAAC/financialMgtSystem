# api_server.py - FastAPI Backend for Financial Management System
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import uvicorn
import json

from enhanced_database import EnhancedDatabase
from ml_engine import MLEngine
from integrations import ExchangeRateProvider, CategoryAnalyzer

# Initialize components
app = FastAPI(title="Finance Pro API", version="2.0.0")
db = EnhancedDatabase()
ml_engine = MLEngine(db)
exchange_provider = ExchangeRateProvider()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== PYDANTIC MODELS =====
class ExpenseCreate(BaseModel):
    category: str
    amount: float
    description: Optional[str] = ""
    payment_method: str = "Cash"
    recurring: bool = False

class IncomeCreate(BaseModel):
    source: str
    amount: float
    description: Optional[str] = ""
    payment_method: str = "Bank Transfer"

class BudgetCreate(BaseModel):
    category: str
    monthly_limit: float
    alert_threshold: float = 80

class GoalCreate(BaseModel):
    name: str
    target_amount: float
    target_date: Optional[str] = None
    monthly_contribution: float = 0

class InvestmentCreate(BaseModel):
    name: str
    investment_type: str
    quantity: float
    buy_price: float
    ticker: Optional[str] = None

# ===== EXPENSE ENDPOINTS =====
@app.post("/api/expenses")
async def create_expense(expense: ExpenseCreate):
    """Create new expense with auto-categorization"""
    try:
        # Auto-categorize if confidence is high
        if not expense.category:
            category, confidence = ml_engine.categorize_expense(expense.description)
            if confidence > 0.7:
                expense.category = category
        
        expense_id = db.add_expense(
            category=expense.category,
            amount=expense.amount,
            description=expense.description,
            payment_method=expense.payment_method,
            recurring=expense.recurring
        )
        
        return {"id": expense_id, "message": "Expense created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/expenses")
async def get_expenses(days: int = Query(30), category: Optional[str] = None):
    """Get expenses with optional filtering"""
    expenses = db.get_expenses(days=days, category=category)
    return {"expenses": expenses, "count": len(expenses)}

@app.get("/api/expenses/analytics")
async def get_expense_analytics(days: int = Query(30)):
    """Get expense analytics with predictions and anomalies"""
    expenses = db.get_expenses(days=days)
    
    # Get predictions
    predictions = ml_engine.predict_spending(expenses, months_ahead=1)
    
    # Detect anomalies
    anomalies = ml_engine.detect_anomalies(expenses, sensitivity=0.15)
    
    # Analyze patterns
    patterns = ml_engine.analyze_spending_patterns(expenses)
    
    return {
        "predictions": predictions,
        "anomalies": anomalies[:5],  # Top 5 anomalies
        "patterns": patterns
    }

# ===== INCOME ENDPOINTS =====
@app.post("/api/income")
async def create_income(income: IncomeCreate):
    """Add income"""
    try:
        income_id = db.add_income(
            source=income.source,
            amount=income.amount,
            description=income.description,
            payment_method=income.payment_method
        )
        return {"id": income_id, "message": "Income recorded"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/income")
async def get_income(days: int = Query(30)):
    """Get recent income"""
    income = db.get_income(days=days)
    return {"income": income, "total": sum(i['amount'] for i in income)}

# ===== DASHBOARD SUMMARY =====
@app.get("/api/dashboard")
async def get_dashboard_summary():
    """Get comprehensive financial dashboard summary"""
    summary = db.get_financial_summary()
    expenses = db.get_expenses(days=30)
    income = db.get_income(days=30)
    
    # Get insights
    budgets = db.get_budget_vs_actual()
    insights = ml_engine.generate_insights(expenses, income, budgets, [])
    
    return {
        "summary": summary,
        "budgets": budgets,
        "insights": insights,
        "timestamp": datetime.now().isoformat()
    }

# ===== BUDGET ENDPOINTS =====
@app.post("/api/budgets")
async def create_budget(budget: BudgetCreate):
    """Set budget for category"""
    try:
        budget_id = db.set_budget(
            category=budget.category,
            monthly_limit=budget.monthly_limit,
            alert_threshold=budget.alert_threshold
        )
        return {"id": budget_id, "message": "Budget set"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/budgets")
async def get_budgets():
    """Get budget vs actual spending"""
    budgets = db.get_budget_vs_actual()
    return {"budgets": budgets}

@app.get("/api/budgets/recommendations")
async def get_budget_recommendations():
    """Get AI-powered budget recommendations"""
    expenses = db.get_expenses(days=90)
    income = db.get_income(days=30)
    
    total_income = sum(i['amount'] for i in income) / 30 if income else 0
    recommendations = ml_engine.recommend_budgets(expenses, total_income)
    
    return {"recommendations": recommendations}

# ===== GOALS ENDPOINTS =====
@app.post("/api/goals")
async def create_goal(goal: GoalCreate):
    """Create financial goal"""
    try:
        goal_id = db.add_goal(
            name=goal.name,
            target_amount=goal.target_amount,
            target_date=goal.target_date,
            monthly_contribution=goal.monthly_contribution
        )
        return {"id": goal_id, "message": "Goal created"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ===== INVESTMENT ENDPOINTS =====
@app.post("/api/investments")
async def create_investment(investment: InvestmentCreate):
    """Add investment to portfolio"""
    try:
        investment_id = db.add_investment(
            name=investment.name,
            investment_type=investment.investment_type,
            quantity=investment.quantity,
            buy_price=investment.buy_price,
            ticker=investment.ticker
        )
        return {"id": investment_id, "message": "Investment added"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/investments/portfolio")
async def get_portfolio():
    """Get investment portfolio summary"""
    summary = db.get_portfolio_summary()
    return {"portfolio": summary}

# ===== EXCHANGE RATES =====
@app.get("/api/exchange-rates")
async def get_exchange_rates(from_currency: str = "UGX", to_currency: str = "USD"):
    """Get current exchange rates"""
    try:
        rate = exchange_provider.get_rate(from_currency, to_currency)
        return {"from": from_currency, "to": to_currency, "rate": rate}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ===== ANALYTICS =====
@app.get("/api/analytics/trends")
async def get_spending_trends(days: int = Query(90)):
    """Get spending trends over time"""
    expenses = db.get_expenses(days=days)
    
    # Group by month
    import pandas as pd
    df = pd.DataFrame(expenses)
    if len(df) > 0:
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M').astype(str)
        trends = df.groupby('month')['amount'].sum().to_dict()
    else:
        trends = {}
    
    return {"trends": trends}

# ===== ML PREDICTIONS =====
@app.get("/api/ml/predictions")
async def get_ml_predictions(month: Optional[str] = None):
    """Get ML predictions for spending"""
    if not month:
        month = datetime.now().strftime('%Y-%m')
    
    expenses = db.get_expenses(days=90)
    predictions = ml_engine.predict_spending(expenses, months_ahead=1)
    
    return {"month": month, "predictions": predictions}

@app.get("/api/ml/anomalies")
async def get_anomalies():
    """Get detected spending anomalies"""
    expenses = db.get_expenses(days=30)
    anomalies = ml_engine.detect_anomalies(expenses, sensitivity=0.15)
    
    return {"anomalies": anomalies}

# ===== INSIGHTS =====
@app.get("/api/insights")
async def get_financial_insights():
    """Get AI-powered financial insights"""
    expenses = db.get_expenses(days=30)
    income = db.get_income(days=30)
    budgets = db.get_budget_vs_actual()
    
    insights = ml_engine.generate_insights(expenses, income, budgets, [])
    
    return {"insights": insights}

# ===== HEALTH CHECK =====
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# ===== RUN SERVER =====
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
