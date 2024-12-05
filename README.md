
---

# Midnite README

This guide provides multiple ways to run, test, and interact with the project.

## Running the project

### Set up environment variables

Make a copy of `.env.example` and name it `.env`. This already has the variables needed for running the application.

### 1. Using Docker

Run the application using the following command:

```bash
make run-me
```

This will set up the application and create a test user with ID `1` for testing API calls.

You can then send API requests using your preferred method. For example:

> **Note**: No transactions are inserted by default. To check functionality, please see the test section where transactions are dynamically created and destroyed to test the requirements of the
exercise
#### Using cURL
```bash
curl --location 'http://localhost:8000/event' \
--header 'Content-Type: application/json' \
--data '{
    "type": "withdraw",
    "amount": "155.00",
    "user_id": 1,
    "t": 10
}'
```

#### Using Postman
- **URL**: `http://localhost:8000/event`
- **Payload**:
```json
{
    "type": "withdraw",
    "amount": "155.00",
    "user_id": 1,
    "t": 10
}
```

---

### 2. Running Manually

If the Docker setup fails or is not preferred, you can run the application manually:

#### Prerequisites
1. Install [Poetry](https://python-poetry.org/docs/#installing-with-pipx).
2. Set up the virtual environment & activate:
   ```bash
   poetry env use 3.11.5 #or your python version
   ```
   ```bash
   poetry shell
   ```
3. Set up the database container:
   ```bash
   docker-compose up -d db
   ```
4. Perform a database migration:
   ```bash
   alembic upgrade head
   ```
5. Install dependencies
   ```bash
   poetry update
   ```
6. Insert a test user:
   ```bash
   poetry run python tests/populate.py
   ```

#### Running the Application
1. Install the required dependencies:
   ```bash
   poetry update
   ```
2. Start the application:
   ```bash
   poetry run python main.py
   ```

---

## Running Tests

### Overview
The application includes 6 tests:
- These cover the 4 main cases specified in the test specification file.
- Additional edge cases, such as scenarios with no errors or multiple errors, are also tested.

### Running Tests with Make
Run the tests using the following command:
```bash
make run-tests
```
> **Note**: This command will rebuild the containers, causing the database and volumes to be destroyed and recreated.
---

### Running Tests Manually

#### Prerequisites
- Ensure the database container is running:
  ```bash
  docker-compose up -d db
  ```
- Insert a test user:
  ```bash
  poetry run python tests/populate.py
  ```

#### Run Tests
Execute the tests using:
```bash
poetry run pytest
```

---
