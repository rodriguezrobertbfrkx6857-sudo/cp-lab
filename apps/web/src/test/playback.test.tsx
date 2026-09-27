import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { PlaygroundWorkbench } from "@/components/playground-workbench";
import { algorithmBySlug } from "@/lib/catalog";

describe("playback controls", () => {
  afterEach(() => vi.restoreAllMocks());
  it("loads deterministic steps and advances", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, json: async () => ({ normalizedInput:[48,18], seed:42, finalResult:6, steps:[
      {index:0,type:"INITIALIZE",description:"Start.",highlightedLines:[1],variables:{a:48,b:18},arrayState:null,graphState:null,treeState:null},
      {index:1,type:"REMAINDER",description:"Continue.",highlightedLines:[3],variables:{a:18,b:12},arrayState:null,graphState:null,treeState:null},
      {index:2,type:"COMPLETE",description:"Done.",highlightedLines:[],variables:{result:6},arrayState:null,graphState:null,treeState:null},
    ] }) }));
    render(<PlaygroundWorkbench algorithm={algorithmBySlug("euclidean-gcd")!} />);
    await waitFor(() => expect(screen.getByText("Start.")).toBeInTheDocument());
    fireEvent.click(screen.getByRole("button", { name: "Next step" }));
    expect(screen.getByText("Continue.")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Last step" }));
    expect(screen.getByText("Done.")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Previous step" }));
    expect(screen.getByText("Continue.")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "First step" }));
    expect(screen.getByText("Start.")).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText("Visualization timeline"), { target: { value: "2" } });
    expect(screen.getByText("Done.")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Restart" }));
    expect(screen.getByText("Start.")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "2×" }));
    expect(screen.getByRole("button", { name: "2×" })).toHaveClass("active");
    fireEvent.click(screen.getByRole("button", { name: "Play" }));
    expect(screen.getByRole("button", { name: "Pause" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Pause" }));
    expect(screen.getByRole("button", { name: "Play" })).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText("Input (JSON)"), { target: { value: "[1, 1]" } });
    fireEvent.click(screen.getByRole("button", { name: "Reset" }));
    expect(screen.getByLabelText("Input (JSON)" )).toHaveValue("[\n  48,\n  18\n]");
  });
});
