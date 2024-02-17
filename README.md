# AGORA - Automated Generation and Omission Recurrent Architecture

Given a speech input (audio recording), this model replaces hate speech and profanity with generated textual content. (Speech to text model.)


### Installation and Setup

Configure environment variables:

```
set OPENAI_API_KEY_AGORA=<API_KEY>
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
print(response["outputText"])
```

### Quickstart examples

```
python -m quickstart.run_sample
```

### Analyze AGORA's ability to Recognize Offensive Content in the Jigsaw Dataset

Note: move `train.csv` into `data/jigsaw-data` from the Jigsaw dataset on Kaggle (https://www.kaggle.com/competitions/jigsaw-toxic-comment-classification-challenge/data)

```
python -m src.run_jigsaw_data
python -m src.analyze_results
```

### Filter and Paraphrase the Speech-to-Text Functionality for Offensive Content

Run the folowing, while making sure to change the filename from `1` to `10` at each new run.

**Warning: the audio files contain explicit content.**

```
python -m src.run_audio_files
```

### Text Prompts

Rephrasing:

```python
f"Paraphrase the following phrase in a non-offfensive way: \"{current_text}\""
```


Toxicity detection:
```python
f"Does the following text prompt contain one or several of toxic, severe toxic, obscene, threat, insult or identity hate: \"{text}\"Provide a single answer: \"yes\" or \"no\"."
```


