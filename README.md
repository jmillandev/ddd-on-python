# Database

## Technologies
- [PostgreSQL](https://www.postgresql.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

## How to run a new migration
1. Create a new migration file
```bash
alembic revision --autogenerate -m "migration name"
```
2. Run the migration
```bash
alembic upgrade head
```

# Dev Notes

## Asyncio and SQLAlchemy

https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
https://testdriven.io/blog/fastapi-sqlmodel/
https://lewoudar.medium.com/anyio-all-you-need-for-async-programming-stuff-4cd084d0f6bd

## Databases
https://sqlmodel.tiangolo.com/
