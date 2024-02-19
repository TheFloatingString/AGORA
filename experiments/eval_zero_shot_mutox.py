import numpy as np
import pandas as pd
from sklearn.metrics import classification_report

df = pd.read_csv("agora-mutox-results.csv")
# print(df.head())
# 
# print(df.columns.values)

true_labels = df["true_label"].values
predicted_labels = df["predict_label"].map({"non-toxic":"No", "toxic":"Yes"}).values 

print(classification_report(true_labels, predicted_labels, target_names=["Non-Toxic", "Toxic"], digits=3))

# print(true_labels)
# print(predicted_labels)

# acc = 0

# for i in range(len(true_labels)):
#     if true_labels[i] == predicted_labels[i]:
#         acc += 1
# print(acc/len(true_labels))


# from sklearn.metrics import confusion_matrix

# tn, fp, fn, tp = confusion_matrix(true_labels, predicted_labels).ravel()
# print(tn,fp,fn,tp)
# specificity = tn / (tn+fp)
# print(specificity)
# sensitivity = tp/(tp+fn)
# print(sensitivity)