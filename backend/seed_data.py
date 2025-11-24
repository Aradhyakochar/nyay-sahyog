"""Script to seed sample data for development and testing"""
from app import create_app
from models import db, User, Provider, Booking, Review, Message
from datetime import datetime, timedelta
import random

def seed_data():
    """Seed the database with sample data"""
    app = create_app()
    
    with app.app_context():
        # Clear existing data (optional - comment out if you want to keep existing data)
        # db.drop_all()
        # db.create_all()
        
        # Create sample clients
        clients = []
        cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad']
        states = ['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'West Bengal', 'Telangana', 'Maharashtra', 'Gujarat']
        
        for i in range(1, 21):  # Increased from 5 to 20
            # Check if user already exists
            existing = User.query.filter_by(username=f'client{i}').first()
            if existing:
                clients.append(existing)
                continue
                
            city_idx = (i - 1) % len(cities)
            client = User(
                username=f'client{i}',
                email=f'client{i}@example.com',
                role='client',
                full_name=f'Client User {i}',
                phone=f'987654321{i:02d}',
                city=cities[city_idx],
                state=states[city_idx],
                pincode=f'{400000+i}',
                is_verified=True,
                is_active=True
            )
            client.set_password('password123')
            clients.append(client)
            db.session.add(client)
        
        # Create sample advocates
        advocates = []
        specializations = [
            'Criminal Law', 'Family Law', 'Corporate Law', 'Property Law', 'Tax Law',
            'Constitutional Law', 'Labour Law', 'Intellectual Property', 'Environmental Law',
            'Immigration Law', 'Banking Law', 'Insurance Law', 'Real Estate Law', 'Employment Law'
        ]
        for i in range(1, 31):  # Increased from 10 to 30
            # Check if user already exists
            existing = User.query.filter_by(username=f'advocate{i}').first()
            if existing:
                advocates.append(existing)
                continue
                
            advocate = User(
                username=f'advocate{i}',
                email=f'advocate{i}@example.com',
                role='advocate',
                full_name=f'Advocate {i}',
                phone=f'987654321{i+10}',
                city=random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata']),
                state=random.choice(['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'West Bengal']),
                pincode=f'{400000+i}',
                is_verified=random.choice([True, True, True, False]),  # 75% verified
                is_active=True
            )
            advocate.set_password('password123')
            advocates.append(advocate)
            db.session.add(advocate)
            db.session.flush()
            
            # Create provider profile if it doesn't exist
            existing_provider = Provider.query.filter_by(user_id=advocate.id).first()
            if not existing_provider:
                provider = Provider(
                    user_id=advocate.id,
                    specialization=random.choice(specializations),
                    experience_years=random.randint(2, 25),
                    bar_council_number=f'BCN{1000+i}',
                    qualification=f'LLB, LLM - University {i}',
                    bio=f'Experienced advocate specializing in {specializations[i % len(specializations)]} with {random.randint(2, 25)} years of practice.',
                    consultation_fee=random.randint(500, 5000),
                    hourly_rate=random.randint(1000, 10000),
                    is_verified=advocate.is_verified,
                    is_active=True
                )
                db.session.add(provider)
        
        # Create sample mediators
        mediators = []
        for i in range(1, 11):  # Increased from 3 to 10
            # Check if user already exists
            existing = User.query.filter_by(username=f'mediator{i}').first()
            if existing:
                mediators.append(existing)
                continue
                
            mediator = User(
                username=f'mediator{i}',
                email=f'mediator{i}@example.com',
                role='mediator',
                full_name=f'Mediator {i}',
                phone=f'987654321{i+20}',
                city=random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata']),
                state=random.choice(['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'West Bengal']),
                pincode=f'{400000+i+20}',
                is_verified=True,
                is_active=True
            )
            mediator.set_password('password123')
            mediators.append(mediator)
            db.session.add(mediator)
            db.session.flush()
            
            # Create provider profile if it doesn't exist
            existing_provider = Provider.query.filter_by(user_id=mediator.id).first()
            if not existing_provider:
                provider = Provider(
                    user_id=mediator.id,
                    specialization='Mediation & Arbitration',
                    experience_years=random.randint(5, 20),
                    qualification=f'Certified Mediator - Institute {i}',
                    bio=f'Certified mediator with expertise in dispute resolution.',
                    consultation_fee=random.randint(1000, 3000),
                    hourly_rate=random.randint(2000, 8000),
                    is_verified=True,
                    is_active=True
                )
                db.session.add(provider)
        
        # Create sample arbitrators
        arbitrators = []
        for i in range(1, 8):  # 7 arbitrators
            existing = User.query.filter_by(username=f'arbitrator{i}').first()
            if existing:
                arbitrators.append(existing)
                continue
                
            arbitrator = User(
                username=f'arbitrator{i}',
                email=f'arbitrator{i}@example.com',
                role='arbitrator',
                full_name=f'Arbitrator {i}',
                phone=f'987654321{i+30}',
                city=random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai']),
                state=random.choice(['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu']),
                pincode=f'{400000+i+30}',
                is_verified=True,
                is_active=True
            )
            arbitrator.set_password('password123')
            arbitrators.append(arbitrator)
            db.session.add(arbitrator)
            db.session.flush()
        
        # Create sample notaries
        notaries = []
        for i in range(1, 6):  # 5 notaries
            existing = User.query.filter_by(username=f'notary{i}').first()
            if existing:
                notaries.append(existing)
                continue
                
            notary = User(
                username=f'notary{i}',
                email=f'notary{i}@example.com',
                role='notary',
                full_name=f'Notary {i}',
                phone=f'987654321{i+40}',
                city=random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Pune']),
                state=random.choice(['Maharashtra', 'Delhi', 'Karnataka', 'Maharashtra']),
                pincode=f'{400000+i+40}',
                is_verified=True,
                is_active=True
            )
            notary.set_password('password123')
            notaries.append(notary)
            db.session.add(notary)
            db.session.flush()
        
        # Create sample document writers
        doc_writers = []
        for i in range(1, 6):  # 5 document writers
            existing = User.query.filter_by(username=f'docwriter{i}').first()
            if existing:
                doc_writers.append(existing)
                continue
                
            doc_writer = User(
                username=f'docwriter{i}',
                email=f'docwriter{i}@example.com',
                role='document_writer',
                full_name=f'Document Writer {i}',
                phone=f'987654321{i+50}',
                city=random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad']),
                state=random.choice(['Maharashtra', 'Delhi', 'Karnataka', 'Telangana']),
                pincode=f'{400000+i+50}',
                is_verified=True,
                is_active=True
            )
            doc_writer.set_password('password123')
            doc_writers.append(doc_writer)
            db.session.add(doc_writer)
            db.session.flush()
        
        # Create provider profiles for arbitrators
        for i, arbitrator in enumerate(arbitrators, 1):
            existing_provider = Provider.query.filter_by(user_id=arbitrator.id).first()
            if not existing_provider:
                provider = Provider(
                    user_id=arbitrator.id,
                    specialization='Arbitration & Dispute Resolution',
                    experience_years=random.randint(8, 25),
                    qualification=f'Certified Arbitrator - Institute {i}',
                    bio=f'Experienced arbitrator specializing in commercial and civil dispute resolution.',
                    consultation_fee=random.randint(2000, 5000),
                    hourly_rate=random.randint(3000, 12000),
                    is_verified=True,
                    is_active=True
                )
                db.session.add(provider)
        
        # Create provider profiles for notaries
        for i, notary in enumerate(notaries, 1):
            existing_provider = Provider.query.filter_by(user_id=notary.id).first()
            if not existing_provider:
                provider = Provider(
                    user_id=notary.id,
                    specialization='Notary Services',
                    experience_years=random.randint(3, 15),
                    qualification=f'Licensed Notary - State {i}',
                    bio=f'Licensed notary providing document attestation and certification services.',
                    consultation_fee=random.randint(500, 2000),
                    hourly_rate=random.randint(1000, 5000),
                    is_verified=True,
                    is_active=True
                )
                db.session.add(provider)
        
        # Create provider profiles for document writers
        for i, doc_writer in enumerate(doc_writers, 1):
            existing_provider = Provider.query.filter_by(user_id=doc_writer.id).first()
            if not existing_provider:
                doc_specializations = ['Contract Drafting', 'Legal Documentation', 'Agreement Writing', 'Petition Drafting']
                provider = Provider(
                    user_id=doc_writer.id,
                    specialization=random.choice(doc_specializations),
                    experience_years=random.randint(2, 12),
                    qualification=f'Legal Document Writer - Certification {i}',
                    bio=f'Professional legal document writer specializing in {random.choice(doc_specializations)}.',
                    consultation_fee=random.randint(1000, 4000),
                    hourly_rate=random.randint(1500, 8000),
                    is_verified=True,
                    is_active=True
                )
                db.session.add(provider)
        
        db.session.commit()
        
        # Create sample bookings
        bookings = []
        all_providers_list = advocates + mediators + arbitrators + notaries + doc_writers
        for i in range(50):  # Increased from 20 to 50 bookings
            client = random.choice(clients)
            provider_user = random.choice(all_providers_list)
            provider = Provider.query.filter_by(user_id=provider_user.id).first()
            
            if provider:
                booking_date = datetime.utcnow() + timedelta(days=random.randint(-30, 30))
                status = random.choice(['pending', 'confirmed', 'completed', 'cancelled'])
                
                booking = Booking(
                    client_id=client.id,
                    provider_id=provider_user.id,
                    provider_profile_id=provider.id,
                    service_type='consultation',
                    booking_date=booking_date,
                    duration_minutes=60,
                    fee=provider.consultation_fee,
                    status=status,
                    description=f'Sample consultation request {i+1}',
                    location=f'Office {i+1}, {provider_user.city}'
                )
                bookings.append(booking)
                db.session.add(booking)
        
        db.session.commit()
        
        # Create sample reviews for completed bookings
        completed_bookings = [b for b in bookings if b.status == 'completed']
        for booking in completed_bookings[:10]:  # Review first 10 completed
            review = Review(
                booking_id=booking.id,
                provider_id=booking.provider_profile_id,
                client_id=booking.client_id,
                rating=random.randint(3, 5),
                comment=f'Great service! Highly recommended.'
            )
            db.session.add(review)
            
            # Update provider rating
            provider = Provider.query.get(booking.provider_profile_id)
            reviews = Review.query.filter_by(provider_id=provider.id).all()
            if reviews:
                provider.total_reviews = len(reviews)
                provider.rating = sum(r.rating for r in reviews) / len(reviews)
        
        db.session.commit()
        
        # Create sample messages
        for booking in bookings[:10]:
            # Client to provider message
            message1 = Message(
                booking_id=booking.id,
                sender_id=booking.client_id,
                receiver_id=booking.provider_id,
                subject=f'Regarding booking #{booking.id}',
                content=f'Hello, I would like to discuss the details of our consultation.'
            )
            db.session.add(message1)
            
            # Provider to client reply
            message2 = Message(
                booking_id=booking.id,
                sender_id=booking.provider_id,
                receiver_id=booking.client_id,
                subject=f'Re: Regarding booking #{booking.id}',
                content=f'Thank you for reaching out. I am available for the scheduled time.'
            )
            db.session.add(message2)
        
        db.session.commit()
        
        print("Sample data seeded successfully!")
        print("\nSample Users:")
        print(f"Clients: client1-client{len(clients)} (password: password123)")
        print(f"Advocates: advocate1-advocate{len(advocates)} (password: password123)")
        print(f"Mediators: mediator1-mediator{len(mediators)} (password: password123)")
        print(f"Arbitrators: arbitrator1-arbitrator{len(arbitrators)} (password: password123)")
        print(f"Notaries: notary1-notary{len(notaries)} (password: password123)")
        print(f"Document Writers: docwriter1-docwriter{len(doc_writers)} (password: password123)")
        print("Admin: admin (password: admin123)")
        print(f"\nTotal Providers: {len(advocates) + len(mediators) + len(arbitrators) + len(notaries) + len(doc_writers)}")
        print(f"Total Bookings: {len(bookings)}")

if __name__ == '__main__':
    seed_data()

