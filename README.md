# SkillPartner

SkillPartner is a web application that connects learners with mentors based on skills and interests. The platform facilitates knowledge sharing and skill development through one-on-one mentoring sessions.

## Features

### For Learners
- Create a profile and select skills you want to learn
- Search for mentors based on specific skills
- Book mentoring sessions with available mentors
- Manage your bookings (cancel, reschedule)
- Track your learning progress

### For Mentors
- Create a profile showcasing your expertise and skills
- Set your availability for mentoring sessions
- Accept or decline session requests
- Manage your mentoring appointments
- Build your reputation through learner ratings

## Technology Stack

- **Backend**: Django (Python web framework)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Django's built-in authentication system

## Project Structure

```
SkillPartner/
├── accounts/                  # Main application directory
│   ├── management/            # Custom management commands
│   │   └── commands/
│   │       └── add_skills.py  # Command to populate skills
│   ├── migrations/            # Database migrations
│   ├── templates/             # HTML templates
│   │   └── accounts/
│   │       ├── dashboard.html
│   │       ├── home.html
│   │       ├── login.html
│   │       ├── profile.html
│   │       ├── register.html
│   │       ├── search_mentors.html
│   │       └── view_bookings.html
│   ├── admin.py               # Admin interface configuration
│   ├── forms.py               # Form definitions
│   ├── models.py              # Database models
│   ├── urls.py                # URL routing
│   └── views.py               # View functions
├── SkillPartner/              # Project settings directory
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py                  # Django management script
└── README.md                  # This file
```

## Models

### User
Django's built-in User model for authentication.

### Profile
Extends the User model with additional information:
- Bio: A text field for user description
- User Type: Either "Learner" or "Mentor"
- Skills: Many-to-many relationship with the Skill model

### Skill
Represents skills that users can learn or teach:
- Name: The name of the skill

### Booking
Represents mentoring sessions:
- Learner: The user requesting the session
- Mentor: The user providing mentoring
- Skill: The skill focus of the session
- Scheduled At: Date and time of the session
- Status: Current status of the booking (Pending, Confirmed, Cancelled, Completed)

## Booking Status Explained

- **Pending**: When a learner requests a session with a mentor, the booking starts in the "Pending" status. This means the request has been sent to the mentor but hasn't been confirmed yet.

- **Confirmed**: Once a mentor accepts a booking request, the status changes to "Confirmed". This indicates that both parties have agreed to the session.

- **Cancelled**: If either the learner or mentor cancels the session, the status changes to "Cancelled".

- **Completed**: After a session has taken place, it can be marked as "Completed".

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Apply migrations:
   ```
   python manage.py migrate
   ```
6. Add initial skills to the database:
   ```
   python manage.py add_skills
   ```
7. Create a superuser (admin):
   ```
   python manage.py createsuperuser
   ```
8. Run the development server:
   ```
   python manage.py runserver
   ```
9. Access the application at http://127.0.0.1:8000/

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
