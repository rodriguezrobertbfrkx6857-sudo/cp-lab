import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { AlgorithmExplorer } from "@/components/algorithm-explorer";

vi.mock("next/navigation", () => ({ useSearchParams: () => new URLSearchParams() }));

describe("algorithm explorer", () => {
  beforeEach(() => render(<AlgorithmExplorer />));

  it("searches titles and descriptions", () => {
    fireEvent.change(screen.getByLabelText("Search algorithms"), { target: { value: "Dijkstra" } });
    expect(screen.getByRole("heading", { name: "Dijkstra" })).toBeInTheDocument();
    expect(screen.queryByRole("heading", { name: "Merge Sort" })).not.toBeInTheDocument();
  });

  it("shows a designed empty state", () => {
    fireEvent.change(screen.getByLabelText("Search algorithms"), { target: { value: "not-an-algorithm" } });
    expect(screen.getByRole("heading", { name: "No algorithms match" })).toBeInTheDocument();
  });
});
