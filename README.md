# Agora

### Installation and Setup

Configure environment variables:

```
set OPENAI_API_KEY=<API_KEY>
```

Setup
```
git clone https://github.com/TheFloatingString/agora.git
cd agora
pip install -r requirements.txt
```

In a Python file:
```python
from src.agora import Agora

agora_model = Agora()
response = agora_model.transcribe("filepath_to_speech_audio.wav")
print(respone["outputText"])
```

### Quickstart examples

```
python -m quickstart.run_sample
```
