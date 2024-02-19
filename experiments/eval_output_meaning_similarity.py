import pandas as pd
from sentence_transformers import SentenceTransformer, util
import numpy as np

df = pd.read_csv("agora-mutox-results.csv")
df_gen = df[df["n_iterations"]>0]
print(df_gen.head())

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
result_scores = []

for i in range(df_gen.shape[0]):
    # print(df_gen["true_transcript"].values[0])
    sentence_init = df_gen["true_transcript"].values[i]
    sentence_pred = df_gen["output_text"].values[i]
    sentences=[sentence_init, sentence_pred]
    embeddings = model.encode(sentences=sentences)
    similarity_score = float(util.pytorch_cos_sim(embeddings[0], embeddings[1])[0][0])
    result_scores.append(similarity_score)
result_scores = np.asarray(result_scores)
print(np.mean(result_scores))
print(np.std(result_scores))



