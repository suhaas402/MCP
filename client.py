import asyncio
import warnings
import re

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

warnings.filterwarnings("ignore", category=DeprecationWarning)


async def main():
    # Start MCP client (servers auto-start)
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["mathser.py"],
                "transport": "stdio",
            },
            "weather": {
                "command": "python",
                "args": ["weather.py"],
                "transport": "stdio",
            },
        }
    )

    print("Connecting to MCP servers...")
    tools = await client.get_tools()

    print("\nAvailable tools:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")

    # Separate tools
    math_tools = [t for t in tools if t.name in ("add", "multiply")]
    weather_tool = next(t for t in tools if t.name == "get_weather")

    # LLM
    model = ChatOllama(model="llama3.2", temperature=0)

    # Math-only agent
    math_agent = create_react_agent(model, math_tools)

    print("\n RESULTS ")

    # Math via agent
    res1 = await math_agent.ainvoke(
        {"messages": [{"role": "user", "content": "15 + 27"}]}
    )
    print("Math:", res1["messages"][-1].content)

    res2 = await math_agent.ainvoke(
        {"messages": [{"role": "user", "content": "12 * 9"}]}
    )
    print("Math:", res2["messages"][-1].content)

    # Weather via forced MCP tool
    print("\nWeather Tokyo:")
    tokyo = await weather_tool.ainvoke({"city": "Tokyo"})
    print(tokyo[0]["text"])

    print("\nWeather London:")
    london = await weather_tool.ainvoke({"city": "London"})
    print(london[0]["text"])

    # FIXED: Weather + Math (Manual approach)
    print("\nWeather + Math (Agent decides tools):")
    
    query = "What is the temperature in Tokyo plus 10?"
    
    # Step 1: Get weather with the tool
    tokyo_weather = await weather_tool.ainvoke({"city": "Tokyo"})
    weather_text = tokyo_weather[0]["text"]
    
    # Step 2: Extract temperature using regex
    temp_match = re.search(r'([\d.]+)\s*°?C', weather_text)
    
    if temp_match:
        temperature = float(temp_match.group(1))
        
        # Step 3: Convert to int and use the add tool
        temperature_int = int(temperature)  # Convert float to int
        add_tool = next(t for t in tools if t.name == "add")
        result = await add_tool.ainvoke({"a": temperature_int, "b": 10})
        
        answer = f"The temperature in Tokyo is {temperature}°C (rounded to {temperature_int}°C). Adding 10 gives us {result[0]['text']}°C"
        
        print("Question:", query)
        print("Answer:", answer)
    else:
        print("Could not extract temperature from weather data")


if __name__ == "__main__":
    asyncio.run(main())