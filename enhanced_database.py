# enhanced_database.py - Advanced Database Layer with ML Support
import sqlite3
from datetime import datetime, timedelta
from contextlib import contextmanager
from typing import List, Dict, Optional, Tuple
import json

class EnhancedDatabase:
    """Professional Database Layer with ML, Analytics, and Advanced Features"""
    
    def __init__(self, db_path: str = "finance_pro_advanced.db"):
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize all tables with advanced features"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Enhanced Expenses table with ML features
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    category TEXT NOT NULL,
                    subcategory TEXT,
                    description TEXT,
                    amount REAL NOT NULL,
                    payment_method TEXT,
                    tags TEXT,
                    recurring BOOLEAN DEFAULT 0,
                    recurring_frequency TEXT,
                    is_flagged BOOLEAN DEFAULT 0,
                    anomaly_score REAL,
                    auto_categorized BOOLEAN DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(date, category, description, amount)
                )
            ''')
            
            # Enhanced Income table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS income (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    source TEXT NOT NULL,
                    description TEXT,
                    amount REAL NOT NULL,
                    payment_method TEXT,
                    recurring BOOLEAN DEFAULT 0,
                    recurring_frequency TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Smart Budgets with AI recommendations
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    monthly_limit REAL NOT NULL,
                    alert_threshold REAL DEFAULT 80,
                    ai_recommended BOOLEAN DEFAULT 0,
                    confidence_score REAL,
                    month_year TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(category, month_year)
                )
            ''')
            
            # Financial Goals
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS financial_goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    target_amount REAL NOT NULL,
                    current_amount REAL DEFAULT 0,
                    target_date TEXT,
                    priority INTEGER DEFAULT 0,
                    category TEXT,
                    monthly_contribution REAL,
                    progress_percentage REAL DEFAULT 0,
                    status TEXT DEFAULT 'active',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Investment Portfolio
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS investments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    ticker TEXT,
                    investment_type TEXT,
                    quantity REAL,
                    buy_price REAL,
                    current_price REAL,
                    purchase_date TEXT,
                    current_value REAL,
                    gain_loss REAL,
                    gain_loss_percentage REAL,
                    currency TEXT DEFAULT 'UGX',
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # ML Predictions Cache
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ml_predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prediction_type TEXT,
                    month TEXT NOT NULL,
                    category TEXT,
                    predicted_amount REAL,
                    confidence REAL,
                    actual_amount REAL,
                    model_version TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(prediction_type, month, category)
                )
            ''')
            
            # Anomaly Alerts
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS anomaly_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    expense_id INTEGER,
                    alert_type TEXT,
                    anomaly_score REAL,
                    description TEXT,
                    severity TEXT,
                    dismissed BOOLEAN DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(expense_id) REFERENCES expenses(id)
                )
            ''')
            
            # Bank Integrations
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bank_accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bank_name TEXT NOT NULL,
                    account_type TEXT,
                    balance REAL,
                    currency TEXT DEFAULT 'UGX',
                    is_synced BOOLEAN DEFAULT 0,
                    last_sync TEXT,
                    api_token TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Exchange Rates Cache
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS exchange_rates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_currency TEXT,
                    to_currency TEXT,
                    rate REAL,
                    timestamp TEXT,
                    source TEXT
                )
            ''')
            
            # User Preferences & Settings
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setting_key TEXT UNIQUE NOT NULL,
                    setting_value TEXT,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Activity Log
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT,
                    entity_type TEXT,
                    entity_id INTEGER,
                    old_value TEXT,
                    new_value TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create Indexes for Performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_expenses_category ON expenses(category)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_income_date ON income(date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_anomaly_alerts_created ON anomaly_alerts(created_at)')
            
            conn.commit()
    
    # ===== EXPENSE OPERATIONS =====
    def add_expense(self, category: str, amount: float, description: str = "", 
                   payment_method: str = "Cash", tags: str = "", 
                   recurring: bool = False, recurring_frequency: str = None) -> int:
        """Add a new expense with advanced features"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''
                INSERT INTO expenses 
                (date, category, description, amount, payment_method, tags, recurring, recurring_frequency)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (current_date, category, description, amount, payment_method, tags, recurring, recurring_frequency))
            conn.commit()
            return cursor.lastrowid
    
    def get_expenses(self, days: int = 30, category: str = None) -> List[Dict]:
        """Get expenses for analytics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            date_threshold = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            if category:
                cursor.execute('''
                    SELECT * FROM expenses 
                    WHERE date >= ? AND category = ? 
                    ORDER BY date DESC
                ''', (date_threshold, category))
            else:
                cursor.execute('''
                    SELECT * FROM expenses 
                    WHERE date >= ? 
                    ORDER BY date DESC
                ''', (date_threshold,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_expense_by_category_period(self, start_date: str, end_date: str) -> Dict:
        """Get expenses grouped by category for a period"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT category, SUM(amount) as total 
                FROM expenses 
                WHERE date BETWEEN ? AND ? 
                GROUP BY category
            ''', (start_date, end_date))
            return {row['category']: row['total'] for row in cursor.fetchall()}
    
    # ===== INCOME OPERATIONS =====
    def add_income(self, source: str, amount: float, description: str = "", 
                  payment_method: str = "Bank Transfer", recurring: bool = False,
                  recurring_frequency: str = None) -> int:
        """Add income"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''
                INSERT INTO income 
                (date, source, description, amount, payment_method, recurring, recurring_frequency)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (current_date, source, description, amount, payment_method, recurring, recurring_frequency))
            conn.commit()
            return cursor.lastrowid
    
    def get_income(self, days: int = 30) -> List[Dict]:
        """Get recent income"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            date_threshold = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            cursor.execute('''
                SELECT * FROM income 
                WHERE date >= ? 
                ORDER BY date DESC
            ''', (date_threshold,))
            return [dict(row) for row in cursor.fetchall()]
    
    # ===== BUDGET OPERATIONS =====
    def set_budget(self, category: str, monthly_limit: float, alert_threshold: float = 80,
                  ai_recommended: bool = False, confidence_score: float = None) -> int:
        """Set or update budget for a category"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            month_year = datetime.now().strftime('%Y-%m')
            
            cursor.execute('''
                INSERT OR REPLACE INTO budgets 
                (category, monthly_limit, alert_threshold, ai_recommended, confidence_score, month_year)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (category, monthly_limit, alert_threshold, ai_recommended, confidence_score, month_year))
            conn.commit()
            return cursor.lastrowid
    
    def get_budget_vs_actual(self, month_year: str = None) -> Dict:
        """Get budget vs actual spending"""
        if not month_year:
            month_year = datetime.now().strftime('%Y-%m')
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT b.category, b.monthly_limit, 
                       COALESCE(SUM(e.amount), 0) as actual_spending
                FROM budgets b
                LEFT JOIN expenses e ON b.category = e.category 
                                   AND strftime('%Y-%m', e.date) = ?
                WHERE b.month_year = ?
                GROUP BY b.category
            ''', (month_year, month_year))
            
            result = {}
            for row in cursor.fetchall():
                result[row['category']] = {
                    'budget': row['monthly_limit'],
                    'actual': row['actual_spending'],
                    'remaining': row['monthly_limit'] - row['actual_spending'],
                    'percentage': (row['actual_spending'] / row['monthly_limit'] * 100) if row['monthly_limit'] > 0 else 0
                }
            return result
    
    # ===== GOAL OPERATIONS =====
    def add_goal(self, name: str, target_amount: float, target_date: str = None, 
                category: str = "", monthly_contribution: float = 0) -> int:
        """Add financial goal"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO financial_goals 
                (name, target_amount, target_date, category, monthly_contribution)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, target_amount, target_date, category, monthly_contribution))
            conn.commit()
            return cursor.lastrowid
    
    def update_goal_progress(self, goal_id: int, current_amount: float):
        """Update goal progress"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT target_amount FROM financial_goals WHERE id = ?', (goal_id,))
            row = cursor.fetchone()
            
            if row:
                progress = (current_amount / row['target_amount'] * 100) if row['target_amount'] > 0 else 0
                cursor.execute('''
                    UPDATE financial_goals 
                    SET current_amount = ?, progress_percentage = ?
                    WHERE id = ?
                ''', (current_amount, progress, goal_id))
                conn.commit()
    
    # ===== INVESTMENT OPERATIONS =====
    def add_investment(self, name: str, investment_type: str, quantity: float, 
                      buy_price: float, ticker: str = None, currency: str = "UGX") -> int:
        """Add investment"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            current_date = datetime.now().strftime('%Y-%m-%d')
            current_value = quantity * buy_price
            
            cursor.execute('''
                INSERT INTO investments 
                (name, ticker, investment_type, quantity, buy_price, current_price, 
                 purchase_date, current_value, currency)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, ticker, investment_type, quantity, buy_price, buy_price, 
                  current_date, current_value, currency))
            conn.commit()
            return cursor.lastrowid
    
    def update_investment_price(self, investment_id: int, current_price: float):
        """Update investment current price"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT quantity, buy_price FROM investments WHERE id = ?', (investment_id,))
            row = cursor.fetchone()
            
            if row:
                current_value = row['quantity'] * current_price
                gain_loss = current_value - (row['quantity'] * row['buy_price'])
                gain_loss_percentage = (gain_loss / (row['quantity'] * row['buy_price']) * 100) if row['quantity'] * row['buy_price'] > 0 else 0
                
                cursor.execute('''
                    UPDATE investments 
                    SET current_price = ?, current_value = ?, gain_loss = ?, 
                        gain_loss_percentage = ?, updated_at = ?
                    WHERE id = ?
                ''', (current_price, current_value, gain_loss, gain_loss_percentage,
                      datetime.now().strftime('%Y-%m-%d %H:%M:%S'), investment_id))
                conn.commit()
    
    def get_portfolio_summary(self) -> Dict:
        """Get investment portfolio summary"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT SUM(current_value) as total_value, SUM(gain_loss) as total_gain_loss FROM investments')
            row = cursor.fetchone()
            return {
                'total_value': row['total_value'] or 0,
                'total_gain_loss': row['total_gain_loss'] or 0,
                'gain_loss_percentage': ((row['total_gain_loss'] or 0) / (row['total_value'] or 1)) * 100
            }
    
    # ===== ML & PREDICTIONS =====
    def save_prediction(self, prediction_type: str, month: str, predicted_amount: float,
                       confidence: float, category: str = None, model_version: str = "1.0"):
        """Save ML prediction"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO ml_predictions 
                (prediction_type, month, category, predicted_amount, confidence, model_version)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (prediction_type, month, category, predicted_amount, confidence, model_version))
            conn.commit()
    
    def get_predictions(self, month: str, prediction_type: str = None) -> List[Dict]:
        """Get predictions for a month"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if prediction_type:
                cursor.execute('''
                    SELECT * FROM ml_predictions 
                    WHERE month = ? AND prediction_type = ?
                ''', (month, prediction_type))
            else:
                cursor.execute('SELECT * FROM ml_predictions WHERE month = ?', (month,))
            return [dict(row) for row in cursor.fetchall()]
    
    # ===== ANOMALY DETECTION =====
    def flag_anomaly(self, expense_id: int, alert_type: str, anomaly_score: float,
                    description: str = "", severity: str = "medium"):
        """Flag anomalous expense"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO anomaly_alerts 
                (expense_id, alert_type, anomaly_score, description, severity)
                VALUES (?, ?, ?, ?, ?)
            ''', (expense_id, alert_type, anomaly_score, description, severity))
            conn.commit()
    
    def get_active_anomalies(self) -> List[Dict]:
        """Get active anomaly alerts"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM anomaly_alerts 
                WHERE dismissed = 0 
                ORDER BY created_at DESC
            ''')
            return [dict(row) for row in cursor.fetchall()]
    
    # ===== STATISTICS & ANALYTICS =====
    def get_financial_summary(self) -> Dict:
        """Get comprehensive financial summary"""
        today = datetime.now().strftime('%Y-%m-%d')
        current_month = datetime.now().strftime('%Y-%m')
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Today's stats
            cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE date LIKE ?', (f'{today}%',))
            today_expenses = cursor.fetchone()[0]
            
            cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM income WHERE date LIKE ?', (f'{today}%',))
            today_income = cursor.fetchone()[0]
            
            # Month stats
            cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE strftime("%Y-%m", date) = ?', (current_month,))
            month_expenses = cursor.fetchone()[0]
            
            cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM income WHERE strftime("%Y-%m", date) = ?', (current_month,))
            month_income = cursor.fetchone()[0]
            
            return {
                'today_income': today_income,
                'today_expenses': today_expenses,
                'today_balance': today_income - today_expenses,
                'month_income': month_income,
                'month_expenses': month_expenses,
                'month_balance': month_income - month_expenses,
            }
