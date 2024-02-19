import sys
from src.agora import Agora
import pandas as pd
from pprint import pprint
from tqdm import trange

df = pd.read_csv("data/mutox/Data/processed_data.tsv", delimiter="\t")
# print(df.head())

list_for_pandas_dict = []

for i in trange(df.shape[0]):
    filename = df["segment_path"][i]
    filepath = "data/mutox/"+filename
    true_label = df["contains_toxicity"][i]
    true_label_detail = df["toxicity_types"][i]
    true_transcript = df["audio_file_transcript"][i]
    agora = Agora()
    agora.config_pandas_dict(true_label=true_label, true_label_detail=true_label_detail, true_transcript=true_transcript)
    _ = agora.transcribe_audio(filepath=filepath)
    pandas_dict = agora.export_pandas_dict()
    pprint(pandas_dict)
    list_for_pandas_dict.append(pandas_dict)

df_results = pd.DataFrame(list_for_pandas_dict)
df_results.to_csv("agora-mutox-results-with-gpt-4-0125.csv", index=False)


# agora = Agora()
# results = agora.transcribe_audio("data/mutox/Data/0e341b515bf1d951cb1_1238784_1243710_segment.wav")
# print(results)