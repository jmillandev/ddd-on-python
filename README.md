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

## 👩‍🏫 Project explanation

### ⛱️ Bounded Contexts

A bounded context is a natural division within a business and provides an explicit boundary within which a domain model exists.

- [Finance Planner](src/planner): Here you'll find the use cases needed by a user in order to manage their finances.
- [Backoffice](src/backoffice): Here you'll find the use cases needed by the Customer Support department in order to manage users, suscriptions and so on.

### 📱 Applications

Applications define "How we'll deploy our domain"(CLI, Web, etc). They are the entry point of our system.

### 🎯 Hexagonal Architecture

This repository follows the Hexagonal Architecture pattern. Also, it's structured using `modules`. A module is an element that have sense inside a Bounded Context. We follow the rule 'One aggregate per module', so, we call `module` to the aggregate.

The current structure of a Bounded Context is:

```bash
$ tree -L 4 src

src
├── planner // Bounded Context
|          └── users // Module
|                 ├── application // Application Layer
|                 │   ├── command_handler.py // Response for handling the command, initialize valueObjects and call the use case. This is the entry point of the application layer, dont return anything
|                 │   ├── command.py // A DTO with the data needed by the use case
|                 │   ├── creator.py // The use case
|                 │   ├── finder.py // The use case
|                 │   ├── query_handler.py // Response for handling the query, initialize valueObjects and call the use case. This is the entry point of the application layer, return the response(only with pimitives) 
|                 │   ├── query.py // A DTO with the data needed by the use case
|                 │   └── responses.py // The response of the query
|                 ├── domain // Domain Layer
|                 │   ├── entity.py // The aggregate
|                 │   ├── exceptions // Exceptions of the domain layer
|                 │   ├── repository.py // The interface of the repository
|                 │   └── value_objects // Value Objects of the aggregate. Contains the business logic and the validation of the data
|                 ├── infrastructure // Infrastructure Layer - Contains the implementation of the interfaces defined in the domain layer
|                     └── repositories // Repositories implementations
|                     └── dependency_injection
└── shared // Shared Kernel - Contains the common infrastructure and domain shared between the different Bounded Contexts
```

## Extras

## Utils

- Run command inside of docker: `make dev <command>`

- Connect to Postgres on bash: `make psql`

- Create a new migration file: `make generate/migration message="migration name"`

- Run the migrations: `make migrate`

## External Links

### Architecture

- [Microservices on Azure](https://learn.microsoft.com/en-us/azure/architecture/microservices)

### Technologies

- [FastAPI](https://fastapi.tiangolo.com/)
- [Docker](https://www.docker.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Alembic(To handle SQL Migration)](https://alembic.sqlalchemy.org/en/latest/)
- [SQLAlchemy(ORM)](https://www.sqlalchemy.org/)
