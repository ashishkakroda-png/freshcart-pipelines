import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

try:
    from mage_ai.data_preparation.decorators import transformer
except ImportError:
    def transformer(fn): return fn

@transformer
def evaluate(df, *args, **kwargs):
    y_true, y_pred = df.target, df.predicted
    print("Confusion matrix:")
    print(pd.crosstab(y_true, y_pred, rownames=["actual"], colnames=["predicted"]))
    return pd.DataFrame({"metric": ["accuracy", "precision", "recall", "f1_score"],
        "value": [accuracy_score(y_true, y_pred),
                  precision_score(y_true, y_pred, average="macro", zero_division=0),
                  recall_score(y_true, y_pred, average="macro", zero_division=0),
                  f1_score(y_true, y_pred, average="macro", zero_division=0)]})
