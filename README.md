# URL Shortener API

A high-performance URL shortener service built with Python, Litestar framework, and PostgreSQL.

## Features

- ✅ URL shortening with custom short codes
- ✅ Click tracking and analytics
- ✅ URL expiration support
- ✅ RESTful API with proper validation
- ✅ PostgreSQL database with optimized indexes
- ✅ Comprehensive test coverage (TDD approach)
- ✅ Clean architecture with separation of concerns
- ✅ Error handling and validation
- ✅ CORS support
- ✅ Environment-based configuration

## Project Structure

```
app/
├── config/          # Configuration and database setup
├── controllers/     # API endpoints and request handling
├── models/          # Data models
├── repositories/    # Data access layer
├── schemas/         # Request/response schemas
├── services/        # Business logic
├── exceptions.py    # Custom exceptions
├── validators.py    # Input validation
└── main.py         # Application entry point

tests/
├── unit/           # Unit tests
└── integration/    # Integration tests

migrations/         # Database migration files
```

## API Endpoints

### Create Short URL
```
POST /api/v1/urls
Content-Type: application/json

{
  "original_url": "https://example.com",
  "custom_code": "my-link",  // optional
  "expires_at": "2024-12-31T23:59:59Z"  // optional
}
```

### Redirect to Original URL
```
GET /{short_code}
```

### Get URL Statistics
```
GET /api/v1/urls/{short_code}/stats
```

## Setup Instructions

### Prerequisites
- Python 3.9+
- PostgreSQL 12+

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd urlshortener
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database:
```sql
CREATE DATABASE urlshortener;
CREATE USER postgres WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE urlshortener TO postgres;
```

5. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

6. Run the application:
```bash
python -m app.main
```

The API will be available at `http://localhost:8000`

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=app

# Run specific test file
python -m pytest tests/unit/test_url_service.py
```

### Database Migrations

Migrations are automatically applied on application startup. Manual migration files are stored in the `migrations/` directory.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `False` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `BASE_URL` | Base URL for short links | `http://localhost:8000` |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` |
| `DB_NAME` | Database name | `urlshortener` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | `password` |
| `SHORT_CODE_LENGTH` | Length of generated short codes | `6` |
| `MAX_URL_LENGTH` | Maximum URL length | `2048` |
| `ALLOWED_ORIGINS` | CORS allowed origins | `*` |

## Performance Considerations

- Database indexes on frequently queried columns
- Connection pooling for database connections
- Optimized SQL queries
- Proper error handling and validation
- Scalable architecture with clear separation of concerns

## Security Features

- Input validation and sanitization
- SQL injection prevention through parameterized queries
- CORS configuration for web security
- URL validation to prevent malicious inputs
- Custom short code validation

## Architecture Highlights

- **Clean Architecture**: Clear separation between layers
- **Dependency Injection**: Services and repositories are injected
- **Test-Driven Development**: Comprehensive test coverage
- **Configuration Management**: Environment-based configuration
- **Error Handling**: Structured exception handling
- **Validation**: Input validation at multiple levels

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Implement the feature
5. Run tests and ensure they pass
6. Submit a pull request

## License

MIT License