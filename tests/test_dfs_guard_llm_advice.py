import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import dfs_guard  # noqa: E402

TOOL = "mcp__dataforseo__ai_optimization_llm_response"


def ask(llm_type):
    decision, reason, _ = dfs_guard.decide(TOOL, {"llm_type": llm_type, "model_name": "m", "user_prompt": "q"}, "s", 0, [])
    assert decision == "ask"
    return reason


def test_gemini_points_to_the_rest_scraper_because_the_connector_has_no_tool():
    assert "gemini/llm_scraper" in ask("gemini")


def test_chatgpt_points_to_the_connector_scraper_tool():
    assert "ai_optimization_chat_gpt_scraper" in ask("chat_gpt")


def test_perplexity_is_told_there_is_no_cheaper_route():
    assert "only route" in ask("perplexity")


def test_api_request_reads_the_model_from_the_path():
    decision, reason, _ = dfs_guard.decide("mcp__dataforseo__api_request",
                                           {"path": "/v3/ai_optimization/gemini/llm_responses/live", "data": [{}]}, "s", 0, [])
    assert decision == "ask" and "gemini/llm_scraper" in reason
