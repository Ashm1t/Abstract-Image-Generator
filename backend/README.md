# FastAPI Backend for Abstract Art Generator

This backend provides API endpoints for generating abstract art and performing similarity search using FastAPI.

## Endpoints

- `POST /generate` — Generate new art variations
- `POST /similar` — Find similar artworks
- `GET /stats` — Get database statistics
- `GET /health` — Health check

## Setup

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run the server locally:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Deploy:**
   - You can deploy this backend to [Railway](https://railway.app/), [Render](https://render.com/), or any cloud VM (AWS, DigitalOcean, etc.).
   - Make sure to set up persistent storage for the vector database files if needed.

## Notes
- This backend calls your existing scripts and uses your FAISS-based vector DB.
- For production, you may want to move the generation logic directly into FastAPI endpoints for better performance.
- Make sure your `src/` directory is available to the backend (or copy necessary files). 