"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", "get_venue_details"]

QUERY_1_VENUE_NAME    = "The Albanach"
QUERY_1_VENUE_ADDRESS = "2 Hunter Square, Edinburgh"
QUERY_2_FINAL_ANSWER  = "This function call will return a list of venues in Edinburgh that can accommodate at least 300 people and have vegan options. The response will include the names of the venues that match these criteria."

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True   # True or False

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
The experiment involved modifying sovereign_agent/tools/mcp_venue_server.py to update the venue database. It's the only
files that needed to be changed. After the change, the agent changed answer to the query 1, it chose the venue with the
name "The Haymarket Vaults" and the address "1 Dalry Road, Edinburgh".
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 1   # count in exercise2_langgraph.py
LINES_OF_TOOL_CODE_EX4 = 42  # count in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP server advertises its tools dynamically. You can update MCP tools without changing the client code. 
MCP allows for easy tool updates and additions. MCP tools can be called by any conforming client.
"""

# ── Week 5 architecture ────────────────────────────────────────────────────
# Describe your full sovereign agent at Week 5 scale.
# At least 5 bullet points. Each bullet must be a complete sentence
# naming a component and explaining why that component does that job.

WEEK_5_ARCHITECTURE = """
- LangChain agent searches for a venue using MCP. LangChain is good for research tasks, because LLM decides about running tools dynamically.
- Rasa CALM agent handles booking confirmation. It's good for a confirmation flow, deterministic and straightforward.
- MCP server with venues, exposes tools for searching a venue. It's flexible and easy to update.
- Actual LLMs that are used are easy to swap out for other Nebius Token Factory models. It's easy to switch between models and compare results.
- All tokens are set via environment variables. It's easy to change settings.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
LangGraph handles the research: it dynamically decided to call tools, in an order that emerged from the 
model's reasoning rather than any hardcoded sequence.
Rasa CALM handles the confirmation call: its flows.yml defines each step explicitly, so out-of-scope inputs (e.g.
train times in Task C) were rejected cleanly rather than triggering a hallucinated tool call.
Swapping feels wrong because the research task has no fixed step order. The model must react to each tool result,
while the booking confirmation is a known, bounded flow where unpredictability is a liability.
"""
