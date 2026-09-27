# Page Specifications

## 1. Dashboard `/`

Purpose: make the project immediately understandable and visually credible.

### Hero

Copy direction:

> Explore algorithms. Understand how they work. Measure how they perform.

Primary actions:
- Explore Algorithms
- Start Benchmark

### Truthful stats

Display only counts derived from actual project metadata, for example:
- Algorithms: 20
- Interactive Labs: derived from metadata
- Benchmark Suites: derived from metadata
- Languages: 2

Do not fabricate usage counts.

### Sections

- Continue Exploring
- Performance Overview
- Algorithm Categories
- Recent Benchmark
- Featured Experiment

---

## 2. Algorithm Explorer `/algorithms`

### Controls

Search:
- title
- description
- tags

Filters:
- category
- difficulty
- time complexity bucket
- language
- visualization availability
- benchmark availability

Sort:
- alphabetical
- category
- difficulty

### Algorithm card

Show:
- title
- category
- one-line description
- time complexity
- supported languages
- visualization badge if available
- benchmark badge if available
- Open Algorithm action

Avoid dense spreadsheet-like cards.

---

## 3. Algorithm Detail `/algorithms/[slug]`

Sections:

1. Overview
2. Intuition
3. Mathematical / conceptual derivation
4. Complexity
5. Implementation tabs
6. Example
7. Related algorithms

Top actions:
- Open Playground
- Benchmark
- Compare

Code tabs:
- C++
- Python

Features:
- copy code
- line numbers
- syntax highlighting
- direct link to playground

---

## 4. Playground `/playground/[slug]`

Desktop composition:

```txt
┌──────────────────────────────────────────────┐
│ Algorithm header / controls                  │
├────────────┬────────────────────┬────────────┤
│ Input      │ Visualization      │ State      │
│ Controls   │ Canvas             │ Inspector  │
├────────────┴────────────────────┴────────────┤
│ Timeline / playback / highlighted code       │
└──────────────────────────────────────────────┘
```

### Input panel

Algorithm-specific parameters:
- input values,
- graph size,
- source / target,
- seed,
- randomize,
- reset.

### Visualization canvas

Must be state-driven, not hand-animated separately from algorithm execution.

### State inspector

Examples:
- current node
- queue / stack
- distances
- visited count
- operations
- current interval
- current factor
- current pivot

### Playback

- first step
- previous
- play
- pause
- next
- last
- restart
- 0.5x
- 1x
- 2x
- step X / Y

### Code

Current logical line should be highlighted according to visualization-step metadata.

---

## 5. Benchmark Lab `/benchmark`

Configuration:
- algorithm(s)
- language
- input size
- iterations
- warmup
- dataset generator
- seed
- generator-specific options

Results:
- runtime
- memory where measurable and trustworthy
- operations where instrumented
- median
- min
- max
- P95
- environment metadata

Charts:
- runtime line chart
- memory bar chart
- operation-count line chart where available

Clearly distinguish browser measurements from backend measurements.

---

## 6. Compare `/compare`

Select Algorithm A and Algorithm B.

Sections:
- conceptual summary
- complexity
- implementation comparison
- runtime chart
- memory chart if supported
- operation chart if supported
- code comparison
- "When to use each"

Do not hard-code a universal "winner". Explain trade-offs.

---

## 7. Docs `/docs`

Include:
- product overview
- visualization model
- benchmark methodology
- architecture
- adding an algorithm
- running locally
- API summary

---

## 8. About `/about`

Short page:
- project mission
- technology
- open-source contribution invitation
- repository link
