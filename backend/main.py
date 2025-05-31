from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
import uuid
from typing import Optional

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/lib')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/scripts')))

from simple_vector_db import ArtVectorDB, find_similar_artworks, add_artwork, get_db_stats
import subprocess

app = FastAPI()

# Allow CORS for local dev and Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    style: int
    variation: str = 'mixed'
    seed: Optional[int] = None
    num_variations: int = 1

@app.post("/generate")
def generate_art(req: GenerateRequest):
    """
    Generate new art variation(s) using the existing script.
    Returns the file paths of generated images.
    """
    output_dir = os.path.abspath("generated_api")
    os.makedirs(output_dir, exist_ok=True)
    
    # Call the existing script
    cmd = [
        sys.executable, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/scripts/generate_variations.py')),
        '--style', str(req.style),
        '--variation', req.variation,
        '--output-dir', output_dir,
        '--num-variations', str(req.num_variations),
        '--no-db'  # DB can be handled here if needed
    ]
    if req.seed is not None:
        cmd += ['--seed', str(req.seed)]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        # Parse output for generated file paths
        output_lines = result.stdout.splitlines()
        image_paths = [line for line in output_lines if line.strip().endswith('.png')]
        return {"images": image_paths}
    except subprocess.CalledProcessError as e:
        return JSONResponse(status_code=500, content={"error": e.stderr or str(e)})

class SimilarRequest(BaseModel):
    image_path: Optional[str] = None
    art_id: Optional[str] = None
    n_results: int = 10

@app.post("/similar")
def similar_art(req: SimilarRequest):
    """
    Find similar artworks using the vector DB.
    """
    try:
        results = find_similar_artworks(
            query_path=req.image_path,
            query_id=req.art_id,
            n_results=req.n_results
        )
        return {"results": results}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/stats")
def db_stats():
    """
    Get database statistics.
    """
    try:
        stats = get_db_stats()
        return stats
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/health")
def health():
    return {"status": "ok"} 