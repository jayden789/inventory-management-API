
# Inventory Management API

A simple Django REST Framework project for managing inventory with JWT authentication for regular users and Basic Authentication for admin users. This API includes CRUD operations on inventory items, data validation, and error handling.

## Features

- User registration and authentication using JWT for regular users.
- CRUD operations for inventory items (admin only, using Basic Authentication).
- Data validation and error handling.
- Regular users can only list items and must be JWT authenticated.

## Installation

Follow these steps to set up the project on your local machine:

### Prerequisites

- Python 3.x
- pip

### Steps

1. **Clone the repository:**

   ```sh
   git clone <repository-url>
   cd inventory_management
   ```

2. **Create and activate a virtual environment:**

   On macOS/Linux:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

   On Windows:
   ```sh
   python -m venv venv
   ./venv/Scripts/activate
   ```

3. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Run migrations:**

   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (for accessing the admin interface and performing CRUD operations):**

   ```sh
   python manage.py createsuperuser
   ```

6. **Start the development server:**

   ```sh
   python manage.py runserver
   ```

## Usage

### Register a New User

1. **Create a new user:**

   ```sh
   curl -X POST http://localhost:8000/register/    -H "Content-Type: application/json"    -d '{
       "username": "your_username",
       "email": "your_email@example.com",
       "password": "your_password"
   }'
   ```

### Obtain JWT Token

1. **Get the JWT token using the user credentials:**

   ```sh
   curl -X POST http://localhost:8000/token/    -d "username=your_username&password=your_password"
   ```

   The response will include the access token and refresh token (Regular user need to include the `access` token in the request)

   ```json
   {
       "refresh": "your_refresh_token",
       "access": "your_access_token"
   }
   ```

### CRUD Operations (Admin Only, without JWT)

1. **Create an Item (Admin Only):**

   ```sh
   curl -X POST http://localhost:8000/items/    -u adminuser:your_admin_password    -H "Content-Type: application/json"    -d '{
       "name": "Item 1",
       "description": "Description of Item 1",
       "quantity": <some-positive-number>
   }'
   ```

2. **Read Items (Admin Only):**

   ```sh
   curl -X GET http://localhost:8000/items/    -u adminuser:your_admin_password
   ```

3. **Read a Specific Item (Admin Only):**

   ```sh
   curl -X GET http://localhost:8000/items/1/    -u adminuser:your_admin_password
   ```

4. **Update an Item (Admin Only):**

   ```sh
   curl -X PUT http://localhost:8000/items/1/    -u adminuser:your_admin_password    -H "Content-Type: application/json"    -d '{
       "name": "Updated Item1",
       "description": "Updated description of Item1",
       "quantity": <some-positive-number>
   }'
   ```

5. **Delete an Item (Admin Only):**

   ```sh
   curl -X DELETE http://localhost:8000/items/1/    -u adminuser:your_admin_password
   ```

### CRUD Operations for Regular Users

Regular users can only list items and must be JWT authenticated.

1. **Read Items:**

   ```sh
   curl -X GET http://localhost:8000/items/    -H "Authorization: Bearer your_access_token"
   ```

2. **Read a Specific Item:**

   ```sh
   curl -X GET http://localhost:8000/items/1/    -H "Authorization: Bearer your_access_token"
   ```

## Running Tests

To run the tests, use the following command:

```sh
python manage.py test
```
