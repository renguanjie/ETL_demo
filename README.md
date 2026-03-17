# ETL_demo

This repository contains a minimal implementation of the data platform features discussed: automatic profiling, test-data generation, simple SQL checks, and a lightweight visual UI served by a Python FastAPI backend.

Quick start (using Docker Compose)

1. Build and start:

   docker-compose up --build

2. Open the UI in your browser:

   http://localhost:8000/

Features included in this initial commit:
- Upload a CSV and get an automated profile (nulls, dtypes, top values, basic stats).
- Generate synthetic test data (CSV) via an endpoint.
- Simple static web UI (index.html + app.js) that uploads CSVs and visualizes results.
- Dockerfile and docker-compose for quick local run.

Notes & next steps:
- This is an initial scaffold. Next iterations can add: db connections, SQL AST auditing, Great Expectations checks, dbt model generation, lineage extraction, user authentication, and a richer frontend (React or Vue).