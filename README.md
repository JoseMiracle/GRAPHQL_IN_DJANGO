# Library Management System with GraphQL API

This project demonstrates how to set up a **GraphQL API** in a Django project, focusing on a **Library Management System**. It showcases key GraphQL concepts like **queries**, **mutations**, and **custom resolvers**, alongside the integration of **JWT-based authentication**.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [GraphQL API Endpoints](#graphql-api-endpoints)
- [Usage](#usage)
- [Testing](#testing)


## Features
- Manage user accounts with custom **Django User model**.
- GraphQL API with JWT authentication.
- Perform **CRUD** operations on library books.
- Manage book requests (create, approve, cancel).
- Track **library statistics** like most requested books and daily book requests.
  
## Requirements
- Python 3.6+
- Django 5.0+
- Graphene-Django
- Django GraphQL JWT

## Installation

1. Clone the repository:
   ```bash
   git clonehttps://github.com/JoseMiracle/GRAPHQL_IN_DJANGO.git
   cd GRAPHQL_IN_DJANGO
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Setup Django project:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the GraphQL Playground at `http://127.0.0.1:8000/graphql/`.

## Project Structure

```
GRAPHQL_IN_DJANGO/
│
├── accounts/           # User model and authentication
│   └── models.py       # Custom User model extending AbstractUser
├── books/              # Book and BookRequest models
│   └── models.py       # Models for Books and Book Requests
├── graphql_core/       # GraphQL schema and types
│   ├── schema.py       # Main GraphQL schema and mutations
│   ├── schema_types.py # Custom GraphQL types for models
│   └── utils/          # JWT and Mutation utilities
├── core/               # Django project settings
│   └── settings.py     # Project configuration
├── manage.py           # Django management script
└── requirements.txt    # Project dependencies
```

## GraphQL API Endpoints

### Queries

- `bookCountInTheLibrary`: Get the total count of books in the library.
- `bookRequestsToday`: Fetch the list of book requests made today.
- `bookWithMostRequestsToday`: Fetch the book with the most requests for the day.

### Mutations

- `createAccount`: Create a new user account.
- `signIn`: Authenticate a user and obtain JWT token.
- `addNewBook`: Add a new book to the library (admin/staff only).
- `deleteBook`: Delete a book from the library (admin/staff only).
- `bookRequest`: Request a book by a user.
- `cancelBookRequest`: Cancel a previously requested book.

### Authentication

JWT authentication is used to secure endpoints. After signing in, use the returned token for authorization by adding it to the request headers as:

```
Authorization: Bearer <your-token>
```

## Usage

1. **Create an Admin Account**:
   After setting up the project, create an admin account via the Django admin panel or GraphQL mutation:
   ```graphql
   mutation {
     createAccount(firstName: "Admin", lastName: "User", email: "admin@example.com", password: "admin123", username: "admin") {
       success
       message
       errors
     }
   }
   ```

2. **Sign In**:
   Use the `signIn` mutation to obtain a JWT token for subsequent authenticated requests:
   ```graphql
   mutation {
     signIn(email: "admin@example.com", password: "admin123") {
       success
       token
       refreshExpiresIn
     }
   }
   ```

3. **Add New Book (Admin/Staff)**:
   Once signed in, admins can add new books:
   ```graphql
   mutation {
     addNewBook(title: "GraphQL for Beginners", author: "John Doe", genre: "Technology", numberOfCopies: 10, isbn: "1234567890") {
       success
       message
       errors
     }
   }
   ```

## Testing

To test the GraphQL API, you can use:
- The GraphiQL interface at `/graphql/`.

Ensure JWT authentication is correctly configured for endpoints requiring authentication.

## Thank You for Your Support!
Thank you for taking the time to explore the project. Whether you're using, contributing, or simply sharing feedback, your involvement means a lot to me. Together, we can continue to improve and grow. Happy coding! 😊
