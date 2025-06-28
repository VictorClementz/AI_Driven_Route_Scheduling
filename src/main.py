import uvicorn
from src.api.routes import app

if __name__ == "__main__":
    # Kör servern på port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)