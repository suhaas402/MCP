import asyncio
import warnings

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

    # LLM for math reasoning
    model = ChatOllama(model="llama3.2", temperature=0)
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

    # Weather via forced MCP tool (ASYNC)
    print("\nWeather Tokyo:")
    tokyo = await weather_tool.ainvoke({"city": "Tokyo"})
    print(tokyo[0]["text"])

    print("\nWeather London:")
    london = await weather_tool.ainvoke({"city": "London"})
    print(london[0]["text"])



if __name__ == "__main__":
    asyncio.run(main())
