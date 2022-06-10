import uvicorn
from fastapi import FastAPI

from api import authentication_api, community_api

app = FastAPI(title="Fidelity hackathon")

app.include_router(authentication_api.router)
app.include_router(community_api.router)

@app.get("/health-check")
def health_check():
    return "OK"

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", log_level="debug", reload=True)