# Tabletop Utils

A modern Django web application providing utilities for tabletop RPG gaming sessions with real-time HTMX updates.

## Features

### 🎲 Initiative Tracker
- Track character turn order and initiatives for combat encounters
- Real-time updates with HTMX (no page reloads)
- Drag-and-drop position reordering
- Automatic sorting by initiative and position
- Add, delete, and manage characters on the fly

### 🌍 Internationalization
- **Multilingual Support**: Available in English, German, and Spanish
- Language switcher in the navigation bar
- All UI elements fully translated

### 🎨 Modern UI/UX
- **Dark/Light Theme Toggle**: Sun/Moon icons for easy theme switching
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Bootstrap 5.3**: Clean, modern interface
- **Font Awesome Icons**: Beautiful iconography throughout

### ⚡ Performance & Technology
- **HTMX Integration**: Dynamic updates without JavaScript frameworks
- **Django 5.2+**: Robust backend with type hints
- **Database Indexing**: Optimized queries for better performance
- **RESTful Design**: Single view class handling all tracker operations

## Development Setup

### Requirements

- Python 3.13 (managed with [pyenv](https://github.com/pyenv/pyenv))
- Pipenv
- Django 5.2+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/SETA1609/tabletop-utils.git
cd tabletop-utils
```

2. Ensure Python 3.13.3 is available via pyenv and install dependencies:
```bash
pyenv install 3.13.3  # if not already installed
pyenv local 3.13.3
pipenv sync --dev
```

3. Run migrations:
```bash
pipenv run python manage.py migrate
```

4. (Optional) Compile translation messages:
```bash
pipenv run python manage.py compilemessages
```

5. Run the development server:
```bash
pipenv run python manage.py runserver
```

6. Visit `http://localhost:8000/en/` (or `/de/`, `/es/` for other languages)

## Project Structure

```
tabletop-utils/
├── core/                      # Core app (homepage, navigation)
│   ├── views.py              # Index, language switch, theme toggle
│   ├── templates/
│   │   └── core/
│   │       ├── base.html     # Base template with Bootstrap & Font Awesome
│   │       ├── _navbar.html  # Navigation with language/theme selectors
│   │       └── index.html    # Homepage
│   └── context_processors.py # Navigation and theme context
├── initiative_tracker/        # Initiative tracker app
│   ├── views.py              # Single TrackerView handling all operations
│   ├── models.py             # Character model with DB indexes
│   ├── forms.py              # Character form with validation
│   ├── tests.py              # Comprehensive test suite
│   └── templates/
│       └── initiative_tracker/
│           ├── tracker.html          # Main tracker page
│           ├── tracker_partial.html  # HTMX partial updates
│           └── _add_character_form.html
├── locale/                    # Translation files (de, en, es)
└── tabletop_utils/           # Project settings
    ├── settings.py           # Django settings with security configurations
    └── urls.py               # URL routing with i18n patterns
```

## Code Quality

This project uses several linting and code quality tools:

### Linting & Formatting
- **Black**: Code formatting (line length: 88)
- **isort**: Import sorting
- **Flake8**: Style guide enforcement
- **mypy**: Static type checking with django-stubs

### Run Code Quality Checks
```bash
# Format code
pipenv run black .

# Sort imports
pipenv run isort .

# Lint code
pipenv run flake8

# Type check
pipenv run mypy .
```

## Testing

Comprehensive test suite with 8+ tests covering:
- Character CRUD operations
- HTMX request handling
- Delete operations
- Tracker view rendering

```bash
# Run all tests
pipenv run python manage.py test

# Run specific app tests
pipenv run python manage.py test initiative_tracker

# Run with verbose output
pipenv run python manage.py test -v 2
```

## Architecture Highlights

### Unified View Pattern
The initiative tracker uses a **single `TrackerView` class** that handles all operations:
- Display tracker list
- Add characters
- Delete characters
- Advance turns
- Reorder positions

This reduces code duplication and makes the codebase easier to maintain.

### HTMX Integration
All dynamic updates use HTMX attributes:
- `hx-get`: Load forms
- `hx-post`: Submit forms
- `hx-delete`: Delete items
- `hx-target` & `hx-swap`: Update specific page sections

### Security Features
- Environment variable support for sensitive settings
- HTTPS/SSL redirect in production
- Secure cookies (CSRF, Session)
- Content Security Policy headers
- HSTS preload support

## Deployment

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com
```

### Production Checklist

- [ ] Set `DJANGO_DEBUG=False`
- [ ] Generate secure `DJANGO_SECRET_KEY`
- [ ] Configure `DJANGO_ALLOWED_HOSTS`
- [ ] Run `python manage.py collectstatic`
- [ ] Run `python manage.py compilemessages`
- [ ] Set up SSL/TLS certificates
- [ ] Configure database backups
- [ ] Set up error monitoring (e.g., Sentry)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Django](https://www.djangoproject.com/)
- UI powered by [Bootstrap 5](https://getbootstrap.com/)
- Dynamic updates via [HTMX](https://htmx.org/)
- Icons from [Font Awesome](https://fontawesome.com/)

---

**Version**: 1.0.0  
**Author**: SETA1609  
**Repository**: [github.com/SETA1609/tabletop-utils](https://github.com/SETA1609/tabletop-utils)
