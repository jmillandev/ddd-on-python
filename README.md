<h1 align="center">
  🐍🎯 Hexagonal Architecture, DDD & CQRS in Python
</h1>


## 🙌 Environment Setup

### 🐳 Needed tools

1. [Install Docker](https://www.docker.com/get-started)

### 🛠️ Environment configuration

1. Create a local environment file (`cp .env.template .env`)
2. If you want, you could modify any parameter

### 🔥 Application execution

1. Install all the dependencies and bring up the project with Docker executing: `./init.sh up --build`

### ✅ Tests execution

1. Install the dependencies if you haven't done it previously: `./init.sh build`
2. Execute PHPUnit and Behat tests: `make test`

## Extras

## Utils

- Run command inside of docker: `make dev <command>`

- Connect to Postgres on bash: `make psql`

- Create a new migration file: `make generate/migration message="migration name"`

- Run the migrations: `make migrate`

## External Links

### Technologies

- [FastAPI](https://fastapi.tiangolo.com/)
- [Docker](https://www.docker.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Alembic(To handle SQL Migration)](https://alembic.sqlalchemy.org/en/latest/)
- [SQLAlchemy(ORM)](https://www.sqlalchemy.org/)
