# python-dotenv 1.2.4 - PyPI Package Page

> Source: https://pypi.org/project/python-dotenv/
> Collected: 2026-11-06
> Published: 2026-10-01

# python-dotenv 1.2.4

Read key-value pairs from a `.env` file and set them as environment variables

## Description

python-dotenv reads key-value pairs from a `.env` file and can set them as environment variables. It helps in the development of applications following the [12-factor](https://12factor.net/) principles.

## Getting Started

```
pip install python-dotenv
```

If your application takes its configuration from environment variables, like a 12-factor application, launching it in development is not very practical because you have to set those environment variables yourself.

To help you with that, you can add python-dotenv to your application to make it load the configuration from a `.env` file when it is present (e.g. in development) while remaining configurable via the environment:

```python
from dotenv import load_dotenv

load_dotenv()  # reads variables from a .env file and sets them in os.environ

# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.
```

By default, `load_dotenv()` will:

- Look for a `.env` file in the same directory as the Python script (or higher up the directory tree).
- Read each key-value pair and add it to `os.environ`.
- **Not override** existing environment variables (`override=False`). Pass `override=True` to override existing variables.

To configure the development environment, add a `.env` in the root directory of your project:

```
.
├── .env
└── foo.py
```

The syntax of `.env` files supported by python-dotenv is similar to that of Bash:

```
# Development settings
DOMAIN=example.org
ADMIN_EMAIL=admin@${DOMAIN}
ROOT_URL=${DOMAIN}/app
```

If you use variables in values, ensure they are surrounded with `{` and `}`, like `${DOMAIN}`, as bare variables such as `$DOMAIN` are not expanded.

You will probably want to add `.env` to your `.gitignore`, especially if it contains secrets like a password.

## Other Use Cases

### Load configuration without altering the environment

The function `dotenv_values` works more or less the same way as `load_dotenv`, except it doesn't touch the environment, it just returns a `dict` with the values parsed from the `.env` file.

```python
from dotenv import dotenv_values

config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}
```

This notably enables advanced configuration management:

```python
import os
from dotenv import dotenv_values

config = {
    **dotenv_values(".env.shared"),  # load shared development variables
    **dotenv_values(".env.secret"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}
```

### Parse configuration as a stream

`load_dotenv` and `dotenv_values` accept [streams](https://docs.python.org/3/library/io.html) via their `stream` argument. It is thus possible to load the variables from sources other than the filesystem (e.g. the network).

```python
from io import StringIO

from dotenv import load_dotenv

config = StringIO("USER=foo\nEMAIL=foo@example.org")
load_dotenv(stream=config)
```

### Load .env files in IPython

You can use dotenv in IPython. By default, it will use `find_dotenv` to search for a `.env` file:

```
%load_ext dotenv
%dotenv
```

You can also specify a path:

```
%dotenv relative/or/absolute/path/to/.env
```

Optional flags:

- `-o` to override existing variables.
- `-v` for increased verbosity.

### Disable load_dotenv

Set `PYTHON_DOTENV_DISABLED=1` to disable `load_dotenv()` from loading .env files or streams. Useful when you can't modify third-party package calls or in production.

## Command-line Interface

A CLI interface `dotenv` is also included, which helps you manipulate the `.env` file without manually opening it.

```
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

Run `dotenv --help` for more information about the options and subcommands.

## File format

The format is not formally specified and still improves over time. That being said, `.env` files should mostly look like Bash files. Reading from FIFOs (named pipes) on Unix systems is also supported.

Keys can be unquoted or single-quoted. Values can be unquoted, single- or double-quoted. Spaces before and after keys, equal signs, and values are ignored. Values can be followed by a comment. Lines can start with the `export` directive, which does not affect their interpretation.

Allowed escape sequences:

- in single-quoted values: `\\`, `\'`
- in double-quoted values: `\\`, `\'`, `\"`, `\a`, `\b`, `\f`, `\n`, `\r`, `\t`, `\v`

### Multiline values

It is possible for single- or double-quoted values to span multiple lines. The following examples are equivalent:

```
FOO="first line
second line"
```

```
FOO="first line\nsecond line"
```

### Variable without a value

A variable can have no value:

```
FOO
```

It results in `dotenv_values` associating that variable name with the value `None` (e.g. `{"FOO": None}`. `load_dotenv`, on the other hand, simply ignores such variables.

This shouldn't be confused with `FOO=`, in which case the variable is associated with the empty string.

### Variable expansion

python-dotenv can interpolate variables using POSIX variable expansion.

With `load_dotenv(override=True)` or `dotenv_values()`, the value of a variable is the first of the values defined in the following list:

1. Value of that variable in the `.env` file.
2. Value of that variable in the environment.
3. Default value, if provided.
4. Empty string.

With `load_dotenv(override=False)`, the value of a variable is the first of the values defined in the following list:

1. Value of that variable in the environment.
2. Value of that variable in the `.env` file.
3. Default value, if provided.
4. Empty string.

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

## Release History

| Version | Date | Notes |
|---------|------|-------|
| 1.2.4 | Oct 1, 2026 | Fixed `dotenv get` exit code for empty string values; fixed unquoted empty value with inline comment parsing; fixed `dotenv run --no-override` variable expansion precedence |
| 1.2.3 | Aug 16, 2026 | Strip leading UTF-8 BOM; `set_key` escapes backslashes; `dotenv run` friendly error; cache parsed result for empty .env files |
| 1.2.2 | Mar 1, 2026 | Support for Python 3.14 (including free-threaded build); `dotenv run` forwards flags; dropped Python 3.9 support |
| 1.2.1 | Oct 26, 2025 | Move more config to `pyproject.toml`; support reading `.env` from FIFOs (Unix) |
| 1.2.0 | Oct 26, 2025 | Upgrade build system to PEP 517 & PEP 518; support Python 3.14; `PYTHON_DOTENV_DISABLED` env var |
| 1.1.0 | Mar 25, 2025 | Support Python 3.13; `dotenv run` uses `execvpe`; drop Python 3.8 |
| 1.0.0 | Feb 24, 2023 | Drop Python 3.7, add Python 3.12-dev |

## Metadata

- **Author:** Saurabh Kumar (me+github@saurabh-kumar.com)
- **Maintainers:** Saurabh Kumar, Bertrand Bonnefoy-Claudet
- **License:** BSD-3-Clause
- **Requires:** Python >=3.10
- **Provides Extra:** `cli`
- **Repository:** https://github.com/theskumar/python-dotenv
- **Latest Release:** 1.2.4 (Oct 1, 2026)