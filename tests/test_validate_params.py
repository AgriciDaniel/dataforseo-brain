import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate_params  # noqa: E402

SPEC = """openapi: 3.0.1
paths:
  /v3/dataforseo_labs/google/keyword_ideas/live:
    post:
      requestBody:
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                oneOf:
                  - $ref: '#/components/schemas/IdeasRequest'
components:
  schemas:
    IdeasRequest:
      type: object
      properties:
        keywords:
          type: array
          description: '<em>keywords</em><br>The maximum number of keywords you can specify: 200.'
        limit:
          type: integer
          description: 'the maximum number of returned keywords<br>maximum value: 1000'
        target:
          type: array
          items:
            $ref: '#/components/schemas/TargetElement'
    TargetElement:
      type: object
      properties:
        search_scope:
          type: string
"""


def make_vault(tmp_path, params_section):
    spec = tmp_path / validate_params.SPEC_REL
    spec.parent.mkdir(parents=True)
    spec.write_text(SPEC, encoding="utf-8")
    note = tmp_path / "wiki" / "concepts" / "cap-x.md"
    note.parent.mkdir(parents=True)
    note.write_text("Uses `/v3/dataforseo_labs/google/keyword_ideas/live`.\n\n## Key parameters / inputs\n"
                    "| field | notes |\n|---|---|\n" + params_section + "\n## Response\n", encoding="utf-8")
    return tmp_path


def test_valid_fields_and_caps_pass(tmp_path):
    vault = make_vault(tmp_path, "| keywords | up to 200 seeds |\n| limit | max 1000 |\n| search_scope | nested in target |\n")
    assert validate_params.audit(vault) == []


def test_unknown_field_is_flagged(tmp_path):
    vault = make_vault(tmp_path, "| aggregation_key | labels groups |\n")
    findings = validate_params.audit(vault)
    assert len(findings) == 1 and "aggregation_key" in findings[0]


def test_wrong_cap_is_flagged(tmp_path):
    vault = make_vault(tmp_path, "| keywords | max 700 |\n")
    findings = validate_params.audit(vault)
    assert len(findings) == 1 and "[700]" in findings[0] and "[200]" in findings[0]
