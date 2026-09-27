# Frontend Specification

## Stack

- Next.js
- React
- TypeScript
- Tailwind CSS
- Framer Motion
- ECharts
- React Flow
- Lucide

## Frontend goals

- clean modern B2B/developer-tool interface
- fast navigation
- excellent desktop experience
- usable tablet/mobile fallbacks
- cohesive design system

## State

Use local/component state where sufficient.
Avoid introducing heavy global state management without a clear need.

Candidate global/shared state:
- command palette
- UI preferences
- current playground session
- benchmark configuration draft

## Data fetching

Use typed API clients.
Handle:
- loading
- success
- empty
- error
- retry

## Responsive behavior

Desktop `1440+`:
- optimal full workbench

Laptop `1024–1439`:
- full feature support

Tablet `768–1023`:
- reflow panels

Mobile `<768`:
- browsing fully supported
- playground stacks:
  1. visualization
  2. controls
  3. state
  4. timeline/code

## Accessibility

- semantic HTML
- keyboard navigation
- ARIA labels
- visible focus
- sufficient contrast
- reduced motion
