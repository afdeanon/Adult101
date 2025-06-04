## Running the Backend Locally

You can run the backend using Docker or manually.

### Option 1: Using Docker

Use the `Dockerfile` found in the project root:

```bash
docker build -t my-backend .
docker run -p 8000:8000 my-backend
```


### Option 2: Running Manually

From the project root folder run these commands
```
cd backend
pip install -r requirements.txt
fastapi dev app/main.py
```

## Running the Frontend

From the project root folder run these commands

```
cd frontend
pip install -r requirements.txt
python3 main.py
```
