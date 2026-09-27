from __future__ import annotations

from fastapi.testclient import TestClient

from apps.api.main import app

client = TestClient(app)


def test_catalog_filters_and_detail() -> None:
    response = client.get("/algorithms")
    assert response.status_code == 200
    assert len(response.json()) == 20
    assert len(client.get("/algorithms", params={"category": "Graph"}).json()) == 4
    assert client.get("/algorithms", params={"query": "shortest path"}).json()
    detail = client.get("/algorithms/dijkstra")
    assert detail.status_code == 200
    assert "def dijkstra" in detail.json()["code"]["python"]
    assert "dijkstra(" in detail.json()["code"]["cpp"]
    missing = client.get("/algorithms/not-real")
    assert missing.status_code == 404
    assert missing.json()["error"]["code"] == "ALGORITHM_NOT_FOUND"


def test_visualization_is_deterministic_for_every_algorithm() -> None:
    for item in client.get("/algorithms").json():
        payload = {"algorithm": item["slug"], "input": None, "parameters": {}, "seed": 42}
        first = client.post("/visualize", json=payload)
        second = client.post("/visualize", json=payload)
        assert first.status_code == 200, (item["slug"], first.text)
        assert first.json() == second.json()
        assert first.json()["steps"][-1]["type"] == "COMPLETE"


def test_dijkstra_visualization_exposes_distances_and_final_shortest_path_tree() -> None:
    response = client.post("/visualize", json={"algorithm": "dijkstra", "input": None, "parameters": {"source": 0}, "seed": 42})
    assert response.status_code == 200
    visit_steps = [step for step in response.json()["steps"] if step["type"] == "VISIT_NODE"]
    assert visit_steps
    assert len(visit_steps[-1]["variables"]["distances"]) == 6
    assert visit_steps[-1]["graphState"]["finalPathEdges"]
    assert all(step["highlightedLines"] for step in visit_steps)


def test_visualization_validation_and_unknown_slug() -> None:
    malformed = client.post("/visualize", json={"algorithm": "UPPER CASE", "seed": -1})
    assert malformed.status_code == 422
    missing = client.post("/visualize", json={"algorithm": "not-real", "input": None, "parameters": {}, "seed": 42})
    assert missing.status_code == 404
    oversized = client.post("/visualize", json={"algorithm": "merge-sort", "input": list(range(501)), "parameters": {}, "seed": 42})
    assert oversized.status_code == 422
    invalid_graph = client.post("/visualize", json={"algorithm": "dijkstra", "input": {"nodes": 2, "edges": [[0, 3, 1]]}, "parameters": {}, "seed": 42})
    assert invalid_graph.status_code == 422


def test_real_python_benchmark_is_persisted() -> None:
    response = client.post("/benchmark", json={
        "algorithms": ["euclidean-gcd", "merge-sort"], "language": "python",
        "dataset": {"kind": "random", "size": 30, "min_value": 1, "max_value": 100, "density": 0.1},
        "warmups": 1, "measured_runs": 3, "seed": 42,
    })
    assert response.status_code == 200, response.text
    body = response.json()
    assert len(body["results"]) == 2
    assert all(len(result["samplesMs"]) == 3 for result in body["results"])
    assert client.get(f"/benchmark/{body['id']}").json() == body
    history = client.get("/benchmark-history/recent", params={"limit": 1})
    assert history.status_code == 200
    assert history.json()[0]["id"] == body["id"]


def test_all_builtin_benchmark_suites_are_declared_and_executable() -> None:
    suites = client.get("/benchmark-suites").json()
    assert len(suites) == 8
    for pair in suites.values():
        response = client.post("/benchmark", json={
            "algorithms": pair, "language": "python",
            "dataset": {"kind": "duplicate-heavy", "size": 12, "min_value": 1, "max_value": 20, "density": 0.1},
            "warmups": 0, "measured_runs": 3, "seed": 42,
        })
        assert response.status_code == 200, (pair, response.text)


def test_compare_and_benchmark_config_validation() -> None:
    compared = client.post("/compare", json={"algorithm_a": "merge-sort", "algorithm_b": "quick-sort"})
    assert compared.status_code == 200
    assert compared.json()["guidance"].startswith("Choose based")
    invalid = client.post("/benchmark", json={
        "algorithms": ["crt"], "language": "python",
        "dataset": {"kind": "random", "size": 0, "min_value": 10, "max_value": 1, "density": 0.1},
        "warmups": 50, "measured_runs": 1, "seed": -1,
    })
    assert invalid.status_code == 422


def test_cpp_benchmark_uses_compiled_runner() -> None:
    response = client.post("/benchmark", json={
        "algorithms": ["naive-gcd", "euclidean-gcd"], "language": "cpp",
        "dataset": {"kind": "random", "size": 12, "min_value": 1, "max_value": 100, "density": 0.1},
        "warmups": 1, "measured_runs": 3, "seed": 42,
    })
    assert response.status_code == 200, response.text
    assert response.json()["environment"]["buildMode"] == "C++20 -O2"
