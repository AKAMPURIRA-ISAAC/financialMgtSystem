# database.py - Professional Database Layer
import sqlite3
from datetime import datetime, timedelta
from contextlib import contextmanager

class Database:
    def __init__(self, db_path="finance_pro.db"):
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
        """Initialize all tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Expenses table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT,
                    amount REAL NOT NULL,
                    payment_method TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Income table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS income (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    source TEXT NOT NULL,
                    description TEXT,
                    amount REAL NOT NULL,
                    payment_method TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Budgets table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT UNIQUE,
                    monthly_limit REAL,
                    month_year TEXT
                )
            ''')
            
            conn.commit()
    
    def add_expense(self, category, description, amount, payment_method):
        """Add a new expense"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''
                INSERT INTO expenses (date, category, description, amount, payment_method)
                VALUES (?, ?, ?, ?, ?)
            ''', (current_date, category, description, amount, payment_method))
            conn.commit()
            return cursor.lastrowid
    
    def add_income(self, source, description, amount, payment_method):
        """Add new income"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''
                INSERT INTO income (date, source, description, amount, payment_method)
                VALUES (?, ?, ?, ?, ?)
            ''', (current_date, source, description, amount, payment_method))
            conn.commit()
            return cursor.lastrowid
    
    def get_today_stats(self):
        """Get today's statistics"""
        today = datetime.now().strftime('%Y-%m-%d')
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Today's expenses
            cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE date LIKE ?', (f'{today}%',))
            today_expenses = cursor.fetchone()[0]
            
            # Today's income
            cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM income WHERE date LIKE ?', (f'{today}%',))
            today_income = cursor.fetchone()[0]
            
            return {'expenses': today_expenses, 'income': today_income}
    
    def get_monthly_stats(self):
        """Get monthly statistics"""
        current_month = datetime.now().strftime('%Y-%m')
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Monthly expenses
            cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE date LIKE ?', (f'{current_month}%',))
            month_expenses = cursor.fetchone()[0]
            
            # Monthly income
            cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM income WHERE date LIKE ?', (f'{current_month}%',))
            month_income = cursor.fetchone()[0]
            
            # Category breakdown
            cursor.execute('''
                SELECT category, SUM(amount) as total 
                FROM expenses 
                WHERE date LIKE ? 
                GROUP BY category 
                ORDER BY total DESC
            ''', (f'{current_month}%',))
            categories = cursor.fetchall()
            
            return {
                'expenses': month_expenses,
                'income': month_income,
                'savings': month_income - month_expenses,
                'categories': [dict(cat) for cat in categories]
            }
    
    def get_recent_transactions(self, limit=20):
        """Get recent transactions"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get expenses
            cursor.execute('''
                SELECT 'expense' as type, date, category as title, description, amount, payment_method
                FROM expenses 
                ORDER BY date DESC 
                LIMIT ?
            ''', (limit,))
            expenses = cursor.fetchall()
            
            # Get income
            cursor.execute('''
                SELECT 'income' as type, date, source as title, description, amount, payment_method
                FROM income 
                ORDER BY date DESC 
                LIMIT ?
            ''', (limit,))
            incomes = cursor.fetchall()
            
            # Combine and sort
            all_transactions = list(expenses) + list(incomes)
            all_transactions.sort(key=lambda x: x['date'], reverse=True)
            
            return all_transactions[:limit]
    
    def get_balance(self):
        """Calculate current balance"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            current_month = datetime.now().strftime('%Y-%m')
            
            cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE date LIKE ?', (f'{current_month}%',))
            total_expenses = cursor.fetchone()[0]
            
            cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM income WHERE date LIKE ?', (f'{current_month}%',))
            total_income = cursor.fetchone()[0]
            
            return total_income - total_expenses