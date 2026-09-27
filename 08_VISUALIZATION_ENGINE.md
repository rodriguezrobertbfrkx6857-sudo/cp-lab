# Visualization Engine

## Architectural principle

Algorithms produce deterministic logical steps.
The UI renders those steps.

Do not tightly couple algorithm code to React animation state.

## Core model

Conceptual schema:

```ts
type VisualizationStep = {
  index: number;
  type: string;
  description: string;
  highlightedLines?: number[];
  variables?: Record<string, unknown>;
  arrayState?: ArrayState;
  graphState?: GraphState;
  treeState?: TreeState;
  metadata?: Record<string, unknown>;
};
```

## Example: Dijkstra relaxation

```json
{
  "index": 17,
  "type": "RELAX_EDGE",
  "description": "Relax edge 3 -> 5",
  "highlightedLines": [8, 9],
  "variables": {
    "u": 3,
    "v": 5,
    "weight": 4,
    "oldDistance": 15,
    "newDistance": 11
  }
}
```

## Playback state

Client playback state should include:

- currentStepIndex
- isPlaying
- playbackSpeed
- totalSteps

Playback is a projection over immutable steps.

## Determinism

Given the same:
- algorithm,
- input,
- seed,
- parameters,

the step sequence must be reproducible.

## Visualization categories

Array:
- active indices
- compared indices
- changed indices
- sorted/final indices

Graph:
- active node
- active edge
- frontier
- visited
- final path
- distances

Number theory:
- current divisor
- quotient/remainder
- factorization progress
- formula substitution
- modular state

Data structures:
- current node/index
- query/update range
- parent/root changes
- tree path / Fenwick traversal

## Performance

Avoid recomputing the full algorithm on each playback tick.
Generate once, render many.
