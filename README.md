# SWAPI Search Service

A scalable backend that ingests Star Wars data from the public [SWAPI](https://swapi.info/) API, normalizes it, and exposes it via a modern RESTful API.  
Built with **FastAPI**, **PostgreSQL**, and deployed **serverless on AWS**.

## Features

- **Automated ETL**  
  CLI script (`run_etl.py`) extracts, transforms, and loads SWAPI data into PostgreSQL.  
  Handles relationship normalization and resilient data fetching.

- **Unified Search**  
  `GET /api/v1/search` supports partial and case-insensitive text search across all resource types, with a **relevance ranking system**.  
  <img width="957" height="754" alt="image" src="https://github.com/user-attachments/assets/33fb5b96-2443-479b-935c-c1475ce4b0d8" />

- **Structured Browse API**  
  REST endpoints per resource type (e.g., `GET /api/v1/films`, `GET /api/v1/people`) with pagination.

- **Dynamic Filtering**  
  Server-side query parameters enable complex filters (e.g., `/api/v1/films?director=lucas&producer=kurtz`).  
  <img width="1894" height="888" alt="image" src="https://github.com/user-attachments/assets/f464f79e-ce47-4d0f-9655-224307ceb4ad" />  
  <img width="884" height="693" alt="image" src="https://github.com/user-attachments/assets/f12f911a-f22d-407e-935a-515f6ae7ae9d" />

- **Security & Stability**  
  Rate limiting via API Gateway.  
  All infrastructure isolated in a **private VPC** with secure **VPC Endpoints** for AWS services.  
  <img width="832" height="846" alt="image" src="https://github.com/user-attachments/assets/b07f3c35-21c8-40b2-b724-330f23697661" />

## Architecture

- **Clean Architecture**: API Layer → Repository Layer → Database Layer (SQLAlchemy ORM).  
- **AWS Lambda + API Gateway**: serverless, scalable, cost-optimized.  
- **AWS RDS (PostgreSQL)**: managed relational database.  
- **Amazon S3**: stores large deployment artifacts for Lambda.

---

### Tech Stack

- **Backend:** FastAPI, Python, SQLAlchemy  
- **Database:** PostgreSQL (AWS RDS)  
- **Infrastructure:** AWS Lambda, API Gateway, VPC, S3  
- **ETL:** Custom Python CLI script  
