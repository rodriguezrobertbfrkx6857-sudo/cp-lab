import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { BenchmarkLab } from "@/components/benchmark-lab";

vi.mock("next/navigation", () => ({ useSearchParams: () => new URLSearchParams() }));
vi.mock("next/dynamic", () => ({ default: () => () => <div data-testid="chart" /> }));

describe("benchmark form", () => {
  it("prevents a run when no algorithm is selected", () => {
    render(<BenchmarkLab />);
    fireEvent.click(screen.getByLabelText("Merge Sort"));
    fireEvent.click(screen.getByLabelText("Quick Sort"));
    expect(screen.getByRole("button", { name: /Run benchmark/ })).toBeDisabled();
  });
});
