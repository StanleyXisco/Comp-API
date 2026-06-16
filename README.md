# 🚀 Xisco API

A production-ready RESTful API built with **FastAPI** and **PostgreSQL**, showcasing real-world backend engineering practices including user authentication, resource management, and an engagement/voting system.

Built demonstrating hands-on experience with REST API design, database modelling, migrations, and cloud deployment — reflecting the type of backend systems designed and delivered during client engagements.

🔗 **Live API:** [https://xisco-api-b58807d67a65.herokuapp.com](https://xisco-api-b58807d67a65.herokuapp.com)  
📄 **API Docs (Swagger UI):** [https://xisco-api-b58807d67a65.herokuapp.com/docs](https://xisco-api-b58807d67a65.herokuapp.com/docs)

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Database Migrations](#database-migrations)
- [Deployment](#deployment)

---

## ✨ Features

- 🔐 **JWT Authentication** — Secure login with OAuth2 password flow
- 📝 **Post Management** — Create, read, update, and delete posts
- 👤 **User Management** — Register and retrieve user profiles
- 👍 **Voting System** — Upvote/downvote posts with a dedicated vote endpoint
- 🔍 **Search & Pagination** — Filter posts by title with `limit`, `skip`, and `search` query params
- 🛡️ **Password Hashing** — Secure password storage using `pwdlib`
- 🌐 **CORS Enabled** — Open CORS policy for flexible frontend integration
- 📦 **Pydantic v2 Schemas** — Strong request/response validation
- 🗄️ **Alembic Migrations** — Version-controlled database schema management
- 📊 **Vote Count Aggregation** — Posts returned with their total vote count

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI 0.128.0 |
| ORM | SQLAlchemy 2.0 |
| Database | PostgreSQL (via psycopg2) |
| Migrations | Alembic |
| Auth | JWT (PyJWT) + OAuth2 |
| Validation | Pydantic v2 |
| Server | Uvicorn |
| Deployment | Heroku |

---

## 📁 Project Structure

```
Comp-API/
├── app/
│   ├── main.py          # App entry point, middleware, router registration
│   ├── models.py        # SQLAlchemy ORM models (Post, User, Vote)
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── database.py      # Database connection & session setup
│   ├── config.py        # Environment variable configuration
│   ├── utils.py         # Password hashing & verification helpers
│   └── routers/
│       ├── post.py      # Post CRUD endpoints
│       ├── user.py      # User registration & retrieval
│       ├── auth.py      # Login & token generation
│       ├── vote.py      # Voting endpoint
│       └── Oauth2.py    # JWT token creation & validation
├── dbmigration/         # Alembic migration scripts
├── alembic.ini          # Alembic configuration
├── requirements.txt     # Python dependencies
├── Procfile             # Heroku process definition
└── .gitignore
```

---

## 🗃️ Database Models

### `Post`
| Column | Type | Description |
|---|---|---|
| `id` | Integer (PK) | Auto-generated post ID |
| `title` | String | Post title |
| `content` | String | Post body content |
| `published` | Boolean | Visibility flag (default: `true`) |
| `created_at` | Timestamp | Auto-set creation time |
| `owner_id` | FK → users.id | Author of the post |

### `User`
| Column | Type | Description |
|---|---|---|
| `id` | Integer (PK) | Auto-generated user ID |
| `email` | String (unique) | User email address |
| `password` | String | Hashed password |
| `created_at` | Timestamp | Auto-set creation time |

### `Vote`
| Column | Type | Description |
|---|---|---|
| `user_id` | FK → users.id (PK) | Voter |
| `post_id` | FK → posts.id (PK) | Post being voted on |

---

## 📡 API Endpoints

### 🔑 Authentication
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/login` | Login and receive JWT token | ❌ |

### 👤 Users
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/users/` | Register a new user | ❌ |
| `GET` | `/users/{id}` | Get user by ID | ❌ |

### 📝 Posts
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/posts/` | Get all posts (with votes, pagination, search) | ✅ |
| `POST` | `/posts/` | Create a new post | ✅ |
| `GET` | `/posts/{id}` | Get a single post by ID | ✅ |
| `PUT` | `/posts/{id}` | Update a post | ✅ |
| `DELETE` | `/posts/{id}` | Delete a post | ✅ |

### 👍 Votes
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/vote/` | Vote on a post (`dir: 1` = upvote, `dir: 0` = remove vote) | ✅ |

#### Query Parameters for `GET /posts/`
| Param | Type | Default | Description |
|---|---|---|---|
| `limit` | int | `10` | Max number of posts to return |
| `skip` | int | `0` | Number of posts to skip (offset) |
| `search` | string | `""` | Filter posts by title keyword |

---

## 🔐 Authentication

This API uses **OAuth2 with JWT Bearer tokens**.

1. Register via `POST /users/`
2. Login via `POST /login` with your `email` (as `username`) and `password`
3. Copy the returned `access_token`
4. Include it in the `Authorization` header for protected routes:

```
Authorization: Bearer <your_token>
```

> You can also use the **Authorize** button in the [Swagger UI](https://xisco-api-b58807d67a65.herokuapp.com/docs) to authenticate directly.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL database
- `pip`

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/StanleyXisco/Comp-API.git
cd Comp-API

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables (see below)
cp .env.example .env

# 5. Run database migrations
alembic upgrade head

# 6. Start the development server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`  
Swagger docs at `http://localhost:8000/docs`

---

## 🔧 Environment Variables

Create a `.env` file in the root directory with the following:

```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_password
DATABASE_NAME=your_db_name
DATABASE_USERNAME=your_db_user
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🗄️ Database Migrations

This project uses **Alembic** for database migrations.

```bash
# Create a new migration
alembic revision --autogenerate -m "your migration message"

# Apply migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1
```

---

## ☁️ Deployment

This API is deployed on **Heroku** using the `Procfile`:

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

To deploy your own instance:

```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:mini
heroku config:set SECRET_KEY=your_secret ALGORITHM=HS256 ACCESS_TOKEN_EXPIRE_MINUTES=30
git push heroku main
heroku run alembic upgrade head
```

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

> Built by [StanleyXisco](https://github.com/StanleyXisco) 🛠️
