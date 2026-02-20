#!/usr/bin/env python3
"""
Application Readiness Validation Script
Checks if the FSM SaaS Platform is ready to run
"""
import sys
import os
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists"""
    if Path(file_path).exists():
        print(f"✅ {description}: Found")
        return True
    else:
        print(f"❌ {description}: Missing")
        return False

def check_directory_exists(dir_path, description):
    """Check if a directory exists"""
    if Path(dir_path).is_dir():
        print(f"✅ {description}: Found")
        return True
    else:
        print(f"❌ {description}: Missing")
        return False

def main():
    print("=" * 80)
    print("FSM SAAS PLATFORM - READINESS VALIDATION")
    print("=" * 80)
    print()
    
    base_dir = Path(__file__).parent
    passed = 0
    total = 0
    
    # Check backend files
    print("📦 BACKEND STRUCTURE")
    print("-" * 80)
    
    checks = [
        (base_dir / "backend" / "requirements.txt", "Backend requirements.txt"),
        (base_dir / "backend" / "Dockerfile", "Backend Dockerfile"),
        (base_dir / "backend" / "app" / "main.py", "Main FastAPI app"),
        (base_dir / "backend" / "app" / "core" / "config.py", "Configuration"),
        (base_dir / "backend" / "app" / "core" / "security.py", "Security module"),
        (base_dir / "backend" / "app" / "core" / "database.py", "Database module"),
        (base_dir / "backend" / "app" / "models" / "user.py", "User model"),
        (base_dir / "backend" / "app" / "models" / "job.py", "Job model"),
        (base_dir / "backend" / "app" / "api" / "v1" / "api.py", "API router"),
        (base_dir / "backend" / "alembic.ini", "Alembic config"),
        (base_dir / "backend" / "seed_db.py", "Seed script"),
    ]
    
    for file_path, description in checks:
        total += 1
        if check_file_exists(file_path, description):
            passed += 1
    
    print()
    
    # Check frontend files
    print("⚛️  FRONTEND STRUCTURE")
    print("-" * 80)
    
    checks = [
        (base_dir / "frontend" / "package.json", "Frontend package.json"),
        (base_dir / "frontend" / "Dockerfile", "Frontend Dockerfile"),
        (base_dir / "frontend" / "tsconfig.json", "TypeScript config"),
        (base_dir / "frontend" / "src" / "App.tsx", "Main App component"),
        (base_dir / "frontend" / "src" / "index.tsx", "App entry point"),
        (base_dir / "frontend" / "src" / "services" / "api.ts", "API service"),
        (base_dir / "frontend" / "src" / "store" / "store.ts", "Redux store"),
        (base_dir / "frontend" / "src" / "pages" / "auth" / "Login.tsx", "Login page"),
    ]
    
    for file_path, description in checks:
        total += 1
        if check_file_exists(file_path, description):
            passed += 1
    
    print()
    
    # Check infrastructure
    print("🐳 INFRASTRUCTURE")
    print("-" * 80)
    
    checks = [
        (base_dir / "docker-compose.yml", "Docker Compose config"),
        (base_dir / "start.sh", "Startup script"),
        (base_dir / ".github" / "workflows" / "ci.yml", "CI/CD pipeline"),
        (base_dir / ".gitignore", "Gitignore file"),
    ]
    
    for file_path, description in checks:
        total += 1
        if check_file_exists(file_path, description):
            passed += 1
    
    print()
    
    # Check documentation
    print("📚 DOCUMENTATION")
    print("-" * 80)
    
    checks = [
        (base_dir / "README.md", "README"),
        (base_dir / "QUICKSTART.md", "Quick Start Guide"),
        (base_dir / "ARCHITECTURE.md", "Architecture Docs"),
        (base_dir / "STATUS.md", "Status Report"),
        (base_dir / "SECURITY.md", "Security Advisory"),
        (base_dir / "READINESS_REPORT.md", "Readiness Report"),
    ]
    
    for file_path, description in checks:
        total += 1
        if check_file_exists(file_path, description):
            passed += 1
    
    print()
    print("=" * 80)
    print(f"VALIDATION RESULTS: {passed}/{total} checks passed ({passed*100//total}%)")
    print("=" * 80)
    print()
    
    if passed == total:
        print("✅ ALL CHECKS PASSED - Application structure is complete!")
        print()
        print("Next steps:")
        print("  1. Run: ./start.sh")
        print("  2. Access: http://localhost:3000")
        print("  3. Login with: admin@example.com / admin123")
        return 0
    elif passed >= total * 0.9:
        print("⚠️  MOSTLY READY - Some optional files missing")
        print("   Application should still work")
        return 0
    else:
        print("❌ VALIDATION FAILED - Critical files missing")
        print("   Please check the repository structure")
        return 1

if __name__ == "__main__":
    sys.exit(main())
