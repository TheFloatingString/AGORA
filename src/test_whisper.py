import whisper

model = whisper.load_model("base")
result = model.transcribe("data/samples/audio/gettysburg10.wav")

print(result.keys())
print(result["text"])

