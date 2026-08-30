"""
Entry point to run the SMRITHI FastAPI Backend server.
"""
import sys
import uvicorn
from pathlib import Path

# Add backend directory to sys.path
BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

if __name__ == "__main__":
    print("=========================================================")
    print("🚀 SMRITHI FastAPI Backend is LIVE")
    print("👉 Base URL:    http://127.0.0.1:8000")
    print("👉 Swagger UI:  http://127.0.0.1:8000/docs")
    print("👉 Health API:  http://127.0.0.1:8000/health")
    print("=========================================================")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
