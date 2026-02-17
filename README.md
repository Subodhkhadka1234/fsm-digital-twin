# FSM SaaS Platform - Field Service Management Digital Twin

A production-ready Field Service Management SaaS application with ML-driven scheduling and risk-aware routing.

## 🚀 Features

- **Multi-role Authentication**: JWT-based auth for Admin, Technician, and Customer roles
- **Job Management**: Complete lifecycle management from creation to completion
- **Smart Scheduling**: ML-powered service duration prediction
- **Route Optimization**: OR-Tools VRP solver for efficient technician routing
- **Real-time Updates**: WebSocket support for live notifications
- **ETL Pipeline**: Robust data ingestion and processing
- **Geospatial Support**: PostGIS integration for location-based features
- **Responsive UI**: React + TypeScript + Material-UI

## 🏗️ Architecture

### Tech Stack

**Backend:**
- FastAPI (Python 3.11+)
- PostgreSQL 14+ with PostGIS
- SQLAlchemy + Alembic
- Redis for caching and sessions
- Celery for async tasks
- scikit-learn for ML predictions
- OR-Tools for route optimization

**Frontend:**
- React 18+ with TypeScript
- Redux Toolkit for state management
- Material-UI components
- Leaflet for maps
- Axios for API calls

**Infrastructure:**
- Docker & Docker Compose
- Nginx (production)

## 📦 Project Structure

```
fsm-digital-twin/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/    # API endpoints
│   │   ├── core/                # Config, security, database
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── services/            # Business logic
│   │   ├── ml_engine/           # ML prediction
│   │   ├── optimization/        # Route optimization
│   │   ├── etl/                 # ETL pipeline
│   │   └── tasks/               # Celery tasks
│   ├── alembic/                 # Database migrations
│   ├── tests/                   # Unit & integration tests
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API service
│   │   ├── store/               # Redux store
│   │   └── types/               # TypeScript types
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
├── docker-compose.yml
├── datasets (2).zip             # Historical data
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Git

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Subodhkhadka1234/fsm-digital-twin.git
cd fsm-digital-twin
```

2. **Set up environment variables:**
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your configuration
```

3. **Start all services:**
```bash
docker-compose up -d
```

4. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/v1/docs

### Default Users (After seeding)

- **Admin**: admin@example.com / admin123
- **Technician**: tech@example.com / tech123
- **Customer**: customer@example.com / customer123

## 🔧 Development

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Running Tests

**Backend:**
```bash
cd backend
pytest tests/ -v --cov=app
```

**Frontend:**
```bash
cd frontend
npm test
```

## 📊 Database Setup

The application uses PostgreSQL with PostGIS extension for geospatial features.

### Manual Database Setup (if not using Docker)

```bash
# Install PostgreSQL with PostGIS
sudo apt-get install postgresql-14 postgresql-14-postgis-3

# Create database
sudo -u postgres psql
CREATE DATABASE fsm_db;
CREATE USER fsm_user WITH PASSWORD 'fsm_password';
GRANT ALL PRIVILEGES ON DATABASE fsm_db TO fsm_user;

# Enable PostGIS
\c fsm_db
CREATE EXTENSION postgis;
```

### Run Migrations

```bash
cd backend
alembic upgrade head
```

## 🔐 API Authentication

All protected endpoints require JWT authentication.

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=admin123"
```

**Use token:**
```bash
curl -X GET http://localhost:8000/api/v1/admin/dashboard \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📡 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/register` - Customer registration
- `POST /api/v1/auth/refresh` - Refresh token
- `POST /api/v1/auth/logout` - Logout

### Admin
- `GET /api/v1/admin/dashboard` - Dashboard KPIs
- `GET /api/v1/admin/jobs` - List all jobs
- `POST /api/v1/admin/jobs` - Create job
- `PUT /api/v1/admin/jobs/{id}` - Update job
- `POST /api/v1/admin/jobs/{id}/assign` - Assign job to technician

### Technician
- `GET /api/v1/technician/dashboard` - Dashboard data
- `GET /api/v1/technician/jobs` - My jobs
- `POST /api/v1/technician/jobs/{id}/start` - Start job
- `POST /api/v1/technician/jobs/{id}/complete` - Complete job

### Customer
- `GET /api/v1/customer/dashboard` - Dashboard data
- `POST /api/v1/customer/jobs` - Create job request
- `GET /api/v1/customer/jobs` - My jobs
- `GET /api/v1/customer/jobs/{id}` - Job details

## 🗄️ Database Schema

### Core Tables

- **users**: User accounts with role-based access
- **organizations**: Multi-tenancy support
- **technicians**: Technician profiles with skills and location
- **customers**: Customer profiles and preferences
- **jobs**: Service requests and assignments
- **routes**: Optimized technician routes
- **job_history**: Audit trail for job changes
- **notifications**: User notifications
- **ml_models**: ML model versioning and metrics

## 🤖 ML & Optimization

### Service Duration Prediction

Uses Random Forest Regressor to predict job duration based on:
- Machine age
- Failure category
- Complexity score
- Client priority
- Technician skill match

### Route Optimization

Uses Google OR-Tools with Vehicle Routing Problem (VRP) solver:
- Skill matching constraints
- Time windows (SLA deadlines)
- Working hours constraints
- Capacity constraints
- Multi-objective optimization

## 📈 ETL Pipeline

Process historical data from CSV files:

1. **Extract**: Load data from CSV files
2. **Transform**: Clean, validate, and enrich data
3. **Load**: Bulk insert into PostgreSQL
4. **Validate**: Generate data quality reports

## 🧪 Testing

### Run All Tests
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

### Test Coverage
```bash
cd backend
pytest --cov=app --cov-report=html
```

## 🚢 Deployment

### Production Deployment with Docker

```bash
# Build and start production containers
docker-compose up -d

# View logs
docker-compose logs -f
```

### Environment Variables

Key environment variables (see `.env.example`):
- `SECRET_KEY`: JWT secret key
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `DEBUG`: Enable/disable debug mode

## 📝 License

This project is licensed under the MIT License.

## 👥 Contributors

- Subodh Khadka

## 📞 Support

For issues and questions, please open an issue on GitHub.

## 🔄 Version History

### v1.0.0 (Current)
- Initial release
- Multi-role authentication
- Job management CRUD
- Basic dashboard for all roles
- Docker containerization
- API documentation

### Roadmap
- [ ] ML model training integration
- [ ] OR-Tools route optimization
- [ ] WebSocket real-time updates
- [ ] Advanced analytics and reporting
- [ ] Mobile app
- [ ] Payment integration
