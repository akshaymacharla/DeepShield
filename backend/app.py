from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from detector import analyze_audio
import time
import asyncio

app = FastAPI(title="DeepShield Detection API")

# Allow all origins for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
