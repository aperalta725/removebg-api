from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
import io
import numpy as np
import cv2

app = FastAPI()

def upscale_image(img_pil, factor=2):
    img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGBA2BGRA)
    w = img_cv.shape[1] * factor
    h = img_cv.shape[0] * factor
    upscaled = cv2.resize(img_cv, (w, h), interpolation=cv2.INTER_CUBIC)
    kernel = np.array(
        [[0, -1, 0],
         [-1, 5, -1],
         [0, -1, 0]], dtype=np.float32
    )
    sharpened = cv2.filter2D(upscaled, -1, kernel)
    return Image.fromarray(cv2.cvtColor(sharpened, cv2.COLOR_BGRA2RGBA))

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    img_bytes = await file.read()
    input_img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
    removed = remove(input_img)
    final_img = upscale_image(removed, 2)

    buf = io.BytesIO()
    final_img.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
