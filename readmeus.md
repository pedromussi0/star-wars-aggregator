# SWAPI Search Service Project Documentation

This document describes the architecture, functionalities, and strategic decisions behind the SWAPI Search Service, a robust and scalable backend for ingesting and querying data from the Star Wars universe.

## Project Overview

The system was designed to integrate with the SWAPI public API. It extracts, normalizes, and stores all resource data (films, characters, planets, etc.) in a PostgreSQL database. Subsequently, it exposes this data through a modern RESTful API, enabling complex searches and structured navigation.

The project was built with a focus on clarity, modularity, scalability, and clean code principles, culminating in a serverless deployment on AWS.

## Implemented Features

The backend offers a set of functionalities for API consumers (such as a React frontend):

### Automated Data Ingestion (ETL)

A command-line script (`run_etl.py`) orchestrates a complete Extract, Transform, and Load (ETL) process. It resiliently fetches all data from SWAPI, normalizes the information (resolving relationship links to readable names), and loads them into a centralized PostgreSQL database.

### Unified Search with Relevance

A single endpoint `GET /api/v1/search` enables textual searches (case-insensitive and partial) across all resource types simultaneously.

**Search API Execution in Postman:**
<img width="957" height="754" alt="image" src="https://github.com/user-attachments/assets/33fb5b96-2443-479b-935c-c1475ce4b0d8" />

**Architectural Decision:** The search implements a relevance ranking system, prioritizing results where the search term matches the resource's name or title. This ensures a more intuitive user experience.

### Structured Navigation (Browse API)

To complement the search, dedicated RESTful endpoints were created for each resource type (e.g., `GET /api/v1/films`, `GET /api/v1/people`). These endpoints allow the frontend to navigate through specific categories in a paginated manner.

### Dynamic and Detailed Filtering

**Architectural Decision:** To provide a rich exploration experience, the navigation endpoints support dynamic server-side filtering. Multiple filters can be combined through query parameters (e.g., `/api/v1/films?director=lucas&producer=kurtz`). This allows the frontend to build complex filter interfaces without needing to fetch and filter large volumes of data on the client side.

<img width="1894" height="888" alt="image" src="https://github.com/user-attachments/assets/f464f79e-ce47-4d0f-9655-224307ceb4ad" />

**API Usage with filters in Postman:**
<img width="884" height="693" alt="image" src="https://github.com/user-attachments/assets/f12f911a-f22d-407e-935a-515f6ae7ae9d" />

### Security and Traffic Control

**Architectural Decision:** The API implements rate limiting at the edge layer (API Gateway). This protects the system against abuse, controls costs, and ensures service stability.

## Architecture and Technology Decisions

The architecture was designed to be scalable and easily maintainable, reflecting modern software engineering practices.

### Clean Architecture

The backend follows a clear separation of responsibilities in layers:

- **API Layer (`api/`):** Defines endpoints, schemas (data contracts), and handles HTTP requests.
- **Repository Layer (`repositories/`):** Abstracts all data access. Endpoints don't know how data is fetched; they simply request it from the repository, making the system testable and allowing for future changes in data sources (e.g., adding a cache).
- **Database Layer (`db/`):** Manages database connection and defines ORM models (SQLAlchemy).

### Serverless Deployment on AWS

**Architectural Decision:** The application is deployed in a serverless environment for maximum scalability and cost optimization.

- **AWS Lambda:** Runs the FastAPI application code without the need to manage servers. The deployment package, containing the code and all dependencies, is created in an automated and consistent manner using a multi-stage Dockerfile.

- **API Gateway:** Acts as the API's "entry point," managing routing, security, and rate limiting.

- **AWS RDS (PostgreSQL):** Provides a managed, secure, and scalable relational database.

#### Amazon S3 for Artifacts

**Architectural Decision:** AWS Lambda has a size limit for code packages uploaded directly. To accommodate complex applications with many dependencies, the industry standard deployment method is to use an S3 bucket as an intermediary. Our automated deployment pipeline uploads the application's .zip package to a private S3 bucket and then instructs Lambda to fetch the code from that location. This increases the size limit and optimizes deployment speed.

#### AWS VPC and VPC Endpoints

**Architectural Decision:** Security is a central pillar. The network infrastructure was designed to keep the database and Lambda in a private network (VPC), isolated from the public internet. To allow Lambda to access other AWS services (such as Secrets Manager to fetch database credentials), VPC Endpoints were configured. They create a private and secure communication tunnel between Lambda and AWS services, ensuring that no sensitive data travels over the internet.

<img width="832" height="846" alt="image" src="https://github.com/user-attachments/assets/b07f3c35-21c8-40b2-b724-330f23697661" />
