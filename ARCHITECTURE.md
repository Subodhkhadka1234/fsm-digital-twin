# Architecture Overview

## System Architecture

The FSM SaaS Platform follows a modern microservices-inspired architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                       Frontend (React)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Admin   │  │Technician│  │ Customer │  │   Maps   │   │
│  │Dashboard │  │Dashboard │  │Dashboard │  │  Leaflet │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                    Redux Toolkit State Management            │
└──────────────────────────┬──────────────────────────────────┘
                           │ REST API (Axios)
                           │ WebSocket (Socket.IO)
┌──────────────────────────┴──────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              API Layer (v1/endpoints)                   │ │
│  │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐   │ │
│  │  │ Auth │  │Admin │  │ Tech │  │ Cust │  │ Jobs │   │ │
│  │  └──────┘  └──────┘  └──────┘  └──────┘  └──────┘   │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │            Business Logic (Services)                    │ │
│  │  • Authentication • Authorization • Job Management      │ │
│  │  • Scheduling • Notifications                          │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌───────────────┬────────────────┬─────────────────────┐  │
│  │  ML Engine    │  Optimization  │    ETL Pipeline     │  │
│  │  ┌─────────┐  │  ┌──────────┐  │  ┌────────────┐    │  │
│  │  │Predictor│  │  │VRP Solver│  │  │Extractors  │    │  │
│  │  │ (RF)    │  │  │(OR-Tools)│  │  │Transformers│    │  │
│  │  └─────────┘  │  └──────────┘  │  │Loaders     │    │  │
│  └───────────────┴────────────────┴─────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                     Data Layer                               │
│  ┌─────────────────┐  ┌─────────────┐  ┌───────────────┐   │
│  │   PostgreSQL    │  │    Redis    │  │    Celery     │   │
│  │   + PostGIS     │  │   Cache &   │  │  Task Queue   │   │
│  │                 │  │   Sessions  │  │               │   │
│  └─────────────────┘  └─────────────┘  └───────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Backend
- **Framework**: FastAPI 0.109.0 (async, high-performance)
- **ORM**: SQLAlchemy 2.0+ with Alembic migrations
- **Database**: PostgreSQL 14+ with PostGIS extension
- **Cache**: Redis 5.0+ for session management and caching
- **Task Queue**: Celery 5.3+ with Redis broker
- **Auth**: JWT (python-jose) with bcrypt password hashing
- **ML**: scikit-learn 1.4+ for Random Forest models
- **Optimization**: Google OR-Tools 9.8+ for VRP solving
- **Validation**: Pydantic 2.5+ for request/response validation

### Frontend
- **Framework**: React 18+ with TypeScript 5.3+
- **State Management**: Redux Toolkit 2.0+
- **UI Library**: Material-UI (MUI) 5.15+
- **Maps**: Leaflet 1.9+ with React-Leaflet
- **HTTP Client**: Axios 1.6+
- **Routing**: React Router 6+

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Monitoring**: Structured logging (JSON format)

## Data Flow

### 1. Authentication Flow
```
User → Login Form → POST /api/v1/auth/login
  ↓
FastAPI → Verify Credentials → Database
  ↓
Generate JWT Tokens (Access + Refresh)
  ↓
Return Tokens → Store in Redux + LocalStorage
  ↓
Subsequent Requests → Bearer Token in Header
```

### 2. Job Creation Flow
```
Customer → Create Job Form
  ↓
POST /api/v1/customer/jobs
  ↓
Validate Request (Pydantic Schema)
  ↓
Create Job Record in Database
  ↓
Trigger ML Prediction (Celery Task)
  ↓
Update predicted_duration_hours
  ↓
Notify Admin Dashboard (WebSocket)
```

### 3. Route Optimization Flow
```
Admin → Trigger Optimization
  ↓
POST /api/v1/admin/scheduling/optimize
  ↓
Create Celery Task (optimize_routes)
  ↓
Fetch Jobs & Technicians from Database
  ↓
Build OR-Tools VRP Model
  ↓
Solve with Constraints
  ↓
Create Route Records
  ↓
Update Job Assignments
  ↓
Publish Routes → Notify Technicians
```

## Security Architecture

### Authentication & Authorization
- **JWT Tokens**: 
  - Access Token: 15 minutes expiration
  - Refresh Token: 7 days expiration with rotation
- **Password Security**: bcrypt hashing with salt
- **RBAC**: Role-based access control (Admin, Technician, Customer)
- **Organization Isolation**: Multi-tenancy with organization_id filtering

### API Security
- **HTTPS Only**: All production traffic encrypted
- **CORS**: Configured allowed origins
- **Rate Limiting**: 100 requests/minute per user
- **Input Validation**: Pydantic schemas for all endpoints
- **SQL Injection Prevention**: Parameterized queries via ORM

## Database Schema

### Core Entities
- **users**: Authentication and role management
- **organizations**: Multi-tenancy support
- **technicians**: Technician profiles with skills and location
- **customers**: Customer profiles with priority tiers
- **jobs**: Service requests and assignments
- **routes**: Optimized technician routes
- **job_history**: Audit trail for job changes
- **notifications**: User notifications
- **ml_models**: ML model versioning

### Relationships
- User → Technician/Customer (1:1)
- Organization → Users/Jobs (1:N)
- Customer → Jobs (1:N)
- Technician → Jobs (1:N)
- Technician → Routes (1:N)
- Job → JobHistory (1:N)

## API Design

### RESTful Principles
- Resource-based URLs
- HTTP methods (GET, POST, PUT, DELETE)
- Status codes (200, 201, 400, 401, 403, 404, 500)
- JSON request/response format
- Pagination for list endpoints

### Versioning
- URL-based versioning: `/api/v1/...`
- Backwards compatibility maintained

### Documentation
- Auto-generated OpenAPI/Swagger docs
- Available at `/api/v1/docs`

## Scalability Considerations

### Horizontal Scaling
- Stateless API servers (JWT-based auth)
- Database connection pooling
- Redis for shared session state
- Load balancer ready

### Performance Optimization
- Database indexes on foreign keys and filters
- Redis caching for frequent queries
- Async endpoints with FastAPI
- Celery for long-running tasks
- CDN for static assets (production)

### Monitoring & Logging
- Structured JSON logging
- Request/response logging via middleware
- Error tracking (Sentry integration ready)
- Performance metrics tracking

## Development Workflow

1. **Local Development**: Docker Compose with hot-reload
2. **Testing**: pytest for backend, Jest for frontend
3. **CI/CD**: GitHub Actions for automated testing
4. **Deployment**: Docker containers to cloud platforms

## Future Enhancements

- [ ] WebSocket real-time updates
- [ ] Advanced ML models (XGBoost, Neural Networks)
- [ ] More sophisticated VRP constraints
- [ ] Mobile app (React Native)
- [ ] Payment integration (Stripe)
- [ ] SMS notifications (Twilio)
- [ ] Advanced analytics dashboard
- [ ] Multi-language support (i18n)
