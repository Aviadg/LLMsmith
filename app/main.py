from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yaml
import os

from .routers import speech_to_text, markdown_converter, url_to_markdown
from .core.config import Settings

# Load configuration
def load_config():
    config_path = os.getenv("CONFIG_PATH", "config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

config = load_config()
settings = Settings(**config)

app = FastAPI(
    title="LLM Swiss Army Knife",
    description="A toolkit for working with LLMs",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers based on configuration
if config["services"]["speech_to_text"]:
    app.include_router(
        speech_to_text.router,
        prefix="/speech-to-text",
        tags=["Speech to Text"]
    )

if config["services"]["markdown_converter"]:
    app.include_router(
        markdown_converter.router,
        prefix="/markdown",
        tags=["Markdown Converter"]
    )

if config["services"]["url_to_markdown"]:
    app.include_router(
        url_to_markdown.router,
        prefix="/url-to-markdown",
        tags=["URL to Markdown"]
    )

@app.get("/")
async def root():
    return {
        "message": "LLM Swiss Army Knife API",
        "docs_url": "/docs",
        "active_services": [
            service for service, enabled in config["services"].items() 
            if enabled
        ]
    }