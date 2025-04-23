from fastapi import APIRouter, UploadFile, HTTPException
from openai import OpenAI
import os

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile,
    model: str = "gpt-4o-transcribe",
    response_format: str = "text"
):
    try:
        # Read the uploaded file
        content = await file.read()
        
        # Create a transcription
        transcription = client.audio.transcriptions.create(
            file=content,
            model=model,
            response_format=response_format
        )
        
        return {"text": transcription.text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/translate")
async def translate_audio(
    file: UploadFile,
    model: str = "whisper-1"
):
    try:
        # Read the uploaded file
        content = await file.read()
        
        # Create a translation
        translation = client.audio.translations.create(
            file=content,
            model=model
        )
        
        return {"text": translation.text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))