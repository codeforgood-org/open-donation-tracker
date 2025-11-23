# Quick Start Guide

Get your donation tracking platform running in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- Git (optional, for cloning)

## 🚀 Quick Start

### 1. Navigate to Project
```bash
cd open-donation-tracker
```

### 2. Set Up Environment
```bash
# Copy example environment file
cp .env.example .env

# The default values work for development!
# For production, update the SECRET_KEY and passwords
```

### 3. Start All Services
```bash
# Start everything with one command
docker-compose up -d

# Wait about 30 seconds for services to start
```

### 4. Initialize Database
```bash
# Create tables and add sample data
docker-compose exec backend python -m app.init_db
```

### 5. Access the Application

**Frontend (User Interface):**
- URL: http://localhost:5173
- Modern React dashboard with all features

**Backend API:**
- URL: http://localhost:8000
- Health Check: http://localhost:8000/api/health

**API Documentation:**
- Interactive Docs: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 🔐 Login Credentials

### Admin Account
- Email: `admin@example.com`
- Password: `changeme123`

### Sample Donor Account
- Email: `john@example.com`
- Password: `password123`

## 📊 What's Included

The initialized database includes:

- **4 Organizations** (Education, Healthcare, Environment, Water)
- **4 Active Campaigns** (one per organization)
- **50+ Sample Donations** with various payment methods
- **Multiple Donor Accounts** for testing

## 🎯 Quick Testing Guide

### 1. Explore as Guest
1. Visit http://localhost:5173
2. Browse organizations and campaigns
3. View impact reports
4. See donation statistics

### 2. Login as Donor
1. Click "Login" → use john@example.com / password123
2. View your dashboard with donation history
3. Browse campaigns and make test donations
4. See your donation analytics

### 3. Login as Admin
1. Login with admin@example.com / changeme123
2. Access all administrative features
3. Create organizations and campaigns
4. Manage impact reports

## 🛠️ Common Commands

```bash
# View logs from all services
docker-compose logs -f

# Stop all services
docker-compose down

# Restart services
docker-compose restart

# View running containers
docker-compose ps

# Access backend shell
docker-compose exec backend /bin/sh

# Access database
docker-compose exec postgres psql -U donationuser -d donationtracker
```

## 🧪 Running Tests

### Backend Tests
```bash
docker-compose exec backend pytest -v
```

### Frontend (requires local Node.js)
```bash
cd frontend
npm install
npm test
```

## 📚 Next Steps

1. **Read the Full Documentation**
   - `README.md` - Complete project overview
   - `docs/API.md` - API endpoint documentation
   - `docs/DEPLOYMENT.md` - Production deployment guide
   - `CONTRIBUTING.md` - How to contribute

2. **Customize Your Instance**
   - Update `.env` with your settings
   - Change default passwords
   - Configure email notifications (optional)
   - Add your organization logo

3. **Explore the Code**
   - Backend: `backend/app/`
   - Frontend: `frontend/src/`
   - Database Models: `backend/app/models/`
   - API Endpoints: `backend/app/api/`

## 🐛 Troubleshooting

### Services won't start?
```bash
# Check if ports are available
docker-compose ps

# View error logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres
```

### Database connection issues?
```bash
# Restart database
docker-compose restart postgres

# Check database logs
docker-compose logs postgres
```

### Frontend can't connect to backend?
```bash
# Check backend is running
curl http://localhost:8000/api/health

# Check CORS settings in .env
cat .env | grep CORS
```

## 💡 Tips

- **Sample Data**: The init_db script creates realistic sample data for testing
- **API Docs**: Use http://localhost:8000/api/docs to test API endpoints interactively
- **Hot Reload**: Both frontend and backend support hot reloading during development
- **Database**: PostgreSQL data persists in a Docker volume
- **Logs**: Check logs with `docker-compose logs -f [service-name]`

## 🎨 Key Features to Try

1. **Dashboard Analytics**
   - Login and view your personalized dashboard
   - Interactive charts and statistics
   - Donation history

2. **Campaign Management**
   - Create a new campaign
   - Set fundraising goals
   - Track progress in real-time

3. **Make a Donation**
   - Browse active campaigns
   - Choose payment method
   - Option for anonymous donations

4. **Impact Reporting**
   - View transparency scores
   - Read impact reports
   - See metrics and outcomes

5. **Visualizations**
   - Pie charts for payment methods
   - Bar charts for donation trends
   - Progress bars for campaigns

## 🌐 Production Deployment

When ready for production:

1. **Update Environment Variables**
   ```bash
   # Generate strong keys
   openssl rand -hex 32

   # Update .env with production values
   ```

2. **Follow Deployment Guide**
   - See `docs/DEPLOYMENT.md` for complete instructions
   - Configure SSL/TLS
   - Set up backups
   - Configure monitoring

3. **Security Checklist**
   - Change all default passwords
   - Use strong SECRET_KEY
   - Enable HTTPS
   - Configure firewall
   - Set up regular backups

## 📞 Get Help

- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Ask questions in GitHub Discussions
- **Documentation**: Check the `/docs` folder

---

**Enjoy building transparency in charitable giving! 🎉**
