# One-Doctor-Service

A backend API for securely storing and retrieving health data using Firebase Firestore.

---

## Features

- REST API for health data (POST and GET)
- API key authentication
- Firebase Firestore integration
- CORS enabled

---

## Prerequisites

- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/)
- [Firebase Service Account Key JSON](https://firebase.google.com/docs/admin/setup)
- [Node.js and npm](https://nodejs.org/) (for frontend or Tailwind CSS, if needed)

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sns-consultancy/one-doctor-service
   cd one-doctor-service
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate   # On Windows
   # Or
   source venv/bin/activate  # On Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your Firebase service account key**
   - Place your Firebase service account JSON file in the project directory (e.g., `serviceAccountKey.json`).

5. **Set up environment variables**
   - Create a `.env` file in the project root:
     ```
     HEALTH_API_KEY=your-secret-api-key
     FIRESTORE_SERVICE_ACCOUNT=serviceAccountKey.json
     ```

---

## Running the Application

```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000/`.

---

## API Endpoints

### POST `/api/health`

Store health data for a user.

- **Headers:** `x-api-key: your-secret-api-key`
- **Body (JSON):**
  ```json
  {
    "user_id": "user123",
    "heartbeat": 72,
    "temperature": 98.6,
    "blood_pressure": "120/80",
    "oxygen_level": 98,
    "last_updated": "2024-05-15T12:00:00Z"
  }
  ```

### GET `/api/health/<user_id>`

Retrieve health data for a user.

- **Headers:** `x-api-key: your-secret-api-key`

---

## Testing

You can use [Postman](https://www.postman.com/) or `curl` to test the API.

**Example:**

```bash
curl -X POST http://127.0.0.1:5000/api/health \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-secret-api-key" \
  -d '{"user_id":"user123","heartbeat":72,"temperature":98.6,"blood_pressure":"120/80","oxygen_level":98,"last_updated":"2024-05-15T12:00:00Z"}'
```

---

## Notes

- Make sure your Firebase project is set up and Firestore is enabled.
- Never commit your `.env` or service account key to public repositories.

---

## License
sns-consultancy
