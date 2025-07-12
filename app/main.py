from app.routes import auth
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Only for development!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register router
app.include_router(auth.router, prefix="/auth")

@app.get("/")
def read_root():
    return {"status": "Algo Trading Backend Ready"}
