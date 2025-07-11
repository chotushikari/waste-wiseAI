# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router

app = FastAPI(
    title="WasteWise AI – Inventory Intelligence API",
    version="1.0.0",
    description="FastAPI backend for smart retail inventory management powered by AI."
)

# Allow frontend (Streamlit) to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:8501"] for Streamlit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routes
app.include_router(api_router)

# Health check root
@app.get("/")
def read_root():
    return {"status": "✅ WasteWise AI is running!"}
