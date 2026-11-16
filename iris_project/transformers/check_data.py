try:
    from mage_ai.data_preparation.decorators import transformer, test
except ImportError:
    def transformer(fn): return fn
    def test(fn): return fn

@transformer
def check_data(df, *args, **kwargs):
    assert not df.isna().any().any(), "Iris data contains missing values"
    assert df["target"].nunique() == 3, "Expected exactly three Iris classes"
    return df

@test
def test_output(output, *args):
    assert len(output) == 150
    assert output["target"].nunique() == 3
    assert not output.isna().any().any()
