"""Script to seed people data as users"""
from flask import Flask
from config import Config
from models import db, User
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

def seed_people():
    """Seed people data as client users"""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        # Create tables first
        db.create_all()
        people_data = [
            ('Aarav Sharma', '9876543210', 'aarav.sharma@example.com', 22),
            ('Priya Mehta', '9823456789', 'priya.mehta@example.com', 25),
            ('Rohan Verma', '9012345678', 'rohan.verma@example.com', 28),
            ('Sneha Kulkarni', '9123456780', 'sneha.kulkarni@example.com', 24),
            ('Vishal Singh', '9556677889', 'vishal.singh@example.com', 30),
            ('Ananya Gupta', '9645234567', 'ananya.gupta@example.com', 21),
            ('Karan Malhotra', '9789102345', 'karan.malhotra@example.com', 27),
            ('Neha Patil', '9087654321', 'neha.patil@example.com', 23),
            ('Arjun Reddy', '9798123456', 'arjun.reddy@example.com', 29),
            ('Meera Joshi', '9890011223', 'meera.joshi@example.com', 26),
            ('Kabir Khanna', '9811234567', 'kabir.khanna@example.com', 24),
            ('Divya Chauhan', '9922345671', 'divya.chauhan@example.com', 22),
            ('Harsh Vardhan', '9877601234', 'harsh.vardhan@example.com', 32),
            ('Pooja Nair', '9998845632', 'pooja.nair@example.com', 23),
            ('Manish Yadav', '9099445566', 'manish.yadav@example.com', 31),
            ('Sara Khan', '9123345612', 'sara.khan@example.com', 20),
            ('Sameer Sheikh', '9088123455', 'sameer.sheikh@example.com', 26),
            ('Isha Bansal', '9900123457', 'isha.bansal@example.com', 25),
            ('Rahul Chawla', '9823012456', 'rahul.chawla@example.com', 27),
            ('Tara Bhat', '9799321456', 'tara.bhat@example.com', 28),
            ('Lakshya Goyal', '9667765432', 'lakshya.goyal@example.com', 22),
            ('Kiara Kapoor', '9776710203', 'kiara.kapoor@example.com', 24),
            ('Dev Negi', '9445566788', 'dev.negi@example.com', 29),
            ('Sonal Arora', '9871230987', 'sonal.arora@example.com', 21),
            ('Vipul Sinha', '8765432190', 'vipul.sinha@example.com', 33),
            ('Natasha Pillai', '9099988776', 'natasha.pillai@example.com', 27),
            ('Krishna Rao', '9887766554', 'krishna.rao@example.com', 30),
            ('Reema Bhatt', '9877000122', 'reema.bhatt@example.com', 23),
            ('Siddharth Jain', '9988776655', 'siddharth.jain@example.com', 28),
            ('Aditi Mishra', '9123654789', 'aditi.mishra@example.com', 22),
            ('Roshan Pillai', '9345678901', 'roshan.pillai@example.com', 25),
            ('Zara Ansari', '9554456778', 'zara.ansari@example.com', 24),
            ('Nikhil Menon', '9876500123', 'nikhil.menon@example.com', 31),
            ('Vani Ramesh', '9765432001', 'vani.ramesh@example.com', 29),
            ('Gaurav Saxena', '9034567899', 'gaurav.saxena@example.com', 26),
            ('Saniya Deshmukh', '9212345600', 'saniya.deshmukh@example.com', 20),
            ('Pranav Kulkarni', '9090011222', 'pranav.kulkarni@example.com', 24),
            ('Irene Joseph', '9123456009', 'irene.joseph@example.com', 21),
            ('Omkara Patil', '9765012345', 'omkara.patil@example.com', 27),
            ('Simran Kaur', '9988543210', 'simran.kaur@example.com', 23),
            ('Jatin Batra', '9876123400', 'jatin.batra@example.com', 32),
            ('Ayesha Rizvi', '9012223344', 'ayesha.rizvi@example.com', 22),
            ('Ritesh Dube', '9543210098', 'ritesh.dube@example.com', 34),
            ('Lavanya Singh', '9874441234', 'lavanya.singh@example.com', 21),
            ('Adarsh Soni', '9767765544', 'adarsh.soni@example.com', 28),
            ('Shruti Prakash', '9655443322', 'shruti.prakash@example.com', 26),
            ('Yashwant Giri', '9788991122', 'yashwant.giri@example.com', 35),
            ('Mithali Iyer', '9122987654', 'mithali.iyer@example.com', 23),
            ('Tejas Desai', '9045671230', 'tejas.desai@example.com', 27),
            ('Chirag Tiwari', '9345671299', 'chirag.tiwari@example.com', 29),
        ]
        
        created_count = 0
        skipped_count = 0
        
        for name, phone, email, age in people_data:
            # Check if user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                print(f"⏭️  Skipped {name} - email already exists")
                skipped_count += 1
                continue
            
            # Generate username from email
            username = email.split('@')[0]
            base_username = username
            counter = 1
            while User.query.filter_by(username=username).first():
                username = f"{base_username}{counter}"
                counter += 1
            
            # Create user
            user = User(
                username=username,
                email=email,
                role='client',
                full_name=name,
                phone=phone,
                is_verified=True,
                is_active=True
            )
            # Set default password
            user.set_password('password123')
            
            db.session.add(user)
            created_count += 1
            print(f"✅ Created: {name} ({username})")
        
        db.session.commit()
        
        print(f"\n{'='*50}")
        print(f"✅ Successfully created {created_count} users")
        print(f"⏭️  Skipped {skipped_count} users (already exist)")
        print(f"{'='*50}")
        print(f"\nAll users have password: password123")

if __name__ == '__main__':
    seed_people()

