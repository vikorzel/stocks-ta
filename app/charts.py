import pandas as pd
import plotly
from typing import List

IGNORE_LIST = [
    'HIGH',
    'LOW',
    'OPEN',
    'VOLUME',
]

def render_chart(numbers: pd.DataFrame, ticker_name: str, include_close=False) -> str:
    fig = plotly.graph_objects.Figure()
    
    for column in numbers.columns:
        if column.upper() in IGNORE_LIST:
            continue
        if column.upper() == 'CLOSE' and not include_close:
            continue
        # Cut off head with nulls
        numbers_without_nulls = numbers.dropna(subset=[column])
        fig.add_trace(plotly.graph_objects.Scatter(x=numbers_without_nulls.index, y=numbers_without_nulls[column], mode='lines', name=column))

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=ticker_name,
        title=f"{ticker_name} Data"
    )
    
    return fig.to_html()
