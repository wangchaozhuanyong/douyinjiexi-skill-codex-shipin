from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_openai_yaml_has_interface_and_policy():
    text = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
    assert "interface:" in text
    assert "display_name:" in text
    assert "short_description:" in text
    assert "default_prompt:" in text
    assert "policy:" in text
    assert "allow_implicit_invocation: true" in text
