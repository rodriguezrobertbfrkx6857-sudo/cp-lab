from __future__ import annotations

import random
from typing import Any

from algorithms.python import cp_algorithms as alg


def _step(steps: list[dict[str, Any]], kind: str, description: str, *, lines: list[int] | None = None,
          variables: dict[str, Any] | None = None, array: dict[str, Any] | None = None,
          graph: dict[str, Any] | None = None, tree: dict[str, Any] | None = None) -> None:
    steps.append({
        "index": len(steps), "type": kind, "description": description,
        "highlightedLines": lines or [], "variables": variables or {},
        "arrayState": array, "graphState": graph, "treeState": tree, "metadata": {},
    })


def visualize(slug: str, raw_input: Any, parameters: dict[str, Any], seed: int) -> dict[str, Any]:
    _validate_visual_input(raw_input, parameters)
    rng = random.Random(seed)
    steps: list[dict[str, Any]] = []
    if slug == "euclidean-gcd":
        a, b = _pair(raw_input, 48, 18)
        _step(steps, "INITIALIZE", "Start with the two integers.", lines=[1], variables={"a": a, "b": b})
        while b:
            remainder = a % b
            _step(steps, "REMAINDER", f"{a} mod {b} = {remainder}", lines=[3, 4], variables={"a": a, "b": b, "remainder": remainder})
            a, b = b, remainder
        result: Any = abs(a)
    elif slug == "extended-gcd":
        a, b = _pair(raw_input, 30, 18); old_r, r, old_s, s, old_t, t = a, b, 1, 0, 0, 1
        _step(steps, "INITIALIZE", "Initialize remainder and coefficient rows.", lines=[1], variables=locals_snapshot(old_r, r, old_s, s, old_t, t))
        while r:
            q = old_r // r
            _step(steps, "ELIMINATE", f"Subtract {q} times the current row.", lines=[3, 4], variables={"quotient": q, **locals_snapshot(old_r, r, old_s, s, old_t, t)})
            old_r, r, old_s, s, old_t, t = r, old_r-q*r, s, old_s-q*s, t, old_t-q*t
        result = {"gcd": abs(old_r), "x": old_s if old_r >= 0 else -old_s, "y": old_t if old_r >= 0 else -old_t}
    elif slug == "binary-exponentiation":
        values = _list(raw_input, [3, 13, 100]); base, exponent = values[:2]; modulus = values[2] if len(values) > 2 else int(parameters.get("modulus", 1_000_000_007)); answer = 1 % modulus; base %= modulus
        _step(steps, "INITIALIZE", "Initialize accumulator and reduced base.", lines=[1, 2], variables={"base": base, "exponent": exponent, "result": answer, "modulus": modulus})
        while exponent:
            if exponent & 1:
                answer = answer * base % modulus; _step(steps, "MULTIPLY", "The current exponent bit is 1; multiply it into the answer.", lines=[4], variables={"base": base, "exponent": exponent, "result": answer})
            base = base * base % modulus; exponent >>= 1
            _step(steps, "SQUARE", "Square the base and shift to the next exponent bit.", lines=[5, 6], variables={"base": base, "exponent": exponent, "result": answer})
        result = answer
    elif slug in {"prime-factorization", "euler-phi"}:
        value = _scalar(raw_input, 360 if slug == "prime-factorization" else 36); remaining = value; factors: list[list[int]] = []
        divisor = 2
        while divisor * divisor <= remaining:
            exponent = 0
            _step(steps, "TRY_DIVISOR", f"Try divisor {divisor}.", lines=[3], variables={"divisor": divisor, "remaining": remaining})
            while remaining % divisor == 0:
                remaining //= divisor; exponent += 1
                _step(steps, "DIVIDE", f"Remove one factor of {divisor}.", lines=[5], variables={"divisor": divisor, "remaining": remaining, "exponent": exponent})
            if exponent: factors.append([divisor, exponent])
            divisor += 1 if divisor == 2 else 2
        if remaining > 1: factors.append([remaining, 1]); _step(steps, "FINAL_PRIME", f"The remainder {remaining} is prime.", lines=[8], variables={"remaining": remaining})
        result = factors if slug == "prime-factorization" else alg.euler_phi(value)
    elif slug in {"eratosthenes-sieve", "euler-linear-sieve"}:
        limit = min(_scalar(raw_input, 30), 200); marked = [False] * (limit + 1); primes: list[int] = []
        for value in range(2, limit + 1):
            if not marked[value]:
                primes.append(value); _step(steps, "DISCOVER_PRIME", f"{value} is prime.", lines=[3], variables={"prime": value}, array={"values": list(range(limit + 1)), "activeIndices": [value], "changedIndices": [], "sortedIndices": primes[:]})
            if slug == "eratosthenes-sieve" and not marked[value] and value * value <= limit:
                changed = list(range(value * value, limit + 1, value));
                for multiple in changed: marked[multiple] = True
                _step(steps, "MARK_MULTIPLES", f"Mark multiples of {value}.", lines=[5], variables={"prime": value}, array={"values": list(range(limit + 1)), "activeIndices": [value], "changedIndices": changed, "sortedIndices": primes[:]})
            elif slug == "euler-linear-sieve":
                for prime in primes:
                    if value * prime > limit: break
                    marked[value * prime] = True; _step(steps, "MARK_ONCE", f"Mark {value * prime} using smallest prime {prime}.", lines=[6, 7], variables={"value": value, "prime": prime}, array={"values": list(range(limit + 1)), "activeIndices": [value], "changedIndices": [value * prime], "sortedIndices": primes[:]})
                    if value % prime == 0: break
        result = primes
    elif slug == "modular-inverse":
        value, modulus = _pair(raw_input, 3, 11); inverse = alg.modular_inverse(value, modulus)
        _step(steps, "BEZOUT", "Extended GCD produces a coefficient for the value.", lines=[1, 2], variables={"value": value, "modulus": modulus, "gcd": 1})
        _step(steps, "NORMALIZE", f"Normalize the coefficient modulo {modulus}.", lines=[4], variables={"inverse": inverse})
        result = inverse
    elif slug == "combination":
        n, k = _pair(raw_input, 8, 3); row = [1] + [0] * k
        _step(steps, "INITIALIZE", "Start Pascal's row with C(0,0)=1.", lines=[1], array={"values": row[:]})
        for current in range(1, n + 1):
            for choice in range(min(current, k), 0, -1): row[choice] += row[choice-1]
            _step(steps, "ROW", f"Complete Pascal row {current}.", lines=[3,4], variables={"n": current}, array={"values": row[:], "activeIndices": list(range(min(current,k)+1))})
        result = row[k] if 0 <= k <= n else 0
    elif slug == "crt":
        congruences = raw_input if isinstance(raw_input, list) and raw_input and isinstance(raw_input[0], list) else [[2,3],[3,5]]
        residue, modulus = 0, 1
        for next_residue, next_modulus in congruences:
            _step(steps, "MERGE", f"Merge x ≡ {next_residue} (mod {next_modulus}).", lines=[2,3], variables={"residue": residue, "modulus": modulus, "nextResidue": next_residue, "nextModulus": next_modulus})
            residue, modulus = alg.chinese_remainder([[residue, modulus], [int(next_residue), int(next_modulus)]])
        result = {"residue": residue, "modulus": modulus}
    elif slug in {"bfs", "dfs", "dijkstra", "topological-sort"}:
        nodes, edges = _graph(raw_input, weighted=slug == "dijkstra"); source = int(parameters.get("source", 0)); visited: list[int] = []
        if slug == "dijkstra":
            graph = [[] for _ in range(nodes)]
            for edge in edges: graph[edge[0]].append((edge[1], edge[2])); graph[edge[1]].append((edge[0], edge[2]))
            result = alg.dijkstra(graph, source); order = sorted(range(nodes), key=lambda node: (result[node] is None, result[node] or 0))
            final_path_edges: list[list[int]] = []
            for node in range(nodes):
                if node == source or result[node] is None:
                    continue
                parent = next((neighbor for neighbor, weight in graph[node] if result[neighbor] is not None and result[neighbor] + weight == result[node]), None)
                if parent is not None:
                    final_path_edges.append([parent, node])
        else:
            graph = [[] for _ in range(nodes)]
            for edge in edges: graph[edge[0]].append(edge[1]);
            if slug not in {"topological-sort"}:
                for edge in edges: graph[edge[1]].append(edge[0])
            if slug == "bfs": result, _ = alg.bfs(graph, source); order = result
            elif slug == "dfs": result = alg.dfs(graph, source); order = result
            else: result = alg.topological_sort(graph); order = result
        for node in order:
            visited.append(node)
            variables = {"currentNode": node, "visitedCount": len(visited)}
            graph_state: dict[str, Any] = {"nodeCount": nodes, "edges": edges, "activeNode": node, "visited": visited[:]}
            if slug == "dijkstra":
                variables.update({"currentDistance": result[node], "distances": result})
                graph_state["finalPathEdges"] = final_path_edges if len(visited) == len(order) else []
            _step(steps, "VISIT_NODE", f"Visit node {node}.", lines=[3,4], variables=variables, graph=graph_state)
    elif slug == "dsu":
        size = int(parameters.get("size", 8)); operations = raw_input if isinstance(raw_input, list) and raw_input else [[0,1],[1,2],[4,5],[2,5]]; dsu = alg.DisjointSetUnion(size)
        for left, right in operations:
            changed = dsu.union(int(left), int(right)); _step(steps, "UNION", f"Union {left} and {right}{'' if changed else ' (already connected)'}.", lines=[3,4], variables={"left": left, "right": right}, tree={"parents": dsu.parent[:]})
        result = dsu.parent
    elif slug in {"fenwick-tree", "segment-tree"}:
        values = _list(raw_input, [2,1,4,3,5,7]); structure = alg.FenwickTree(values) if slug == "fenwick-tree" else alg.SegmentTree(values)
        _step(steps, "BUILD", f"Build the {slug.replace('-', ' ')}.", lines=[1,2], array={"values": values[:]}, tree={"values": structure.tree[:]})
        for index in range(len(values)):
            total = structure.prefix_sum(index) if slug == "fenwick-tree" else structure.range_sum(0,index+1)
            _step(steps, "QUERY", f"Read prefix ending at index {index}.", lines=[4,5], variables={"index": index, "prefixSum": total}, array={"values": values[:], "activeIndices": list(range(index+1))}, tree={"values": structure.tree[:]})
        result = [structure.prefix_sum(i) if slug == "fenwick-tree" else structure.range_sum(0,i+1) for i in range(len(values))]
    elif slug in {"binary-search", "merge-sort", "quick-sort"}:
        values = _list(raw_input, [7,2,9,1,5,3]);
        if slug == "binary-search":
            values.sort(); target = int(parameters.get("target", values[len(values)//2])); low, high = 0, len(values)-1; result = -1
            while low <= high:
                middle = (low+high)//2; _step(steps, "COMPARE", f"Compare target {target} with index {middle}.", lines=[3], variables={"low": low, "middle": middle, "high": high, "target": target}, array={"values": values[:], "activeIndices": [middle], "comparedIndices": list(range(low,high+1))})
                if values[middle] == target: result = middle; break
                if values[middle] < target: low = middle+1
                else: high = middle-1
        else:
            working = values[:]; _step(steps, "INITIALIZE", "Load the input array.", lines=[1], array={"values": working[:]})
            if slug == "merge-sort":
                width = 1
                while width < len(working):
                    for start in range(0,len(working),2*width):
                        end=min(start+2*width,len(working)); working[start:end]=sorted(working[start:end]); _step(steps,"MERGE",f"Merge interval [{start},{end}).",lines=[3,4],variables={"width":width},array={"values":working[:],"changedIndices":list(range(start,end))})
                    width*=2
            else:
                target = sorted(working)
                for index, desired in enumerate(target):
                    current = working.index(desired,index); working[index],working[current]=working[current],working[index]; _step(steps,"PARTITION",f"Place {desired} at index {index}.",lines=[4,5],variables={"pivot":desired},array={"values":working[:],"activeIndices":[index],"changedIndices":[index,current]})
            result = working
    else:
        raise KeyError(slug)
    _step(steps, "COMPLETE", "Algorithm complete.", lines=[], variables={"result": result})
    return {"normalizedInput": raw_input, "steps": steps, "finalResult": result, "seed": seed}


def _scalar(value: Any, default: int) -> int:
    if isinstance(value, (int, float)): return int(value)
    if isinstance(value, list) and value: return int(value[0])
    return default


def _pair(value: Any, left: int, right: int) -> tuple[int, int]:
    values = _list(value, [left, right]); return int(values[0]), int(values[1])


def _list(value: Any, default: list[int]) -> list[int]:
    return [int(item) for item in value] if isinstance(value, list) and len(value) >= 2 else default[:]


def _graph(value: Any, weighted: bool) -> tuple[int, list[list[int]]]:
    if isinstance(value, dict) and isinstance(value.get("edges"), list):
        edges = [[int(part) for part in edge] for edge in value["edges"]]
        nodes = int(value.get("nodes", max(max(edge[:2]) for edge in edges)+1 if edges else 1))
        expected_parts = 3 if weighted else 2
        if not 1 <= nodes <= 100:
            raise ValueError("graph node count must be between 1 and 100")
        if len(edges) > 500 or any(len(edge) != expected_parts for edge in edges):
            raise ValueError(f"graph edges must contain at most 500 entries with {expected_parts} values each")
        if any(not 0 <= endpoint < nodes for edge in edges for endpoint in edge[:2]):
            raise ValueError("graph edge endpoint is out of range")
        if weighted and any(edge[2] < 0 or edge[2] > 1_000_000 for edge in edges):
            raise ValueError("graph weights must be between 0 and 1000000")
        return nodes, edges
    return (6, [[0,1,4],[0,2,1],[2,1,2],[1,3,1],[2,4,5],[3,5,3],[4,5,1]] if weighted else [[0,1],[0,2],[1,3],[2,4],[3,5],[4,5]])


def _validate_visual_input(value: Any, parameters: dict[str, Any]) -> None:
    if len(parameters) > 20:
        raise ValueError("too many visualization parameters")
    if isinstance(value, list) and len(value) > 500:
        raise ValueError("visualization input may contain at most 500 items")
    if isinstance(value, dict) and len(value) > 20:
        raise ValueError("visualization input object has too many fields")
    def inspect(item: Any, depth: int = 0) -> None:
        if depth > 5:
            raise ValueError("visualization input nesting is too deep")
        if isinstance(item, (int, float)) and abs(item) > 10**12:
            raise ValueError("visualization numeric input exceeds the supported bound")
        if isinstance(item, list):
            for child in item:
                inspect(child, depth + 1)
        elif isinstance(item, dict):
            for child in item.values():
                inspect(child, depth + 1)
    inspect(value)


def locals_snapshot(old_r: int, r: int, old_s: int, s: int, old_t: int, t: int) -> dict[str, int]:
    return {"oldR": old_r, "r": r, "oldS": old_s, "s": s, "oldT": old_t, "t": t}
