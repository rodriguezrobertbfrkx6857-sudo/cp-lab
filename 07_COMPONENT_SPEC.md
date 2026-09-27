# Component Specification

## Core reusable components

Application:
- AppShell
- Sidebar
- TopHeader
- CommandPalette
- PageHeader
- Breadcrumbs

Cards:
- MetricCard
- AlgorithmCard
- BenchmarkCard
- CategoryCard
- EmptyStateCard
- ErrorStateCard

Algorithm:
- ComplexityBadge
- LanguageBadge
- DifficultyBadge
- CodeTabs
- CodeViewer
- RelatedAlgorithmCard

Playground:
- ControlPanel
- VisualizationCanvas
- StateInspector
- PlaybackControls
- Timeline
- StepDescription
- CodeExecutionPanel

Benchmark:
- BenchmarkConfigurator
- DatasetConfigurator
- BenchmarkSummary
- RuntimeChart
- MemoryChart
- OperationsChart
- EnvironmentCard

Forms:
- Select
- NumberInput
- Slider
- Toggle
- SegmentedControl
- Button
- IconButton
- Tooltip

Feedback:
- Skeleton
- Toast
- InlineError
- ErrorBoundary
- EmptyState

## Component requirements

- semantic markup,
- keyboard accessibility,
- shared tokens,
- no page-specific one-off styling where a reusable primitive fits,
- tests for interaction-heavy components.
