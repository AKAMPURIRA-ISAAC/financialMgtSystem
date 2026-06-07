# analytics.py - Advanced Analytics & Reporting Engine
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json

class AnalyticsEngine:
    """Advanced financial analytics and reporting"""
    
    def __init__(self, db=None):
        self.db = db
    
    def get_monthly_report(self, month: str = None) -> Dict:
        """Generate comprehensive monthly financial report"""
        if not month:
            month = datetime.now().strftime('%Y-%m')
        
        if not self.db:
            return {}
        
        # Get data for the month
        expenses = self.db.get_expenses(days=31)
        income = self.db.get_income(days=31)
        
        df_expenses = pd.DataFrame(expenses) if expenses else pd.DataFrame()
        df_income = pd.DataFrame(income) if income else pd.DataFrame()
        
        report = {
            'month': month,
            'summary': self._generate_summary(df_expenses, df_income),
            'category_breakdown': self._category_breakdown(df_expenses),
            'daily_trends': self._daily_trends(df_expenses),
            'top_transactions': self._top_transactions(df_expenses, top_n=5),
            'income_sources': self._income_breakdown(df_income),
        }
        
        return report
    
    def _generate_summary(self, df_expenses: pd.DataFrame, df_income: pd.DataFrame) -> Dict:
        """Generate summary statistics"""
        total_income = df_income['amount'].sum() if len(df_income) > 0 else 0
        total_expenses = df_expenses['amount'].sum() if len(df_expenses) > 0 else 0
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net': total_income - total_expenses,
            'savings_rate': ((total_income - total_expenses) / total_income * 100) if total_income > 0 else 0,
            'avg_daily_expense': total_expenses / 30,
            'transaction_count': len(df_expenses),
            'avg_transaction': total_expenses / len(df_expenses) if len(df_expenses) > 0 else 0,
        }
    
    def _category_breakdown(self, df: pd.DataFrame) -> Dict:
        """Get spending by category"""
        if len(df) == 0:
            return {}
        
        category_spending = df.groupby('category')['amount'].agg(['sum', 'count', 'mean']).round(2)
        
        breakdown = {}
        total = category_spending['sum'].sum()
        
        for category, row in category_spending.iterrows():
            breakdown[category] = {
                'total': row['sum'],
                'percentage': (row['sum'] / total * 100) if total > 0 else 0,
                'count': int(row['count']),
                'average': row['mean']
            }
        
        return breakdown
    
    def _daily_trends(self, df: pd.DataFrame) -> Dict:
        """Get daily spending trends"""
        if len(df) == 0:
            return {}
        
        df['date'] = pd.to_datetime(df['date'])
        df['date_only'] = df['date'].dt.date
        
        daily_spending = df.groupby('date_only')['amount'].sum().to_dict()
        
        # Convert dates to strings for JSON serialization
        return {str(date): amount for date, amount in daily_spending.items()}
    
    def _top_transactions(self, df: pd.DataFrame, top_n: int = 5) -> List[Dict]:
        """Get top N transactions"""
        if len(df) == 0:
            return []
        
        top = df.nlargest(top_n, 'amount')[['date', 'category', 'description', 'amount']]
        return top.to_dict('records')
    
    def _income_breakdown(self, df: pd.DataFrame) -> Dict:
        """Get income by source"""
        if len(df) == 0:
            return {}
        
        sources = df.groupby('source')['amount'].agg(['sum', 'count']).round(2)
        
        breakdown = {}
        total = sources['sum'].sum()
        
        for source, row in sources.iterrows():
            breakdown[source] = {
                'total': row['sum'],
                'percentage': (row['sum'] / total * 100) if total > 0 else 0,
                'count': int(row['count'])
            }
        
        return breakdown
    
    def get_quarterly_report(self, year: int, quarter: int) -> Dict:
        """Generate quarterly report"""
        months = {
            1: ['01', '02', '03'],
            2: ['04', '05', '06'],
            3: ['07', '08', '09'],
            4: ['10', '11', '12']
        }
        
        q_months = months.get(quarter, [])
        
        if not self.db:
            return {}
        
        all_expenses = self.db.get_expenses(days=90)
        all_income = self.db.get_income(days=90)
        
        df_expenses = pd.DataFrame(all_expenses) if all_expenses else pd.DataFrame()
        df_income = pd.DataFrame(all_income) if all_income else pd.DataFrame()
        
        report = {
            'period': f'{year} Q{quarter}',
            'summary': self._generate_summary(df_expenses, df_income),
            'monthly_breakdown': {},
        }
        
        return report
    
    def get_year_to_date_summary(self) -> Dict:
        """Get year-to-date summary"""
        today = datetime.now()
        days_this_year = (today - datetime(today.year, 1, 1)).days + 1
        
        if not self.db:
            return {}
        
        expenses = self.db.get_expenses(days=days_this_year)
        income = self.db.get_income(days=days_this_year)
        
        df_expenses = pd.DataFrame(expenses) if expenses else pd.DataFrame()
        df_income = pd.DataFrame(income) if income else pd.DataFrame()
        
        return self._generate_summary(df_expenses, df_income)
    
    def get_spending_forecast(self, months_ahead: int = 6) -> Dict:
        """Forecast spending for next N months"""
        if not self.db:
            return {}
        
        expenses = self.db.get_expenses(days=180)
        
        if len(expenses) < 10:
            return {'message': 'Insufficient data for forecasting'}
        
        df = pd.DataFrame(expenses)
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
        
        # Monthly totals
        monthly = df.groupby('month')['amount'].sum()
        
        # Simple exponential smoothing for forecast
        forecast = {}
        
        for category in df['category'].unique():
            cat_data = df[df['category'] == category].groupby('month')['amount'].sum()
            
            if len(cat_data) >= 3:
                # Use simple moving average
                avg = cat_data.mean()
                forecast[category] = {
                    'current_average': avg,
                    'trend': 'stable',
                    'forecast_months': [avg] * months_ahead
                }
        
        return forecast
    
    def compare_periods(self, period1_start: str, period1_end: str, 
                       period2_start: str, period2_end: str) -> Dict:
        """Compare spending between two periods"""
        if not self.db:
            return {}
        
        # Get expenses for both periods
        expenses1 = self.db.get_expenses(days=365)
        expenses2 = self.db.get_expenses(days=365)
        
        df1 = pd.DataFrame(expenses1) if expenses1 else pd.DataFrame()
        df2 = pd.DataFrame(expenses2) if expenses2 else pd.DataFrame()
        
        # Filter by date ranges
        if len(df1) > 0:
            df1['date'] = pd.to_datetime(df1['date'])
            df1 = df1[(df1['date'] >= period1_start) & (df1['date'] <= period1_end)]
        
        if len(df2) > 0:
            df2['date'] = pd.to_datetime(df2['date'])
            df2 = df2[(df2['date'] >= period2_start) & (df2['date'] <= period2_end)]
        
        total1 = df1['amount'].sum() if len(df1) > 0 else 0
        total2 = df2['amount'].sum() if len(df2) > 0 else 0
        
        change = ((total2 - total1) / total1 * 100) if total1 > 0 else 0
        
        return {
            'period1': {
                'range': f'{period1_start} to {period1_end}',
                'total': total1,
                'transactions': len(df1)
            },
            'period2': {
                'range': f'{period2_start} to {period2_end}',
                'total': total2,
                'transactions': len(df2)
            },
            'change_percentage': change,
            'trend': 'increasing' if change > 0 else 'decreasing' if change < 0 else 'stable'
        }
    
    def identify_outliers(self, threshold_sigma: float = 2.0) -> List[Dict]:
        """Identify spending outliers using standard deviation"""
        if not self.db:
            return []
        
        expenses = self.db.get_expenses(days=90)
        
        if len(expenses) < 5:
            return []
        
        df = pd.DataFrame(expenses)
        
        outliers = []
        for category in df['category'].unique():
            cat_expenses = df[df['category'] == category]['amount']
            
            if len(cat_expenses) < 3:
                continue
            
            mean = cat_expenses.mean()
            std = cat_expenses.std()
            
            if std == 0:
                continue
            
            for idx, amount in enumerate(cat_expenses):
                z_score = abs((amount - mean) / std)
                if z_score > threshold_sigma:
                    outliers.append({
                        'category': category,
                        'amount': amount,
                        'mean': mean,
                        'std': std,
                        'z_score': z_score,
                        'deviation': f'{z_score:.2f}σ'
                    })
        
        return sorted(outliers, key=lambda x: x['z_score'], reverse=True)
    
    def get_savings_potential(self) -> Dict:
        """Analyze potential savings opportunities"""
        if not self.db:
            return {}
        
        expenses = self.db.get_expenses(days=90)
        
        if len(expenses) < 10:
            return {'message': 'Insufficient data'}
        
        df = pd.DataFrame(expenses)
        category_spending = df.groupby('category')['amount'].sum()
        
        # Identify highest spending categories
        highest = category_spending.sort_values(ascending=False).head(3)
        
        potential = {}
        for category, amount in highest.items():
            # Assume 10-20% reduction potential
            potential[category] = {
                'current': amount,
                'potential_savings_10pct': amount * 0.1,
                'potential_savings_20pct': amount * 0.2,
            }
        
        total_potential = sum(v['potential_savings_10pct'] for v in potential.values())
        
        return {
            'categories': potential,
            'total_potential_savings_10pct': total_potential,
            'total_potential_savings_20pct': total_potential * 2,
        }
    
    def export_report_pdf(self, report: Dict, filename: str = "financial_report.pdf") -> str:
        """Export report as PDF (requires reportlab)"""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            
            c = canvas.Canvas(filename, pagesize=letter)
            
            # Add title
            c.setFont("Helvetica-Bold", 20)
            c.drawString(50, 750, "Financial Report")
            
            # Add content
            y = 700
            for key, value in report.items():
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, y, f"{key.upper()}")
                y -= 20
                
                if isinstance(value, dict):
                    for k, v in value.items():
                        c.setFont("Helvetica", 10)
                        c.drawString(70, y, f"{k}: {v}")
                        y -= 15
            
            c.save()
            return f"Report exported to {filename}"
        except:
            return "PDF export requires reportlab library"
