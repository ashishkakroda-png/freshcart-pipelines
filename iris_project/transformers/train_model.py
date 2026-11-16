from sklearn.tree import DecisionTreeClassifier

try:
    from mage_ai.data_preparation.decorators import transformer, test
except ImportError:
    def transformer(fn): return fn
    def test(fn): return fn

FEATURES = ["sepal length (cm)", "sepal width (cm)", "petal length (cm)", "petal width (cm)"]

@transformer
def train(df, *args, **kwargs):
    depth = int(kwargs.get("max_depth", 3))
    train_df = df[df.split == "train"]
    test_df = df[df.split == "test"].copy()
    model = DecisionTreeClassifier(max_depth=depth, random_state=42)
    model.fit(train_df[FEATURES], train_df.target)
    test_df["predicted"] = model.predict(test_df[FEATURES])
    test_df.attrs["max_depth"] = depth
    return test_df

@test
def test_accuracy(output, *args):
    accuracy = (output.predicted == output.target).mean()
    assert accuracy >= 0.80, f"Model accuracy {accuracy:.3f} is below 80%"
