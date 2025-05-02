# Token Pool API

A FastAPI-based REST API for retrieving token pool information.

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the server:

```bash
python api.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Get Single Token Pool Info

```
GET /token/{chain}/{token_address}
```

Example:

```
GET /token/solana/FQgtfugBdpFN7PZ6NdPrZpVLDBrPGxXesi4gVu3vErhY
```

### Get Multiple Token Pool Info

```
POST /tokens/batch?chain=solana
Body: ["token_address1", "token_address2"]
```

Example:

```bash
curl -X POST "http://localhost:8000/tokens/batch?chain=solana" \
     -H "Content-Type: application/json" \
     -d '["FQgtfugBdpFN7PZ6NdPrZpVLDBrPGxXesi4gVu3vErhY"]'
```

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.
