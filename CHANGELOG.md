# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive project documentation
  - PROJECT_COMPLETION_PLAN.md - Honest assessment and roadmap
  - REQUIREMENTS.md - Detailed requirements specification
  - ARCHITECTURE.md - Technical design documentation
  - CONTRIBUTING.md - Contribution guidelines
  - QUICKSTART.md - Getting started guide
  - CHANGELOG.md - This file
- Updated README.md with realistic project status
- Development badges in README

### Changed
- README now accurately reflects project's early development status
- Removed misleading claims about non-existent features

### Known Issues
- Default template not fully implemented
- Notebook parser returns incorrect format
- No configuration file support
- Limited error handling
- Cannot be installed via pip yet

## [0.1.0] - 2024-XX-XX

### Added
- Initial project structure
- Basic Python parser using AST
  - Extract classes with methods
  - Extract functions with parameters
  - Extract docstrings
- Notebook parser foundation (incomplete)
- Template system using Jinja2
  - Base template
  - API template
- CLI using Click
  - `generate` command
  - Basic options (--repo, --output, --template)
- Repository processing
  - Clone Git repositories
  - Process local directories
  - Basic file discovery
- Test infrastructure
  - pytest configuration
  - 4 initial unit tests
- CI/CD
  - GitHub Actions workflow
  - Tests on Python 3.8-3.11
- Documentation
  - Initial README
  - LICENSE (MIT)
  - Basic pyproject.toml

### Known Limitations
- Many advertised features not yet implemented
- Template system incomplete
- No error handling
- No configuration support
- Limited test coverage (~30%)

---

## Release Notes Format

For future releases, use this format:

### Added
- New features

### Changed
- Changes to existing functionality

### Deprecated
- Features that will be removed

### Removed
- Features that were removed

### Fixed
- Bug fixes

### Security
- Security improvements or fixes
