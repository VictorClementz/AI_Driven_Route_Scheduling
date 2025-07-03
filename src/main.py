import uvicorn
from src.api.routes import app
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    # Kör servern på port 8001
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)