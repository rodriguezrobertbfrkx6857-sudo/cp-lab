# Design Tokens

Suggested token map:

```ts
export const tokens = {
  color: {
    bg: "#F5F7FA",
    surface: "#FFFFFF",
    textPrimary: "#111318",
    textSecondary: "#69717D",
    border: "rgba(17,24,39,0.08)"
  },
  radius: {
    card: 20,
    control: 12,
    small: 8
  },
  motion: {
    fast: 180,
    normal: 220,
    slow: 240
  },
  layout: {
    sidebarCollapsed: 72,
    maxContentWidth: 1600
  }
}
```

Accent colors should be implemented as a restrained palette rather than hard-coded ad hoc values.
