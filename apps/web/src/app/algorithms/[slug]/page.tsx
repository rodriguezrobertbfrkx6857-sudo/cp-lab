import { ArrowRight, BarChart3, FlaskConical } from "lucide-react";
import { notFound } from "next/navigation";
import Link from "next/link";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { AlgorithmCard } from "@/components/algorithm-card";
import { CodeTabs } from "@/components/code-tabs";
import { Badge, Card, LinkButton } from "@/components/ui";
import { algorithmBySlug, algorithms } from "@/lib/catalog";

const names: Record<string,string> = { "euclidean-gcd":"euclidean_gcd", "extended-gcd":"extended_gcd", "binary-exponentiation":"binary_exponentiation", "modular-inverse":"modular_inverse", "prime-factorization":"prime_factorization", "eratosthenes-sieve":"eratosthenes_sieve", "euler-linear-sieve":"euler_linear_sieve", "euler-phi":"euler_phi", combination:"combination", crt:"chinese_remainder", bfs:"bfs", dfs:"dfs", dijkstra:"dijkstra", "topological-sort":"topological_sort", dsu:"DisjointSetUnion", "fenwick-tree":"FenwickTree", "segment-tree":"SegmentTree", "binary-search":"binary_search", "merge-sort":"merge_sort", "quick-sort":"quick_sort" };
export function generateStaticParams() { return algorithms.map(({slug}) => ({slug})); }

export default async function AlgorithmDetail({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params; const algorithm = algorithmBySlug(slug); if (!algorithm) notFound();
  const root = path.resolve(process.cwd(), "../.."); const [pythonAll, cppAll] = await Promise.all([readFile(path.join(root,"algorithms/python/cp_algorithms.py"),"utf8"), readFile(path.join(root,"algorithms/cpp/include/cp_algorithms.hpp"),"utf8")]);
  const related = algorithm.relatedAlgorithms.map((item) => algorithmBySlug(item)).filter(Boolean).slice(0,3);
  return <article className="page-stack detail-page"><div className="breadcrumbs"><Link href="/algorithms">Algorithms</Link><span>/</span><span>{algorithm.category}</span><span>/</span><strong>{algorithm.title}</strong></div>
    <header className="detail-hero"><div><Badge tone="indigo">{algorithm.category}</Badge><h1>{algorithm.title}</h1><p>{algorithm.shortDescription}</p><div className="tag-row">{algorithm.tags.map((tag) => <Badge key={tag}>{tag}</Badge>)}</div></div><div className="detail-actions"><LinkButton href={`/playground/${algorithm.slug}`}><FlaskConical size={17}/>Open Playground</LinkButton>{algorithm.benchmark && <LinkButton href={`/benchmark?algorithm=${algorithm.slug}`} secondary><BarChart3 size={17}/>Benchmark</LinkButton>}<LinkButton href={`/compare?a=${algorithm.slug}`} secondary>Compare</LinkButton></div></header>
    <section className="complexity-strip"><div><span>Time complexity</span><strong>{algorithm.timeComplexity}</strong></div><div><span>Space complexity</span><strong>{algorithm.spaceComplexity}</strong></div><div><span>Difficulty</span><strong>{algorithm.difficulty}</strong></div><div><span>Languages</span><strong>C++20 · Python</strong></div></section>
    <div className="detail-layout"><div className="article-flow"><section><p className="eyebrow">Overview</p><h2>Intuition</h2><p>{algorithm.intuition}</p></section><section><p className="eyebrow">Why it works</p><h2>Conceptual derivation</h2><p>{algorithm.derivation}</p></section><section><p className="eyebrow">Implementation</p><h2>Production-ready reference</h2><p>The same trusted implementation is exercised by the repository test suite and backend adapters.</p><CodeTabs python={extract(pythonAll,names[slug],"python")} cpp={extract(cppAll,names[slug],"cpp")}/></section></div>
      <aside className="detail-aside"><Card><p className="eyebrow">Worked example</p><dl><dt>Input</dt><dd><code>{algorithm.exampleInput}</code></dd><dt>Output</dt><dd><code>{algorithm.exampleOutput}</code></dd></dl></Card><Card><p className="eyebrow">Edge cases</p><ul>{algorithm.edgeCases.map((item) => <li key={item}>{item}</li>)}</ul></Card></aside></div>
    <section><div className="section-heading"><div><p className="eyebrow">Keep learning</p><h2>Related algorithms</h2></div><Link href="/algorithms">Explore catalog <ArrowRight size={16}/></Link></div><div className="card-grid">{related.map((item) => item && <AlgorithmCard key={item.slug} algorithm={item}/>)}</div></section>
  </article>;
}

function extract(source: string, name: string, language: "python" | "cpp") {
  const lines = source.split("\n"); const pattern = language === "python" ? new RegExp(`^(def|class) ${name}\\b`) : new RegExp(`(class ${name}\\b|\\b${name}\\()`); const start = lines.findIndex((line) => pattern.test(line)); if (start < 0) return source;
  if (language === "python") { let end = start+1; while (end < lines.length && (lines[end].startsWith(" ") || !lines[end].trim())) end++; return lines.slice(start,end).join("\n").trim(); }
  let depth = 0, began = false, end = start; for (; end < lines.length; end++) { for (const char of lines[end]) { if (char === "{") { depth++; began = true; } if (char === "}") depth--; } if (began && depth === 0) { end++; break; } } return lines.slice(start,end).join("\n").trim();
}
