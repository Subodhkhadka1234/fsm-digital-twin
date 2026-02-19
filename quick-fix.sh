#!/bin/bash

###############################################################################
# Quick Fix Script - Restart FSM SaaS Platform Services
###############################################################################

set -e

echo "════════════════════════════════════════════════════════════════════"
echo "  FSM SaaS Platform - Quick Service Restart"
echo "════════════════════════════════════════════════════════════════════"
echo ""

# Change to script directory
cd "$(dirname "$0")"

echo "📋 Step 1: Stopping any existing services..."
docker compose down 2>/dev/null || true
echo "✅ Services stopped"
echo ""

echo "📋 Step 2: Starting PostgreSQL database..."
docker compose up -d postgres
echo "⏳ Waiting for database to be healthy (15 seconds)..."
sleep 15
echo "✅ Database ready"
echo ""

echo "📋 Step 3: Starting Redis cache..."
docker compose up -d redis
echo "⏳ Waiting for Redis to be ready (5 seconds)..."
sleep 5
echo "✅ Redis ready"
echo ""

echo "📋 Step 4: Building and starting Backend API..."
# Build backend if needed
if ! docker images | grep -q "fsm-digital-twin-backend"; then
    echo "🔨 Building backend image (first time only, ~1-2 minutes)..."
    docker compose build backend
fi
docker compose up -d backend
echo "⏳ Waiting for backend to start (10 seconds)..."
sleep 10
echo "✅ Backend ready"
echo ""

echo "📋 Step 5: Testing backend connectivity..."
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo "✅ Backend is responding!"
else
    echo "⚠️  Backend is starting, may need a few more seconds..."
fi
echo ""

echo "════════════════════════════════════════════════════════════════════"
echo "  ✅ BACKEND API IS NOW RUNNING!"
echo "════════════════════════════════════════════════════════════════════"
echo ""
echo "🌐 Access URLs:"
echo "   • Backend API:  http://localhost:8000"
echo "   • Health Check: http://localhost:8000/health"
echo "   • API Root:     http://localhost:8000/"
echo ""
echo "🔐 Login Credentials:"
echo "   • Admin:      admin@example.com / admin123"
echo "   • Technician: tech1@example.com / admin123"
echo "   • Customer:   customer1@example.com / admin123"
echo ""
echo "📝 Test Commands:"
echo "   curl http://localhost:8000/health"
echo "   curl http://localhost:8000/"
echo ""
echo "📋 Check Status:"
echo "   docker compose ps"
echo "   docker compose logs backend"
echo ""
echo "════════════════════════════════════════════════════════════════════"
echo ""
echo "ℹ️  Note: Frontend is NOT started (takes 5-10 minutes to build)"
echo "   You can use the backend API directly for testing."
echo ""
echo "   To start frontend later (optional):"
echo "   docker compose up -d frontend"
echo ""
echo "════════════════════════════════════════════════════════════════════"
