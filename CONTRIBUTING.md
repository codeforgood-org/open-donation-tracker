# Contributing to Open Donation Tracker

Thank you for your interest in contributing to Open Donation Tracker! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in GitHub Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, browser, etc.)

### Suggesting Features

1. Check existing issues and discussions
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/open-donation-tracker.git
   cd open-donation-tracker
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the code style guidelines
   - Add tests for new functionality
   - Update documentation as needed

4. **Run tests**
   ```bash
   make test
   make lint
   ```

5. **Commit your changes**
   ```bash
   git commit -m "feat: add amazing feature"
   ```

   Use conventional commit messages:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `style:` Code style changes (formatting, etc.)
   - `refactor:` Code refactoring
   - `test:` Adding or updating tests
   - `chore:` Maintenance tasks

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear description
   - Reference related issues
   - Include screenshots for UI changes

## Development Setup

### Backend Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Set up environment
cp ../.env.example ../.env

# Run migrations
alembic upgrade head

# Run development server
uvicorn app.main:app --reload
```

### Frontend Development

```bash
# Install dependencies
cd frontend
npm install

# Run development server
npm run dev
```

## Code Style

### Python (Backend)

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use meaningful variable names
- Add docstrings to functions and classes

Example:
```python
def create_donation(
    donation_data: DonationCreate,
    current_user: User,
    db: Session
) -> Donation:
    """
    Create a new donation.

    Args:
        donation_data: Donation data from request
        current_user: Authenticated user making donation
        db: Database session

    Returns:
        Created donation object

    Raises:
        HTTPException: If organization not found
    """
    # Implementation
```

### TypeScript/React (Frontend)

- Use functional components with hooks
- Use TypeScript for type safety
- Follow React best practices
- Use meaningful component and variable names
- Add JSDoc comments for complex functions

Example:
```typescript
interface DonationFormProps {
  campaignId: number;
  onSuccess: () => void;
}

const DonationForm: React.FC<DonationFormProps> = ({
  campaignId,
  onSuccess
}) => {
  // Implementation
};
```

## Testing

### Backend Tests

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest app/tests/test_auth.py::test_login_success -v
```

### Frontend Tests

```bash
# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

### Test Guidelines

- Write tests for new features
- Maintain test coverage above 80%
- Test edge cases and error conditions
- Use descriptive test names

## Documentation

- Update README.md for major changes
- Add docstrings to all functions and classes
- Update API documentation in comments
- Include examples for complex functionality

## Database Migrations

When making database changes:

```bash
# Create a new migration
cd backend
alembic revision -m "description of changes"

# Edit the generated migration file
# Run migration
alembic upgrade head

# Downgrade if needed
alembic downgrade -1
```

## Review Process

1. All PRs require at least one review
2. CI/CD pipeline must pass
3. Code coverage should not decrease
4. Documentation must be updated
5. Changes should follow the project architecture

## Questions?

Feel free to:
- Open an issue for questions
- Join our discussions
- Reach out to maintainers

Thank you for contributing! 🎉
