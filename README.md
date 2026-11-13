# TaskAPI

A simple REST API for managing personal tasks.  
**One Day · One Build — Day 02** (November 12, 2026)

Built to learn how APIs work by creating a complete, functional example.

## What it does

- Create tasks
- List all tasks
- Get a single task
- Update a task
- Delete a task

Data is stored in a local SQLite database (`tasks.db`).

## Tech

- Python
- FastAPI
- SQLite
- Uvicorn

## Setup

```bash
# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn main:app --reload --port 8001
```

- API: http://127.0.0.1:8001
- Interactive docs: http://127.0.0.1:8001/docs

## Run the client (optional)

While the API is running, open another terminal and run:

```bash
python client.py
```

## Endpoints

| Method | Endpoint       | Description          |
|--------|----------------|----------------------|
| GET    | /              | Welcome message      |
| POST   | /tasks         | Create a task        |
| GET    | /tasks         | List all tasks       |
| GET    | /tasks/{id}    | Get one task         |
| PUT    | /tasks/{id}    | Update a task        |
| DELETE | /tasks/{id}    | Delete a task        |

## Project structure

```
TaskAPI/
├── main.py           # The API
├── client.py         # Example client
├── requirements.txt
├── README.md
└── tasks.db          # Created automatically
```

## GitHub

https://github.com/atomsk717/TaskAPI
