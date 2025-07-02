# LinkedIn Clone - Professional Networking Platform

A modern professional networking platform built with NiceGUI and FastAPI, featuring user profiles, connections, posts, and professional information management.

## Features

### 🔐 Authentication & User Management
- User registration and login
- Secure password hashing with bcrypt
- JWT token-based authentication
- Profile management with professional information

### 👥 Professional Networking
- Send and receive connection requests
- Accept/decline connection requests
- View network connections
- People you may know suggestions

### 📝 Content Sharing
- Create and share posts
- Like and comment on posts
- Personalized feed based on connections
- Real-time interaction updates

### 💼 Professional Profiles
- Comprehensive user profiles
- Experience and work history
- Education background
- Skills and endorsements
- Professional headlines and summaries

### 🎨 Modern UI/UX
- Clean, professional interface
- Responsive design
- LinkedIn-inspired styling
- Intuitive navigation

## Technology Stack

- **Frontend**: NiceGUI (Python-based UI framework)
- **Backend**: FastAPI (High-performance Python web framework)
- **Database**: SQLAlchemy V2 with SQLite (easily upgradeable to PostgreSQL)
- **Authentication**: JWT tokens with bcrypt password hashing
- **Validation**: Pydantic V2 for data validation
- **Styling**: Tailwind CSS classes via NiceGUI

## Quick Start

### Prerequisites
- Python 3.9 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd linkedin-clone
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8000`

## Project Structure

```
linkedin-clone/
├── app/
│   ├── core/                   # Core application configuration
│   │   ├── config.py          # Settings and configuration
│   │   ├── database.py        # Database setup and connection
│   │   ├── security.py        # Authentication utilities
│   │   └── logging.py         # Logging configuration
│   ├── models/                 # SQLAlchemy database models
│   │   ├── user.py            # User model
│   │   ├── profile.py         # Professional profile models
│   │   └── social.py          # Social networking models
│   ├── schemas/                # Pydantic validation schemas
│   │   ├── user.py            # User schemas
│   │   ├── profile.py         # Profile schemas
│   │   └── social.py          # Social schemas
│   ├── services/               # Business logic layer
│   │   ├── auth_service.py    # Authentication service
│   │   ├── user_service.py    # User management service
│   │   ├── profile_service.py # Profile management service
│   │   └── social_service.py  # Social networking service
│   └── main.py                # NiceGUI frontend application
├── data/                       # Database files
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Usage Guide

### Getting Started

1. **Create an Account**
   - Click "Sign In" on the homepage
   - Switch to the "Register" tab
   - Fill in your information and create an account

2. **Complete Your Profile**
   - Add a professional headline
   - Write a summary about yourself
   - Add your work experience
   - Include your education background
   - List your skills

3. **Build Your Network**
   - Visit the "My Network" page
   - Send connection requests to other professionals
   - Accept incoming connection requests
   - Explore "People you may know" suggestions

4. **Share Content**
   - Create posts on your dashboard
   - Share professional insights and updates
   - Engage with your network's content through likes and comments

### Key Features

#### Professional Profiles
- **Experience Section**: Add your work history with company, title, dates, and descriptions
- **Education Section**: Include your educational background
- **Skills Section**: List your professional skills
- **Professional Summary**: Write about your career and expertise

#### Networking
- **Connection Requests**: Send and receive connection requests with optional messages
- **Network Management**: View all your professional connections
- **Discovery**: Find new people to connect with based on the platform's suggestions

#### Content Sharing
- **Post Creation**: Share updates, insights, and professional content
- **Engagement**: Like and comment on posts from your network
- **Feed Algorithm**: See content from your connections in chronological order

## Configuration

### Environment Variables

Key configuration options in `.env`:

```env
# Application
APP_NAME=LinkedIn Clone
DEBUG=False

# Server
HOST=0.0.0.0
PORT=8000

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=sqlite:///./data/linkedin_clone.db
```

### Database Configuration

The application uses SQLite by default for easy setup. For production, you can switch to PostgreSQL:

```env
DATABASE_URL=postgresql://username:password@localhost/linkedin_clone
```

## Development

### Adding New Features

1. **Database Models**: Add new models in `app/models/`
2. **API Schemas**: Define Pydantic schemas in `app/schemas/`
3. **Business Logic**: Implement services in `app/services/`
4. **UI Components**: Add UI components in `app/main.py`

### Code Quality

The project follows modern Python best practices:
- Type hints throughout the codebase
- Pydantic V2 for data validation
- SQLAlchemy V2 for database operations
- Comprehensive error handling
- Structured logging

## Security Features

- **Password Security**: Bcrypt hashing for password storage
- **Authentication**: JWT token-based authentication
- **Input Validation**: Pydantic schemas validate all user inputs
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **CORS Configuration**: Configurable CORS settings for API security

## Performance Considerations

- **Database Optimization**: Efficient queries with SQLAlchemy relationships
- **Connection Pooling**: Database connection pooling for better performance
- **Lazy Loading**: Optimized data loading strategies
- **Pagination**: Built-in pagination for large datasets

## Deployment

### Production Deployment

1. **Set Production Environment**
   ```env
   DEBUG=False
   SECRET_KEY=your-production-secret-key
   DATABASE_URL=postgresql://user:pass@host/db
   ```

2. **Use Production Database**
   - Set up PostgreSQL or another production database
   - Update the `DATABASE_URL` in your environment

3. **Deploy with Docker** (optional)
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "main.py"]
   ```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the code examples in the project

## Roadmap

Future enhancements planned:
- [ ] Real-time messaging system
- [ ] Company pages and job postings
- [ ] Advanced search and filtering
- [ ] File upload for profile images and post media
- [ ] Email notifications
- [ ] Mobile-responsive improvements
- [ ] Analytics and insights
- [ ] Recommendation algorithms
- [ ] API rate limiting
- [ ] Advanced security features

---

Built with ❤️ using NiceGUI and FastAPI