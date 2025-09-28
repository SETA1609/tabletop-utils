# Tabletop Utils

A Django web application providing utilities for tabletop RPG gaming sessions.

## Features

- **Initiative Tracker**: Track character turn order and initiatives for combat encounters with HTMX-powered inline updates
- Clean, modern Bootstrap-based UI
- Responsive design for desktop and mobile use
- Built-in light/dark theme toggle and localized navigation controls

## Development Setup

### Requirements

- Python 3.12+
- Django 5.2+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/SETA1609/tabletop-utils.git
cd tabletop-utils
```

2. Install dependencies:
```bash
pip install django django-bootstrap5 htmx django-crispy-forms crispy-bootstrap5
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Run the development server:
```bash
python manage.py runserver
```

## Code Quality

This project uses several linting and code quality tools:

### Linting Tools

- **flake8**: Python linting for style and error checking
- **black**: Code formatting
- **isort**: Import sorting
- **mypy**: Static type checking

### Development Dependencies

Install development dependencies:
```bash
pip install flake8 black isort mypy django-stubs
```

### Running Linting

```bash
# Run all linting checks
flake8 core/ initiative_tracker/ tabletop_utils/ manage.py
black --check .
isort --check-only .
mypy core/ initiative_tracker/ tabletop_utils/ --ignore-missing-imports

# Format code
black .
isort .
```

### Configuration

- **flake8**: `.flake8`
- **black, isort, mypy**: `pyproject.toml`

## Testing

Run all tests:
```bash
python manage.py test
```

Run only the initiative tracker suite (unit and end-to-end tests):
```bash
python manage.py test initiative_tracker
```

### Initiative Tracker Workflow

1. Open the tracker at `/tracker/` to review the current turn order.
2. Click **Add Character** to open the inline form and submit a new character.
3. Use **Next Turn** to advance the current combatant to the end of the queue.
4. Adjust ordering with the position inputs or remove entries with **Delete**.

The HTMX integration ensures the tracker updates without full page reloads when adding, reordering, or deleting entries.

### Localization & Theming

- Switch between **Spanish (es)**, **English (US)**, and **German (de)** using the language dropdown in the navigation bar. The selection is persisted to both the session and the language cookie.
- Toggle between light and dark themes using the navbar switch. The current theme preference is stored in `localStorage` and re-applied on subsequent visits.

## GitHub Actions

The project includes a GitHub Actions workflow (`.github/workflows/lint.yml`) that runs on pull requests to the main branch. It performs:

- Django project validation
- Code linting (flake8)
- Code formatting checks (black)
- Import sorting checks (isort)
- Type checking (mypy)
- Test execution

## Project Structure

```
tabletop_utils/
├── core/                   # Core app (home page)
├── initiative_tracker/     # Initiative tracker app
├── tabletop_utils/         # Django settings and configuration
├── .github/workflows/      # GitHub Actions CI/CD
├── .flake8                 # Flake8 configuration
├── .gitignore              # Git ignore rules
├── pyproject.toml          # Python project configuration
└── manage.py               # Django management script
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure all linting passes: `flake8 . && black --check . && isort --check-only . && mypy . --ignore-missing-imports`
5. Run tests: `python manage.py test`
6. Submit a pull request

The GitHub Actions workflow will automatically run linting and tests on your pull request.