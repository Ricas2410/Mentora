# Mentora - Educational Learning Platform

Mentora is a comprehensive educational platform designed to provide quality learning experiences for students from Grade 1 to Grade 12. The platform offers interactive quizzes, study materials, progress tracking, and comprehensive assessments across multiple subjects.

## Features

### 🎓 **Educational Content**
- **Subjects**: English Language Arts, Mathematics, Science, Social Studies, and Life Skills
- **Grade Levels**: Complete K-12 curriculum (Grades 1-12)
- **Interactive Quizzes**: Multiple choice, fill-in-the-blank, and short answer questions
- **Study Materials**: Comprehensive learning content for each topic
- **Final Exams**: Comprehensive assessments for each grade level

### 📊 **Progress Tracking**
- Individual topic progress monitoring
- Subject completion tracking
- Grade-level advancement system
- Performance analytics and scoring
- Achievement badges and milestones

### 👨‍💼 **Admin Features**
- Content management system
- CSV bulk import for questions and study materials
- Quiz settings and configuration
- User progress monitoring
- System maintenance tools

### 📱 **Mobile-First Design**
- Responsive design optimized for mobile devices
- Clean, professional UI/UX
- Accessible for first-time technology users
- Optimized for limited connectivity environments

## Technology Stack

- **Backend**: Django 5.2.1
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Authentication**: Django's built-in authentication system
- **API**: Django REST Framework

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mentora.git
   cd mentora
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv mentora_env
   
   # On Windows
   mentora_env\Scripts\activate
   
   # On macOS/Linux
   source mentora_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env file with your configuration
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

8. **Access the Application**
   - Main site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Site Domain Configuration (IMPORTANT for email verification)
SITE_DOMAIN=localhost:8000
SITE_PROTOCOL=http

# Database Configuration (for production)
# DATABASE_URL=postgresql://username:password@localhost:5432/mentora_db

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=Mentora <noreply@mentora.com>

# Application Settings
SITE_NAME=Mentora
ADMIN_EMAIL=admin@mentora.com
```

### 🚀 Production Deployment (PythonAnywhere)

For production deployment, update your `.env` file with:

```env
# Production Settings
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com

# IMPORTANT: Update these for email verification to work
SITE_DOMAIN=yourusername.pythonanywhere.com
SITE_PROTOCOL=https

# Email Configuration (use real SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
```

### 🔧 Fix Email Verification URLs

If email verification links show `localhost:8000` instead of your production domain:

```bash
# Run the fix script
python scripts/fix_email_verification.py

# Or use the management command
python manage.py update_site_domain --domain yourusername.pythonanywhere.com --protocol https
```

## Usage

### For Students
1. **Registration**: Create an account to start learning
2. **Subject Selection**: Choose from available subjects for your grade level
3. **Learning Path**: Follow structured learning paths through topics
4. **Quizzes**: Take interactive quizzes to test your knowledge
5. **Progress Tracking**: Monitor your learning progress and achievements
6. **Final Exams**: Complete comprehensive exams to advance to the next grade

### For Administrators
1. **Content Management**: Add and manage educational content
2. **User Management**: Monitor student progress and performance
3. **Bulk Import**: Use CSV files to import questions and study materials
4. **System Configuration**: Adjust quiz settings and platform parameters

## Contributing

We welcome contributions to improve Mentora! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, email admin@mentora.com or create an issue in the GitHub repository.

## Acknowledgments

- Built with Django and modern web technologies
- Designed for accessibility and mobile-first experience
- Focused on serving underprivileged learners worldwide
