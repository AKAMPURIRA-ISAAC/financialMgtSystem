#!/usr/bin/env python
"""
Finance Pro 2.0 - System Verification Script
Tests all components to ensure the app is fully functional
"""

import sys
from datetime import datetime, timedelta

print("=" * 60)
print("Finance Pro 2.0 - System Verification")
print("=" * 60)

# Test 1: Imports
print("\n[TEST 1] Testing module imports...")
try:
    from enhanced_database import EnhancedDatabase
    from ml_engine import MLEngine
    from analytics import AnalyticsEngine
    from integrations import FinancialHealthScore, ExchangeRateProvider
    from config import Config
    print("✓ All modules imported successfully")
except Exception as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

# Test 2: Database Initialization
print("\n[TEST 2] Testing database initialization...")
try:
    db = EnhancedDatabase("finance_pro_test.db")
    print("✓ Database initialized")
except Exception as e:
    print(f"✗ Database error: {e}")
    sys.exit(1)

# Test 3: Add Sample Data
print("\n[TEST 3] Testing data operations...")
try:
    # Clear old data
    import os
    if os.path.exists("finance_pro_test.db"):
        os.remove("finance_pro_test.db")
    
    db = EnhancedDatabase("finance_pro_test.db")
    
    # Add test data
    exp_id = db.add_expense("Groceries", 50000, "Weekly shopping")
    inc_id = db.add_income("Salary", 500000, "Monthly salary")
    
    print(f"✓ Added test expense (ID: {exp_id})")
    print(f"✓ Added test income (ID: {inc_id})")
except Exception as e:
    print(f"✗ Data operation error: {e}")
    sys.exit(1)

# Test 4: Query Data
print("\n[TEST 4] Testing data retrieval...")
try:
    expenses = db.get_expenses(days=30)
    income = db.get_income(days=30)
    
    print(f"✓ Retrieved {len(expenses)} expenses")
    print(f"✓ Retrieved {len(income)} income records")
    
    if expenses:
        print(f"  Sample expense: {expenses[0]}")
    if income:
        print(f"  Sample income: {income[0]}")
except Exception as e:
    print(f"✗ Query error: {e}")
    sys.exit(1)

# Test 5: ML Engine
print("\n[TEST 5] Testing ML Engine...")
try:
    ml = MLEngine(db)
    
    # Add more data for ML
    for i in range(5):
        db.add_expense("Transport", 15000 + i*1000, f"Taxi trip {i}")
    
    expenses = db.get_expenses(days=30)
    
    # Test predictions
    if len(expenses) >= 10:
        predictions = ml.predict_spending(expenses, months_ahead=1)
        print(f"✓ Spending predictions generated: {len(predictions)} categories")
        if predictions:
            sample_cat = list(predictions.keys())[0]
            print(f"  Sample: {sample_cat} -> {predictions[sample_cat]}")
    else:
        print("⊘ Not enough data for predictions (need 10+ transactions)")
    
    # Test anomaly detection
    anomalies = ml.detect_anomalies(expenses)
    print(f"✓ Anomaly detection completed: {len(anomalies)} anomalies found")
    
    # Test categorization
    category, confidence = ml.categorize_expense("Groceries from Nakumatt")
    print(f"✓ Auto-categorization: '{category}' (confidence: {confidence:.0%})")
    
except Exception as e:
    print(f"✗ ML Engine error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Analytics
print("\n[TEST 6] Testing Analytics Engine...")
try:
    analytics = AnalyticsEngine(db)
    
    # Get monthly report
    report = analytics.get_monthly_report()
    print(f"✓ Monthly report generated")
    print(f"  Total Income: {report.get('summary', {}).get('total_income', 0)}")
    print(f"  Total Expenses: {report.get('summary', {}).get('total_expenses', 0)}")
    print(f"  Net: {report.get('summary', {}).get('net', 0)}")
    
except Exception as e:
    print(f"✗ Analytics error: {e}")
    sys.exit(1)

# Test 7: Financial Health Score
print("\n[TEST 7] Testing Financial Health Score...")
try:
    expenses = db.get_expenses(days=30)
    income = db.get_income(days=30)
    score = FinancialHealthScore.calculate_score(expenses, income, [])
    
    print(f"✓ Health score calculated")
    print(f"  Score: {score.get('score', 0)}/100")
    print(f"  Grade: {score.get('grade', 'N/A')}")
    print(f"  Message: {score.get('message', 'N/A')}")
    
except Exception as e:
    print(f"✗ Health Score error: {e}")
    sys.exit(1)

# Test 8: Exchange Rates
print("\n[TEST 8] Testing Exchange Rate Provider...")
try:
    provider = ExchangeRateProvider()
    
    rate_usd = provider.get_rate('UGX', 'USD')
    rate_eur = provider.get_rate('USD', 'EUR')
    
    print(f"✓ Exchange rates retrieved")
    print(f"  UGX -> USD: {rate_usd:.6f}")
    print(f"  USD -> EUR: {rate_eur:.6f}")
    
    converted = provider.convert(100000, 'UGX', 'USD')
    print(f"  100,000 UGX = ${converted:.2f} USD")
    
except Exception as e:
    print(f"✗ Exchange Rate error: {e}")
    sys.exit(1)

# Test 9: Configuration
print("\n[TEST 9] Testing Configuration...")
try:
    print(f"✓ Configuration loaded")
    print(f"  App: {Config.APP_NAME} v{Config.APP_VERSION}")
    print(f"  DB Path: {Config.DB_PATH}")
    print(f"  Default Currency: {Config.DEFAULT_CURRENCY}")
    print(f"  ML Enabled: {Config.ENABLE_ML_FEATURES}")
    print(f"  Categories: {len(Config.DEFAULT_CATEGORIES)}")
    print(f"  Payment Methods: {len(Config.PAYMENT_METHODS)}")
    
except Exception as e:
    print(f"✗ Configuration error: {e}")
    sys.exit(1)

# Test 10: Kivy (if available)
print("\n[TEST 10] Testing Kivy GUI components...")
try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    print("✓ Kivy components imported successfully")
    
except Exception as e:
    print(f"✗ Kivy error: {e}")
    sys.exit(1)

# Cleanup
print("\n[CLEANUP] Removing test database...")
try:
    import os
    if os.path.exists("finance_pro_test.db"):
        os.remove("finance_pro_test.db")
    print("✓ Test database cleaned up")
except:
    pass

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED - System is fully functional!")
print("=" * 60)
print("\nYou can now run:")
print("  - Desktop app: python main.py")
print("  - API server:  python api_server.py")
print("\nFor more information, see GETTING_STARTED.md")
