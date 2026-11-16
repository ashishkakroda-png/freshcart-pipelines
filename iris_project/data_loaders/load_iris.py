from sklearn.datasets import load_iris

try:
    from mage_ai.data_preparation.decorators import data_loader, test
except ImportError:
    def data_loader(fn): return fn
    def test(fn): return fn

@data_loader
def load_data(*args, **kwargs):
    return load_iris(as_frame=True).frame

@test
def test_output(output, *args):
    assert len(output) == 150
