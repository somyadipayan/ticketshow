This is a guide to help you set up and run the project. The project has a backend, frontend, and instances folder, each serving different purposes.

## Folder Structure

- **backend:** Contains all Python files, `requirements.txt`, YAML for API, database, and configuration files.
- **frontend:** Contains Vue templates and JavaScript files.

## Getting Started

Our project runs best on Linux. For Windows users, it's recommended to run it on WSL (Windows Subsystem for Linux).

### Running the Backend

1. Open a terminal and navigate to the backend directory:
`cd backend`

2. Start WSL (Windows Subsystem for Linux):
`wsl`

3. Install the required packages using `requirements.txt`:
`pip install -r requirements.txt`

4. Start the Flask app:
`python app.py`

5. Start the Redis server (for caching and Celery):
`redis-server`

6. Start Celery Beat (Task Scheduler):
`celery -A app.celery beat --max-interval 1 -l info`

7. Start Celery Worker:
`celery -A app.celery worker --loglevel=INFO`


### Running the Frontend

1. Open a terminal and navigate to the frontend directory:
`cd frontend`


2. Install the required Node.js modules:
`npm install`

3. Start the frontend server:
`npm run serve`

4. Access the frontend at `http://localhost:8080`.

Please note that the project assumes a Linux environment. For Windows users, running the project in WSL is recommended for better compatibility.

## Accessing the Frontend

After following the steps above, you can access the frontend of the application by opening your web browser and navigating to `http://localhost:8080`.

Feel free to explore and enjoy using the application!