FROM python:3.11.2-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Update system and install base dependencies 
RUN apt-get update && apt-get -y install gcc \
  # Network utilities
  netcat curl \
  # Database dependencies
  postgresql \
  # Makefiles
  make \
  # Cleaning
  && apt-get clean

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements ./requirements
RUN pip install -r requirements/develop.txt

COPY ["./docker/develop/fastapi/entrypoint.sh", "/entrypoint.sh"]

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "8080"]
