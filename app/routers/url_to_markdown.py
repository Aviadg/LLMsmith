from fastapi import APIRouter, HTTPException
import httpx
from typing import Optional

router = APIRouter()

@router.get("/convert")
async def convert_url_to_markdown(
    url: str,
    title: Optional[bool] = None,
    links: Optional[bool] = None,
    clean: Optional[bool] = None
):
    """
    Convert a webpage to markdown using the urltomarkdown service.
    
    Args:
        url: The URL to convert
        title: Whether to include title in markdown
        links: Whether to include links in markdown
        clean: Whether to clean the content before conversion
    """
    try:
        params = {"url": url}
        if title is not None:
            params["title"] = str(title).lower()
        if links is not None:
            params["links"] = str(links).lower()
        if clean is not None:
            params["clean"] = str(clean).lower()

        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://urltomarkdown:1337",
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            
            # Get title from header if present
            title = response.headers.get("X-Title")
            
            return {
                "title": title,
                "markdown": response.text
            }
            
    except httpx.HTTPError as e:
        raise HTTPException(status_code=400, detail=f"Error converting URL: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))