# Mini Patient Portal

A Django-based patient portal for medication refill workflow management, featuring role-based access control and comprehensive refill request processing.

## Features

- **Multi-Role Authentication**: Patient, Provider, Staff, and Admin roles
- **Patient Dashboard**: View medications, request refills, track status
- **Provider Dashboard**: Review and approve/deny refill requests with notes
- **Staff Dashboard**: System statistics and patient management
- **Secure Workflow**: State machine for refill requests (PENDING → APPROVED/DENIED/CANCELLED)
- **Duplicate Prevention**: Prevents multiple pending requests for same medication
- **Comprehensive Testing**: 23 test cases covering all functionality

## Tech Stack

- **Backend**: Python, Django 6.0
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Database**: SQLite (dev), PostgreSQL ready
- **Testing**: Django Test Framework
- **Security**: CSRF protection, environment variables, security headers

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/chelsbun/mini-patient-portal.git
   cd mini-patient-portal
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create test users**
   ```bash
   python manage.py shell
   # Run the user creation commands from PROJECT_STATUS.md
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000` to access the application.

## Usage

### Test Accounts
| Username | Password | Role |
|----------|----------|------|
| admin | Admin1Pass123 | Superuser |
| patient1 | Patient1Pass123 | Patient |
| provider1 | ProviderPassword123 | Provider |
| staff1 | Staff1Pass123 | Staff |

### Patient Workflow
1. Login as a patient
2. View assigned medications
3. Request refills for medications
4. Track refill request status

### Provider Workflow
1. Login as a provider
2. Review pending refill requests
3. Approve or deny requests with optional notes
4. View decision history

### Staff Workflow
1. Login as staff
2. View system statistics
3. Create new patient accounts
4. Add medications to patient records

## Testing

Run the comprehensive test suite:

```bash
python manage.py test
```

**Test Coverage**: 23 tests covering models, views, services, and business logic.

## Security Features

- Environment variable configuration
- CSRF protection
- Security headers (X-Frame-Options, CSP, etc.)
- Role-based access control
- Input validation and sanitization
- Proper HTTP status codes

## Project Structure

```
mini-patient-portal/
├── accounts/          # User authentication and profiles
├── meds/             # Medication management
├── refills/          # Refill request workflow
├── templates/        # HTML templates
├── config/           # Django settings
└── tests/           # Test suite
```

## API Endpoints

- `/accounts/login/` - User authentication
- `/portal/` - Dashboard routing
- `/refills/request/<id>/` - Create refill request
- `/refills/approve/<id>/` - Approve refill request
- `/refills/deny/<id>/` - Deny refill request
- `/admin/` - Django admin interface

## Development

### Key Design Patterns
- **Service Layer**: Business logic separated from views
- **State Machine**: Controlled refill request workflow
- **Repository Pattern**: Django ORM abstraction
- **Defensive Programming**: Comprehensive error handling

### Code Quality
- Comprehensive docstrings
- Type hints where applicable
- Clean separation of concerns
- Professional error handling
- 23 automated tests

## Future Enhancements

- REST API with Django REST Framework
- Email notifications for status updates
- Mobile-responsive improvements
- Advanced reporting and analytics
- Integration with pharmacy systems

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## License

This project is part of an academic portfolio. All rights reserved.

---

**Author**: Chelsea Bonyata  
**Contact**: [GitHub](https://github.com/chelsbun)  
**Project**: Mini Patient Portal - Healthcare Technology Portfolio