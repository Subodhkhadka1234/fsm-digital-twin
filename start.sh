#!/bin/bash
# Startup script for FSM SaaS Platform

set -e

echo "🚀 Starting FSM SaaS Platform Setup..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check for docker compose (new command) or docker-compose (old command)
if command -v docker &> /dev/null && docker compose version &> /dev/null; then
    echo "✅ Docker Compose (v2) is available"
elif command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose (v1) is available"
else
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating .env file from example..."
    cp backend/.env.example backend/.env
    echo "⚠️  Please update backend/.env with your configuration"
fi

# Create models directory
mkdir -p backend/models

echo "🐳 Starting Docker containers..."
docker compose up -d postgres redis

echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 10

# Check if PostgreSQL is ready
until docker compose exec -T postgres pg_isready -U fsm_user -d fsm_db &> /dev/null; do
    echo "Waiting for PostgreSQL..."
    sleep 2
done

echo "✅ PostgreSQL is ready"

# Enable PostGIS extension
echo "📍 Enabling PostGIS extension..."
docker compose exec -T postgres psql -U fsm_user -d fsm_db -c "CREATE EXTENSION IF NOT EXISTS postgis;" || echo "PostGIS may already be enabled"

echo "🚀 Starting backend service..."
docker compose up -d --build backend

echo "⏳ Waiting for backend to be ready..."
sleep 15

echo "🔄 Running database migrations..."
docker compose exec -T backend alembic upgrade head 2>/dev/null || echo "⚠️  Migrations will run on backend startup"

echo "🌱 Seeding database with initial data..."
docker compose exec -T backend python seed_db.py 2>/dev/null || echo "⚠️  Database already seeded or will seed on startup"

echo "🎨 Starting frontend service (this may take 2-5 minutes on first run)..."
docker compose up -d frontend

echo ""
echo "⏳ Services are starting..."
echo "   Backend should be ready in ~15 seconds"
echo "   Frontend may take 2-5 minutes to build (first time only)"
echo ""

echo ""
echo "✅ Setup complete!"
echo ""
echo "📌 Access the application:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - API Documentation: http://localhost:8000/api/v1/docs"
echo ""
echo "👤 Default credentials:"
echo "   - Admin: admin@example.com / admin123"
echo "   - Technician: tech1@example.com / tech123"
echo "   - Customer: customer1@example.com / customer123"
echo ""
echo "📋 View logs with: docker compose logs -f"
echo "🛑 Stop services with: docker compose down"
echo ""
echo "💡 Troubleshooting: See TROUBLESHOOTING.md if you have issues"
echo "📖 Full documentation: See ACCESS_GUIDE.md for all URLs"
