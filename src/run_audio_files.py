from src.agora import Agora

filepaths = [
        "data/audio/audio-1.wav"
        ]

for filepath in filepaths:
    agora_model = Agora()
    resp = agora_model.transcribe_audio(filepath)
    print(resp)
