from flask import render_template, Flask, request
from . import config
from . import charts
from . import tickers


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
        llm = "NOT IMPLEMENTED YET"
        analysis = "NOT IMPLEMENTED YET"
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
        return render_template("chart.html", charts=render, llm=llm, analysis=analysis)
