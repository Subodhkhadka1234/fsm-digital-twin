# Troubleshooting Guide - "Site Cannot Be Reached"

## Problem: Site Cannot Be Reached

If you see "This site can't be reached" or "Connection refused" errors, follow these steps:

---

## ✅ Solution Steps

### Step 1: Check if Services are Running

```bash
cd /home/runner/work/fsm-digital-twin/fsm-digital-twin
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

**If services are NOT running (empty list):**
→ Go to Step 2

**If some services show "Exited" or "Unhealthy":**
→ Go to Step 3

---

### Step 2: Start the Services

#### Quick Start (Recommended)

```bash
# Start all services
docker compose up -d
```

#### Or Start Services Individually

```bash
# Start database and cache first
docker compose up -d postgres redis

# Wait 10 seconds for them to be healthy
sleep 10

# Start backend
docker compose up -d backend

# Start frontend (takes 2-5 minutes first time)
docker compose up -d frontend
```

---

### Step 3: Fix Common Issues

#### Issue: Services Keep Exiting

**Check logs:**
```bash
docker compose logs backend
docker compose logs frontend
```

**Common solutions:**
```bash
# Rebuild images
docker compose up -d --build

# Or rebuild specific service
docker compose up -d --build backend
```

#### Issue: Port Already in Use

**Error:** `Bind for 0.0.0.0:3000 failed: port is already allocated`

**Solution:**
```bash
# Find what's using the port
lsof -i :3000   # or :8000, :5432, :6379

# Kill the process
kill -9 <PID>

# Or change the port in docker-compose.yml
```

#### Issue: Database Not Healthy

**Check database logs:**
```bash
docker compose logs postgres
```

**Reset database:**
```bash
docker compose down -v  # Warning: deletes data
docker compose up -d postgres
```

---

## 🧪 Verify Services are Working

### Test Backend API (Port 8000)

```bash
# Health check
curl http://localhost:8000/health
# Expected: {"status":"healthy"}

# Root endpoint
curl http://localhost:8000/
# Expected: {"message":"FSM SaaS Platform API",...}
```

### Test Frontend (Port 3000)

```bash
# Check if port is listening
curl -I http://localhost:3000
# Expected: HTTP/1.1 200 OK
```

**In browser:** Open `http://localhost:3000`

---

## 📋 Quick Diagnostic Commands

```bash
# Check all containers
docker ps -a

# Check service status
docker compose ps

# View logs (all services)
docker compose logs -f

# View logs (specific service)
docker compose logs -f backend
docker compose logs -f frontend

# Check network connectivity
docker network ls
docker network inspect fsm-digital-twin_default

# Check volumes
docker volume ls
docker volume inspect fsm-digital-twin_postgres_data
```

---

## 🔍 Detailed Troubleshooting

### Backend API Not Responding

**Symptoms:**
- `curl http://localhost:8000` fails
- Connection refused
- Port 8000 not listening

**Debug steps:**

1. **Check if container is running:**
   ```bash
   docker compose ps backend
   ```

2. **Check logs:**
   ```bash
   docker compose logs backend | tail -50
   ```

3. **Check database connection:**
   ```bash
   docker compose exec backend python -c "from app.core.database import engine; print(engine.url)"
   ```

4. **Restart backend:**
   ```bash
   docker compose restart backend
   docker compose logs -f backend
   ```

5. **Rebuild backend:**
   ```bash
   docker compose up -d --build backend
   ```

### Frontend Not Loading

**Symptoms:**
- `http://localhost:3000` shows "This site can't be reached"
- Frontend container not running
- Build taking too long

**Debug steps:**

1. **Check if frontend is building:**
   ```bash
   docker compose logs frontend | tail -100
   ```

2. **Frontend build takes 2-5 minutes on first run:**
   - Installing 800+ npm packages
   - Building React application
   - **Be patient!**

3. **Check if build completed:**
   ```bash
   docker compose logs frontend | grep -i "compiled successfully"
   ```

4. **If build failed, rebuild:**
   ```bash
   docker compose down frontend
   docker compose up -d --build frontend
   ```

5. **Watch build progress:**
   ```bash
   docker compose logs -f frontend
   ```

### Database Connection Issues

**Symptoms:**
- Backend logs show database errors
- "Connection refused" to postgres
- "password authentication failed"

**Debug steps:**

1. **Check postgres is healthy:**
   ```bash
   docker compose ps postgres
   # Should show "Up (healthy)"
   ```

2. **Test database connection:**
   ```bash
   docker compose exec postgres psql -U fsm_user -d fsm_db -c "SELECT 1;"
   ```

3. **Check environment variables:**
   ```bash
   docker compose exec backend env | grep DATABASE_URL
   ```

4. **Reset database:**
   ```bash
   docker compose down postgres
   docker volume rm fsm-digital-twin_postgres_data
   docker compose up -d postgres
   
   # Wait for healthy
   sleep 10
   
   # Run migrations and seed
   docker compose exec backend alembic upgrade head
   docker compose exec backend python seed_db.py
   ```

---

## 🚨 Nuclear Option: Full Reset

If nothing else works, reset everything:

```bash
# Stop all services
docker compose down

# Remove all volumes (deletes data!)
docker compose down -v

# Remove all images
docker rmi $(docker images -q 'fsm-digital-twin*')

# Start fresh
docker compose up -d --build

# Wait for services to start
sleep 30

# Check status
docker compose ps

# Test backend
curl http://localhost:8000/health
```

---

## 📊 Service Startup Times

**Normal startup times:**
- **PostgreSQL**: 5-10 seconds
- **Redis**: 3-5 seconds
- **Backend**: 10-15 seconds
- **Frontend** (first time): 2-5 minutes
- **Frontend** (subsequent): 30-60 seconds

---

## 💡 Prevention Tips

### Always Start Services Before Accessing

```bash
# Add to your workflow
cd fsm-digital-twin
docker compose up -d
sleep 30  # Wait for services
# Now access http://localhost:3000 or :8000
```

### Use the Start Script

```bash
./start.sh
# This script handles service startup automatically
```

### Check Status Regularly

```bash
# Add alias to your .bashrc or .zshrc
alias fsm-status='docker compose ps'
alias fsm-logs='docker compose logs -f'
alias fsm-restart='docker compose restart'
```

---

## 📞 Still Having Issues?

### Collect Debug Information

```bash
# Save all logs
docker compose logs > debug-logs.txt

# Save system info
docker version >> debug-logs.txt
docker compose version >> debug-logs.txt
docker compose ps >> debug-logs.txt
docker network ls >> debug-logs.txt
docker volume ls >> debug-logs.txt
```

### Check Documentation

- `README.md` - Project overview
- `QUICKSTART.md` - Setup guide
- `ACCESS_GUIDE.md` - URL and access information
- `DEMO_STATUS.md` - Current implementation status

---

## ✅ Success Checklist

After fixing, verify:

- [ ] `docker compose ps` shows all services "Up"
- [ ] `curl http://localhost:8000/health` returns `{"status":"healthy"}`
- [ ] Backend accessible at `http://localhost:8000`
- [ ] Frontend accessible at `http://localhost:3000` (wait 5 min if building)
- [ ] Can login with test credentials
- [ ] No error messages in `docker compose logs`

---

**Last Updated:** 2026-02-19

**Most Common Issue:** Services not started → Run `docker compose up -d`
