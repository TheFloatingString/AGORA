# AGORA

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
response = agora_model.transcribe_audio("filepath_to_speech_audio.wav")
print(respone["outputText"])
```

### Quickstart examples

```
python -m quickstart.run_sample
```

### Analyze AGORA's ability to Recognize Offensive Content in the Jigsaw Dataset

Note: move `train.csv` into `data` from the Jigsaw dataset on Kaggle (https://www.kaggle.com/competitions/jigsaw-toxic-comment-classification-challenge/data)

```
python -m src.run_jigsaw
python -m src.analyze_resutls
```
