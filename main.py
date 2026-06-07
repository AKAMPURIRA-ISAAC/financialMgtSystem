# main.py - Finance Pro 2.0 - Advanced Financial Management System
"""
Finance Pro 2.0: AI-Powered Financial Management
Features:
- Smart ML-based spending prediction & anomaly detection
- Automated expense categorization
- Advanced budget recommendations
- Investment portfolio tracking
- Real-time exchange rates
- Comprehensive financial analytics
- Web API backend (FastAPI)
- Modern Kivy UI
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock

from datetime import datetime, timedelta
from enhanced_database import EnhancedDatabase
from ml_engine import MLEngine
from analytics import AnalyticsEngine
from integrations import FinancialHealthScore
from config import Config

# Window Configuration
Window.size = (Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
Window.clearcolor = (0.95, 0.95, 0.95, 1)

# Color Scheme
COLORS = {
    'primary': (0.35, 0.2, 0.65, 1),
    'success': (0.2, 0.7, 0.3, 1),
    'danger': (0.9, 0.2, 0.2, 1),
    'warning': (1, 0.6, 0, 1),
    'dark': (0.2, 0.2, 0.2, 1),
    'light': (0.96, 0.96, 0.96, 1),
    'white': (1, 1, 1, 1),
    'text': (0.2, 0.2, 0.2, 1),
    'text_light': (0.5, 0.5, 0.5, 1),
}

class ModernButton(Button):
    """Modern button with styling"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.color = (1, 1, 1, 1)
        self.font_size = 14
        self.bold = True


class DashboardScreen(Screen):
    """Main Dashboard with AI Insights"""
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()
        Clock.schedule_interval(self.refresh_data, 60)
    
    def build_ui(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        main_layout.add_widget(self._build_header())
        main_layout.add_widget(self._build_summary_cards())
        main_layout.add_widget(self._build_ai_insights())
        main_layout.add_widget(self._build_quick_actions())
        self.add_widget(main_layout)
    
    def _build_header(self):
        """Build header"""
        header = BoxLayout(orientation='vertical', size_hint_y=0.12, spacing=5)
        title = Label(text='💰 FINANCE PRO 2.0', font_size=24, bold=True,
                     color=COLORS['primary'])
        health = self.app.get_health_score()
        health_text = f"Health: {health.get('score', 0)}/100 ({health.get('grade', 'N/A')})"
        health_label = Label(text=health_text, font_size=11, 
                            color=(0.2, 0.7, 0.3, 1) if health.get('score', 0) >= 70 else COLORS['warning'])
        header.add_widget(title)
        header.add_widget(health_label)
        return header
    
    def _build_summary_cards(self):
        """Build financial summary cards"""
        cards = GridLayout(cols=2, spacing=10, size_hint_y=0.25)
        summary = self.app.db.get_financial_summary() or {}
        
        cards.add_widget(self._create_card('Balance', f"₨{summary.get('today_balance', 0):,.0f}", COLORS['primary']))
        cards.add_widget(self._create_card('Income', f"₨{summary.get('today_income', 0):,.0f}", COLORS['success']))
        cards.add_widget(self._create_card('Expenses', f"₨{summary.get('today_expenses', 0):,.0f}", COLORS['danger']))
        cards.add_widget(self._create_card('Month', f"₨{summary.get('month_balance', 0):,.0f}", COLORS['warning']))
        
        return cards
    
    def _create_card(self, title: str, value: str, bg_color: tuple):
        """Create summary card"""
        from kivy.graphics import RoundedRectangle, Color as GraphicsColor
        card = BoxLayout(orientation='vertical', padding=10)
        try:
            if card.canvas:
                with card.canvas.before:
                    GraphicsColor(*bg_color)
                    RoundedRectangle(size=card.size, pos=card.pos, radius=[10])
        except Exception:
            pass
        card.add_widget(Label(text=f"{title}\n{value}", color=(1,1,1,1), bold=True, font_size=11))
        return card
    
    def _build_ai_insights(self):
        """Build AI insights"""
        insights_box = BoxLayout(orientation='vertical', size_hint_y=0.25, spacing=5)
        insights_box.add_widget(Label(text='🤖 AI INSIGHTS', font_size=12, bold=True, color=COLORS['primary']))
        
        try:
            expenses = self.app.db.get_expenses(days=30) or []
            income = self.app.db.get_income(days=30) or []
            budgets = self.app.db.get_budget_vs_actual() or {}
            insights = self.app.ml_engine.generate_insights(expenses, income, budgets, []) or []
            
            insights_text = '\n'.join(insights[:3]) if insights else "Add transactions to see insights"
            insights_box.add_widget(Label(text=insights_text, font_size=9, color=COLORS['text']))
        except Exception as e:
            insights_box.add_widget(Label(text=f"Insights unavailable: {str(e)[:50]}", font_size=9, color=COLORS['text_light']))
        
        return insights_box
    
    def _build_quick_actions(self):
        """Build quick action buttons"""
        actions = GridLayout(cols=2, spacing=10, size_hint_y=0.2)
        
        expense_btn = ModernButton(text='➕ Expense', background_color=COLORS['danger'])
        expense_btn.bind(on_press=lambda x: self._change_screen('add_expense'))  # type: ignore
        actions.add_widget(expense_btn)
        
        income_btn = ModernButton(text='💵 Income', background_color=COLORS['success'])
        income_btn.bind(on_press=lambda x: self._change_screen('add_income'))  # type: ignore
        actions.add_widget(income_btn)
        
        analytics_btn = ModernButton(text='📊 Analytics', background_color=COLORS['primary'])
        analytics_btn.bind(on_press=lambda x: self._change_screen('analytics'))  # type: ignore
        actions.add_widget(analytics_btn)
        
        settings_btn = ModernButton(text='⚙️ Settings', background_color=COLORS['dark'])
        settings_btn.bind(on_press=lambda x: self._change_screen('settings'))  # type: ignore
        actions.add_widget(settings_btn)
        
        return actions
    
    def _change_screen(self, screen_name):
        """Change to another screen"""
        self.app.root.current = screen_name
    
    def refresh_data(self, dt):
        """Refresh dashboard"""
        self.clear_widgets()
        self.build_ui()


class AddExpenseScreen(Screen):
    """Add Expense Screen"""
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        layout.add_widget(Label(text='Add Expense', size_hint_y=0.1, font_size=18, bold=True))
        
        self.amount_input = TextInput(multiline=False, hint_text='Amount', 
                                     input_filter='float', size_hint_y=0.1)
        layout.add_widget(self.amount_input)
        
        self.description_input = TextInput(multiline=False, hint_text='Description',
                                          size_hint_y=0.1)
        layout.add_widget(self.description_input)
        
        self.category_spinner = Spinner(text='Select Category', size_hint_y=0.1,
                                        values=Config.DEFAULT_CATEGORIES)
        layout.add_widget(self.category_spinner)
        
        payment_spinner = Spinner(text='Payment Method', size_hint_y=0.1,
                                 values=Config.PAYMENT_METHODS)
        layout.add_widget(payment_spinner)
        
        save_btn = ModernButton(text='💾 Save', background_color=COLORS['success'], size_hint_y=0.1)
        save_btn.bind(on_press=self.save_expense)  # type: ignore
        layout.add_widget(save_btn)
        
        back_btn = ModernButton(text='← Back', background_color=COLORS['text_light'], size_hint_y=0.1)
        back_btn.bind(on_press=self._go_back)  # type: ignore
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def _go_back(self, instance):
        """Go back to dashboard"""
        self.app.root.current = 'dashboard'
    
    def save_expense(self, instance):
        """Save expense"""
        try:
            amount = float(self.amount_input.text)
            description = self.description_input.text
            category = self.category_spinner.text
            
            if category == 'Select Category':
                try:
                    category, confidence = self.app.ml_engine.categorize_expense(description)
                except Exception:
                    category = 'Other'
            
            self.app.db.add_expense(category, amount, description)
            
            self.amount_input.text = ''
            self.description_input.text = ''
            self.category_spinner.text = 'Select Category'
            
            popup = Popup(title='Success', size_hint=(0.8, 0.3))
            popup.add_widget(Label(text='Expense added!'))
            popup.open()
            Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)
            
        except Exception as e:
            popup = Popup(title='Error', size_hint=(0.8, 0.3))
            popup.add_widget(Label(text=f'Error: {str(e)[:50]}'))
            popup.open()


class AddIncomeScreen(Screen):
    """Add Income Screen"""
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        layout.add_widget(Label(text='Add Income', size_hint_y=0.1, font_size=18, bold=True))
        
        self.amount_input = TextInput(multiline=False, hint_text='Amount',
                                     input_filter='float', size_hint_y=0.1)
        layout.add_widget(self.amount_input)
        
        self.source_input = TextInput(multiline=False, hint_text='Source', size_hint_y=0.1)
        layout.add_widget(self.source_input)
        
        payment_spinner = Spinner(text='Payment Method', size_hint_y=0.1,
                                 values=Config.PAYMENT_METHODS)
        layout.add_widget(payment_spinner)
        
        save_btn = ModernButton(text='💾 Save', background_color=COLORS['success'], size_hint_y=0.1)
        save_btn.bind(on_press=self.save_income)  # type: ignore
        layout.add_widget(save_btn)
        
        back_btn = ModernButton(text='← Back', background_color=COLORS['text_light'], size_hint_y=0.1)
        back_btn.bind(on_press=self._go_back)  # type: ignore
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def _go_back(self, instance):
        """Go back to dashboard"""
        self.app.root.current = 'dashboard'
    
    def save_income(self, instance):
        """Save income"""
        try:
            amount = float(self.amount_input.text)
            source = self.source_input.text or 'Income'
            
            self.app.db.add_income(source, amount)
            
            self.amount_input.text = ''
            self.source_input.text = ''
            
            popup = Popup(title='Success', size_hint=(0.8, 0.3))
            popup.add_widget(Label(text='Income added!'))
            popup.open()
            Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)
            
        except Exception as e:
            popup = Popup(title='Error', size_hint=(0.8, 0.3))
            popup.add_widget(Label(text=f'Error: {str(e)[:50]}'))
            popup.open()


class AnalyticsScreen(Screen):
    """Analytics Screen"""
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        layout.add_widget(Label(text='📊 Analytics', size_hint_y=0.1, font_size=18, bold=True))
        
        try:
            expenses = self.app.db.get_expenses(days=30) or []
            
            if expenses:
                # Create simple stats without pandas
                stats_text = "Spending by Category:\n"
                category_totals = {}
                for exp in expenses:
                    cat = exp.get('category', 'Other') if isinstance(exp, dict) else getattr(exp, 'category', 'Other')
                    amount = exp.get('amount', 0) if isinstance(exp, dict) else getattr(exp, 'amount', 0)
                    category_totals[cat] = category_totals.get(cat, 0) + amount
                
                for category, total in sorted(category_totals.items()):
                    stats_text += f"{category}: ₨{total:,.0f}\n"
                
                try:
                    predictions = self.app.ml_engine.predict_spending(expenses, months_ahead=1) or {}
                    pred_text = "\nNext Month Predictions:\n"
                    for cat, pred in list(predictions.items())[:3]:
                        if isinstance(pred, dict):
                            pred_text += f"{cat}: ₨{pred.get('predicted_amount', 0):,.0f}\n"
                    stats_text += pred_text
                except Exception:
                    pass
                
                layout.add_widget(Label(text=stats_text, font_size=10))
            else:
                layout.add_widget(Label(text='No expenses recorded yet.', font_size=12))
        except Exception as e:
            layout.add_widget(Label(text=f'Analytics unavailable: {str(e)[:50]}', font_size=10))
        
        back_btn = ModernButton(text='← Back', background_color=COLORS['text_light'])
        back_btn.bind(on_press=self._go_back)  # type: ignore
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def _go_back(self, instance):
        """Go back to dashboard"""
        self.app.root.current = 'dashboard'


class SettingsScreen(Screen):
    """Settings Screen"""
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        layout.add_widget(Label(text='⚙️ Settings', size_hint_y=0.1, font_size=18, bold=True))
        layout.add_widget(Label(text=f'Version: {Config.APP_VERSION}', size_hint_y=0.1))
        layout.add_widget(Label(text=f'Currency: {Config.DEFAULT_CURRENCY}', size_hint_y=0.1))
        layout.add_widget(Label(text=f'ML: {"Enabled" if Config.ENABLE_ML_FEATURES else "Disabled"}', 
                               size_hint_y=0.1))
        
        back_btn = ModernButton(text='← Back', background_color=COLORS['text_light'])
        back_btn.bind(on_press=self._go_back)  # type: ignore
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def _go_back(self, instance):
        """Go back to dashboard"""
        self.app.root.current = 'dashboard'


class FinanceProApp(App):
    """Main Application"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = EnhancedDatabase(Config.DB_PATH)
        self.ml_engine = MLEngine(self.db)
        self.analytics = AnalyticsEngine(self.db)
    
    def build(self):
        self.title = 'Finance Pro 2.0'
        
        sm = ScreenManager()
        sm.add_widget(DashboardScreen(self, name='dashboard'))
        sm.add_widget(AddExpenseScreen(self, name='add_expense'))
        sm.add_widget(AddIncomeScreen(self, name='add_income'))
        sm.add_widget(AnalyticsScreen(self, name='analytics'))
        sm.add_widget(SettingsScreen(self, name='settings'))
        
        self._init_sample_data()
        
        return sm
    
    def _init_sample_data(self):
        """Initialize with sample data"""
        try:
            expenses = self.db.get_expenses(days=1) or []
            if not expenses:
                self.db.add_expense('Groceries', 50000, 'Weekly shopping')
                self.db.add_expense('Transport', 15000, 'Taxi')
                self.db.add_income('Salary', 500000, 'Monthly salary')
        except Exception as e:
            print(f"Warning: Could not initialize sample data: {str(e)[:100]}")
    
    def get_health_score(self) -> dict:
        """Get financial health score"""
        try:
            expenses = self.db.get_expenses(days=30) or []
            income = self.db.get_income(days=30) or []
            return FinancialHealthScore.calculate_score(expenses, income, [])
        except Exception as e:
            print(f"Warning: Could not calculate health score: {str(e)[:100]}")
            return {'score': 0, 'grade': 'N/A', 'message': 'Unable to calculate'}


if __name__ == '__main__':
    FinanceProApp().run()
