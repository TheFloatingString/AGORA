from fastapi import FastAPI, File, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from gtts import gTTS

from src.agora import Agora

# Fast API Setup
app = FastAPI()

# CORS Setup
origins = [
        "*"
        ]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
        )



@app.get("/")
async def root():
    return {"data": "McGill AI Society Project X, 2022-2023"}


@app.post("api/upload")
async def api_upload(request: Request):
    form = await request.form()
    filename = form["upload_file"].filename
    contents = await form["upload_file"].read()
    with open(filename, "wb") as f:
        f.write(contents)
    return {"data": "Completed"}

@app.post("/api/transcribe")
async def api_transcribe(request: Request):
    agora_model = Agora()
    form = await request.form()
    
    # print(form)
    # print(dir(form))
    # print("---")
    # print(form["file"])
    # print(dir(form["file"]))

    filename = form["file"].filename+".wav"
    filepath = f"static/{filename}"
    file_contents = await form["file"].read()

    with open(filepath, "wb") as f:
        f.write(file_contents)

    response = agora_model.transcribe_audio(filepath)
    print(response)
    print(dir(response))

    tts = gTTS(response["outputText"])
    tts.save("static/output_speech.mp3")

    response["audioFilepath"] = "C:\\Users\\laure\\Desktop\\Projects\\AGORA\\static\\output_speech.mp3"

    return {"data": response}

if __name__ == "__main__":
    uvicorn.run(app, port=8080)
