from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.lawyer import router as lawyer_router

app = FastAPI(
    title="LegalMind API",
    description="AI-powered legal ecosystem — Lawyer Mode Backend",
    version="1.0.0"
)

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(lawyer_router)


@app.get("/", tags=["Health"])
async def root():
    return {"message": "LegalMind Lawyer Mode API is running! 🚀"}
