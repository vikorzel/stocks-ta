from google import genai
from google.genai import types
import json

from . import config


def get_recomendation(type: str, numbers: dict, config: config.AppConfig) -> str:
    client = genai.Client(
        vertexai=True,
        project="lucky-essence-409609",
        location="global",
    )
    serializable_numbers = {
        key: {
            "data": value["data"].to_json(orient="split"),
            "description": value["description"],
        }
        for key, value in numbers.items()
    }
    data = json.dumps(serializable_numbers)
    if type == "sell":
        prompt = recommendations_to_sell()
    elif type == "buy":
        prompt = recommendations_to_buy()
    elif type == "stop-loss":
        prompt = recommendations_to_stop_loss()
    else:
        return "NOT IMPLEMENTED YET"

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=data),
                   types.Part.from_text(text=prompt)],
        )
    ]

    resp = ""
    for chunk in client.models.generate_content_stream(
        contents=contents,
        model=config['llmModel'],
        config=types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            max_output_tokens=config['llmMaxTokens'],
            safety_settings=[
                types.SafetySetting(
                    category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_HARASSMENT", threshold="OFF"
                ),
            ],
            thinking_config=types.ThinkingConfig(
                thinking_budget=0,
            ),
        ),
    ):
        resp += chunk.text
    return resp


def recommendations_to_sell() -> str:
    return f"""
        You are an expert in stock trading and technical analysis. Based on the following data, provide a detailed recommendation on whether to sell the stock, including specific indicators and their implications. Provide only conclusions in 3-4 sentences."
    """


def recommendations_to_buy() -> str:
    return f"""
        You are an expert in stock trading and technical analysis. Based on the following data, provide a detailed recommendation on whether to buy the stock, including specific indicators and their implications. Provide only conclusions in 3-4 sentences."
    """


def recommendations_to_stop_loss() -> str:
    return f"""
        You are an expert in stock trading and technical analysis. Based on the following data, provide a detailed recommendation on whether to set a stop-loss for the stock, including specific indicators and their implications. Provide only conclusions in 3-4 sentences."
    """
