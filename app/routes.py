from flask import render_template, Flask, request
from . import config
from . import tickers
from . import ticker_meta
from . import llm
import json


def init_routes(app: Flask, config_data: config.AppConfig):
    @app.route("/")
    def index():
        return render_template("index.html", version=config_data["version"])

    @app.route("/static/<path:path>")
    def serve_static(path):
        return app.send_static_file(path)

    @app.route("/chart")
    def chart():
        quote = request.args.get("stock")
        chart_type = request.args.get("type")
        numbers = tickers.build(quote, chart_type)
        llm_response = llm.get_recomendation(chart_type, numbers, config_data)
        ticker_meta_data = ticker_meta.get_ticker_meta(quote)
        ticker_name = f"{ticker_meta_data['longName']} ({ticker_meta_data['ticker']})"
        render = "".join(
            [
                render_template(
                    "chart-container.html",
                    chart=number['rendered'],
                    description=number['description'],
                )
                for number in numbers.values()
            ]
        )
        
        
        
        return render_template("chart.html", 
                               charts=render, 
                               llm=llm_response, 
                               ticker_name=ticker_name,
                               toBuy=ticker_meta_data['toBuy'],
                               toSell=ticker_meta_data['toSell'],
                               toHold=ticker_meta_data['toHold'],
                               toStrongBuy=ticker_meta_data['toStrongBuy'],
                               toStrongSell=ticker_meta_data['toStrongSell']
                            )
