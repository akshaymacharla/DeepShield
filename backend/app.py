from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from detector import analyze_audio
import asyncio
import os

app = FastAPI(title="DeepShield Detection API")

# Allow all origins for local development (and for frontend being on separate port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoints
@app.post("/v1/analyze")
async def analyze_endpoint(audio: UploadFile = File(...)):
    # Read bytes 
    file_bytes = await audio.read()
    
    # Simulate network/processing latency
    await asyncio.sleep(2.0)
    
    verdict, confidence = analyze_audio(audio.filename, file_bytes)
    
    return {
        "verdict": verdict,
        "confidence": confidence,
        "filename": audio.filename
    }

@app.get("/v1/models")
async def get_models():
    return [
        {"id": "resnet-spec-v2", "name": "ResNet Spectrogram Analyzer v2", "active": True},
        {"id": "wav2vec-micro", "name": "Wav2Vec Micro-timing", "active": True}
    ]

# Serve static files from frontend/dist (copied to backend/static)
# Mount the assets folder explicitly
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="assets")

# Root route serves index.html
@app.get("/")
async def root():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"status": "DeepShield API is running, but UI was not found."}

# Catch-all route to handle React Router client-side navigation
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    # Only serve index.html if it's not a v1 API request
    if full_path.startswith("v1/"):
        return {"error": "Not Found"}
    
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "Not Found"}

if __name__ == "__main__":
    import uvicorn
    # Use port 10000 for Render, or fallback to 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
