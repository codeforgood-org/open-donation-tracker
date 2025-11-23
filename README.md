# Open Donation Tracker

[![CI/CD](https://github.com/yourusername/open-donation-tracker/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/yourusername/open-donation-tracker/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive, production-ready donation tracking platform that ensures transparency in charitable giving, helps donors track their impact, and enables organizations to demonstrate their work.

## Features

### For Donors
- **Track Donations**: Complete history of all donations with detailed transaction records
- **Visualize Impact**: Interactive dashboards showing donation analytics and trends
- **Support Campaigns**: Contribute to specific fundraising campaigns with real-time progress tracking
- **Transparency**: View detailed impact reports from organizations

### For Organizations
- **Manage Campaigns**: Create and manage fundraising campaigns with goals and deadlines
- **Impact Reporting**: Publish detailed impact reports with metrics and evidence
- **Transparency Scores**: Build trust through transparent reporting and verification
- **Donor Management**: Track donations and donor relationships

### Technical Features
- **Secure Authentication**: JWT-based authentication with password hashing
- **RESTful API**: Comprehensive FastAPI backend with auto-generated documentation
- **Modern Frontend**: React with TypeScript, Tailwind CSS, and React Query
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Docker Support**: Full containerization for easy deployment
- **Testing**: Comprehensive test coverage for backend and frontend
- **CI/CD**: Automated testing and deployment with GitHub Actions

## Tech Stack

### Backend
- **FastAPI**: High-performance async Python web framework
- **PostgreSQL**: Reliable and scalable relational database
- **SQLAlchemy**: Powerful ORM for database operations
- **Pydantic**: Data validation and settings management
- **JWT**: Secure token-based authentication
- **Pytest**: Comprehensive testing framework

### Frontend
- **React 18**: Modern UI library with hooks
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **TanStack Query**: Powerful data fetching and caching
- **Recharts**: Beautiful and customizable charts
- **Axios**: HTTP client for API requests

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **GitHub Actions**: CI/CD pipeline
- **Nginx**: Production web server

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/open-donation-tracker.git
   cd open-donation-tracker
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Initialize the database**
   ```bash
   make init-db
   # or: docker-compose exec backend python -m app.init_db
   ```

5. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/api/docs

### Default Credentials

**Admin User:**
- Email: admin@example.com
- Password: changeme123

**Sample Donor:**
- Email: john@example.com
- Password: password123

**⚠️ Change these credentials in production!**

## Development

### Backend Development

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Run development server
uvicorn app.main:app --reload

# Run tests
pytest -v --cov=app

# Run linter
flake8 app
```

### Frontend Development

```bash
# Install dependencies
cd frontend
npm install

# Run development server
npm run dev

# Run tests
npm test

# Build for production
npm run build

# Run linter
npm run lint
```

### Using Makefile

The project includes a comprehensive Makefile for common tasks:

```bash
make help          # Show all available commands
make install       # Install all dependencies
make dev           # Start development environment
make test          # Run all tests
make lint          # Lint all code
make logs          # View container logs
make init-db       # Initialize database
make clean         # Clean up generated files
```

## Project Structure

```
open-donation-tracker/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core functionality (config, security, db)
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── tests/          # Backend tests
│   │   ├── main.py         # FastAPI application
│   │   └── init_db.py      # Database initialization
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── contexts/       # React contexts
│   │   ├── hooks/          # Custom hooks
│   │   ├── types/          # TypeScript types
│   │   └── utils/          # Utility functions
│   ├── package.json
│   └── Dockerfile
├── .github/
│   └── workflows/          # GitHub Actions CI/CD
├── docker-compose.yml
├── Makefile
└── README.md
```

## API Documentation

The API is fully documented using OpenAPI (Swagger). When the backend is running, visit:

- **Interactive Docs**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

### Main Endpoints

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get tokens
- `GET /api/auth/me` - Get current user

#### Organizations
- `GET /api/organizations` - List all organizations
- `POST /api/organizations` - Create organization
- `GET /api/organizations/{id}` - Get organization details
- `GET /api/organizations/{id}/stats` - Get organization statistics
- `PATCH /api/organizations/{id}` - Update organization
- `DELETE /api/organizations/{id}` - Delete organization (admin)

#### Campaigns
- `GET /api/campaigns` - List all campaigns
- `POST /api/campaigns` - Create campaign
- `GET /api/campaigns/{id}` - Get campaign details
- `GET /api/campaigns/{id}/progress` - Get campaign progress
- `PATCH /api/campaigns/{id}` - Update campaign
- `DELETE /api/campaigns/{id}` - Delete campaign

#### Donations
- `GET /api/donations` - Get user's donations
- `GET /api/donations/all` - Get all public donations
- `POST /api/donations` - Create donation
- `GET /api/donations/stats` - Get donation statistics
- `GET /api/donations/{id}` - Get donation details
- `PATCH /api/donations/{id}` - Update donation

#### Impact Reports
- `GET /api/impact-reports` - List all impact reports
- `POST /api/impact-reports` - Create impact report
- `GET /api/impact-reports/{id}` - Get report details
- `PATCH /api/impact-reports/{id}` - Update report
- `DELETE /api/impact-reports/{id}` - Delete report

## Testing

### Backend Tests

```bash
# Run all tests with coverage
cd backend
pytest -v --cov=app --cov-report=html

# Run specific test file
pytest app/tests/test_auth.py -v

# Run with coverage report
pytest --cov=app --cov-report=term-missing
```

### Frontend Tests

```bash
# Run tests
cd frontend
npm test

# Run tests with coverage
npm test -- --coverage

# Run tests in watch mode
npm test -- --watch
```

## Deployment

### Docker Production Deployment

1. **Build production images**
   ```bash
   docker-compose -f docker-compose.prod.yml build
   ```

2. **Start services**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Set up SSL/TLS**
   - Use Let's Encrypt with Certbot
   - Configure Nginx as reverse proxy

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database
POSTGRES_USER=donationuser
POSTGRES_PASSWORD=<strong-password>
POSTGRES_DB=donationtracker
DATABASE_URL=postgresql://user:pass@postgres:5432/db

# Backend
SECRET_KEY=<generate-random-32+-char-string>
JWT_SECRET_KEY=<generate-random-32+-char-string>
ENVIRONMENT=production
CORS_ORIGINS=https://yourdomain.com

# Frontend
VITE_API_URL=https://api.yourdomain.com
```

### Security Checklist

- [ ] Change all default passwords
- [ ] Generate strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set up database backups
- [ ] Enable rate limiting
- [ ] Configure firewall rules
- [ ] Set up monitoring and logging
- [ ] Regular security updates

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: Check the `/docs` folder for detailed guides
- **Issues**: Report bugs or request features on GitHub Issues
- **Discussions**: Join our community discussions on GitHub Discussions

## Roadmap

- [ ] Payment gateway integration (Stripe, PayPal)
- [ ] Email notifications for donations and campaigns
- [ ] Mobile app (React Native)
- [ ] Advanced analytics and reporting
- [ ] Multi-language support
- [ ] Blockchain integration for donation tracking
- [ ] API rate limiting and throttling
- [ ] Advanced search and filtering
- [ ] Social media integration
- [ ] Automated tax receipt generation

## Acknowledgments

- FastAPI for the excellent web framework
- React team for the amazing UI library
- All contributors who help improve this project

## Screenshots

### Homepage
![Homepage](docs/screenshots/homepage.png)

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### Campaign Details
![Campaign](docs/screenshots/campaign.png)

---

Made with ❤️ by the Open Donation Tracker team
