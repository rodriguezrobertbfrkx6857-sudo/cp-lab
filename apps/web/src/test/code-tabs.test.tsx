import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { CodeTabs } from "@/components/code-tabs";

describe("code tabs", () => {
  it("switches language and copies the selected source", async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.assign(navigator, { clipboard: { writeText } });
    render(<CodeTabs cpp="int main() {}" python="print('ok')" />);
    fireEvent.click(screen.getByRole("button", { name: "Python" }));
    expect(screen.getByText("print('ok')")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Copy code" }));
    expect(writeText).toHaveBeenCalledWith("print('ok')");
  });
});
