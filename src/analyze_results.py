import pandas as pd
from sklearn.metrics import classification_report
from sklearn.metrics import multilabel_confusion_matrix
from sklearn.metrics import confusion_matrix


TRAIN_FILEPATH = "data/jigsaw-dataset/train.csv"
RESULTS_FILEPATH = "results/results.csv"

df_train = pd.read_csv(TRAIN_FILEPATH)
df_results = pd.read_csv(RESULTS_FILEPATH)

print(df_train.head())
print()
print(df_results.head())

"""
Check if toxicity is contained
"""

y_true = []
y_pred = []


target_cols_true = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"] 
target_cols_pred = ["toxic", "severe toxic", "obscene", "threat", "insult", "identity hate"]


for i in range(df_results.shape[0]):
    print(list(df_train.iloc[i][target_cols_true]))
    print(1 in list(df_train.iloc[i][target_cols_true]))
    if 1 in list(df_train.iloc[i][target_cols_true]):
        y_true.append(1)
    else:
        y_true.append(0)

for i in range(df_results.shape[0]):
    if 1 in list(df_results.iloc[i][target_cols_pred]):
        y_pred.append(1)
    else:
        y_pred.append(0)


print(y_true)
print(y_pred)



match_counter = 0
for i in range(len(y_true)):
    if y_true[i] == y_pred[i]:
        match_counter += 1

print(match_counter/df_results.shape[0])



print(classification_report(y_true, y_pred, target_names=["non-offensive", "offensive"]))
print(confusion_matrix(y_true, y_pred))


print("---")

print(classification_report(df_train[target_cols_true].iloc[:200].values, df_results[target_cols_pred].values, target_names=target_cols_pred))
print(multilabel_confusion_matrix(df_train[target_cols_true].iloc[:200].values, df_results[target_cols_pred].values))
