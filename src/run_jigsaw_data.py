import pandas as pd
from src.agora import Agora

TRAIN_FILEPATH = "data/jigsaw-dataset/train.csv"
TEST_FILEPATH = "data/jigsaw-dataset/test.csv"

train_df = pd.read_csv(TRAIN_FILEPATH)
print(train_df.head(5))

agora_obj = Agora()
resp = agora_obj.contains_jigsaw_hate_speech("Unblock me or I'll get my lawyers on to you for blocking my constitutional right to free speech")
print(resp)
