from src.agora import Agora

filepath = "data/samples/audio/gettysburg10.wav"

agora_model = Agora()
response = agora_model.transcribe_audio(filepath)
print(response)
