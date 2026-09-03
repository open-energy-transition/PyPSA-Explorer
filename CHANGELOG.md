# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.2] - 2026-09-03

### Fixed
- Handle array input for PyPSA ≥ 1.2.3's merged multi-element bar traces
- Require IPython dependency for all installs, fixing missing dependency for maps

## [0.1.1] - 2025-11-26

### Added
- Automatic carrier validation and color assignment after network loading

### Fixed
- GitHub URLs in pyproject.toml

## [0.1.0] - 2024-10-04

### Added
- Initial release of PyPSA Explorer
- Interactive dashboard with multiple visualization tabs:
  - Energy Balance Timeseries
  - Energy Balance Totals
  - Capacity Totals
  - CAPEX Totals
  - OPEX Totals
  - Network Configuration (map + metadata)
- Multi-network support with dropdown selector
- Global filters for carriers and countries
- Command-line interface for easy deployment
- Python API for programmatic usage
- Comprehensive documentation and examples
- Production-ready package structure with:
  - Modular codebase organization
  - Type hints throughout
  - Testing infrastructure with pytest
  - CI/CD pipeline with GitHub Actions
  - Pre-commit hooks for code quality
  - Professional README and documentation

### Changed
- Refactored from single-file application to modular package structure
- Improved code organization with separate modules for layouts, callbacks, and utilities

### Fixed
- None

### Security
- None

[Unreleased]: https://github.com/open-energy-transition/pypsa-explorer/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/open-energy-transition/pypsa-explorer/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/open-energy-transition/pypsa-explorer/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/open-energy-transition/pypsa-explorer/releases/tag/v0.1.0
