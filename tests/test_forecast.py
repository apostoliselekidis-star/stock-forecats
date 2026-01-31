import pandas as pd
from utils.forecast import train_and_forecast


def test_forecast_short():
    dates = pd.date_range(end=pd.Timestamp.today(), periods=200)
    s = pd.Series(100 + (pd.np.sin(range(200))/10).cumsum(), index=dates)
    model, preds = train_and_forecast(s, days=5, retrain=True)
    assert preds is not None
    assert len(preds) == 5
