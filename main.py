import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import replicate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# Initialize the FastAPI app
app = FastAPI(
    title="Image Generation API",
    description="API for generating images using Replicate's Stable Diffusion model.",
    version="1.0.0",
)

# Define the request model for image generation
class ImageRequest(BaseModel):
    prompt: str
    width: int = 512
    height: int = 512

@app.post("/generate-image/", response_model=dict)
async def generate_image(request: ImageRequest):
    """
    Generate an image from a prompt using Replicate's Stable Diffusion model.

    - **prompt**: The text prompt for image generation.
    - **width**: The width of the generated image (default is 512).
    - **height**: The height of the generated image (default is 512).
    
    Returns a URL to the generated image.
    """
    try:
        # Call the Replicate API to generate an image
        output = replicate.run(
            "stability-ai/stable-diffusion-3",
            input={
                "prompt": request.prompt,
                "width": request.width,
                "height": request.height
            }
        )
        return {"image_url": output}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Start the FastAPI application
    uvicorn.run(app, host="127.0.0.1", port=8000)
