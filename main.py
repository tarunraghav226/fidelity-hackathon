import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Fidelity hackathon")

@app.get("/health-check")
def health_check():
    return "OK"

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", log_level="debug", reload=True)