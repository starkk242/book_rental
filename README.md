# Book Rental Project

This is a Django-based book rental application configured to run with Docker and PostgreSQL.

1. **User Registration**: 
   - Users can sign up to use the library system. 
   - After signing up, they can access the library services.
   - Defaulted the Registration to be Admin User Registration, we can have User or Staff Registration

2. **User Login**:
   - Registered users can log in to the system using their credentials.
   - Upon logging in, users can view the current status of their rented books, including details such as due dates and book titles.

3. **Homepage Redirect**: 
   - When users visit the homepage, they are directed to a page where they can see what books they have rented from the library.

4. **Admin Functions**: 
   - Admins, or library staff, have special privileges:
     - They can start a new rental for a user, assigning them a book from the library's collection.
     - They can extend the rental period for a book if needed.
     - They have access to view all rentals across all users, which helps them manage the library's inventory effectively.

5. **User Selection in Start Rental**:
   - When starting a new rental, the system presents a dropdown menu containing existing users.
   - Additionally, there's a button available next to the dropdown, allowing staff to directly add new users to the system if needed.

6. **Book Title Input in Start Rental**:
   - As staff members type in the title of the book they want to assign for rental, the system provides a dropdown menu with up to 5 matching book options available in the library's collection.
   - This feature helps staff quickly find and select the correct book for the rental process, improving efficiency and accuracy.

7. **Rental Reporting**: 
   - For library administrators, there's a feature to generate reports. These reports provide valuable insights into the library's operations:
     - How many times each book has been rented.
     - How many books each user has rented.
     - The average duration of book rentals.
     - The most popular books in the library.

8. **User Addition**: 
   - There's also a feature to add new users to the system. This allows the library to expand its user base and serve more people.


## Prerequisites

- Docker
- Docker Compose

## Project Setup

Follow these steps to set up and run the project:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/book_rental_project.git
cd book_rental_project
```

### 2. Create a `.env` File

Copy the provided `.env.example` file to `.env` and update the environment variables as needed:

```bash
cp .env.example .env
```

Edit the `.env` file to set your environment variables:

```env
POSTGRES_DB=book_rental_db
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

Replace `your_db_user` and `your_db_password` with your desired PostgreSQL username and password.

### 3. Build and Run the Docker Containers

Build and start the Docker containers using Docker Compose:

```bash
docker-compose build
docker-compose up
```

This will start the PostgreSQL database and run your Django application.

### 4. Apply Migrations

In a new terminal window, apply the migrations to set up the database schema:

```bash
docker-compose exec web python manage.py migrate
```

### 5. Create a Superuser

Create a superuser to access the Django admin interface:

```bash
docker-compose exec web python manage.py createsuperuser
```

Follow the prompts to create the superuser account.

### 6. Access the Application

The application should now be running at `http://localhost:8000`. You can access the Django admin interface at `http://localhost:8000/admin`.

## Project Structure

Here's an overview of the project structure:

```
book_rental_project/
├── book_rental_project/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── rentals/
│   ├── __pycache__/
│   ├── migrations/
│   ├── templates/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── static/
│   └── styles.css
├── .env
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── manage.py
└── requirements.txt
```

## Additional Commands

### Stop the Containers

To stop the running containers, use:

```bash
docker-compose down
```

### Rebuild the Containers

If you make changes to the `Dockerfile` or `docker-compose.yml`, you may need to rebuild the containers:

```bash
docker-compose build
docker-compose up
```

### Run Tests

To run tests for the Django application, use:

```bash
docker-compose exec web python manage.py test
```
