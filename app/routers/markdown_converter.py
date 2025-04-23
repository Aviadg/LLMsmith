from fastapi import APIRouter, UploadFile, HTTPException
from markitdown import MarkItDown
import io

router = APIRouter()
md = MarkItDown(enable_plugins=True)

@router.post("/convert")
async def convert_to_markdown(
    file: UploadFile,
    include_llm_descriptions: bool = False
):
    try:
        # Read the uploaded file
        content = await file.read()
        
        # Create a file-like object
        file_obj = io.BytesIO(content)
        file_obj.name = file.filename
        
        # Convert to markdown
        result = md.convert(file_obj)
        
        return {
            "text": result.text_content,
            "metadata": result.metadata
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))