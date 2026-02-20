# 🌐 FSM SaaS Platform - Access Guide

## Quick Answer: Where to Access the Application

### 🎯 Main Application URLs

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | **http://localhost:3000** | Main UI - Login and Dashboards |
| **Backend API** | **http://localhost:8000** | REST API Endpoints |
| **API Docs** | **http://localhost:8000/api/v1/docs** | Interactive Swagger UI |
| **API Docs (Alt)** | **http://localhost:8000/api/v1/redoc** | ReDoc Documentation |
| **Database** | `localhost:5432` | PostgreSQL + PostGIS |
| **Redis** | `localhost:6379` | Cache & Task Queue |

---

## 🚀 How to Start the Application

### Step 1: Start All Services

```bash
cd /path/to/fsm-digital-twin
./start.sh
```

**OR** using Docker Compose directly:

```bash
docker compose up -d
```

### Step 2: Wait for Services to Start

The services take about 30-60 seconds to fully start up:
- ✅ PostgreSQL (5-10 seconds)
- ✅ Redis (3-5 seconds)
- ✅ Backend API (10-15 seconds)
- ⏳ Frontend (2-5 minutes for first build)

### Step 3: Access the Application

Once services are running, open your web browser:

**🌟 Main Application:**
```
http://localhost:3000
```

**📚 API Documentation:**
```
http://localhost:8000/api/v1/docs
```

---

## 🔐 Login Credentials

Use these test accounts to login:

### 👨‍💼 Admin User
```
Email:    admin@example.com
Password: admin123
```
**Access to:**
- Dashboard with KPIs
- Job management
- Technician management
- Customer management
- Route optimization
- Analytics

### 👷 Technician User
```
Email:    tech1@example.com
Password: admin123
```
**Access to:**
- Personal dashboard
- Assigned jobs
- Job start/complete
- Schedule view
- Profile settings

### 👤 Customer User
```
Email:    customer1@example.com
Password: admin123
```
**Access to:**
- Dashboard
- Create service requests
- Track jobs
- View invoices
- Contact support

---

## 📱 What You'll See

### Frontend (http://localhost:3000)

**Login Page** → Choose your role and login
↓
**Dashboard** → Role-specific interface:
- **Admin**: KPIs, job management, technician tracking
- **Technician**: Today's schedule, active jobs
- **Customer**: Service requests, job tracking

### API Documentation (http://localhost:8000/api/v1/docs)

Interactive Swagger UI where you can:
- ✅ Browse all API endpoints
- ✅ Test endpoints directly
- ✅ See request/response schemas
- ✅ Authenticate with JWT tokens
- ✅ Try out API calls

---

## 🔍 Service Details

### Frontend Service
```yaml
Container:  fsm_frontend
Port:       3000
Tech:       React 18 + TypeScript
Features:   
  - Login/Logout
  - Role-based dashboards
  - Job management UI
  - Material-UI components
```

### Backend Service
```yaml
Container:  fsm_backend
Port:       8000
Tech:       FastAPI + Python 3.11
Features:   
  - 15+ REST API endpoints
  - JWT authentication
  - Role-based access control
  - PostgreSQL + PostGIS
  - Swagger/ReDoc docs
```

### Database Service
```yaml
Container:  fsm_postgres
Port:       5432
Tech:       PostgreSQL 14 + PostGIS
Database:   fsm_db
Username:   fsm_user
Password:   fsm_password
```

### Redis Service
```yaml
Container:  fsm_redis
Port:       6379
Tech:       Redis 7
Purpose:    
  - Session caching
  - Celery task queue
  - Rate limiting
```

---

## 🛠️ Checking Service Status

### Check if Services are Running

```bash
docker compose ps
```

**Expected output:**
```
NAME           STATUS    PORTS
fsm_backend    Up        0.0.0.0:8000->8000/tcp
fsm_frontend   Up        0.0.0.0:3000->3000/tcp
fsm_postgres   Up        0.0.0.0:5432->5432/tcp
fsm_redis      Up        0.0.0.0:6379->6379/tcp
```

### View Logs

**All services:**
```bash
docker compose logs -f
```

**Specific service:**
```bash
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f postgres
```

### Test Backend Health

```bash
curl http://localhost:8000/health
```

**Expected:**
```json
{"status":"healthy"}
```

---

## 🌍 Production/Deployment URLs

### When Deployed to a Server

Replace `localhost` with your server's IP address or domain:

**Frontend:**
```
http://YOUR_DOMAIN:3000
```

**Backend API:**
```
http://YOUR_DOMAIN:8000
```

### Common Deployment Scenarios

#### 1. Same Server with Nginx Reverse Proxy
```
Frontend:  https://your-domain.com
Backend:   https://your-domain.com/api
API Docs:  https://your-domain.com/api/v1/docs
```

#### 2. Separate Domains
```
Frontend:  https://app.your-domain.com
Backend:   https://api.your-domain.com
API Docs:  https://api.your-domain.com/v1/docs
```

#### 3. Cloud Platforms

**AWS:**
```
Frontend:  https://your-app.elasticbeanstalk.com
Backend:   https://your-api.elasticbeanstalk.com
```

**Heroku:**
```
Frontend:  https://your-app.herokuapp.com
Backend:   https://your-api.herokuapp.com
```

**DigitalOcean:**
```
Frontend:  https://your-droplet-ip:3000
Backend:   https://your-droplet-ip:8000
```

---

## 🔧 Troubleshooting Access Issues

### Frontend Not Loading (http://localhost:3000)

**Issue:** "This site can't be reached"

**Solutions:**
```bash
# 1. Check if frontend is running
docker compose ps frontend

# 2. Check frontend logs
docker compose logs frontend

# 3. Restart frontend
docker compose restart frontend

# 4. Rebuild if needed
docker compose up -d --build frontend
```

**Common causes:**
- Frontend still building (wait 5 min)
- Port 3000 already in use
- npm install failed

### Backend Not Responding (http://localhost:8000)

**Issue:** Connection refused or timeout

**Solutions:**
```bash
# 1. Check backend status
docker compose ps backend

# 2. Check backend logs
docker compose logs backend | tail -50

# 3. Restart backend
docker compose restart backend

# 4. Check database connection
docker compose exec backend python -c "from app.core.database import engine; print(engine.url)"
```

### API Documentation Not Loading

**Issue:** Swagger UI blank or CDN errors

**Cause:** External CDN resources may be blocked

**Solutions:**
1. Use ReDoc instead: `http://localhost:8000/api/v1/redoc`
2. Allow CDN access in network settings
3. Use direct API endpoints with curl/Postman

### Port Already in Use

**Issue:** "Port 3000 (or 8000) is already allocated"

**Solutions:**
```bash
# Find what's using the port
lsof -i :3000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different ports in docker-compose.yml
ports:
  - "3001:3000"  # Frontend on 3001
  - "8001:8000"  # Backend on 8001
```

---

## 📞 Need Help?

### Quick Diagnostics

Run this command to check everything:
```bash
./validate_readiness.py
```

### View All Documentation

```bash
# Project overview
cat README.md

# Setup guide
cat QUICKSTART.md

# Current status
cat DEMO_STATUS.md

# Architecture
cat ARCHITECTURE.md
```

### Manual API Testing

Even if frontend isn't working, you can use the API:

```bash
# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=admin123"

# Get dashboard (use token from above)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/v1/admin/dashboard
```

---

## 📊 Summary

### ✅ Primary Access Points

**For Users:**
1. Open browser
2. Go to **http://localhost:3000**
3. Login with credentials above
4. Use the application

**For Developers:**
1. API Docs: **http://localhost:8000/api/v1/docs**
2. Test endpoints directly
3. View request/response examples
4. Generate client code

**For DevOps:**
1. Check service health: `docker compose ps`
2. View logs: `docker compose logs -f`
3. Database access: `docker compose exec postgres psql -U fsm_user -d fsm_db`

---

## 🎯 Next Steps

Once you have access:

1. **Explore the Frontend**
   - Login as different roles
   - Create test jobs
   - View dashboards

2. **Test the API**
   - Try authentication
   - Call protected endpoints
   - Test CRUD operations

3. **Review Documentation**
   - Read architecture docs
   - Check implementation status
   - Plan next features

---

**Current Status**: Backend fully operational, Frontend ready to build

**Access Now**: Run `./start.sh` and visit **http://localhost:3000** 🚀
