"""FastAPI entry point for Target RP Finder."""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(title="Target RP Finder")

@app.get("/")
async def root():
    return {"message": "Target RP Finder API"}

@app.get("/health")
async def health():
    return {"status": "ok"}
