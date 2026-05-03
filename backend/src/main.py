from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from src.api.routes import router

app = FastAPI(
    title="Bob Dylan AI",
    description="Felsefi metinler ve kapı görselleri üreten yapay zeka servisi.",
    version="1.0.0"
)

# CORS ayarları (React frontend'e izin vermek için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Geliştirme aşamasında her şeye izin veriyoruz
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temp klasörünü dışa aç (eğer yoksa oluştur)
os.makedirs("temp", exist_ok=True)
app.mount("/temp", StaticFiles(directory="temp"), name="temp")

app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Bob Dylan AI API is running. Check /docs for endpoints."}
