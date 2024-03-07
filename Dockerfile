FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION 1.5.1

RUN apt-get update && apt-get install -y curl make

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python - --version ${POETRY_VERSION}

# Add Poetry's virtual environment to PATH variable
ENV PATH="${PATH}:/root/.local/bin"

# Create a working directory
WORKDIR /app

# Copy the project 'pyproject.toml' and 'poetry.lock' file into the container
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false \
  && poetry install

# Copy the project into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["make", "run"]
