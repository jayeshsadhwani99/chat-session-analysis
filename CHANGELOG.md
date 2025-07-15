# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Comprehensive GitHub repository setup
- Professional documentation and contributing guidelines
- Package distribution configuration

## [1.2.0] - 2024-12-19

### Added

- **Session Analytics**: Enhanced session-level metrics tracking
  - `num_user_messages` per session
  - Session length statistics in summary output
  - Average and median session metrics
- **Performance Optimizations**: Pre-compiled regex patterns for faster intent classification
- **Professional Logging**: Proper logging module with file and console output
- **Type Safety**: Added `FunnelStage` enum for consistent funnel stage values
- **Configuration**: Added `SMOKE_TEST` flag for explicit testing mode
- **Brand Reorganization**: Properly categorized 100+ brands into 8 industry categories

### Changed

- **Enum Consistency**: Updated `classify_funnel()` to return `FunnelStage` enum instead of strings
- **JSON Serialization**: Fixed enum serialization in summary output
- **Code Structure**: Improved error handling and documentation
- **Brand Categories**: Reorganized brands into logical industry groupings:
  - Global Tech
  - SaaS & Cloud
  - Ecommerce & D2C
  - Automotive
  - Travel & Hospitality
  - Food & Beverage
  - Media & Entertainment
  - Financial Services

### Fixed

- **Support Percentage**: Corrected formatting in JSON summary output
- **Documentation**: Added comprehensive docstrings and inline comments

## [1.1.0] - 2024-12-18

### Added

- **Brand Detection**: Comprehensive brand mention extraction with 100+ brands
- **Support Query Flagging**: Automatic identification of troubleshooting requests
- **Enhanced Intent Classification**: Improved patterns for educational/quiz detection
- **Session Metadata**: Added session length tracking

### Changed

- **Intent Categories**: Refined classification logic with better keyword matching
- **Funnel Mapping**: Enhanced funnel stage assignment based on intent and keywords

## [1.0.0] - 2024-12-17

### Added

- **Initial Release**: Core pipeline functionality
- **Intent Classification**: 6-category intent classification system
- **Funnel Stage Mapping**: Customer journey stage assignment
- **JSONL Processing**: Efficient chunked processing of large datasets
- **Sampling**: Configurable 1% sampling for performance
- **Output Formats**: Parquet and JSON summary outputs

### Features

- Commercial, paraphrase/edit, educational/quiz, informational, navigational, and other intent categories
- Awareness, consideration, decision, and retention funnel stages
- Memory-efficient chunked processing
- Reproducible sampling with fixed random seed

---

## Version History Summary

- **v1.0.0**: Core pipeline with intent classification and funnel mapping
- **v1.1.0**: Added brand detection and support query flagging
- **v1.2.0**: Enhanced session analytics, performance optimizations, and professional setup
