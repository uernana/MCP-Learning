## ❓ How Questions Are Interpreted (Important)

### 1️⃣ Scope of Knowledge: **United States Only**

This MCP Weather Assistant is **intentionally limited to U.S. weather data**.

Why?

* The FastMCP server uses the **National Weather Service (NWS) API**
* The NWS API **only supports U.S. locations**
* All MCP tools (`get_alerts`, `get_forecast`) are designed around:

  * U.S. state codes (CA, NY, WA, etc.)
  * U.S. latitude/longitude within NWS coverage

As a result:

✅ Supported:

* “What are the weather alerts in Washington?”
* “Any severe weather in California?”
* “Forecast for New York City”
* “Weather alerts in NY”

❌ Not supported:

* “Weather in London”
* “Typhoon alerts in Japan”
* “Forecast in Paris”

If a non-U.S. location is asked, the LLM will either:

* Answer generically (without tools), or
* Respond that it cannot retrieve official data

---

### 2️⃣ The LLM Does **Not** Fetch Weather by Itself

A critical design principle of MCP:

> **The LLM never directly calls weather APIs.**

Instead:

* The LLM only:

  * Understands natural language
  * Chooses whether a tool should be used
* All real weather data comes from:

  * **FastMCP tools**
  * **NWS API**

This prevents:

* Hallucinated forecasts
* Outdated weather information
* Inconsistent data sources

---

### 3️⃣ How the LLM Decides to Call a Tool

When you ask a question, the following happens:

#### Example:

> “What are the weather alerts in Washington?”

**Step-by-step reasoning (simplified):**

1. LLM reads the question
2. LLM sees available MCP tools:

   * `get_alerts(state: str)`
   * `get_forecast(latitude, longitude)`
3. LLM infers:

   * “Washington” → U.S. state
   * “alerts” → matches `get_alerts`
4. LLM issues a **tool call**:

   ```json
   {
     "name": "get_alerts",
     "arguments": { "state": "WA" }
   }
   ```
5. MCP server executes the tool
6. Results are returned to the LLM
7. LLM formats a human-friendly answer

✔ The final response is **grounded in real data**, not LLM memory.




