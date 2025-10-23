# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a Python-based repository for German language learning resources and content. It contains:
- German language reference materials (vocabulary, grammar, etc.)
- Python scripts and tools for language processing and learning
- Structured data for German language content

## Technology Stack

- **Language:** Python 3.11+
- **Package Manager:** uv (preferred) or pip
- **Project Structure:** Python package with language resources

## Common Development Commands

### Package Management

```bash
# Install/sync dependencies
uv sync

# Add a new dependency
uv add <package-name>

# Add a development dependency
uv add --dev <package-name>
```

### Running Code

```bash
# Run Python scripts
uv run python -m <module_name>

# Run tests (when implemented)
uv run pytest

# Run tests with coverage (when implemented)
uv run pytest --cov=src --cov-report=term
```

### Development Workflow

```bash
# Install pre-commit hooks (if configured)
uv run pre-commit install

# Format code (if formatter configured)
uv run ruff format src/

# Lint code (if linter configured)
uv run ruff check src/
```

## Expected Repository Structure

As the project develops, expect this structure:

```
german/
├── src/
│   └── german/              # Main Python package
│       ├── __init__.py
│       ├── vocabulary/      # Vocabulary-related code
│       ├── grammar/         # Grammar-related code
│       └── utils/           # Utility functions
├── resources/               # Language data and content
│   ├── vocabulary/
│   │   ├── nouns.json      # Noun vocabulary lists
│   │   ├── verbs.json      # Verb conjugations
│   │   └── adjectives.json
│   └── grammar/
│       ├── rules.md        # Grammar rules documentation
│       └── examples.json   # Example sentences
├── tests/                   # Test files
│   ├── test_vocabulary.py
│   └── test_grammar.py
├── scripts/                 # Utility scripts
│   └── import_data.py      # Data import/processing scripts
├── pyproject.toml          # Python project configuration
├── README.md               # User-facing documentation
└── CLAUDE.md               # This file
```

## Development Guidelines

### Adding German Language Content

1. **Vocabulary:**
   - Store in structured JSON/YAML files under `resources/vocabulary/`
   - Include: German word, English translation, gender (for nouns), plural forms
   - Use consistent schema across all vocabulary files

2. **Grammar Rules:**
   - Document in Markdown under `resources/grammar/`
   - Include examples with explanations
   - Cross-reference related rules

3. **Examples and Exercises:**
   - Store in structured data formats (JSON preferred)
   - Include correct answers and explanations
   - Tag by difficulty level and topic

### Code Organization

- Keep language data separate from code (`resources/` vs `src/`)
- Write Python code to process, validate, or serve language content
- Use type hints for all Python functions
- Document German-specific terminology in docstrings

### Testing

- Write tests for data validation (e.g., checking JSON schema)
- Test Python utilities and processing scripts
- Validate German language data integrity (gender agreement, conjugation correctness)

### File Naming Conventions

- Python files: `snake_case.py`
- Resource files: `lowercase_with_underscores.json` or `.yaml`
- Documentation: `CamelCase.md` or `lowercase-with-hyphens.md`

## Project-Specific Context

### German Language Data

When working with German language content:
- Nouns have grammatical gender (der/die/das) - always include this
- Verbs have separable prefixes - track this attribute
- Adjectives have declension - may need tables
- Cases (Nominativ, Akkusativ, Dativ, Genitiv) affect articles and adjectives

### Data Quality

- Validate umlauts (ä, ö, ü) and eszett (ß) are correctly represented
- Ensure consistent encoding (UTF-8)
- Cross-check translations for accuracy
- Cite sources for language data when possible

## Future Development

As the project grows, update this file with:
- Specific API documentation (if building web service)
- Data schema definitions
- Content contribution guidelines
- Build and deployment instructions
