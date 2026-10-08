# Bulk Certificate Generator

A backend API for generating certificates in bulk for multiple recipients.

## Overview

This project provides a REST API that accepts a certificate generation request containing multiple recipients and generates an individual PDF certificate for each valid recipient.

The system also tracks the generation job status and allows generated certificates to be retrieved.

## Features

- Bulk certificate generation
- Input validation
- PDF certificate generation
- Job status tracking
- Success and failure tracking
- Individual certificate retrieval
- Handles individual certificate failures without stopping the entire job
- REST API
- SQLite relational database
- Automated tests
- Swagger API documentation

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- ReportLab
- Pytest
- Uvicorn

## Project Structure

```text
bulk-certificate-generator/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   │
│   ├── routers/
│   │   └── certificates.py
│   │
│   └── services/
│       ├── certificate_generator.py
│       └── job_processor.py
│
├── generated_certificates/
│
├── tests/
│   ├── test_jobs.py
│   ├── test_validation.py
│   ├── test_generation.py
│   └── test_retrieval.py
│
├── .gitignore
├── README.md
└── requirements.txt