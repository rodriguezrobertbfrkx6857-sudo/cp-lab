import { Activity } from "lucide-react";
import { AlgorithmCard } from "@/components/algorithm-card";
import { PageHeader } from "@/components/ui";
import { algorithms } from "@/lib/catalog";
export default function PlaygroundIndex(){return <div className="page-stack"><PageHeader eyebrow="Experiment" title="Playground" description="Choose an algorithm to generate and replay its deterministic execution state." actions={<Activity size={28}/>}/><div className="card-grid">{algorithms.map((item)=><AlgorithmCard key={item.slug} algorithm={item}/>)}</div></div>}
