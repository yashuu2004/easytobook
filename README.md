# EasyToBook – Django Travel Booking

EasyToBook is a full-stack travel booking web application built with Django, featuring secure trip reservations, Razorpay payment gateway integration, and automated email confirmations.

## Overview

EasyToBook allows users to search trips, select seats, complete secure payments, and manage bookings through a user dashboard. The system ensures seat availability using transaction-safe booking logic and provides confirmation after successful payment.

## Tech Stack

- Backend: Django (Python)
- Frontend: HTML, CSS, JavaScript, Django Templates
- Database: SQLite
- Payment Gateway: Razorpay
- Authentication: Custom user model (email login)

## Features

- User registration and login
- Trip search by transport type, source, destination, and date
- Dynamic state and city selection using AJAX
- Secure seat booking with availability checks
- Razorpay payment gateway integration
- Booking confirmation after payment success
- Email notifications
- User dashboard with booking history
- Admin panel for managing trips
- Responsive UI

## Running Locally

1. Create virtual environment
2. Install dependencies
3. Run migrations
4. Create superuser
5. Run server

## Payment Integration

Payments are processed through Razorpay. Booking status is updated only after successful transaction verification.

## Email

Booking confirmation emails are sent after payment success. Configure SMTP for production.

## Future Improvements

- Live seat map
- Booking cancellation
- Cloud deployment
- Advanced notifications
