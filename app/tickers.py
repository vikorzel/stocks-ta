import yfinance
import pandas_ta as ta
import pandas as pd
import typing
from . import charts

class ChartData(typing.TypedDict):
    data: pd.DataFrame
    description: str
    rendered: str


def build(quote: str, chart_type: str) -> dict[str,ChartData]:
    data = yfinance.download(quote, period="2mo", interval="60m")
    print(f"Data for {quote} downloaded successfully.")
    print(data.head())
    # Flatten the MultiIndex columns
    data.columns = data.columns.get_level_values(0) if isinstance(data.columns, pd.MultiIndex) else data.columns
    
    
    if chart_type == "stop-loss":
        return stop_loss_indicators(data)
    if chart_type == "buy":
        return buy_indicators(data) 
    if chart_type == "sell":
        return sell_indicators(data)
    
def stop_loss_indicators(data):
    sma = data.copy()
    sma.ta.sma(length=50, append=True)
    sma.ta.sma(length=200, append=True)
    
    psar = data.copy()
    psar.ta.psar(append=True)
    
    atr = data.copy()
    atr.ta.atr(length=14, append=True)
    
    return {
        'SMA': ChartData(
            data=sma,
            description='The Simple Moving Average is a key technical indicator used to identify the medium-term trend and act as a dynamic level of support or resistance. As a lagging indicator, traders must be cautious of false signals in choppy markets and should always use it in conjunction with other analytical tools for confirmation.',
            rendered=charts.render_chart(sma, 'SMA', include_close=True)
        ),
        'PSAR': ChartData(
            data=psar,
            description='The Parabolic SAR (PSAR) is a trend-following indicator used to determine potential reversals in the market direction. It is often used to set trailing stop-loss orders.',
            rendered=charts.render_chart(psar, 'PSAR')
        ),
        'ATR_14': ChartData(
            data=atr,
            description='The Average True Range (ATR) is a volatility indicator that shows how much an asset moves on average. It is commonly used to set stop-loss levels based on market volatility.',
            rendered=charts.render_chart(atr, 'ATR 14')
        ),
    }

def buy_indicators(data):

    sma = data.copy()
    sma.ta.sma(length=50, append=True)
    sma.ta.sma(length=200, append=True)
    print(sma.columns)

    rsi = data.copy()
    rsi.ta.rsi(length=14, append=True)

    macd = data.copy()
    macd.ta.macd(fast=12, slow=26, signal=9, append=True)
    print(macd.columns)

    bbands = data.copy()
    bbands.ta.bbands(length=20, std=2, append=True)

    return {
        'SMA': ChartData(
            data=sma,
            description='Simple Moving Average is a key technical indicator used to identify the medium-term trend and act as a dynamic level of support or resistance. As a lagging indicator, traders must be cautious of false signals in choppy markets and should always use it in conjunction with other analytical tools for confirmation.',
            rendered=charts.render_chart(sma, 'SMA', include_close=True)
        ),
        'RSI_14': ChartData(
            data=rsi,
            description='The 14-day Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements. It ranges from 0 to 100, with values above 70 indicating overbought conditions and below 30 indicating oversold conditions.',
            rendered=charts.render_chart(rsi, 'RSI 14')
        ),
        'MACD_12_26_9': ChartData(
            data=macd,
            description='Moving Average Convergence Divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price. A crossover of the MACD line above the signal line is often a bullish signal.',
            rendered=charts.render_chart(macd, 'MACD 12 26 9')
        ),
        'BBANDS_20_2': ChartData(
            data=bbands,
            description='Bollinger Bands are a volatility indicator consisting of a middle band (a simple moving average) and two outer bands. Prices are considered overextended on the upside when they touch the upper band and on the downside when they touch the lower band.',
            rendered=charts.render_chart(bbands, 'BBANDS 20 2')
        ),
    }

def sell_indicators(data):
    sma = data.copy()
    sma.ta.sma(length=50, append=True)
    sma.ta.sma(length=200, append=True)

    rsi = data.copy()
    rsi.ta.rsi(length=14, append=True)

    obv = data.copy()
    obv.ta.obv(append=True)

    stoch = data.copy()
    stoch.ta.stoch(k=14, smooth_k=3, smooth_d=3, append=True)
    
    return {
        'SMA': ChartData(
            data=sma,
            description='The Simple Moving Averages (SMA) are key technical indicators.',
            rendered=charts.render_chart(sma, 'SMA', include_close=True)
        ),
        'RSI_14': ChartData(
            data=rsi,
            description='The 14-day Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements. It ranges from 0 to 100, with values above 70 indicating overbought conditions (potential sell signal) and below 30 indicating oversold conditions.',
            rendered=charts.render_chart(rsi, 'RSI 14')
        ),
        'OBV': ChartData(
            data=obv,
            description='On-Balance Volume (OBV) is a technical analysis indicator that uses volume flow to predict changes in stock price. A declining OBV can indicate selling pressure, even if the price is flat or rising, suggesting a potential price drop.',
            rendered=charts.render_chart(obv, 'OBV')
        ),
        'STOCHk_14_3_3': ChartData(
            data=stoch,
            description='The Stochastic Oscillator (STOCH) is a momentum indicator comparing a particular closing price of a stock to a range of its prices over a certain period. A reading above 80 is considered overbought and may signal a price reversal to the downside.',
            rendered=charts.render_chart(stoch, 'STOCH k 14 3 3')
        ),
    }