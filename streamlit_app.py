import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from enhanced_database import EnhancedDatabase
from ml_engine import MLEngine
from analytics import AnalyticsEngine
from integrations import ExchangeRateProvider, FinancialHealthScore
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Finance Pro 2.0",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'db' not in st.session_state:
    st.session_state.db = EnhancedDatabase()
    st.session_state.ml_engine = MLEngine()
    st.session_state.analytics = AnalyticsEngine(st.session_state.db)
    st.session_state.exchange_provider = ExchangeRateProvider()
    st.session_state.health_scorer = FinancialHealthScore()

db = st.session_state.db
ml_engine = st.session_state.ml_engine
analytics = st.session_state.analytics
exchange_provider = st.session_state.exchange_provider
health_scorer = st.session_state.health_scorer

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("💰 Finance Pro 2.0")
    page = st.radio("Navigation", [
        "📊 Dashboard",
        "💵 Add Expense",
        "💸 Add Income",
        "📈 Analytics",
        "⚙️ Settings"
    ])

# ============================================================================
# DASHBOARD PAGE
# ============================================================================
if page == "📊 Dashboard":
    st.title("💰 Financial Dashboard")
    
    # Get financial summary
    summary = db.get_financial_summary()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Income",
            f"UGX {summary.get('month_income', 0):,.0f}",
            delta=f"{summary.get('month_income', 0) - summary.get('today_income', 0):,.0f}" if summary else None
        )
    
    with col2:
        st.metric(
            "Total Expenses",
            f"UGX {summary.get('month_expenses', 0):,.0f}",
            delta=f"{summary.get('month_expenses', 0) - summary.get('today_expenses', 0):,.0f}" if summary else None
        )
    
    with col3:
        balance = summary.get('month_income', 0) - summary.get('month_expenses', 0)
        st.metric(
            "Balance",
            f"UGX {balance:,.0f}",
            delta="Positive" if balance > 0 else "Negative"
        )
    
    with col4:
        # Calculate health score
        try:
            score_data = health_scorer.calculate_score(db)
            health_score = score_data.get('score', 0)
            grade = score_data.get('grade', 'F')
            st.metric("Financial Health", f"{grade} ({health_score}%)")
        except:
            st.metric("Financial Health", "N/A")
    
    st.divider()
    
    # Recent transactions
    st.subheader("📝 Recent Transactions")
    
    recent_expenses = db.get_expenses(days=30)[:5] if db.get_expenses(days=30) else []
    recent_income = db.get_income(days=30)[:5] if db.get_income(days=30) else []
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Recent Expenses:**")
        if recent_expenses:
            expense_df = pd.DataFrame(recent_expenses)
            expense_df['date'] = pd.to_datetime(expense_df['date'])
            st.dataframe(
                expense_df[['date', 'category', 'amount', 'description']].sort_values('date', ascending=False),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No expenses recorded yet")
    
    with col2:
        st.write("**Recent Income:**")
        if recent_income:
            income_df = pd.DataFrame(recent_income)
            income_df['date'] = pd.to_datetime(income_df['date'])
            st.dataframe(
                income_df[['date', 'source', 'amount', 'description']].sort_values('date', ascending=False),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No income recorded yet")
    
    st.divider()
    
    # AI Insights
    st.subheader("🤖 AI Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Spending Predictions:**")
        try:
            predictions = ml_engine.predict_spending()
            if predictions:
                pred_df = pd.DataFrame(predictions).head(5)
                st.dataframe(pred_df, use_container_width=True, hide_index=True)
        except:
            st.info("Running ML predictions...")
    
    with col2:
        st.write("**Anomalies Detected:**")
        try:
            anomalies = ml_engine.detect_anomalies()
            if anomalies:
                st.warning(f"⚠️ {len(anomalies)} unusual transactions detected")
                for anomaly in anomalies[:3]:
                    st.text(f"• {anomaly}")
            else:
                st.success("✅ No anomalies detected")
        except:
            st.info("Analyzing transactions...")

# ============================================================================
# ADD EXPENSE PAGE
# ============================================================================
elif page == "💵 Add Expense":
    st.title("💵 Add Expense")
    
    with st.form("expense_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.number_input("Amount (UGX)", min_value=0.0, step=1000.0)
            category = st.selectbox(
                "Category",
                ["Food", "Transport", "Utilities", "Entertainment", "Healthcare", "Shopping", "Other"]
            )
        
        with col2:
            date = st.date_input("Date", datetime.now())
            description = st.text_input("Description (optional)")
        
        payment_method = st.selectbox(
            "Payment Method",
            ["Cash", "Debit Card", "Credit Card", "Mobile Money", "Check", "Bank Transfer"]
        )
        
        submitted = st.form_submit_button("Save Expense", use_container_width=True)
        
        if submitted:
            if amount > 0:
                try:
                    db.add_expense(
                        amount=amount,
                        category=category,
                        date=str(date),
                        description=description or category,
                        payment_method=payment_method
                    )
                    st.success(f"✅ Expense saved: UGX {amount:,.0f}")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("Please enter a valid amount")

# ============================================================================
# ADD INCOME PAGE
# ============================================================================
elif page == "💸 Add Income":
    st.title("💸 Add Income")
    
    with st.form("income_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.number_input("Amount (UGX)", min_value=0.0, step=1000.0)
            source = st.selectbox(
                "Source",
                ["Salary", "Freelance", "Business", "Investment", "Gift", "Bonus", "Other"]
            )
        
        with col2:
            date = st.date_input("Date", datetime.now())
            description = st.text_input("Description (optional)")
        
        submitted = st.form_submit_button("Save Income", use_container_width=True)
        
        if submitted:
            if amount > 0:
                try:
                    db.add_income(
                        amount=amount,
                        source=source,
                        date=str(date),
                        description=description or source
                    )
                    st.success(f"✅ Income saved: UGX {amount:,.0f}")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("Please enter a valid amount")

# ============================================================================
# ANALYTICS PAGE
# ============================================================================
elif page == "📈 Analytics":
    st.title("📈 Financial Analytics")
    
    # Time period selector
    period = st.radio("Select Period", ["Monthly", "Quarterly", "Year to Date"], horizontal=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Spending by Category")
        try:
            expenses = db.get_expenses(days=90)
            if expenses:
                expense_df = pd.DataFrame(expenses)
                category_totals = expense_df.groupby('category')['amount'].sum().sort_values(ascending=False)
                
                fig = px.pie(
                    values=category_totals.values,
                    names=category_totals.index,
                    title="Expense Distribution",
                    hole=0.3
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available")
        except Exception as e:
            st.warning(f"Could not load chart: {str(e)}")
    
    with col2:
        st.subheader("💰 Income vs Expenses")
        try:
            monthly_report = analytics.get_monthly_report()
            if monthly_report:
                fig = go.Figure(data=[
                    go.Bar(name='Income', x=['This Month'], y=[monthly_report.get('income', 0)]),
                    go.Bar(name='Expenses', x=['This Month'], y=[monthly_report.get('expenses', 0)])
                ])
                fig.update_layout(barmode='group', title="Income vs Expenses")
                st.plotly_chart(fig, use_container_width=True)
        except:
            st.info("Loading data...")
    
    # Detailed analytics
    st.divider()
    st.subheader("📋 Monthly Breakdown")
    
    try:
        if period == "Monthly":
            report = analytics.get_monthly_report()
        elif period == "Quarterly":
            report = analytics.get_quarterly_report()
        else:
            report = analytics.get_year_to_date_summary()
        
        if report:
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Income", f"UGX {report.get('income', 0):,.0f}")
            col2.metric("Total Expenses", f"UGX {report.get('expenses', 0):,.0f}")
            col3.metric("Net Savings", f"UGX {report.get('income', 0) - report.get('expenses', 0):,.0f}")
    except Exception as e:
        st.warning(f"Analytics unavailable: {str(e)}")

# ============================================================================
# SETTINGS PAGE
# ============================================================================
elif page == "⚙️ Settings":
    st.title("⚙️ Settings")
    
    st.subheader("💱 Currency Exchange Rates")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        amount_ugx = st.number_input("Enter UGX amount", value=100000.0, min_value=0.0)
    
    with col2:
        currency = st.selectbox("Convert to", ["USD", "EUR", "GBP", "KES"])
    
    with col3:
        try:
            rate = exchange_provider.get_exchange_rate("UGX", currency)
            converted = amount_ugx * rate
            st.metric(f"{currency} Value", f"{converted:,.2f}", f"Rate: {rate:.4f}")
        except:
            st.warning("Could not fetch exchange rates")
    
    st.divider()
    
    st.subheader("📊 Database Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    try:
        all_expenses = db.get_expenses(days=365)
        all_income = db.get_income(days=365)
        
        col1.metric("Total Transactions", len(all_expenses) + len(all_income))
        col2.metric("Expense Records", len(all_expenses))
        col3.metric("Income Records", len(all_income))
    except:
        st.info("Loading statistics...")
    
    st.divider()
    
    st.subheader("🔧 App Information")
    st.text(f"Finance Pro 2.0")
    st.text(f"Database: SQLite")
    st.text(f"API: FastAPI")
    st.text(f"ML: scikit-learn")
    st.text(f"Version: 2.0.0")
    st.text(f"Current Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Footer
st.divider()
st.caption("💳 Finance Pro 2.0 - AI-Powered Financial Management System")
