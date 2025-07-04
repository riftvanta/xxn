from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from decimal import Decimal
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'

# Database Configuration
# Railway provides DATABASE_URL for PostgreSQL
if os.environ.get('DATABASE_URL'):
    # Railway PostgreSQL connection (production)
    database_url = os.environ.get('DATABASE_URL')
    # Handle Railway's postgres:// vs postgresql:// URL format
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
elif os.environ.get('POSTGRES_USER'):
    # Build PostgreSQL URL from environment variables (local development)
    postgres_user = os.environ.get('POSTGRES_USER', 'bankuser')
    postgres_password = os.environ.get('POSTGRES_PASSWORD', 'bankpass123')
    postgres_host = os.environ.get('POSTGRES_HOST', 'localhost')
    postgres_port = os.environ.get('POSTGRES_PORT', '5432')
    postgres_db = os.environ.get('POSTGRES_DB', 'bank_accounts_db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}'
else:
    # Default to SQLite for development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank_accounts.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    starting_balance = db.Column(db.Numeric(12, 2), nullable=False)
    current_balance = db.Column(db.Numeric(12, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BankAccount {self.name}>'

class CorrespondingAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # client, expense, supplier, bank, revenue, commission
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CorrespondingAccount {self.name}>'

class GeneralJournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<GeneralJournalEntry {self.id} on {self.transaction_date}>'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank_account_id = db.Column(db.Integer, db.ForeignKey('bank_account.id'), nullable=True)
    corresponding_account_id = db.Column(db.Integer, db.ForeignKey('corresponding_account.id'), nullable=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)  # credit or debit
    transaction_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    journal_entry_id = db.Column(db.Integer, db.ForeignKey('general_journal_entry.id'), nullable=True)
    
    bank_account = db.relationship('BankAccount', backref=db.backref('transactions', lazy=True))
    corresponding_account = db.relationship('CorrespondingAccount', backref=db.backref('transactions', lazy=True))
    journal_entry = db.relationship('GeneralJournalEntry', backref=db.backref('transactions', lazy=True))
    
    def __repr__(self):
        return f'<Transaction {self.amount} {self.transaction_type}>'

# Routes
@app.route('/')
def dashboard():
    bank_accounts = BankAccount.query.all()
    total_balance = sum(account.current_balance for account in bank_accounts)
    total_accounts = len(bank_accounts)
    total_transactions = Transaction.query.count()
    
    return render_template('dashboard.html', 
                         bank_accounts=bank_accounts,
                         total_balance=total_balance,
                         total_accounts=total_accounts,
                         total_transactions=total_transactions)

@app.route('/setup')
def setup():
    bank_accounts = BankAccount.query.all()
    corresponding_accounts = CorrespondingAccount.query.all()
    return render_template('setup.html', 
                         bank_accounts=bank_accounts,
                         corresponding_accounts=corresponding_accounts)

@app.route('/add_bank_account', methods=['POST'])
def add_bank_account():
    name = request.form['name']
    starting_balance = Decimal(request.form['starting_balance'])
    
    bank_account = BankAccount(
        name=name,
        starting_balance=starting_balance,
        current_balance=starting_balance
    )
    
    db.session.add(bank_account)
    db.session.commit()
    
    flash('تم إضافة الحساب البنكي بنجاح', 'success')
    return redirect(url_for('setup'))

@app.route('/add_corresponding_account', methods=['POST'])
def add_corresponding_account():
    name = request.form['name']
    account_type = request.form['type']
    
    corresponding_account = CorrespondingAccount(
        name=name,
        type=account_type
    )
    
    db.session.add(corresponding_account)
    db.session.commit()
    
    flash('تم إضافة الحساب المقابل بنجاح', 'success')
    return redirect(url_for('setup'))

@app.route('/transactions')
def transactions():
    bank_accounts = BankAccount.query.all()
    corresponding_accounts = CorrespondingAccount.query.all()
    return render_template('transactions.html',
                         bank_accounts=bank_accounts,
                         corresponding_accounts=corresponding_accounts)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    try:
        bank_account_id = int(request.form['bank_account_id'])
        corresponding_account_id = int(request.form['corresponding_account_id'])
        amount = Decimal(request.form['amount'])
        transaction_type = request.form['transaction_type']
        transaction_date = datetime.strptime(request.form['transaction_date'], '%Y-%m-%d').date()
        notes = request.form.get('notes', '')
        
        # Validation: Regular transactions must have both accounts
        if not bank_account_id or not corresponding_account_id:
            return jsonify({
                'success': False,
                'message': 'يجب تحديد كل من الحساب البنكي والحساب المقابل'
            })
        
        # Create transaction
        transaction = Transaction(
            bank_account_id=bank_account_id,
            corresponding_account_id=corresponding_account_id,
            amount=amount,
            transaction_type=transaction_type,
            transaction_date=transaction_date,
            notes=notes
        )
        
        # Update bank account balance
        bank_account = BankAccount.query.get(bank_account_id)
        if transaction_type == 'credit':
            bank_account.current_balance += amount
        else:  # debit
            bank_account.current_balance -= amount
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم إضافة المعاملة بنجاح',
            'new_balance': float(bank_account.current_balance)
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'خطأ في إضافة المعاملة: {str(e)}'
        })

@app.route('/transaction_history')
def transaction_history():
    transactions = Transaction.query.order_by(Transaction.transaction_date.desc()).limit(100).all()
    return render_template('transaction_history.html', transactions=transactions)

@app.route('/bulk_transactions')
def bulk_transactions():
    bank_accounts = BankAccount.query.all()
    corresponding_accounts = CorrespondingAccount.query.all()
    
    # Convert corresponding accounts to dictionaries for JavaScript
    corresponding_accounts_json = [
        {
            'id': acc.id,
            'name': acc.name,
            'type': acc.type
        }
        for acc in corresponding_accounts
    ]
    
    return render_template('bulk_transactions.html',
                         bank_accounts=bank_accounts,
                         corresponding_accounts=corresponding_accounts,
                         corresponding_accounts_json=corresponding_accounts_json)

@app.route('/add_bulk_transactions', methods=['POST'])
def add_bulk_transactions():
    try:
        data = request.get_json()
        bank_account_id = int(data['bank_account_id'])
        transaction_date = datetime.strptime(data['transaction_date'], '%Y-%m-%d').date()
        transactions_data = data['transactions']
        
        # Validate transactions data
        if not transactions_data:
            return jsonify({
                'success': False,
                'message': 'لا توجد معاملات للحفظ'
            })
        
        saved_count = 0
        errors = []
        
        # Get bank account for balance updates
        bank_account = BankAccount.query.get_or_404(bank_account_id)
        
        for i, trans_data in enumerate(transactions_data):
            try:
                amount = Decimal(str(abs(float(trans_data['amount']))))  # Always positive
                original_amount = float(trans_data['amount'])
                corresponding_account_id = int(trans_data['corresponding_account_id'])
                
                # Validation: Bulk transactions must have both accounts
                if not bank_account_id or not corresponding_account_id:
                    errors.append(f'المعاملة {i + 1}: يجب تحديد كل من الحساب البنكي والحساب المقابل')
                    continue
                
                # Determine transaction type based on sign
                transaction_type = 'debit' if original_amount < 0 else 'credit'
                
                # Create transaction
                transaction = Transaction(
                    bank_account_id=bank_account_id,
                    corresponding_account_id=corresponding_account_id,
                    amount=amount,
                    transaction_type=transaction_type,
                    transaction_date=transaction_date,
                    notes=''
                )
                
                # Update bank account balance
                if transaction_type == 'credit':
                    bank_account.current_balance += amount
                else:  # debit
                    bank_account.current_balance -= amount
                
                db.session.add(transaction)
                saved_count += 1
                
            except Exception as e:
                errors.append(f'المعاملة {i + 1}: {str(e)}')
        
        if saved_count > 0:
            db.session.commit()
            
        if errors:
            return jsonify({
                'success': True,
                'message': f'تم حفظ {saved_count} معاملة بنجاح. أخطاء: {"; ".join(errors)}',
                'new_balance': float(bank_account.current_balance),
                'saved_count': saved_count
            })
        else:
            return jsonify({
                'success': True,
                'message': f'تم حفظ {saved_count} معاملة بنجاح',
                'new_balance': float(bank_account.current_balance),
                'saved_count': saved_count
            })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'خطأ في حفظ المعاملات: {str(e)}'
        })

@app.route('/api/account_balance/<int:account_id>')
def get_account_balance(account_id):
    account = BankAccount.query.get_or_404(account_id)
    return jsonify({
        'balance': float(account.current_balance),
        'name': account.name
    })

@app.route('/general_journal')
def general_journal():
    bank_accounts = BankAccount.query.all()
    corresponding_accounts = CorrespondingAccount.query.all()
    
    # Combine all accounts for the dropdown
    all_accounts = []
    
    # Add bank accounts
    for account in bank_accounts:
        all_accounts.append({
            'id': f'bank_{account.id}',
            'name': account.name,
            'type': 'bank',
            'balance': float(account.current_balance)
        })
    
    # Add corresponding accounts
    for account in corresponding_accounts:
        all_accounts.append({
            'id': f'corresponding_{account.id}',
            'name': account.name,
            'type': account.type,
            'balance': 0  # We don't track balance for corresponding accounts
        })
    
    return render_template('general_journal.html',
                         all_accounts=all_accounts,
                         all_accounts_json=all_accounts)

@app.route('/add_general_journal_entry', methods=['POST'])
def add_general_journal_entry():
    try:
        data = request.get_json()
        transaction_date = datetime.strptime(data['transaction_date'], '%Y-%m-%d').date()
        journal_entries = data['journal_entries']
        
        if not journal_entries:
            return jsonify({
                'success': False,
                'message': 'لا توجد قيود للحفظ'
            })
        
        saved_entries = 0
        errors = []
        
        for entry_index, entry_data in enumerate(journal_entries):
            try:
                accounts_data = entry_data['accounts']
                
                # Validate that entry balances
                total_balance = sum(float(acc['amount']) for acc in accounts_data)
                if abs(total_balance) > 0.01:  # Allow small rounding differences
                    errors.append(f'القيد {entry_index + 1}: القيد غير متوازن (المجموع: {total_balance:.2f})')
                    continue
                
                # Create journal entry
                journal_entry = GeneralJournalEntry(transaction_date=transaction_date)
                db.session.add(journal_entry)
                db.session.flush()  # Get the ID
                
                # Process each account in this entry
                for acc_data in accounts_data:
                    amount = float(acc_data['amount'])
                    if abs(amount) < 0.01:  # Skip zero amounts
                        continue
                        
                    account_id = acc_data['account_id']
                    account_type = acc_data['account_type']
                    
                    # Validation: Must have an account specified
                    if not account_id or not account_type:
                        continue  # Skip invalid entries
                    
                    # Parse account ID
                    if account_type == 'bank':
                        bank_account_id = int(account_id.replace('bank_', ''))
                        corresponding_account_id = None
                        
                        # Update bank account balance
                        bank_account = BankAccount.query.get(bank_account_id)
                        if bank_account:
                            bank_account.current_balance += Decimal(str(amount))
                        
                    else:
                        bank_account_id = None
                        corresponding_account_id = int(account_id.replace('corresponding_', ''))
                    
                    # Determine transaction type
                    transaction_type = 'credit' if amount > 0 else 'debit'
                    
                    # Create transaction record
                    transaction = Transaction(
                        bank_account_id=bank_account_id,
                        corresponding_account_id=corresponding_account_id,
                        amount=Decimal(str(abs(amount))),
                        transaction_type=transaction_type,
                        transaction_date=transaction_date,
                        notes='',
                        journal_entry_id=journal_entry.id
                    )
                    
                    db.session.add(transaction)
                
                saved_entries += 1
                
            except Exception as e:
                errors.append(f'القيد {entry_index + 1}: {str(e)}')
        
        if saved_entries > 0:
            db.session.commit()
            
        if errors:
            return jsonify({
                'success': True,
                'message': f'تم حفظ {saved_entries} قيد بنجاح. أخطاء: {"; ".join(errors)}',
                'saved_count': saved_entries
            })
        else:
            return jsonify({
                'success': True,
                'message': f'تم حفظ {saved_entries} قيد بنجاح',
                'saved_count': saved_entries
            })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'خطأ في حفظ القيود: {str(e)}'
        })

@app.route('/system_info')
def system_info():
    """Debug route to show system information"""
    return jsonify({
        'database_uri': app.config['SQLALCHEMY_DATABASE_URI'],
        'database_engine': str(db.session.get_bind()),
        'database_name': db.session.get_bind().url.database if hasattr(db.session.get_bind().url, 'database') else 'N/A',
        'environment_vars': {
            'DATABASE_URL': os.environ.get('DATABASE_URL', 'Not set'),
            'POSTGRES_USER': os.environ.get('POSTGRES_USER', 'Not set'),
            'POSTGRES_DB': os.environ.get('POSTGRES_DB', 'Not set')
        }
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Get port from environment variable (Railway sets this)
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(host='0.0.0.0', port=port, debug=debug) 