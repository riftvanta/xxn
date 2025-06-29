#!/bin/bash

# Bank Accounts Management System - PostgreSQL Backup Script
# Based on the guide from https://shallowsky.com/blog/tags/postgresql/

# Configuration
POSTGRES_USER=bankuser
POSTGRES_PASSWORD=bankpass123
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=bank_accounts_db

# Backup directory
BACKUP_DIR="./backups"
mkdir -p $BACKUP_DIR

# Generate timestamp for backup filename
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/bank_accounts_backup_$TIMESTAMP.sql"

echo "🏦 Bank Accounts Management System - Database Backup"
echo "📅 Date: $(date)"
echo "🗄️  Database: $POSTGRES_DB"
echo "📁 Backup file: $BACKUP_FILE"
echo ""

# Check if PostgreSQL is running
if ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT > /dev/null 2>&1; then
    echo "❌ PostgreSQL is not running. Please start PostgreSQL service first:"
    echo "   sudo systemctl start postgresql"
    exit 1
fi

echo "✅ PostgreSQL is running"
echo "🔄 Creating backup..."

# Create backup using pg_dump
export PGPASSWORD=$POSTGRES_PASSWORD
pg_dump -U $POSTGRES_USER -h $POSTGRES_HOST -p $POSTGRES_PORT $POSTGRES_DB > $BACKUP_FILE

# Check if backup was successful
if [ $? -eq 0 ]; then
    echo "✅ Backup completed successfully!"
    echo "📄 Backup saved to: $BACKUP_FILE"
    echo "📊 Backup size: $(du -h $BACKUP_FILE | cut -f1)"
    echo ""
    echo "💡 To restore from this backup:"
    echo "   psql -U $POSTGRES_USER -h $POSTGRES_HOST -d $POSTGRES_DB < $BACKUP_FILE"
else
    echo "❌ Backup failed!"
    exit 1
fi

# Clean up old backups (keep last 10)
echo "🧹 Cleaning up old backups (keeping last 10)..."
ls -t $BACKUP_DIR/bank_accounts_backup_*.sql | tail -n +11 | xargs -r rm -f

echo "✅ Backup process completed!" 