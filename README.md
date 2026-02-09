# MCP
🧠 MCP Tool Chaining Demo (Weather + Math)

This project demonstrates a Model Context Protocol (MCP)–based multi-tool system where an AI agent orchestrates external tools to answer composite queries using multi-step reasoning.

The system integrates:

a Weather API tool (external data)

a Math computation tool (add / multiply)

an LLM agent that coordinates tool usage

🚀 What This Project Shows

✔ MCP client–server communication
✔ Tool discovery and invocation
✔ Async tool execution
✔ Multi-step tool chaining
✔ Tool output normalization (text → numeric)
✔ Real-world agent orchestration pattern

This is not a UI demo — the focus is on AI systems design.

🧩 Architecture Overview
User Query
   ↓
LLM Agent (ReAct)
   ↓
Weather Tool (MCP)
   ↓
Text Output
   ↓
Numeric Extraction (Regex)
   ↓
Math Tool (MCP)
   ↓
Final Answer

🛠 Tools Used
1️⃣ Weather Tool

MCP server exposing get_weather

Returns textual weather information for a city

Example output:

Tokyo: few clouds, 7.71°C

2️⃣ Math Tool

MCP server exposing:

add(a, b)

multiply(a, b)

Expects numeric inputs

🔑 Key Design Challenge Solved
Problem

In real agent systems:

Tool A returns unstructured text

Tool B requires structured numeric input

Passing text directly causes failures.

Solution

This project explicitly normalizes tool outputs:

Call weather tool

Extract numeric temperature using regex

Pass clean number to math tool

Produce final composed answer

This mirrors production-grade agent workflows.

🧪 Example Query

Input

What is the temperature in Tokyo plus 10?


Execution Flow

Weather tool → returns text

Temperature extracted (7.71)

Math tool → adds 10

Final answer returned

Output

The temperature in Tokyo is 7.71°C (rounded to 7°C). Adding 10 gives us 17°C.

🧠 Why This Matters

This project demonstrates:

Understanding of MCP internals

Practical handling of tool output mismatches

Safe and deterministic multi-tool chaining

Engineering-first approach to agent design

These are common failure points in real LLM agent systems.

📦 Tech Stack

Python 3.11+

LangChain MCP Adapters

LangGraph (ReAct Agent)

Ollama (LLaMA 3.2)

AsyncIO

▶️ How to Run
python client.py


Make sure:

MCP tool servers (mathser.py, weather.py) are present

Ollama is running locally

📌 Notes

No UI framework (Streamlit) is used — CLI output is intentional

Focus is on agent orchestration, not presentation

Code is structured for clarity and debuggability

📈 Future Improvements (Optional)

Structured JSON outputs from tools

Additional computation tools

Integration with RAG pipelines

Logging and tracing of tool calls

👤 Author

Built as a learning + portfolio project to understand MCP-based agent systems and multi-tool reasoning.
