FROM python:3.11.2-slim-buster

ARG USERNAME=developer
ARG USER_UID=1000
ARG USER_GID=$USER_UID

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="${PATH}:/home/$USERNAME/.local/bin"

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
  && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
  # Update system and install base dependencies 
  && apt-get update && apt-get -y install gcc \
  # Network utilities
  netcat curl \
  # Database dependencies
  postgresql \
  # Makefiles
  make \
  # Superuser
  sudo \
  # Cleaning
  && apt-get clean \
  # Add sudo support
  && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
  && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements ./requirements
RUN pip install -r requirements/develop.txt

COPY ["./docker/planner/develop/fastapi/entrypoint.sh", "/entrypoint.sh"]

ENTRYPOINT ["/entrypoint.sh"]
CMD ["make", "up"]
