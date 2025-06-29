# 🚀 Deploy to Railway

This guide shows how to deploy your Bank Accounts Management System to Railway.

## Prerequisites

- GitHub repository with your code
- Railway account (free tier available)

## Quick Deploy Steps

### Option 1: Direct GitHub Deploy

1. **Visit Railway**: Go to [railway.app](https://railway.app)

2. **Create New Project**: Click "Deploy from GitHub repo"

3. **Select Repository**: Choose `riftvanta/xxn`

4. **Add PostgreSQL Database**:
   - Click "+ New" → "Database" → "Add PostgreSQL"
   - Railway will automatically create a DATABASE_URL environment variable

5. **Deploy**: Railway will automatically:
   - Detect your Flask app
   - Install dependencies from `requirements.txt`
   - Use `nixpacks.toml` for startup configuration
   - Start your app with Gunicorn

6. **Generate Domain**: 
   - Go to Settings → Networking
   - Click "Generate Domain" for public access

### Option 2: Railway CLI Deploy

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up

# Add PostgreSQL
railway add postgresql

# Generate domain
railway domain
```

## Environment Variables

Railway automatically provides:
- `DATABASE_URL` - PostgreSQL connection string
- `PORT` - Application port (handled automatically)

Optional variables you can set:
- `SECRET_KEY` - Flask secret key (recommended for production)
- `FLASK_ENV` - Set to "production"

## Post-Deployment

1. **Verify Database**: Check Railway dashboard for PostgreSQL service
2. **Test Application**: Visit your generated domain
3. **Monitor Logs**: Use Railway dashboard to view application logs

## Features Included

✅ **Production-ready**: Gunicorn WSGI server
✅ **Database**: PostgreSQL with automatic connection
✅ **Security**: Production configurations
✅ **Monitoring**: Railway dashboard logs and metrics
✅ **Scaling**: Automatic scaling capabilities
✅ **HTTPS**: Automatic SSL certificates

## Estimated Costs

- **Free Tier**: $0/month (500 hours execution time)
- **Hobby Plan**: $5/month (unlimited usage)
- **PostgreSQL**: Included in plans

## Support

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Community Discord: [Railway Discord](https://discord.gg/railway) 