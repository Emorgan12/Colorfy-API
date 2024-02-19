from typing import Any
from io import BytesIO
import urllib.request
from urllib.parse import urlparse

import numpy as np
from PIL import Image
from spotify_background_color import SpotifyBackgroundColor
from fastapi import FastAPI, HTTPException, Query
from colorsys import rgb_to_hsv
from pydantic import BaseModel

app = FastAPI()

SPOTIFY_CDN_URL = "i.scdn.co"

class RGB(BaseModel):
    r: int
    g: int
    b: int

class HSV(BaseModel):
    h: float
    s: float
    v: float

class Values(BaseModel):
    rgb: RGB
    hsv: HSV

def is_spotify_CDN(url: str) -> bool:
    parsed_url = urlparse(url)
    return parsed_url.netloc == SPOTIFY_CDN_URL

@app.get("/", response_model=Values)
async def colorfy(image_url: str = Query(..., title="Image URL", description="The Spotify CDN URL of the album artwork to be colorfied"),
                  
                  k: int = Query(8, title="Number of clusters", description="Number of clusters to form"),
                  
                  color_tol: float = Query(0, title="Color tolerance", description="""Tolerance for a colorful color, Colorfulness is defined as described by 
                                                                                        Hasler and Süsstrunk (2003) in
                                                                                        https://infoscience.epfl.ch/record/33994/files/HaslerS03.pdf."""),
                  width: int = 100,
                  height: int = 100):
    
    if not is_spotify_CDN(image_url):
        raise HTTPException(status_code=400, detail="Must be a link to Spotify's CDN")
    
    size = (width, height)

    #attempt download
    try:
        image_bytes = BytesIO(urllib.request.urlopen(image_url).read())

    except:
        raise HTTPException(status_code=422, detail="Unable to download image")

    artwork = np.array(Image.open(image_bytes))
    background_color = SpotifyBackgroundColor(img=artwork, image_processing_size=size)
    
    r, g, b = background_color.best_color(k=k, color_tol=color_tol)
    h, s, v = rgb_to_hsv(r/255, g/255, b/255)
    
    return {
        "rgb": {
            "r": int(r),
            "g": int(g),
            "b": int(b)
        },
        "hsv": {
            "h": h,
            "s": s,
            "v": v
        }
    }
