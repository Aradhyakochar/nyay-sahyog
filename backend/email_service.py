"""Email service for sending transactional emails"""
from flask_mail import Message
from flask import current_app
from datetime import datetime, timedelta
import random

def send_otp_email(mail, user_email, otp_code):
    """Send OTP email to user"""
    try:
        msg = Message(
            subject='Your Nyay Sahyog Login OTP',
            recipients=[user_email],
            html=f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #667eea;">Nyay Sahyog - Login Verification</h2>
                    <p>Your One-Time Password (OTP) for login is:</p>
                    <div style="background: #f0f4ff; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0;">
                        <h1 style="color: #667eea; font-size: 32px; letter-spacing: 5px; margin: 0;">{otp_code}</h1>
                    </div>
                    <p>This OTP is valid for 10 minutes. Please do not share it with anyone.</p>
                    <p style="color: #666; font-size: 12px;">If you didn't request this OTP, please ignore this email.</p>
                </body>
            </html>
            """
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def send_welcome_email(mail, user_email, user_name):
    """Send welcome email to new user"""
    try:
        msg = Message(
            subject='Welcome to Nyay Sahyog!',
            recipients=[user_email],
            html=f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #667eea;">Welcome to Nyay Sahyog, {user_name}!</h2>
                    <p>Thank you for joining our legal services marketplace. We're excited to have you on board!</p>
                    <p>You can now:</p>
                    <ul>
                        <li>Browse verified legal service providers</li>
                        <li>Book consultations with experts</li>
                        <li>Manage all your legal needs in one place</li>
                    </ul>
                    <p>Get started by exploring our platform!</p>
                    <p style="color: #666; font-size: 12px;">Best regards,<br>The Nyay Sahyog Team</p>
                </body>
            </html>
            """
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending welcome email: {str(e)}")
        return False

def send_booking_reminder_email(mail, user_email, user_name, bookings):
    """Send daily booking reminder email"""
    try:
        booking_list = ""
        for booking in bookings:
            booking_list += f"""
            <li style="margin: 10px 0;">
                <strong>{booking.get('provider_name', 'Provider')}</strong><br>
                Date: {booking.get('date', 'N/A')}<br>
                Time: {booking.get('time', 'N/A')}
            </li>
            """
        
        msg = Message(
            subject='Your Upcoming Bookings - Nyay Sahyog',
            recipients=[user_email],
            html=f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #667eea;">Hello {user_name}!</h2>
                    <p>You have the following bookings scheduled for tomorrow:</p>
                    <ul>
                        {booking_list}
                    </ul>
                    <p>Please make sure to be available at the scheduled time.</p>
                    <p style="color: #666; font-size: 12px;">Best regards,<br>The Nyay Sahyog Team</p>
                </body>
            </html>
            """
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending reminder email: {str(e)}")
        return False

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

