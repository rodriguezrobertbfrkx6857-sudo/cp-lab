# Information Architecture

## Global navigation

Primary sidebar:

- Dashboard
- Algorithms
- Playground
- Benchmark
- Compare

Secondary:

- Documentation
- GitHub

## Global header

- current page title
- global search
- command palette trigger
- GitHub link
- settings / display preferences

## Command palette

Keyboard shortcut:

- `Ctrl + K`
- `Cmd + K`

Search targets:
- algorithms,
- categories,
- Benchmark Lab,
- Playground,
- Compare,
- Documentation.

## Routes

```txt
/
 /algorithms
 /algorithms/[slug]
 /playground
 /playground/[slug]
 /benchmark
 /compare
 /docs
 /about
```

## Error/utility states

- 404
- 500
- loading skeletons
- empty benchmark state
- benchmark failure state
- unsupported visualization state
- API unavailable state

## Desktop shell

Recommended:
- 72px collapsed sidebar
- optional expanded sidebar around 220px
- sticky top header
- main content max width around 1600px
- generous page gutters
