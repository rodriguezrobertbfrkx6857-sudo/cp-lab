"use client";

import { ArrowRight, Clock3 } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";
import { apiRequest } from "@/lib/api";
import { Badge, Card } from "./ui";

type Run = { id:string; results:{algorithm:string;language:string;medianMs:number}[]; environment:{timestamp:string;seed:number;language:string}; dataset:{kind:string;size:number} };

export function RecentBenchmarks() {
  const [runs, setRuns] = useState<Run[] | null>(null);
  const [unavailable, setUnavailable] = useState(false);
  useEffect(() => {
    apiRequest<Run[]>("/benchmark-history/recent?limit=3").then(setRuns).catch(() => setUnavailable(true));
  }, []);
  return <Card className="recent-benchmarks">
    <div className="section-heading compact"><div><p className="eyebrow">Measured history</p><h2>Recent benchmarks</h2></div><Link href="/benchmark">Open lab <ArrowRight size={16}/></Link></div>
    {runs === null && !unavailable && <span className="skeleton recent-skeleton" aria-label="Loading recent benchmarks"/>}
    {unavailable && <p className="fine-print">Benchmark history is temporarily unavailable. The rest of the catalog remains fully browsable.</p>}
    {runs?.length === 0 && <p className="fine-print">No measured runs yet. Start a trusted benchmark to create the first persisted record.</p>}
    {runs?.map((run) => <div className="recent-run" key={run.id}><span className="recent-run-icon"><Clock3 size={17}/></span><span><strong>{run.results.map((item)=>item.algorithm).join(" · ")}</strong><small>{run.dataset.kind} · n={run.dataset.size} · seed {run.environment.seed}</small></span><span><Badge tone="green">{run.environment.language}</Badge><small>{Math.min(...run.results.map((item)=>item.medianMs)).toFixed(3)} ms min median</small></span></div>)}
  </Card>;
}
