# The Loom

A real-time collaborative web IDE, enabling multiple users to work on the same project simultaneously.

## Overview

The Loom is a powerful, self-hosted platform designed for developers who need to collaborate in real time. It provides a shared workspace, or "room," where users can upload files, edit code together, and see each other's changes live. This is made possible by a robust backend built with FastAPI and WebSockets, which uses Conflict-free Replicated Data Types (CRDTs) to seamlessly merge concurrent edits without conflicts.

The project is architected to be scalable and maintainable, featuring a clean separation of concerns, dependency injection, and a full suite of modern development tools. It's an ideal solution for pair programming, team projects, and educational purposes.

## Core Features

*   **Real-Time Collaboration**: Utilizes WebSockets and the `y-py` library (a Python port of Y.js) for high-performance, real-time text synchronization between multiple users.
*   **Project Rooms**: Users can create isolated rooms, each with a unique, shareable ID. Each room acts as a container for a project's files.
*   **File Management**: Securely upload project files into a room. The application enforces limits on the number of files per room and the maximum size of each file.
*   **Project Snapshots**: Create a point-in-time backup of all files in a room, which are downloadable as a single `.zip` archive.
*   **User Authentication**: Secure JWT-based authentication system for user registration and login, ensuring that only authorized users can create and manage rooms.
*   **Automated Cleanup**: A background task runs periodically to clean up old and inactive rooms, freeing up server resources and keeping the environment tidy.
*   **Structured Logging & Error Handling**: Centralized logging and exception handling provide clear insights into the application's behavior and make debugging easier.

## Tech Stack

The Loom is built with a modern, asynchronous Python stack:

*   **Backend Framework**: **FastAPI** for building high-performance, asynchronous REST APIs.
*   **Real-Time Communication**: **WebSockets** for full-duplex communication between clients and the server.
*   **Database**: **PostgreSQL** as the primary relational database.
*   **ORM**: **SQLAlchemy 2.0** (async) for powerful and asynchronous database interactions.
*   **Database Migrations**: **Alembic** for managing database schema changes.
*   **In-Memory Data Store**: **Redis** is used to manage and persist CRDT document states and track room activity.
*   **Collaboration Protocol**: **y-py** for handling CRDTs, ensuring that concurrent edits are merged correctly and efficiently.
*   **Web Server**: **Uvicorn**, an ASGI server for running the FastAPI application.
*   **Authentication**: **python-jose** and **passlib** for JWT generation/validation and password hashing.
*   **Environment Configuration**: **pydantic-settings** for managing application settings through environment variables.

## Architecture Overview

The application follows a layered architecture to ensure a clean separation of concerns.

1.  **Entrypoint (`main.py`)**: Initializes the FastAPI application and the Uvicorn ASGI server.
2.  **Application Factory (`backend/app.py`)**: Creates and configures the main FastAPI app instance. This is where middleware (like CORS), routers, exception handlers, and lifespan events (like the cleanup scheduler) are registered.
3.  **Routing Layer (`backend/routes.py`, `backend/*/router.py`)**: Defines all the API and WebSocket endpoints. It delegates the business logic to the service layer.
4.  **Service Layer (`backend/*/service.py`)**: Contains all the business logic of the application. Services coordinate operations between repositories and other components. For example, `RoomService` handles the logic for creating rooms, uploading files, and checking user permissions.
5.  **Repository Layer (`backend/*/repositories/*.py`)**: Abstract an interface for data access. Repositories are responsible for all database operations (CRUD) for a specific model, interacting directly with the SQLAlchemy session.
6.  **Database & Models (`backend/*/models/*.py`)**: Defines the SQLAlchemy ORM models, which represent the database tables (`users`, `rooms`, `files`, etc.).
7.  **Real-Time Collaboration Core**:
    *   **`ConnectionManager`**: A singleton that manages all active WebSocket connections, organizing them by room and file. It handles connecting, disconnecting, and broadcasting messages.
    *   **WebSocket Endpoint**: The main entry point for real-time communication. It authenticates users, connects them to the manager, and relays CRDT updates to the `CollaborationService`.
    *   **`CollaborationService`**: Interacts with Redis to save and retrieve the binary state of shared documents (YDocs).

## Getting Started

Follow these instructions to set up and run the project locally for development.

### Prerequisites

*   Python 3.10+
*   PostgreSQL
*   Redis
*   An environment variable management tool (e.g., `python-dotenv`)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/The-Loom.git
cd The-Loom
```

### 2. Install Dependencies

It is highly recommended to use a virtual environment.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root directory. You can copy the example below and fill in your own values.

```env
# .env

# PostgreSQL Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=the_loom_db
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
DB_URL_SCHEME=postgresql+asyncpg

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# Security and JWT Configuration
SECRET_KEY=a_very_secret_and_long_random_string_for_jwt
HASH_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Background Task Configuration
CLEANUP_INTERVAL_SECONDS=3600 # 1 hour
ROOM_LIFETIME_DAYS=7
ROOM_INACTIVITY_HOURS=3
```

**Important**: Make sure your PostgreSQL server is running and you have created a database with the name specified in `DB_NAME`.

### 4. Run Database Migrations

Alembic is used to manage the database schema. To apply all migrations and create the necessary tables, run:

```bash
alembic upgrade head
```

### 5. Start the Application

You can now start the development server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`, with interactive documentation at `http://localhost:8000/docs`.

## API Endpoints

The application exposes both a RESTful API and a WebSocket endpoint for collaboration.

### REST API

A brief overview of the main endpoints. For full details, see the auto-generated OpenAPI docs at `/docs`.

*   **Authentication (`/api/auth`)**
    *   `POST /token`: Login to receive JWT access and refresh tokens.
*   **Users (`/api/users`)**
    *   `POST /`: Register a new user.
    *   `GET /me`: Get the profile of the currently authenticated user.
    *   `GET /me/rooms`: List all rooms the current user owns or participates in.
*   **Rooms (`/api/rooms`)**
    *   `POST /`: Create a new collaboration room.
    *   `GET /{room_id}`: Get detailed information about a specific room, including its file list.
    *   `POST /{room_id}/files`: Upload a file to a room.
    *   `POST /{room_id}/snapshots`: Create a zip archive snapshot of all files in the room.

### WebSocket Endpoint

*   `WS /ws/{room_id}/{file_id}?token={jwt_token}`
    *   This is the endpoint for real-time collaboration.
    *   A client connects to this endpoint to join a collaborative session for a specific file within a room.
    *   The `token` query parameter is required for authentication.
    *   Once connected, the server sends the initial document state, and clients can then send and receive binary CRDT updates to synchronize their changes.

## Project Structure

The project is organized into modules, with each module responsible for a specific domain.

```
.
├── backend/
│   ├── auth/         # Authentication logic and routes
│   ├── collaboration/  # WebSocket connection management and CRDT logic
│   ├── config/       # Application configuration (DB, Redis, Security)
│   ├── file/         # File-related models and DTOs
│   ├── libs/         # Shared base models and custom exceptions
│   ├── redis_client/ # Redis connection utility
│   ├── room/         # Room management logic, models, and routes
│   ├── security/     # JWT services, password hashing, and dependencies
│   ├── snapshot/     # Snapshot creation logic and models
│   ├── tasks/        # Background cleanup tasks
│   ├── user/         # User management logic, models, and routes
│   ├── app.py        # FastAPI application factory
│   ├── handlers.py   # Global exception handlers
│   ├── logging_setup.py # Logging configuration
│   └── routes.py     # Main API router aggregation
├── migrations/       # Alembic database migration scripts
├── storage/          # Default location for uploaded files and snapshots
├── main.py           # Application entry point
├── requirements.txt  # Project dependencies
└── README.md         # This file
```