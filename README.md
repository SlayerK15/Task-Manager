# Simple Task Manager

A minimalist Task Manager application built with Flask and MongoDB, containerized using Docker.

## Features
- Add new tasks
- View all tasks
- Simple and clean interface

## Tech Stack
- Python
- Flask
- MongoDB
- Docker

## Quick Start
```bash
# Clone repository
git clone https://github.com/yourusername/Task-Manager.git
cd Task-Manager

# Run with Docker Compose
docker-compose up -d

# Or run directly with Python
python app.py
```

## Structure
```
Task-Manager/
├──templates
│       └──index.html
├── requirements.txt
├── app.py
├── Dockerfile
└── docker-compose.yml
```

## Docker Configuration

### Dockerfile
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "0.0.0.0:5000:5000"
    environment:
      - FLASK_APP=app.py
      - FLASK_ENV=development
      - MONGO_URI=mongodb://mongodb:27017/taskmanager
    volumes:
      - .:/app
    depends_on:
      - mongodb
    networks:
      - app-network
    restart: unless-stopped

  mongodb:
    image: mongo:latest
    ports:
      - "127.0.0.1:27017:27017"
    volumes:
      - mongodb_data:/data/db
    networks:
      - app-network
    restart: unless-stopped

networks:
  app-network:
    driver: bridge

volumes:
  mongodb_data:
```

## Requirements
```
blinker==1.9.0
click==8.1.7
colorama==0.4.6
dnspython==2.7.0
Flask==3.0.3
Flask-PyMongo==2.3.0
itsdangerous==2.2.0
Jinja2==3.1.4
MarkupSafe==3.0.2
pymongo==4.10.1
python-dotenv==1.0.1
Werkzeug==3.1.3
```

## Usage
1. Access the application at http://localhost:5000
2. Add new tasks using the input field
3. Tasks are automatically displayed in the list

## Port Configuration
- Web Application: 5000 (Flask default port)
- MongoDB: 27017

##Update
1.Added the Jenkisfile

