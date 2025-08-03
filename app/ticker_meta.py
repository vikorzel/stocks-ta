import typing
import yfinance

class TickerMeta(typing.TypedDict):
    """
    TickerMeta is a TypedDict that defines the structure for ticker metadata.
    It includes fields for the ticker symbol, name, and exchange.
    """
    ticker: str
    longName: str
    toSell: int
    toBuy: int
    toHold: int
    toStrongBuy: int
    toStrongSell: int
    

def get_ticker_meta(ticker: str) -> TickerMeta:
    t = yfinance.Ticker(ticker)
    info = t.info
    recommendations = t.recommendations
    last_recommendations = recommendations[recommendations['period'] == '0m']
    return TickerMeta(
        ticker=ticker,
        longName=info.get('longName', 'N/A'),
        toBuy= last_recommendations['buy'][0] if not last_recommendations.empty else 0,
        toSell= last_recommendations['sell'][0] if not last_recommendations.empty else 0,
        toHold= last_recommendations['hold'][0] if not last_recommendations.empty else 0,
        toStrongBuy= last_recommendations['strongBuy'][0] if not last_recommendations.empty else 0,
        toStrongSell= last_recommendations['strongSell'][0] if not last_recommendations.empty else 0
    )