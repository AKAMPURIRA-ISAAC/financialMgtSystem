# integrations.py - External Integrations & Utilities
try:
    import requests
except ImportError:
    requests = None
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import json

class ExchangeRateProvider:
    """Exchange rate provider for multi-currency support"""
    
    def __init__(self):
        self.cache = {}
        self.cache_duration = timedelta(hours=1)
        self.last_fetch = {}
    
    def get_rate(self, from_currency: str, to_currency: str) -> float:
        """Get exchange rate between two currencies"""
        
        # Check cache first
        cache_key = f"{from_currency}_{to_currency}"
        if cache_key in self.cache:
            cached_time, rate = self.cache[cache_key]
            if datetime.now() - cached_time < self.cache_duration:
                return rate
        
        try:
            # Using free API
            if not requests:
                raise ImportError("requests module not available")
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            rate = data['rates'].get(to_currency, 1.0)
            self.cache[cache_key] = (datetime.now(), rate)
            return rate
        except Exception as e:
            # Fallback rates (approximate)
            fallback_rates = {
                'UGX_USD': 0.00027,
                'USD_UGX': 3700,
                'UGX_EUR': 0.00025,
                'EUR_UGX': 4000,
                'UGX_GBP': 0.00021,
                'GBP_UGX': 4700,
            }
            return fallback_rates.get(cache_key, 1.0)
    
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Convert amount between currencies"""
        if from_currency == to_currency:
            return amount
        
        rate = self.get_rate(from_currency, to_currency)
        return amount * rate


class CategoryAnalyzer:
    """Analyze and manage expense categories"""
    
    # Predefined category keywords
    CATEGORY_KEYWORDS = {
        'Groceries': ['grocery', 'supermarket', 'market', 'food', 'shop', 'carrefour', 'nakumatt'],
        'Utilities': ['electricity', 'water', 'internet', 'phone', 'utility', 'bill'],
        'Transport': ['transport', 'taxi', 'bus', 'fuel', 'gas', 'car', 'bike', 'ride', 'uber', 'logistics'],
        'Entertainment': ['movie', 'cinema', 'game', 'entertainment', 'show', 'concert', 'event'],
        'Dining': ['restaurant', 'food', 'pizza', 'cafe', 'coffee', 'bar', 'meal', 'lunch', 'dinner'],
        'Healthcare': ['hospital', 'clinic', 'doctor', 'pharmacy', 'medicine', 'health'],
        'Education': ['school', 'university', 'college', 'education', 'course', 'training'],
        'Shopping': ['shop', 'mall', 'store', 'buy', 'purchase', 'clothes', 'apparel'],
        'Rent': ['rent', 'accommodation', 'house', 'apartment', 'landlord'],
        'Savings': ['savings', 'save', 'investment', 'deposit'],
    }
    
    @staticmethod
    def analyze_description(description: str) -> tuple:
        """Analyze description and suggest category"""
        description_lower = description.lower()
        
        best_match = None
        best_score = 0
        
        for category, keywords in CategoryAnalyzer.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in description_lower:
                    score = len(keyword)
                    if score > best_score:
                        best_score = score
                        best_match = category
        
        confidence = min(best_score / len(description_lower), 1.0) if description_lower else 0.5
        return best_match or "Other", confidence
    
    @staticmethod
    def get_category_color(category: str) -> str:
        """Get color for category for UI visualization"""
        colors = {
            'Groceries': '#FF6B6B',
            'Utilities': '#4ECDC4',
            'Transport': '#45B7D1',
            'Entertainment': '#FFA07A',
            'Dining': '#FFB6C1',
            'Healthcare': '#98D8C8',
            'Education': '#6C5CE7',
            'Shopping': '#A29BFE',
            'Rent': '#74B9FF',
            'Savings': '#55EFC4',
        }
        return colors.get(category, '#95A5A6')


class BudgetOptimizer:
    """Smart budget optimization using spending patterns"""
    
    @staticmethod
    def optimize_budget(spending_history: List[Dict]) -> Dict:
        """
        Optimize budget recommendations based on spending history
        Uses 50/30/20 rule with historical analysis
        """
        if not spending_history:
            return {}
        
        import pandas as pd
        df = pd.DataFrame(spending_history)
        
        # Calculate spending distribution
        total = df['amount'].sum()
        category_spending = df.groupby('category')['amount'].sum()
        
        # Categorize expenses
        essential_categories = ['Groceries', 'Rent', 'Utilities', 'Healthcare', 'Transport']
        lifestyle_categories = ['Dining', 'Entertainment', 'Shopping']
        
        essential_total = category_spending[[c for c in essential_categories if c in category_spending.index]].sum()
        lifestyle_total = category_spending[[c for c in lifestyle_categories if c in category_spending.index]].sum()
        
        essential_pct = (essential_total / total * 100) if total > 0 else 0
        lifestyle_pct = (lifestyle_total / total * 100) if total > 0 else 0
        savings_pct = 100 - essential_pct - lifestyle_pct
        
        return {
            'essential_percentage': essential_pct,
            'lifestyle_percentage': lifestyle_pct,
            'savings_percentage': savings_pct,
            'recommendations': {
                'essential': max(50, min(essential_pct, 60)),
                'lifestyle': max(20, min(lifestyle_pct, 30)),
                'savings': max(10, min(savings_pct, 30))
            }
        }


class RecurringExpenseDetector:
    """Detect and analyze recurring expenses"""
    
    @staticmethod
    def detect_recurring(expenses: List[Dict]) -> List[Dict]:
        """
        Detect recurring expenses (e.g., monthly subscriptions)
        """
        if len(expenses) < 3:
            return []
        
        import pandas as pd
        df = pd.DataFrame(expenses)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        recurring = []
        
        for category in df['category'].unique():
            cat_expenses = df[df['category'] == category]
            
            if len(cat_expenses) < 2:
                continue
            
            amounts = cat_expenses['amount'].values
            dates = cat_expenses['date'].values
            
            # Check if amounts are similar (within 10%)
            avg_amount = amounts.mean()
            if len(amounts) > 1:
                variations = [abs(a - avg_amount) / avg_amount * 100 for a in amounts]
                if all(v < 15 for v in variations):
                    # Calculate frequency
                    date_diffs = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
                    avg_frequency = sum(date_diffs) / len(date_diffs)
                    
                    frequency = 'daily' if avg_frequency < 2 else \
                               'weekly' if avg_frequency < 14 else \
                               'monthly' if avg_frequency < 60 else 'quarterly'
                    
                    recurring.append({
                        'category': category,
                        'average_amount': avg_amount,
                        'frequency': frequency,
                        'confidence': 1 - (sum(variations) / len(variations) / 100),
                        'count': len(cat_expenses)
                    })
        
        return recurring


class SpendingAlertSystem:
    """Generate alerts for spending anomalies and budget overruns"""
    
    @staticmethod
    def check_alerts(current_spending: Dict, budgets: Dict, anomalies: List[Dict]) -> List[Dict]:
        """
        Generate alerts for various spending conditions
        """
        alerts = []
        
        # Check budget overruns
        for category, data in current_spending.items():
            if category in budgets:
                budget = budgets[category]
                percentage = (data['amount'] / budget['limit'] * 100) if budget['limit'] > 0 else 0
                
                if percentage >= 100:
                    alerts.append({
                        'type': 'budget_exceeded',
                        'category': category,
                        'percentage': percentage,
                        'severity': 'high',
                        'message': f'Budget for {category} exceeded by {percentage - 100:.1f}%'
                    })
                elif percentage >= 80:
                    alerts.append({
                        'type': 'budget_warning',
                        'category': category,
                        'percentage': percentage,
                        'severity': 'medium',
                        'message': f'{category} at {percentage:.0f}% of budget'
                    })
        
        # Add anomaly alerts
        for anomaly in anomalies:
            if anomaly['anomaly_score'] > 0.8:
                alerts.append({
                    'type': 'unusual_spending',
                    'severity': 'medium',
                    'message': f"Unusual spending pattern detected: {anomaly['description']}",
                    'anomaly_score': anomaly['anomaly_score']
                })
        
        return alerts


class DataExporter:
    """Export financial data in various formats"""
    
    @staticmethod
    def export_to_csv(expenses: List[Dict], filename: str = "expenses.csv") -> str:
        """Export expenses to CSV"""
        import csv
        
        try:
            import pandas as pd
            df = pd.DataFrame(expenses)
            df.to_csv(filename, index=False)
            return f"Exported {len(expenses)} expenses to {filename}"
        except Exception as e:
            return f"Export failed: {str(e)}"
    
    @staticmethod
    def export_to_json(expenses: List[Dict], filename: str = "expenses.json") -> str:
        """Export expenses to JSON"""
        try:
            with open(filename, 'w') as f:
                json.dump(expenses, f, indent=2, default=str)
            return f"Exported {len(expenses)} expenses to {filename}"
        except Exception as e:
            return f"Export failed: {str(e)}"


class FinancialHealthScore:
    """Calculate financial health score based on multiple metrics"""
    
    @staticmethod
    def calculate_score(expenses: List[Dict], income: List[Dict], goals: List[Dict]) -> Dict:
        """
        Calculate comprehensive financial health score (0-100)
        """
        score = 50  # Base score
        
        if not income or not expenses:
            return {'score': score, 'grade': 'F', 'breakdown': {}}
        
        total_income = sum(i['amount'] for i in income)
        total_expenses = sum(e['amount'] for e in expenses)
        
        breakdown = {}
        
        # Savings rate (0-30 points)
        if total_income > 0:
            savings_rate = ((total_income - total_expenses) / total_income) * 100
            savings_score = min(savings_rate, 30)
            breakdown['savings'] = savings_score
            score += savings_score
        
        # Goals progress (0-20 points)
        if goals:
            avg_progress = sum(g.get('progress_percentage', 0) for g in goals) / len(goals)
            goals_score = min(avg_progress / 5, 20)
            breakdown['goals'] = goals_score
            score += goals_score
        
        # Category diversity (0-20 points)
        import pandas as pd
        df = pd.DataFrame(expenses)
        category_count = df['category'].nunique()
        diversity_score = min(category_count * 2, 20)
        breakdown['diversity'] = diversity_score
        score += diversity_score
        
        # Cap score at 100
        score = min(score, 100)
        
        # Determine grade
        grade = 'A' if score >= 90 else 'B' if score >= 80 else 'C' if score >= 70 else 'D' if score >= 60 else 'F'
        
        return {
            'score': score,
            'grade': grade,
            'breakdown': breakdown
        }
