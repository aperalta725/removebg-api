import os
from fastapi import FastAPI, File, UploadFile
from rembg import remove

app = FastAPI()

@app.get("/")
def root():
    return {"status": "API funcionando"}

@app.post("/remove")
async def remove_bg(file: UploadFile = File(...)):
    contents = await file.read()
    result = remove(contents)
    return Response(content=result, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 10000))  # Render asigna PORT
    uvicorn.run(app, host="0.0.0.0", port=port)
