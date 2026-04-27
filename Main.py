from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import h5py
import numpy as np
import time

app = FastAPI()

# Initialize the .h5 "Brain"
DB_PATH = "brain.h5"

def init_db():
    with h5py.File(DB_PATH, "a") as f:
        if "logs" not in f:
            # Create a table for timestamps and value data
            f.create_dataset("logs", (0, 2), maxshape=(None, 2))

@app.post("/log-data")
async def log_data(value: float):
    with h5py.File(DB_PATH, "a") as f:
        dset = f["logs"]
        dset.resize((dset.shape[0] + 1, 2))
        dset[-1] = [time.time(), value]
    return {"status": "stored_in_h5"}

# Simple HTML Interface for your Mobile
@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { background: #0f0f0f; color: #00f2ff; font-family: sans-serif; text-align: center; }
                .hex-btn { border: 2px solid #00f2ff; padding: 20px; background: none; color: #00f2ff; font-size: 20px; cursor: pointer; }
            </style>
        </head>
        <body>
            <h1>PYH5 NEURAL HUB</h1>
            <button class="hex-btn" onclick="sendData()">LOG PULSE</button>
            <script>
                async function sendData() {
                    const val = Math.random() * 100;
                    await fetch('/log-data?value=' + val, {method: 'POST'});
                    alert('Data Pushed to .h5 Storage');
                }
            </script>
        </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    init_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)
