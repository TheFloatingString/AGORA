import pandas as pd
from src.agora import Agora

TRAIN_FILEPATH = "data/jigsaw-dataset/train.csv"
TEST_FILEPATH = "data/jigsaw-dataset/test.csv"

train_df = pd.read_csv(TRAIN_FILEPATH)
print(train_df.head(5))
print(train_df.shape)


results_df = pd.DataFrame()

pred_dict_map = {
        False: 0,
        True: 1
        }


for i in range(0, 200):
    agora_obj = Agora()
    input_text = train_df.iloc[i]["comment_text"]

    agora_pred = agora_obj.contains_jigsaw_hate_speech(input_text)
    print(i, agora_pred)

    temp_results_dict = {
            "id": train_df.iloc[i]["id"],
            "toxic": pred_dict_map[agora_pred["toxic"]],
            "severe toxic": pred_dict_map[agora_pred["severe toxic"]],
            "obscene": pred_dict_map[agora_pred["obscene"]],
            "threat": pred_dict_map[agora_pred["threat"]],
            "insult": pred_dict_map[agora_pred["insult"]],
            "identity hate": pred_dict_map[agora_pred["identity hate"]]
            }

    results_df = results_df.append(temp_results_dict, ignore_index=True)

results_df.to_csv("results/results.csv", index=False)

