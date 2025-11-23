"""Initialize database with sample data"""
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.core.config import settings
from app.models.user import User
from app.models.organization import Organization
from app.models.campaign import Campaign
from app.models.donation import Donation, DonationStatus, PaymentMethod


def create_admin_user(db: Session):
    """Create admin user"""
    admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
    if not admin:
        admin = User(
            email=settings.ADMIN_EMAIL,
            hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
            full_name="Admin User",
            is_admin=True,
            is_active=True,
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print(f"✓ Created admin user: {settings.ADMIN_EMAIL}")
    else:
        print(f"✓ Admin user already exists: {settings.ADMIN_EMAIL}")
    return admin


def create_sample_data(db: Session):
    """Create sample organizations, campaigns, and donations"""

    # Check if sample data already exists
    if db.query(Organization).count() > 0:
        print("✓ Sample data already exists")
        return

    # Create sample users (donors)
    donors = []
    donor_names = [
        ("john@example.com", "John Smith"),
        ("sarah@example.com", "Sarah Johnson"),
        ("mike@example.com", "Mike Davis"),
        ("emma@example.com", "Emma Wilson"),
    ]

    for email, name in donor_names:
        donor = User(
            email=email,
            hashed_password=get_password_hash("password123"),
            full_name=name,
            is_active=True,
        )
        db.add(donor)
        donors.append(donor)

    db.commit()
    print(f"✓ Created {len(donors)} sample donors")

    # Create sample organizations
    organizations_data = [
        {
            "name": "Clean Water Initiative",
            "description": "Providing clean water to communities in need",
            "category": "Water & Sanitation",
            "ein": "12-3456789",
            "transparency_score": 95.5,
            "is_verified": True,
        },
        {
            "name": "Education for All",
            "description": "Building schools and providing education in developing countries",
            "category": "Education",
            "ein": "98-7654321",
            "transparency_score": 92.0,
            "is_verified": True,
        },
        {
            "name": "Healthcare Access Fund",
            "description": "Improving healthcare access for underserved communities",
            "category": "Healthcare",
            "ein": "45-6789012",
            "transparency_score": 88.5,
            "is_verified": True,
        },
        {
            "name": "Environmental Protection Society",
            "description": "Protecting endangered species and preserving natural habitats",
            "category": "Environment",
            "ein": "34-5678901",
            "transparency_score": 90.0,
            "is_verified": True,
        },
    ]

    organizations = []
    for org_data in organizations_data:
        org = Organization(
            **org_data,
            owner_id=donors[0].id,
            email=f"contact@{org_data['name'].lower().replace(' ', '')}.org",
            website=f"https://{org_data['name'].lower().replace(' ', '')}.org",
        )
        db.add(org)
        organizations.append(org)

    db.commit()
    print(f"✓ Created {len(organizations)} sample organizations")

    # Create sample campaigns
    campaigns = []
    for org in organizations:
        campaign = Campaign(
            name=f"Annual {org.name} Campaign 2024",
            description=f"Help us raise funds for {org.description.lower()}",
            goal_amount=50000.0,
            current_amount=0.0,
            start_date=datetime.utcnow() - timedelta(days=30),
            end_date=datetime.utcnow() + timedelta(days=60),
            organization_id=org.id,
            is_active=True,
        )
        db.add(campaign)
        campaigns.append(campaign)

    db.commit()
    print(f"✓ Created {len(campaigns)} sample campaigns")

    # Create sample donations
    payment_methods = list(PaymentMethod)
    donation_count = 0

    for campaign in campaigns:
        num_donations = random.randint(10, 20)

        for _ in range(num_donations):
            donor = random.choice(donors)
            amount = random.choice([25, 50, 100, 250, 500, 1000, 2500])

            donation = Donation(
                amount=amount,
                currency="USD",
                status=DonationStatus.COMPLETED,
                payment_method=random.choice(payment_methods),
                transaction_id=f"TXN-{random.randint(100000, 999999)}",
                donor_id=donor.id,
                organization_id=campaign.organization_id,
                campaign_id=campaign.id,
                is_anonymous=random.choice([True, False]),
                donation_date=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
            )
            db.add(donation)

            # Update campaign amount
            campaign.current_amount += amount
            donation_count += 1

    db.commit()
    print(f"✓ Created {donation_count} sample donations")


def init_db():
    """Initialize database"""
    print("Initializing database...")

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")

    # Create admin user and sample data
    db = SessionLocal()
    try:
        create_admin_user(db)
        create_sample_data(db)
        print("\n✓ Database initialization complete!")
        print(f"\nAdmin credentials:")
        print(f"  Email: {settings.ADMIN_EMAIL}")
        print(f"  Password: {settings.ADMIN_PASSWORD}")
        print(f"\nSample donor credentials:")
        print(f"  Email: john@example.com")
        print(f"  Password: password123")
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
