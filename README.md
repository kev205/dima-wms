# My Monorepo

A monorepo containing the Vue.js MSWebclient and a Django MSSales microservice.

## Structure

- `mswebclient/`: Vue.js MSWebclient
- `mssales/`: Django MSSales

## Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed.
- A database (postgres or mysql). You will have to edit the .env.local for cli test or .env.docker for docker run

## Running the Applications

1. **Clone the repository** and navigate to the project root.

2. **Edit Configs** Change .env.local (or .env.docker) to fit your configuration

3. **Start all services** using Docker Compose:

    ```bash
    docker-compose up --build
    ```

    This will build and start the following services:
    - **mssales**: Django backend (served behind Nginx gateway)
    - **mswebclient**: Vue.js frontend
    - **gateway**: Nginx reverse proxy for backend API

3. **Access the applications:**
    - **Frontend (Vue.js)**: [http://localhost:3000](http://localhost:3000)
    - **Backend API (Django, proxied by Nginx)**: [http://localhost:8080/api](http://localhost:8080/api)

## Notes

- The backend (`mssales`) is served behind an Nginx gateway on port 8080.
- The frontend (`mswebclient`) is available on port 3000 and communicates with the backend via the gateway.
- Environment variables for the backend are set in `mssales/.env.docker`.
- The PostgreSQL database service is commented out in the provided `docker-compose.yml`. Uncomment and configure it as needed.

## Stopping the Applications

To stop all running services:

```bash
docker-compose down
```