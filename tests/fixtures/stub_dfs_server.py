"""Stub upstream for the gateway test: two tools named like the official server's, echoing their arguments."""
import json

from mcp.server import MCPServer

app = MCPServer("stub-dataforseo")


@app.tool()
def kw_data_google_ads_search_volume(keywords: list[str], location_name: str = "United States") -> str:
    return json.dumps({"called": "kw_data_google_ads_search_volume", "keywords": len(keywords)})


@app.tool()
def dataforseo_labs_google_ranked_keywords(target: str, limit: int = 100) -> str:
    return json.dumps({"called": "ranked_keywords", "target": target, "limit": limit})


if __name__ == "__main__":
    app.run("stdio")
