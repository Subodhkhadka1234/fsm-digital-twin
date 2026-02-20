"""
Seed script to populate database with initial data
Run this after database migrations
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.organization import Organization
from app.models.technician import Technician, TechnicianStatus
from app.models.customer import Customer, CustomerPriority
from geoalchemy2.elements import WKTElement
import uuid


def seed_database():
    """Populate database with seed data"""
    db = SessionLocal()
    
    try:
        print("Starting database seeding...")
        
        # Check if already seeded
        existing_org = db.query(Organization).first()
        if existing_org:
            print("Database already seeded. Skipping...")
            return
        
        # Create default organization
        org = Organization(
            name="Demo FSM Company",
            subscription_tier="enterprise",
            settings={
                "timezone": "UTC",
                "currency": "USD"
            }
        )
        db.add(org)
        db.flush()
        print(f"Created organization: {org.name}")
        
        # Create admin user
        admin_user = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            organization_id=org.id,
            is_active=True
        )
        db.add(admin_user)
        print(f"Created admin user: {admin_user.email}")
        
        # Create technician users
        tech_data = [
            {
                "email": "tech1@example.com",
                "password": "tech123",
                "employee_id": "TECH001",
                "skills": ["plumbing", "electrical", "hvac"],
                "rating": 4.5
            },
            {
                "email": "tech2@example.com",
                "password": "tech123",
                "employee_id": "TECH002",
                "skills": ["electrical", "carpentry"],
                "rating": 4.2
            },
            {
                "email": "tech3@example.com",
                "password": "tech123",
                "employee_id": "TECH003",
                "skills": ["plumbing", "hvac"],
                "rating": 4.8
            }
        ]
        
        for tech in tech_data:
            user = User(
                email=tech["email"],
                hashed_password=get_password_hash(tech["password"]),
                role=UserRole.TECHNICIAN,
                organization_id=org.id,
                is_active=True
            )
            db.add(user)
            db.flush()
            
            # Create technician profile
            technician = Technician(
                user_id=user.id,
                organization_id=org.id,
                employee_id=tech["employee_id"],
                skills=tech["skills"],
                availability_status=TechnicianStatus.AVAILABLE,
                current_location=WKTElement("POINT(-122.4194 37.7749)", srid=4326),  # San Francisco
                max_jobs_per_day=8,
                working_hours={"start": "08:00", "end": "17:00"},
                certifications=["OSHA", "EPA"],
                rating=tech["rating"]
            )
            db.add(technician)
            print(f"Created technician: {tech['email']}")
        
        # Create customer users
        customer_data = [
            {
                "email": "customer1@example.com",
                "password": "customer123",
                "company_name": "ABC Corp",
                "contact_person": "John Doe",
                "phone": "+1-555-0101",
                "priority": CustomerPriority.PREMIUM
            },
            {
                "email": "customer2@example.com",
                "password": "customer123",
                "company_name": "XYZ Industries",
                "contact_person": "Jane Smith",
                "phone": "+1-555-0102",
                "priority": CustomerPriority.STANDARD
            }
        ]
        
        for cust in customer_data:
            user = User(
                email=cust["email"],
                hashed_password=get_password_hash(cust["password"]),
                role=UserRole.CUSTOMER,
                organization_id=org.id,
                is_active=True
            )
            db.add(user)
            db.flush()
            
            # Create customer profile
            customer = Customer(
                user_id=user.id,
                organization_id=org.id,
                company_name=cust["company_name"],
                contact_person=cust["contact_person"],
                phone=cust["phone"],
                address=WKTElement("POINT(-122.4194 37.7749)", srid=4326),
                customer_priority=cust["priority"]
            )
            db.add(customer)
            print(f"Created customer: {cust['email']}")
        
        db.commit()
        print("\n✅ Database seeding completed successfully!")
        print("\nDefault credentials:")
        print("Admin: admin@example.com / admin123")
        print("Technician: tech1@example.com / tech123")
        print("Customer: customer1@example.com / customer123")
        
    except Exception as e:
        print(f"Error seeding database: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
