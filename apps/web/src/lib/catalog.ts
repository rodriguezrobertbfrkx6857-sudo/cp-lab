import catalogData from "../../../../packages/catalog/algorithms.json";

export type Algorithm = {
  slug: string;
  title: string;
  category: "Number Theory" | "Graph" | "Data Structures" | "Fundamental";
  difficulty: "Beginner" | "Intermediate" | "Advanced";
  shortDescription: string;
  intuition: string;
  derivation: string;
  timeComplexity: string;
  spaceComplexity: string;
  languages: ("cpp" | "python")[];
  visualization: boolean;
  benchmark: boolean;
  tags: string[];
  exampleInput: string;
  exampleOutput: string;
  edgeCases: string[];
  relatedAlgorithms: string[];
};

export const algorithms = catalogData as Algorithm[];
export const algorithmBySlug = (slug: string) => algorithms.find((item) => item.slug === slug);
export const categories = ["All", "Number Theory", "Graph", "Data Structures", "Fundamental"] as const;
export const benchmarkAlgorithms = algorithms.filter((algorithm) => algorithm.benchmark);
