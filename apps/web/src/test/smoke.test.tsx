import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import Home from "@/app/page";

describe("home", () => {
  it("presents the product promise", () => {
    render(<Home />);
    expect(screen.getByRole("heading", { name: /Explore algorithms/ })).toBeInTheDocument();
    expect(screen.getByText(/trusted C\+\+20 and Python implementations/)).toBeInTheDocument();
  });
});
