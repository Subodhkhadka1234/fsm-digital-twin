# Quick Start Guide

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Git

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Subodhkhadka1234/fsm-digital-twin.git
cd fsm-digital-twin
```

### 2. Quick Start with Docker (Recommended)

```bash
# Make the startup script executable
chmod +x start.sh

# Run the automated setup
./start.sh
```

This script will:
- Check Docker installation
- Create `.env` file from example
- Start PostgreSQL and Redis
- Enable PostGIS extension
- Run database migrations
- Seed the database with sample data
- Start all services

### 3. Access the Application

Once all services are running:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/v1/docs
- **Health Check**: http://localhost:8000/health

### 4. Login Credentials

Default test accounts:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@example.com | admin123 |
| Technician | tech1@example.com | tech123 |
| Customer | customer1@example.com | customer123 |

## Manual Setup (Without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration

# Install PostgreSQL with PostGIS
# Ubuntu/Debian:
sudo apt-get install postgresql-14 postgresql-14-postgis-3

# Create database
sudo -u postgres createdb fsm_db
sudo -u postgres psql fsm_db -c "CREATE EXTENSION postgis;"

# Run migrations
alembic upgrade head

# Seed database
python seed_db.py

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The frontend will be available at http://localhost:3000

## Docker Commands

### Start All Services
```bash
docker-compose up -d
```

### Stop All Services
```bash
docker-compose down
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Restart a Service
```bash
docker-compose restart backend
```

### Rebuild Containers
```bash
docker-compose up -d --build
```

### Access Container Shell
```bash
# Backend
docker-compose exec backend bash

# Database
docker-compose exec postgres psql -U fsm_user -d fsm_db
```

## Database Management

### Run Migrations
```bash
docker-compose exec backend alembic upgrade head
```

### Create New Migration
```bash
docker-compose exec backend alembic revision --autogenerate -m "Description"
```

### Reset Database
```bash
docker-compose down -v  # This removes volumes
docker-compose up -d
./start.sh  # Re-seed database
```

## Testing

### Backend Tests
```bash
# With Docker
docker-compose exec backend pytest tests/ -v

# Without Docker
cd backend
pytest tests/ -v --cov=app
```

### Frontend Tests
```bash
# With Docker
docker-compose exec frontend npm test

# Without Docker
cd frontend
npm test
```

## Development Workflow

1. **Make Changes**: Edit files in your local directory
2. **Hot Reload**: Changes are automatically reflected
   - Backend: FastAPI auto-reloads
   - Frontend: React hot module replacement
3. **Test**: Run tests locally
4. **Commit**: Push to repository
5. **CI/CD**: GitHub Actions runs tests automatically

## Troubleshooting

### Port Already in Use
```bash
# Check what's using the port
lsof -i :8000  # Backend
lsof -i :3000  # Frontend
lsof -i :5432  # PostgreSQL

# Stop the service or change ports in docker-compose.yml
```

### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

### Frontend Won't Start
```bash
# Remove node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Backend Module Not Found
```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## Environment Variables

Key environment variables in `backend/.env`:

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key (change in production!)
- `REDIS_URL`: Redis connection string
- `DEBUG`: Enable debug mode (set to False in production)
- `CORS_ORIGINS`: Allowed CORS origins

## Production Deployment

For production deployment:

1. Change `SECRET_KEY` to a strong random value
2. Set `DEBUG=False`
3. Configure proper CORS origins
4. Use production database
5. Set up HTTPS/TLS
6. Configure rate limiting
7. Set up monitoring and logging
8. Use production-grade WSGI server (Gunicorn)

## API Usage Examples

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=admin123"
```

### Get Dashboard (with token)
```bash
curl -X GET http://localhost:8000/api/v1/admin/dashboard \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Create Job
```bash
curl -X POST http://localhost:8000/api/v1/admin/jobs \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "uuid-here",
    "job_type": "Plumbing",
    "priority": "high",
    "location": {"lat": 37.7749, "lng": -122.4194},
    "address": "123 Main St, San Francisco, CA"
  }'
```

## Getting Help

- Check the [README.md](README.md) for overview
- Read [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- View API docs at http://localhost:8000/api/v1/docs
- Open an issue on GitHub for bugs or questions

## Next Steps

After getting the application running:

1. Explore the API documentation
2. Try creating jobs and assigning them
3. Test different user roles
4. Review the code structure
5. Customize for your needs
6. Add your own features
