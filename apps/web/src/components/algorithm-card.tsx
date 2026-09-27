import { ArrowUpRight, FlaskConical, Gauge } from "lucide-react";
import Link from "next/link";
import type { Algorithm } from "@/lib/catalog";
import { Badge, Card } from "./ui";

export function AlgorithmCard({ algorithm }: { algorithm: Algorithm }) {
  const tone = algorithm.category === "Number Theory" ? "indigo" : algorithm.category === "Graph" ? "cyan" : algorithm.category === "Data Structures" ? "green" : "amber";
  return <Card className="algorithm-card">
    <div className="algorithm-card-top"><Badge tone={tone}>{algorithm.category}</Badge><span className="difficulty">{algorithm.difficulty}</span></div>
    <div><h3><Link href={`/algorithms/${algorithm.slug}`}>{algorithm.title}</Link></h3><p>{algorithm.shortDescription}</p></div>
    <div className="algorithm-meta"><span><Gauge size={15}/>{algorithm.timeComplexity}</span>{algorithm.visualization && <span><FlaskConical size={15}/>Interactive</span>}</div>
    <div className="algorithm-card-footer"><div><Badge>C++20</Badge><Badge>Python</Badge></div><Link href={`/algorithms/${algorithm.slug}`} aria-label={`Open ${algorithm.title}`}><ArrowUpRight size={18}/></Link></div>
  </Card>;
}
