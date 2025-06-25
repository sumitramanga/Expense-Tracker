
import json
import sqlite3
from datetime import datetime, date
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

class ExpenseTracker:
    def __init__(self, db_path='expenses.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the SQLite database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
                category TEXT NOT NULL,
                date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
                UNIQUE(name, type)
            )
        ''')
        
        # Insert default categories
        default_categories = [
            ('Salary', 'income'),
            ('Freelance', 'income'),
            ('Investment', 'income'),
            ('Gift', 'income'),
            ('Other Income', 'income'),
            ('Food', 'expense'),
            ('Transportation', 'expense'),
            ('Entertainment', 'expense'),
            ('Bills', 'expense'),
            ('Shopping', 'expense'),
            ('Healthcare', 'expense'),
            ('Education', 'expense'),
            ('Other', 'expense')
        ]
        
        cursor.executemany(
            'INSERT OR IGNORE INTO categories (name, type) VALUES (?, ?)',
            default_categories
        )
        
        conn.commit()
        conn.close()
    
    def add_transaction(self, description, amount, transaction_type, category, date_str=None):
        """Add a new transaction to the database."""
        if date_str is None:
            date_str = date.today().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO transactions (description, amount, type, category, date) VALUES (?, ?, ?, ?, ?)',
            (description, amount, transaction_type, category, date_str)
        )
        
        conn.commit()
        transaction_id = cursor.lastrowid
        conn.close()
        
        return transaction_id
    
    def get_transactions(self, limit=None, transaction_type=None):
        """Retrieve transactions from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = 'SELECT id, description, amount, type, category, date FROM transactions'
        params = []
        
        if transaction_type:
            query += ' WHERE type = ?'
            params.append(transaction_type)
        
        query += ' ORDER BY date DESC'
        
        if limit:
            query += ' LIMIT ?'
            params.append(limit)
        
        cursor.execute(query, params)
        transactions = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': t[0],
                'description': t[1],
                'amount': t[2],
                'type': t[3],
                'category': t[4],
                'date': t[5]
            }
            for t in transactions
        ]
    
    def delete_transaction(self, transaction_id):
        """Delete a transaction from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
    
    def get_balance(self):
        """Calculate the current balance."""
        transactions = self.get_transactions()
        
        income = sum(t['amount'] for t in transactions if t['type'] == 'income')
        expenses = sum(t['amount'] for t in transactions if t['type'] == 'expense')
        
        return {
            'income': income,
            'expenses': expenses,
            'balance': income - expenses
        }
    
    def get_categories(self, transaction_type=None):
        """Get categories from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if transaction_type:
            cursor.execute('SELECT name FROM categories WHERE type = ? ORDER BY name', (transaction_type,))
        else:
            cursor.execute('SELECT name, type FROM categories ORDER BY type, name')
        
        categories = cursor.fetchall()
        conn.close()
        
        if transaction_type:
            return [cat[0] for cat in categories]
        else:
            result = {'income': [], 'expense': []}
            for cat_name, cat_type in categories:
                result[cat_type].append(cat_name)
            return result
    
    def get_expense_breakdown(self):
        """Get expenses broken down by category."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT category, SUM(amount) as total
            FROM transactions 
            WHERE type = 'expense'
            GROUP BY category
            ORDER BY total DESC
        ''')
        
        breakdown = cursor.fetchall()
        conn.close()
        
        return [{'category': cat, 'amount': amount} for cat, amount in breakdown]

# Initialize the expense tracker
tracker = ExpenseTracker()

@app.route('/')
def index():
    """Main dashboard page."""
    balance = tracker.get_balance()
    recent_transactions = tracker.get_transactions(limit=10)
    expense_breakdown = tracker.get_expense_breakdown()
    categories = tracker.get_categories()
    
    return render_template('dashboard.html',
                         balance=balance,
                         transactions=recent_transactions,
                         expense_breakdown=expense_breakdown,
                         categories=categories)

@app.route('/api/transactions', methods=['GET'])
def api_get_transactions():
    """API endpoint to get transactions."""
    transaction_type = request.args.get('type')
    limit = request.args.get('limit', type=int)
    
    transactions = tracker.get_transactions(limit=limit, transaction_type=transaction_type)
    return jsonify(transactions)

@app.route('/api/transactions', methods=['POST'])
def api_add_transaction():
    """API endpoint to add a new transaction."""
    try:
        data = request.get_json()
        
        required_fields = ['description', 'amount', 'type', 'category']
        for field in required_fields:
            if field not in data:
                raise BadRequest(f'Missing required field: {field}')
        
        transaction_id = tracker.add_transaction(
            description=data['description'],
            amount=float(data['amount']),
            transaction_type=data['type'],
            category=data['category'],
            date_str=data.get('date')
        )
        
        return jsonify({'id': transaction_id, 'status': 'success'}), 201
        
    except (ValueError, BadRequest) as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/transactions/<int:transaction_id>', methods=['DELETE'])
def api_delete_transaction(transaction_id):
    """API endpoint to delete a transaction."""
    if tracker.delete_transaction(transaction_id):
        return jsonify({'status': 'success'})
    else:
        return jsonify({'error': 'Transaction not found'}), 404

@app.route('/api/balance')
def api_get_balance():
    """API endpoint to get current balance."""
    return jsonify(tracker.get_balance())

@app.route('/api/categories')
def api_get_categories():
    """API endpoint to get categories."""
    transaction_type = request.args.get('type')
    categories = tracker.get_categories(transaction_type)
    return jsonify(categories)

@app.route('/api/expense-breakdown')
def api_expense_breakdown():
    """API endpoint to get expense breakdown by category."""
    return jsonify(tracker.get_expense_breakdown())

if __name__ == '__main__':
    app.run(debug=True)

