# Database

## Technologies
- [PostgreSQL](https://www.postgresql.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

## How to run a new migration
1. Create a new migration file
```bash
$ alembic revision --autogenerate -m "migration name"
```
2. Run the migration
```bash
$ alembic upgrade head
```
