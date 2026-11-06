# Python Dotenv Usage

> Sources: The Codex - Python Module 05 BIS - Course material; 2026-11-01; PyPI - python-dotenv 1.2.4; 2026-10-01
> Raw: [The Codex: Packages, Environments and the Alchemist's Toolchain](../../raw/python-programming/2026-11-01-the-codex-python05-bis.md); [python-dotenv 1.2.4 - PyPI Package Page](../../raw/python-programming/2026-11-06-pypi-python-dotenv.md)
> Updated: 2026-11-06

## Overview

Python dotenv is a library that allows configuration management through environment variables loaded from `.env` files. It solves the critical problem of secret management in software development by keeping sensitive configuration outside version control while providing a consistent interface for accessing configuration values.

## Core Concept

Environment variables provide a universal way for programs to access configuration settings without hardcoding values. However, managing these variables across different environments (development, testing, production) presents challenges:

**The Problem:**
- Database credentials, API keys, and configuration often need to be embedded in code
- Development environments need different settings than production
- Secrets can be accidentally committed to version control

**The Solution:**
- Store configuration in `.env` files (ignored by git)
- Use `python-dotenv` to load these variables into `os.environ`
- Access configuration consistently throughout the application

## Installation and Setup

### Required Dependencies

**In `requirements.txt` (pip):**
```
python-dotenv>=0.19.0
```

**In `pyproject.toml` (Poetry):**
```toml
[tool.poetry.dependencies]
python = "^3.10"
python-dotenv = "^0.19.0"
```

### Project Structure

```
ex1/
    |--.env.example          # Template for .env file
    |--.gitignore            # .env should never be committed
    |--oracle.py            # Uses dotenv for configuration
    |--requirements.txt
    |--pyproject.toml
```

## Basic Usage

### 1. Creating the .env File

**.env example:**
```bash
# Development Configuration
MATRIX_MODE=development
DATABASE_URL=sqlite:///dev_database.db
API_KEY=dev_api_key_12345
LOG_LEVEL=DEBUG
ZION_ENDPOINT=http://localhost:8000

# Production Configuration (separate file)
MATRIX_MODE=production
DATABASE_URL=postgresql://prod:secret@prod-db:5432/mydb
API_KEY=prod_secret_key_67890
LOG_LEVEL=INFO
ZION_ENDPOINT=https://api.example.com
```

### 2. The .env.example Template

**.env.example (never commit actual secrets):**
```bash
# Configuration Variables
MATRIX_MODE=development
DATABASE_URL=YOUR_DATABASE_URL_HERE
API_KEY=YOUR_API_KEY_HERE
LOG_LEVEL=DEBUG
ZION_ENDPOINT=YOUR_ENDPOINT_URL_HERE

# Optional Configuration
CACHE_TIMEOUT=3600
MAX_RETRIES=3
```

### 3. Using Dotenv in Code

**Example `oracle.py`:**
```python
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access configuration variables
matrix_mode = os.getenv("MATRIX_MODE")
database_url = os.getenv("DATABASE_URL")
api_key = os.getenv("API_KEY")
log_level = os.getenv("LOG_LEVEL", "INFO")  # Default value
zion_endpoint = os.getenv("ZION_ENDPOINT")

print(f"Environment: {matrix_mode}")
print(f"Database: {database_url}")
print(f"API Key: {'*' * len(api_key) if api_key else 'Not set'}")
```

## Configuration Management

### 1. Development vs Production Behavior

**Development Configuration:**
```python
def configure_for_development():
    load_dotenv()  # Loads from .env file
    
    matrix_mode = os.getenv("MATRIX_MODE", "development")
    database_url = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    
    return {
        "debug": True,
        "database": database_url,
        "testing": False
    }
```

**Production Configuration:**
```python
def configure_for_production():
    # Load from system environment or .env
    load_dotenv()  # Can also use different file: load_dotenv('.env.production')
    
    matrix_mode = os.getenv("MATRIX_MODE", "production")
    database_url = os.getenv("DATABASE_URL")  # Required in production
    
    if not database_url:
        raise ValueError("DATABASE_URL is required in production")
    
    return {
        "debug": False,
        "database": database_url,
        "testing": False
    }
```

### 2. Default Values and Validation

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration with defaults and validation
class Config:
    def __init__(self):
        self.matrix_mode = os.getenv("MATRIX_MODE", "development")
        self.database_url = os.getenv("DATABASE_URL")
        self.api_key = os.getenv("API_KEY")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.zion_endpoint = os.getenv("ZION_ENDPOINT")
        
    def validate(self):
        """Validate configuration based on environment"""
        if self.matrix_mode == "production":
            if not self.database_url:
                raise ValueError("DATABASE_URL required in production")
            if not self.api_key:
                raise ValueError("API_KEY required in production")
        
        return True

# Usage
config = Config()
config.validate()
```

## Security Best Practices

### 1. .gitignore Configuration

**.gitignore example:**
```bash
# Environment files
.env
.env.local
.env.*.local

# IDE specific
.vscode/
.idea/

# OS specific
.DS_Store
Thumbs.db

# Python specific
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
```

### 2. Configuration Templates

**.env.example (production-ready template):**
```bash
# Application Configuration
MATRIX_MODE=production
DATABASE_URL=postgresql://username:password@localhost/dbname
API_KEY=your_production_api_key_here
LOG_LEVEL=INFO
ZION_ENDPOINT=https://api.yourdomain.com

# Optional Production Settings
CACHE_URL=redis://localhost:6379/0
CACHE_TTL=3600
MAX_WORKERS=4
```

### 3. Environment-Specific Files

Multiple environment files for different deployments:

- **.env**: Local development (contains test/dev data)
- **.env.production**: Production configuration
- **.env.staging**: Staging/QA configuration
- **.env.testing**: Test suite configuration

**Example: Loading different environments**
```python
import os
from dotenv import load_dotenv

environment = os.getenv("ENVIRONMENT", "development")

if environment == "production":
    load_dotenv(".env.production")
elif environment == "testing":
    load_dotenv(".env.testing")
else:
    load_dotenv(".env")

# Load environment-specific configuration
load_dotenv(f".env.{environment}")
```

## Testing Configuration

### 1. Test Configuration Isolation

**Test setup:**
```python
import pytest
import os
from dotenv import load_dotenv
from unittest.mock import patch

@pytest.fixture
def test_config():
    """Test configuration fixture"""
    test_env = {
        "MATRIX_MODE": "testing",
        "DATABASE_URL": "sqlite:///:memory:",
        "API_KEY": "test_key",
        "LOG_LEVEL": "DEBUG"
    }
    
    with patch.dict(os.environ, test_env):
        load_dotenv()
        yield test_env

def test_development_config(test_config):
    assert test_config["MATRIX_MODE"] == "testing"
    assert "memory" in test_config["DATABASE_URL"]
```

### 2. Mock Environment in Tests

```python
import pytest
from unittest.mock import patch, mock_open
import dotenv

def test_oracle_with_mocked_env():
    """Test oracle.py with mocked environment variables"""
    with patch.dict(os.environ, {
        "MATRIX_MODE": "development",
        "DATABASE_URL": "sqlite:///test.db",
        "API_KEY": "test_key_123"
    }):
        # Reload dotenv to pick up mocked environment
        dotenv.load_dotenv()
        
        # Import and test oracle functionality
        from ex1.oracle import OracleConfig
        config = OracleConfig()
        
        assert config.matrix_mode == "development"
        assert "test.db" in config.database_url
```

## Advanced Dotenv Features

### 1. Loading from Different Sources

```python
from dotenv import load_dotenv, find_dotenv

# Load from specific file
load_dotenv("/path/to/custom.env")

# Find and load from nearest .env file
load_dotenv(find_dotenv())  # Searches up the directory tree

# Load with explicit encoding
load_dotenv("config.env", encoding="utf-8")
```

### 2. Environment Variable Expansion

**.env with expansion:**
```bash
BASE_DIR=/app
DATABASE_URL=sqlite:///$BASE_DIR/data.db
API_KEY=${API_PREFIX}_secret_key
```

**Code access:**
```python
from dotenv import dotenv_values

config = dotenv_values()
print(f"Database: {config['DATABASE_URL']}")  # sqlite://///app/data.db
```

## Package Metadata

| Attribute | Value |
|-----------|-------|
| Package | `python-dotenv` |
| Latest Version | 1.2.4 (released Oct 1, 2026) |
| License | BSD-3-Clause |
| Python Requirement | >=3.10 |
| Optional Extra | `cli` |
| Author | Saurabh Kumar |
| Maintainers | Saurabh Kumar, Bertrand Bonnefoy-Claudet |
| Repository | https://github.com/theskumar/python-dotenv |

## Command-Line Interface

The `dotenv` CLI helps you manipulate `.env` files without manually opening them:

```bash
$ pip install "python-dotenv[cli]"
$ dotenv set USER foo
$ dotenv set EMAIL foo@example.org
$ dotenv list
USER=foo
EMAIL=foo@example.org
$ dotenv list --format=json
{
  "USER": "foo",
  "EMAIL": "foo@example.org"
}
$ dotenv run -- python foo.py
```

Run `dotenv --help` for more information about options and subcommands.

## File Format Reference

### General Rules

- Keys can be unquoted or single-quoted
- Values can be unquoted, single- or double-quoted
- Spaces before/after keys, equal signs, and values are ignored
- Values can be followed by a comment
- Lines can start with the `export` directive (does not affect interpretation)

### Escape Sequences

| Context | Allowed Escapes |
|---------|-----------------|
| Single-quoted values | `\\`, `\'` |
| Double-quoted values | `\\`, `\'`, `\"`, `\a`, `\b`, `\f`, `\n`, `\r`, `\t`, `\v` |

### Multiline Values

Single- or double-quoted values can span multiple lines:

```bash
FOO="first line
second line"
```

Equivalent to:

```bash
FOO="first line\nsecond line"
```

### Variable Without a Value

A variable can have no value:

```bash
FOO
```

`dotenv_values` associates this with `None` (e.g., `{"FOO": None}`). `load_dotenv` simply ignores such variables.

This differs from `FOO=`, which associates the variable with the empty string.

### Variable Expansion Precedence

python-dotenv interpolates variables using POSIX variable expansion (`${VAR}`).

**With `load_dotenv(override=True)` or `dotenv_values()`:**
1. Value in the `.env` file
2. Value in the environment
3. Default value, if provided
4. Empty string

**With `load_dotenv(override=False)` (default):**
1. Value in the environment
2. Value in the `.env` file
3. Default value, if provided
4. Empty string

## Disabling Dotenv

Set `PYTHON_DOTENV_DISABLED=1` to disable `load_dotenv()` from loading `.env` files or streams. Useful when you can't modify third-party package calls or in production.

## IPython Support

You can use dotenv in IPython:

```
%load_ext dotenv
%dotenv
```

You can also specify a path:

```
%dotenv relative/or/absolute/path/to/.env
```

Optional flags:

- `-o` to override existing variables
- `-v` for increased verbosity

## Related Projects

- [environs](https://github.com/sloria/environs)
- [Honcho](https://github.com/nickstenning/honcho)
- [dump-env](https://github.com/sobolevn/dump-env)
- [dynaconf](https://github.com/dynaconf/dynaconf)
- [parse_it](https://github.com/naorlivne/parse_it)
- [django-dotenv](https://github.com/jpadilla/django-dotenv)
- [django-environ](https://github.com/joke2k/django-environ)
- [python-decouple](https://github.com/HBNetwork/python-decouple)
- [django-configuration](https://github.com/jezdez/django-configurations)

## Common Issues and Solutions

### 1. "Environment variable not found"

**Problem:** Code expects variables that don't exist
**Solution:** Provide defaults and validate:
```python
database_url = os.getenv("DATABASE_URL", "sqlite:///dev.db")
if not database_url:
    raise ValueError("DATABASE_URL is required")
```

### 2. `.env` file not loading

**Problem:** dotenv not working as expected
**Solutions:**
1. Check if `.env` exists in the current directory
2. Ensure `python-dotenv` is installed
3. Verify file permissions
4. Check for syntax errors in `.env` file

### 3. Production vs Development confusion

**Problem:** Using development settings in production
**Solution:** Environment-specific validation and separation

## See Also

- [Environment Configuration](/wiki/python-programming/environment-configuration)
- [Virtual Environment Management](/wiki/python-programming/virtual-environments)
- [Dependency Management](/wiki/python-programming/python-dependency-management)
- [Python pip: Standard Package Manager](/wiki/python-programming/python-pip.md)

## Status Notes

> **Status: Draft**
> This article covers dotenv configuration management from Exercise 1 of The Codex and the python-dotenv 1.2.4 PyPI package page. Content includes `load_dotenv()`, `dotenv_values()`, CLI usage, file format, variable expansion precedence, IPython support, and related projects.