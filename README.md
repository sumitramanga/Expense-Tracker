# 💰 Expense Tracker
Created by Autohive.com 

A simple yet powerful expense tracking application to help you manage your personal finances. Track your income and expenses, categorize transactions, and visualize your spending patterns.

## Features

- ✅ **Add Transactions**: Record income and expenses with descriptions and categories
- 📊 **Visual Dashboard**: See your balance, income, and expenses at a glance
- 🎯 **Categorization**: Organize transactions by categories (Food, Transportation, Bills, etc.)
- 📈 **Expense Breakdown**: Visual chart showing expense distribution by category
- 💾 **Local Storage**: Data persists in your browser (HTML version) or SQLite database (Python version)
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices
- 🗑️ **Transaction Management**: Edit and delete transactions as needed

## Quick Start

### HTML Version (Client-Side Only)

The easiest way to get started is with the standalone HTML file:

1. Download `expense-tracker.html`
2. Open it in any modern web browser
3. Start tracking your expenses immediately!

**Features:**
- No installation required
- Data stored in browser's local storage
- Interactive charts with Chart.js
- Responsive design with Tailwind CSS

### Python Version (Full-Featured)

For more advanced features and server-side data storage:

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Open in Browser**
   Navigate to `http://localhost:5000`

**Features:**
- SQLite database for data persistence
- REST API for programmatic access
- Server-side data validation
- Multi-user support (with additional authentication)

## Usage Guide

### Adding Transactions

1. Fill in the transaction details:
   - **Description**: What was the transaction for?
   - **Amount**: How much money was involved?
   - **Type**: Income or Expense
   - **Category**: Select from predefined categories

2. Click "Add Transaction" to save

### Managing Transactions

- View all transactions in the history table
- Delete individual transactions using the "Delete" button
- Clear all history with the "Clear History" button
- See real-time updates to your balance and charts

### Understanding Your Finances

- **Total Income**: Sum of all income transactions
- **Total Expenses**: Sum of all expense transactions  
- **Balance**: Income minus expenses (green=positive, red=negative)
- **Expense Chart**: Visual breakdown of spending by category

## Categories

### Income Categories
- Salary
- Freelance
- Investment
- Gift
- Other Income

### Expense Categories
- Food
- Transportation
- Entertainment
- Bills
- Shopping
- Healthcare
- Education
- Other

## API Endpoints (Python Version)

### Get Transactions
```http
GET /api/transactions
GET /api/transactions?type=expense
GET /api/transactions?limit=10
```

### Add Transaction
```http
POST /api/transactions
Content-Type: application/json

{
    "description": "Grocery shopping",
    "amount": 45.67,
    "type": "expense",
    "category": "Food",
    "date": "2025-06-25"
}
```

### Delete Transaction
```http
DELETE /api/transactions/{id}
```

### Get Balance
```http
GET /api/balance
```

### Get Categories
```http
GET /api/categories
GET /api/categories?type=expense
```

### Get Expense Breakdown
```http
GET /api/expense-breakdown
```

## Technology Stack

### HTML Version
- **HTML5** - Structure
- **Tailwind CSS** - Styling and responsive design
- **Vanilla JavaScript** - Application logic
- **Chart.js** - Data visualization
- **LocalStorage** - Data persistence

### Python Version
- **Flask** - Web framework
- **SQLite** - Database
- **HTML/CSS/JavaScript** - Frontend
- **RESTful API** - Backend architecture

## Data Storage

### HTML Version
Data is stored in the browser's localStorage, which means:
- ✅ No server required
- ✅ Instant response
- ⚠️ Data is browser-specific
- ⚠️ Data may be cleared if browser storage is cleared

### Python Version
Data is stored in a SQLite database (`expenses.db`), which provides:
- ✅ Persistent storage
- ✅ Data integrity
- ✅ Backup and restore capabilities
- ✅ Multi-user support potential

## Browser Compatibility

- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes
4. Commit your changes: `git commit -am 'Add new feature'`
5. Push to the branch: `git push origin feature/new-feature`
6. Submit a pull request

## Future Enhancements

- [ ] **Budget Setting**: Set monthly budgets for categories
- [ ] **Expense Analytics**: Monthly/yearly spending reports
- [ ] **Export Data**: CSV/Excel export functionality
- [ ] **Multi-Currency**: Support for different currencies
- [ ] **Recurring Transactions**: Automatic recurring income/expenses
- [ ] **Receipt Upload**: Attach receipts to transactions
- [ ] **Goal Tracking**: Savings goals and progress tracking
- [ ] **User Authentication**: Multi-user support with login
- [ ] **Mobile App**: React Native or Flutter mobile application

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions:

1. Check the existing issues in the repository
2. Create a new issue with detailed information
3. Include steps to reproduce any bugs
4. Specify your browser/environment details

---

**Start tracking your expenses today and take control of your finances! 💰**
