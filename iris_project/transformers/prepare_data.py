from sklearn.model_selection import train_test_split

try:
    from mage_ai.data_preparation.decorators import transformer, test
except ImportError:
    def transformer(fn): return fn
    def test(fn): return fn

@transformer
def transform(df, *args, **kwargs):
    train_df, test_df = train_test_split(
        df, test_size=float(kwargs.get("test_size", 0.3)), random_state=42,
        stratify=df["target"] if "target" in df else None,
    )
    train_df = train_df.copy(); test_df = test_df.copy()
    train_df["split"] = "train"; test_df["split"] = "test"
    return __import__("pandas").concat([train_df, test_df])

@test
def test_output(output, *args):
    assert "split" in output.columns
    assert set(output["split"].unique()) == {"train", "test"}
    assert output["target"].nunique() == 3
