#!/bin/bash

# Bank Accounts Management System - PostgreSQL Startup Script
# This script starts the application with PostgreSQL configuration

echo "🏦 Starting Bank Accounts Management System with PostgreSQL..."

# Set PostgreSQL environment variables
export POSTGRES_USER=bankuser
export POSTGRES_PASSWORD=bankpass123
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_DB=bank_accounts_db

# Set Flask environment
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key-here

echo "📊 Database: PostgreSQL"
echo "🗄️  Database Name: $POSTGRES_DB"
echo "👤 Database User: $POSTGRES_USER"
echo "🖥️  Host: $POSTGRES_HOST:$POSTGRES_PORT"
echo ""

# Check if PostgreSQL is running
if ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT > /dev/null 2>&1; then
    echo "❌ PostgreSQL is not running. Please start PostgreSQL service first:"
    echo "   sudo systemctl start postgresql"
    exit 1
fi

echo "✅ PostgreSQL is running"
echo "🚀 Starting Flask application..."
echo ""

# Activate virtual environment and start the application
source venv/bin/activate && python app.py 