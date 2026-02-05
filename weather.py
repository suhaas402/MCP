from mcp.server.fastmcp import FastMCP
import requests
import os
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("weather")


@mcp.tool()
def get_weather(city: str) -> str:
    """Return current weather for a city"""

    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Weather API key not found."

    url = "https://api.openweathermap.org/data/2.5/weather"

    try:
        response = requests.get(
            url,
            params={
                "q": city,
                "appid": api_key,
                "units": "metric",
            },
            timeout=5,
        )

        response.raise_for_status()
        data = response.json()

        return (
            f"[FROM MCP TOOL] {city}: "
            f"{data['weather'][0]['description']}, "
            f"{data['main']['temp']}°C"
        )


    except Exception:
        return f"Unable to fetch weather for {city}."


if __name__ == "__main__":
    mcp.run()
