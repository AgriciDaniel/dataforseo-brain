"""Second stub upstream (the 3.x shape): docs search plus api_request, and one name that clashes with the first stub."""
import json

from mcp.server import MCPServer

app = MCPServer("stub-dataforseo-docs")


@app.tool()
def docs_search(query: str) -> str:
    return json.dumps({"called": "docs_search", "query": query})


@app.tool()
def dataforseo_labs_google_ranked_keywords(target: str, limit: int = 100) -> str:
    return json.dumps({"called": "SHADOWED", "target": target})


if __name__ == "__main__":
    app.run("stdio")
