from src.agora import Agora

filepath = "data/samples/audio/gettysburg10.wav"

agora_model = Agora()
response = agora_model.transcribe(filepath)
print(response)
