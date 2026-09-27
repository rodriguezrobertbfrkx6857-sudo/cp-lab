import { ArrowRight, BarChart3, Binary, Boxes, Network, Sigma } from "lucide-react";
import Link from "next/link";
import { AlgorithmCard } from "@/components/algorithm-card";
import { Badge, Card, LinkButton } from "@/components/ui";
import { RecentBenchmarks } from "@/components/recent-benchmarks";
import { algorithms, benchmarkAlgorithms, categories } from "@/lib/catalog";

const categoryIcons = { "Number Theory": Sigma, Graph: Network, "Data Structures": Boxes, Fundamental: Binary };

export default function Dashboard() {
  const featured = ["dijkstra", "euler-linear-sieve", "segment-tree"].map((slug) => algorithms.find((item) => item.slug === slug)!);
  return <div className="page-stack dashboard">
    <section className="hero-card">
      <div className="hero-copy"><Badge tone="indigo">Interactive algorithm laboratory</Badge><h1>Explore algorithms.<br/><span>Understand every move.</span></h1><p>Run concrete inputs, inspect deterministic execution steps, and measure trusted C++20 and Python implementations.</p><div className="hero-actions"><LinkButton href="/algorithms">Explore algorithms <ArrowRight size={17}/></LinkButton><LinkButton href="/benchmark" secondary>Start benchmark <BarChart3 size={17}/></LinkButton></div></div>
      <div className="hero-visual" aria-label="Algorithm execution preview"><div className="execution-label"><span className="pulse-dot"/>Dijkstra · step 7 / 12</div><div className="graph-preview"><Node label="0" x="12%" y="44%" active/><Node label="1" x="42%" y="18%" visited/><Node label="2" x="42%" y="70%" visited/><Node label="3" x="75%" y="26%"/><Node label="4" x="78%" y="72%"/><svg viewBox="0 0 100 70" preserveAspectRatio="none"><path d="M15 34 L39 18 M15 34 L39 50 M45 18 L72 23 M45 50 L74 50 M44 20 L43 48"/></svg></div><div className="execution-footer"><span>frontier</span><strong>[1, 3, 4]</strong><span>distance</span><strong>6</strong></div></div>
    </section>
    <section className="metric-grid" aria-label="Project coverage"><Metric label="Algorithms" value={algorithms.length} note="curated and tested"/><Metric label="Interactive labs" value={algorithms.filter((item) => item.visualization).length} note="deterministic replay"/><Metric label="Benchmark adapters" value={benchmarkAlgorithms.length} note="real backend timing"/><Metric label="Languages" value={2} note="C++20 + Python"/></section>
    <section><div className="section-heading"><div><p className="eyebrow">Continue exploring</p><h2>Featured experiments</h2></div><Link href="/algorithms">View all <ArrowRight size={16}/></Link></div><div className="card-grid">{featured.map((item) => <AlgorithmCard key={item.slug} algorithm={item}/>)}</div></section>
    <section className="dashboard-split"><Card className="performance-card"><div className="section-heading compact"><div><p className="eyebrow">Performance overview</p><h2>Complexity at a glance</h2></div><Badge tone="green">Methodology first</Badge></div><div className="complexity-chart"><div className="chart-grid-lines"/><ComplexityLine name="O(log n)" width="30%" tone="indigo"/><ComplexityLine name="O(n)" width="57%" tone="cyan"/><ComplexityLine name="O(n log n)" width="78%" tone="green"/><ComplexityLine name="O(n²)" width="96%" tone="rose"/></div><p className="fine-print">Illustrative growth curves only. Measured results appear exclusively after a real benchmark run.</p></Card>
      <Card><div className="section-heading compact"><div><p className="eyebrow">Browse by family</p><h2>Algorithm categories</h2></div></div><div className="category-list">{(categories.slice(1) as (keyof typeof categoryIcons)[]).map((category) => { const Icon = categoryIcons[category]; const count = algorithms.filter((item) => item.category === category).length; return <Link key={category} href={`/algorithms?category=${encodeURIComponent(category)}`}><span className="category-icon"><Icon size={18}/></span><span><strong>{category}</strong><small>{count} algorithms</small></span><ArrowRight size={16}/></Link>; })}</div></Card>
    </section>
    <RecentBenchmarks/>
  </div>;
}

function Metric({ label, value, note }: { label: string; value: number; note: string }) { return <Card className="metric-card"><span>{label}</span><strong>{value.toString().padStart(2,"0")}</strong><small>{note}</small></Card>; }
function Node({ label, x, y, active, visited }: { label: string; x: string; y: string; active?: boolean; visited?: boolean }) { return <span className={`graph-node ${active ? "active" : ""} ${visited ? "visited" : ""}`} style={{ left: x, top: y }}>{label}</span>; }
function ComplexityLine({ name, width, tone }: { name: string; width: string; tone: string }) { return <div className="complexity-line"><span>{name}</span><i className={tone} style={{ width }}/></div>; }
