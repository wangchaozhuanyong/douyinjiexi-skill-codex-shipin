import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_schema_files_are_valid_json():
    for path in (ROOT / "schemas").glob("*.json"):
        data = load_json(path)
        assert data["type"] == "object"


def test_topic_candidates_example_matches_required_shape():
    data = load_json(ROOT / "templates" / "topic_candidates.example.json")
    assert len(data["candidates"]) >= 3
    required = set(load_json(ROOT / "schemas" / "topic_candidates.schema.json")["properties"]["candidates"]["items"]["required"])
    for candidate in data["candidates"]:
        assert required.issubset(candidate.keys())


def test_storyboard_example_matches_required_shape():
    data = load_json(ROOT / "templates" / "storyboard.example.json")
    assert len(data["scenes"]) >= 6
    required = set(load_json(ROOT / "schemas" / "storyboard.schema.json")["properties"]["scenes"]["items"]["required"])
    for scene in data["scenes"]:
        assert required.issubset(scene.keys())


def test_qa_report_example_passes_shape():
    data = load_json(ROOT / "templates" / "qa_report.example.json")
    assert data["status"] == "passed"
    assert data["blocking_issues"] == []
    assert data["revision_required"] is False
