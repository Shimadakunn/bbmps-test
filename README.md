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
POST /tokens/batch
```

Example:

```bash
curl -X POST "https://bbmps-test.vercel.app/tokens/batch" \
     -H "Content-Type: application/json" \
     -d '[{"chain": "solana", "address": "FQgtfugBdpFN7PZ6NdPrZpVLDBrPGxXesi4gVu3vErhY"}]'
```

The request body should be a JSON array of objects with `chain` and `address` fields. Supported chains are "solana" and "ethereum".

## API Documentation

Visit `https://bbmps-test.vercel.app/docs` for interactive API documentation.
