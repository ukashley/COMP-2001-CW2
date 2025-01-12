# COMP-2001-CW2
# Trail Service Microservice

## Overview
This microservice manages trails and supports the following features:
- Create, Read, Update, Delete (CRUD) operations on trails.
- Authentication via an external Authenticator API.
- Data storage in Azure Data Studio.

## Technologies Used
- Python (In VS Code)
- Flask
- Connexion (for Swagger/OpenAPI integration)
- SQLAlchemy
- Azure Data Studio
- Docker

## API Documentation
The API supports the following endpoints:
- `GET /api/trails`: Retrieve all trails.
- `POST /api/trails`: Create a new trail.
- `PUT /api/trails/{trail_id}`: Update an existing trail.
- `DELETE /api/trails/{trail_id}`: Delete a trail.

## Testing of the Microservice
I tested the microservice by:
1. Accessing Swagger UI at `http://127.0.0.1:8000/ui/#/`.
2. Testing API endpoints using Swagger.
