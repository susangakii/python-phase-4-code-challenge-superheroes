# Superheroes API

A Flask API for tracking superheroes and their superpowers.

## Description

This API allows you to manage heroes, powers, and their relationships. Each hero can have multiple powers through the HeroPower join table.

## Setup Instructions

1. Clone the repository
2. Navigate to the project directory
3. Install dependencies:
```bash
   pipenv install
   pipenv shell
```

4. Navigate to the server directory:
```bash
   cd server
```

5. Initialize the database:
```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
```

6. Seed the database:
```bash
   python seed.py
```

7. Run the application:
```bash
   python app.py
```

The server will run on `http://localhost:5555`

## API Endpoints

- `GET /heroes` - Get all heroes
- `GET /heroes/:id` - Get a specific hero
- `GET /powers` - Get all powers
- `GET /powers/:id` - Get a specific power
- `PATCH /powers/:id` - Update a power's description
- `POST /hero_powers` - Create a new hero-power relationship

## Testing

Import the `challenge-2-superheroes.postman_collection.json` file into Postman to test all endpoints.

## Summary

Your project structure should now look like this:
```
superheroes-api/
├── server/
│   ├── app.py
│   ├── models.py
│   ├── seed.py
│   ├── instance/
│   │   └── app.db
│   └── migrations/
├── challenge-2-superheroes.postman_collection.json
├── Pipfile
├── Pipfile.lock
└── README.md
```

## Technologies Used

- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-RESTful
- Flask-Mail
- SQLAlchemy-Serializer

## License

MIT License

## Author

Susan Gakii