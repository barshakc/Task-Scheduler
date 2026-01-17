# Task Scheduler

## Overview

This is a task scheduler system designed for scheduling, executing, and monitoring tasks. It combines a FastAPI backend, Celery-based task queue, and a Streamlit dashboard for task monitoring, making it ideal for automated workflows and testing scheduled tasks such as email notifications.

## Features

* **REST API for Task Management**: Create, update, pause, resume, delete, and trigger tasks.
* **Task Scheduling**: Supports one-time, interval-based, and cron-like recurring tasks.
* **Celery Workers**: Asynchronous task execution with retries and status tracking.
* **Task Monitoring Dashboard**: Streamlit-based UI for viewing tasks and their runs.
* **Authentication**: JWT-based login and registration.
* **Email Execution Example**: Sends email notifications for scheduled tasks via SMTP (for testing purposes).
* **Dockerized Setup**: Easy deployment using Docker containers.

## Architecture

```
[Streamlit Dashboard] <--> [FastAPI API] <--> [Database: SQLAlchemy]
                                |
                                v
                           [Celery Beat] ---> [Celery Worker]
```

* FastAPI handles API requests and user authentication.
* Celery Beat polls the database and schedules tasks.
* Celery Worker executes tasks asynchronously.
* Streamlit dashboard communicates with the API to display task and run status.

## Installation

### Requirements

* Docker & Docker Compose
* Python 3.10+

### Steps

1. Clone the repository:

```bash
git clone https://github.com/yourusername/task-scheduler.git
```

2. Navigate to the project directory:

```bash
cd task-scheduler
```

3. Build and run containers using Docker Compose:

```bash
docker-compose up --build
```

4. Access services:

   * FastAPI API: `http://localhost:8000/docs`
   * Streamlit Dashboard: `http://localhost:8501`

## Dockerization

The project is fully dockerized with separate services for API, Celery workers, Celery Beat, and Streamlit dashboard.

* **Docker Compose** orchestrates all services.
* **Dockerfiles** for:

  * FastAPI API
  * Celery Worker
  * Streamlit Dashboard
* **Environment Variables**: Configure database URL, email credentials, and other settings in `.env` file.

### Docker Commands

* Build containers:

```bash
docker-compose build
```

* Start all services:

```bash
docker-compose up
```

* Stop all services:

```bash
docker-compose down
```

* Run a one-off command inside the API container:

```bash
docker-compose run api python manage.py migrate
```

## Deployment

For production deployment, follow these steps:

1. **Prepare Environment Variables**

   * Create a `.env.prod` file with production configurations, including:

     * `DATABASE_URL`
     * `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USER`, `EMAIL_PASSWORD`, `EMAIL_FROM`
     * `JWT_SECRET_KEY`

2. **Persistent Storage**

   * Map a volume for your database container to persist task and user data.

3. **Start Services in Detached Mode**

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

4. **Optional Reverse Proxy and SSL**

   * Use NGINX or Traefik to expose FastAPI and Streamlit over HTTPS.
   * Configure firewall rules to allow traffic on required ports.

5. **Monitoring & Logs**

   * Check logs for API and Celery services:

```bash
docker-compose logs -f api
```

```bash
docker-compose logs -f worker
```

* Ensure Celery Beat is scheduling tasks correctly and workers are processing them.

## Usage

1. **Register a user** via `/register` endpoint.
2. **Login** to obtain JWT token.
3. **Create tasks** with `schedule_type` (once, interval, cron) and optional payload (e.g., email details).
4. **Trigger tasks** manually via API or let Celery Beat schedule them automatically.
5. **Monitor tasks and runs** in the Streamlit dashboard.
6. **Task management**: pause, resume, update, or delete tasks using API endpoints.

## Example Task Payload (Email)

```json
{
  "recipient": "user@example.com",
  "subject": "Test Task",
  "message": "This is a test scheduled email."
}
```

## Testing

* Basic health checks for API endpoints, Celery workers, and task execution.
* Sample tasks can be scheduled and monitored through the dashboard.

## Contributing

Contributions are welcome! Steps:

1. Fork the repository.
2. Create a feature branch.
3. Make changes and commit.
4. Push the branch and open a pull request.

## License

MIT License. See LICENSE file for details.

*Efficiently schedule, monitor, and execute tasks with a full-stack Python scheduler.*
