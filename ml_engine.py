# ml_engine.py - Advanced Machine Learning for Financial Intelligence
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import json
import warnings

warnings.filterwarnings('ignore')

class MLEngine:
    """AI/ML Engine for Financial Intelligence"""
    
    def __init__(self, db=None):
        self.db = db
        self.scalers = {}
        self.encoders = {}
        self.models = {}
        self.category_model = None
        self.scaler = StandardScaler()
        
    # ===== ANOMALY DETECTION =====
    def detect_anomalies(self, expenses: List[Dict], sensitivity: float = 0.1) -> List[Dict]:
        """
        Detect anomalous spending patterns using Isolation Forest
        Sensitivity: 0-1, higher = more sensitive to anomalies
        """
        if len(expenses) < 5:
            return []
        
        df = pd.DataFrame(expenses)
        
        # Feature engineering
        features = []
        dates = []
        expense_ids = []
        
        for expense in expenses:
            try:
                amount = float(expense.get('amount', 0))
                date = expense.get('date', '')
                expense_ids.append(expense.get('id', 0))
                dates.append(date)
                
                # Extract features
                hour = int(date.split()[1].split(':')[0]) if ' ' in date else 0
                dow = datetime.fromisoformat(date).weekday() if ' ' in date else 0
                
                features.append([amount, hour, dow])
            except:
                continue
        
        if len(features) < 5:
            return []
        
        X = np.array(features)
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Isolation Forest
        contamination = min(sensitivity, 0.5)
        iso_forest = IsolationForest(contamination=contamination, random_state=42)
        predictions = iso_forest.fit_predict(X_scaled)
        scores = iso_forest.score_samples(X_scaled)
        
        # Collect anomalies
        anomalies = []
        for i, (pred, score) in enumerate(zip(predictions, scores)):
            if pred == -1:  # Anomaly
                anomaly_score = abs(score) * 100
                anomalies.append({
                    'expense_id': expense_ids[i],
                    'anomaly_score': anomaly_score,
                    'alert_type': 'unusual_amount' if features[i][0] > np.mean([f[0] for f in features]) * 2 else 'unusual_pattern',
                    'description': f"Unusual {'amount' if anomaly_score > 70 else 'pattern'} detected"
                })
        
        return sorted(anomalies, key=lambda x: x['anomaly_score'], reverse=True)
    
    # ===== SPENDING PREDICTION =====
    def predict_spending(self, expenses: List[Dict], months_ahead: int = 1) -> Dict:
        """
        Predict future spending using Gradient Boosting
        Returns predictions for next N months by category
        """
        if len(expenses) < 10:
            return {}
        
        df = pd.DataFrame(expenses)
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
        df['year_month'] = df['date'].dt.strftime('%Y-%m')
        
        # Monthly spending by category
        monthly_spending = df.groupby(['year_month', 'category'])['amount'].sum().reset_index()
        monthly_spending.columns = ['month', 'category', 'amount']
        
        predictions = {}
        categories = df['category'].unique()
        
        for category in categories:
            cat_data = monthly_spending[monthly_spending['category'] == category].sort_values('month')
            
            if len(cat_data) < 3:
                # Use simple average if insufficient data
                predictions[category] = {
                    'predicted_amount': cat_data['amount'].mean(),
                    'confidence': 0.4
                }
                continue
            
            # Prepare training data
            cat_data['month_num'] = range(len(cat_data))
            X = cat_data[['month_num']].values
            y = cat_data['amount'].values
            
            if len(cat_data) >= 5:
                # Use Gradient Boosting
                model = GradientBoostingRegressor(n_estimators=50, random_state=42)
                model.fit(X, y)
                
                # Predict next month
                next_month = len(cat_data)
                prediction = model.predict([[next_month]])[0]
                
                # Confidence based on trend consistency
                residuals = np.abs(y - model.predict(X))
                cv = np.std(residuals) / np.mean(y) if np.mean(y) > 0 else 1
                confidence = 1 - min(cv, 1)
            else:
                prediction = np.mean(y)
                confidence = 0.5
            
            predictions[category] = {
                'predicted_amount': max(0, prediction),
                'confidence': confidence,
                'historical_avg': cat_data['amount'].mean(),
                'trend': 'up' if len(cat_data) > 2 and cat_data['amount'].iloc[-1] > cat_data['amount'].iloc[0] else 'down'
            }
        
        return predictions
    
    # ===== AUTO-CATEGORIZATION =====
    def train_categorizer(self, expenses: List[Dict]) -> bool:
        """Train expense categorizer using Random Forest"""
        if len(expenses) < 20:
            return False
        
        df = pd.DataFrame(expenses)
        
        # Feature engineering from description
        descriptions = df.get('description', [''] * len(df)).fillna('')
        
        # Create simple features
        features = []
        for desc in descriptions:
            words = str(desc).lower().split()
            features.append({
                'word_count': len(words),
                'has_numbers': any(c.isdigit() for c in desc),
                'first_word_length': len(words[0]) if words else 0,
            })
        
        feature_df = pd.DataFrame(features)
        categories = df['category'].values
        
        # Train classifier
        try:
            X = feature_df.values
            y_encoded = pd.Categorical(categories).codes
            
            self.category_model = RandomForestClassifier(n_estimators=20, random_state=42)
            self.category_model.fit(X, y_encoded)
            self.category_encoder = pd.Categorical(categories)
            
            return True
        except:
            return False
    
    def categorize_expense(self, description: str) -> Tuple[str, float]:
        """Auto-categorize expense based on description"""
        if not self.category_model or not hasattr(self, 'category_encoder'):
            return "Other", 0.5
        
        words = str(description).lower().split()
        features = np.array([[
            len(words),
            any(c.isdigit() for c in description),
            len(words[0]) if words else 0
        ]])
        
        try:
            prediction = self.category_model.predict(features)[0]
            confidence = self.category_model.predict_proba(features).max()
            category = self.category_encoder.categories[prediction]
            return category, float(confidence)
        except:
            return "Other", 0.5
    
    # ===== BUDGET RECOMMENDATIONS =====
    def recommend_budgets(self, expenses: List[Dict], income_avg: float) -> Dict:
        """
        AI-powered budget recommendations
        Uses 50/30/20 rule with category analysis
        """
        df = pd.DataFrame(expenses)
        
        # Last 3 months average spending by category
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
        
        monthly_by_category = df.groupby(['month', 'category'])['amount'].sum().reset_index()
        avg_by_category = monthly_by_category.groupby('category')['amount'].mean()
        
        total_avg_spending = avg_by_category.sum()
        
        recommendations = {}
        
        # Prioritize: Needs > Wants > Savings
        needs_categories = ['groceries', 'utilities', 'rent', 'transport', 'healthcare', 'education']
        wants_categories = ['entertainment', 'dining', 'shopping', 'leisure']
        
        total_income = income_avg * 30  # Monthly equivalent
        
        if total_income > 0:
            for category, amount in avg_by_category.items():
                category_lower = category.lower()
                percentage = (amount / total_income) * 100
                
                # Smart recommendation
                if category_lower in needs_categories:
                    recommended = total_income * 0.5  # 50% for needs
                elif category_lower in wants_categories:
                    recommended = total_income * 0.3  # 30% for wants
                else:
                    recommended = total_income * 0.2  # 20% for savings/other
                
                recommendations[category] = {
                    'current_average': amount,
                    'recommended_budget': recommended,
                    'confidence': 0.7 if len(avg_by_category) > 3 else 0.5,
                    'category_type': 'need' if category_lower in needs_categories else 'want' if category_lower in wants_categories else 'other'
                }
        
        return recommendations
    
    # ===== FINANCIAL INSIGHTS =====
    def generate_insights(self, expenses: List[Dict], income: List[Dict], 
                         budgets: Dict, goals: List[Dict]) -> List[str]:
        """Generate AI-powered financial insights"""
        insights = []
        
        if not expenses or not income:
            return ["Start tracking expenses and income to get personalized insights"]
        
        df_expenses = pd.DataFrame(expenses)
        df_income = pd.DataFrame(income)
        
        total_expenses = df_expenses['amount'].sum()
        total_income = df_income['amount'].sum()
        
        # Insight 1: Savings rate
        if total_income > 0:
            savings_rate = ((total_income - total_expenses) / total_income) * 100
            if savings_rate < 10:
                insights.append(f"⚠️ Your savings rate is only {savings_rate:.1f}%. Consider reducing expenses.")
            elif savings_rate > 30:
                insights.append(f"✅ Great! You're saving {savings_rate:.1f}% of your income.")
        
        # Insight 2: Top spending category
        category_spending = df_expenses.groupby('category')['amount'].sum().sort_values(ascending=False)
        if len(category_spending) > 0:
            top_category = category_spending.index[0]
            top_pct = (category_spending.iloc[0] / total_expenses) * 100
            insights.append(f"💸 Your biggest spending is {top_category} ({top_pct:.1f}% of total)")
        
        # Insight 3: Budget alerts
        if budgets:
            for category, data in budgets.items():
                if data['percentage'] > 100:
                    insights.append(f"🚨 You've exceeded your {category} budget by {data['percentage'] - 100:.0f}%!")
                elif data['percentage'] > 80:
                    insights.append(f"⚡ {category} is at {data['percentage']:.0f}% of budget")
        
        # Insight 4: Goal progress
        if goals:
            for goal in goals:
                progress = goal.get('progress_percentage', 0)
                if progress >= 100:
                    insights.append(f"🎉 Goal '{goal['name']}' is complete!")
                elif progress >= 50:
                    insights.append(f"📈 '{goal['name']}' is {progress:.0f}% complete")
        
        return insights if insights else ["Keep tracking to unlock personalized insights"]
    
    # ===== PATTERN ANALYSIS =====
    def analyze_spending_patterns(self, expenses: List[Dict]) -> Dict:
        """Analyze spending patterns over time"""
        if len(expenses) < 5:
            return {}
        
        df = pd.DataFrame(expenses)
        df['date'] = pd.to_datetime(df['date'])
        df['day_of_week'] = df['date'].dt.day_name()
        df['hour'] = df['date'].dt.hour
        
        patterns = {
            'peak_day': df['day_of_week'].value_counts().index[0] if len(df) > 0 else "Unknown",
            'peak_hour': df['hour'].mode()[0] if len(df) > 0 else 0,
            'avg_transaction': df['amount'].mean(),
            'max_transaction': df['amount'].max(),
            'transaction_frequency': len(df),
            'category_distribution': df['category'].value_counts().to_dict()
        }
        
        return patterns
