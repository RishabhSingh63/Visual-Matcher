# Visual Product Matcher (React + Flask) - Demo Project

This is a simplified scaffold for the "Visual Product Matcher" assignment.

## What it contains
- `backend/` - Flask app with a small product dataset (50 generated product images) and a `/api/search` endpoint.
- `frontend/` - React app (plain create-react-app structure) which allows uploading an image and viewing similar products.
- `README.md` - This file
- `approach.txt` - 200-word approach summary.

## How similarity works in this demo
For this offline demo, similarity is computed by comparing the average RGB color of the query image with stored product images. This is NOT production-grade image similarity but provides a working pipeline you can extend (use embeddings, CLIP, or other ML models).

## Run locally (suggested)
1. Backend:
   - `cd backend`
   - Create a virtualenv and install: `pip install -r requirements.txt`
   - Run: `python app.py`
2. Frontend:
   - `cd frontend`
   - `npm install`
   - `npm start`
3. The frontend expects the backend at the same host (`/api/search`). For development, you may run frontend on a different port and configure proxy in `package.json` or use CORS.

## Notes
- URL-based image search is disabled in this offline package.
- Product images are stored in `backend/products/`.