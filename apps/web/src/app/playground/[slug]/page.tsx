import { notFound } from "next/navigation";
import { PlaygroundWorkbench } from "@/components/playground-workbench";
import { Badge } from "@/components/ui";
import { algorithmBySlug, algorithms } from "@/lib/catalog";
export function generateStaticParams(){return algorithms.map(({slug})=>({slug}));}
export default async function PlaygroundPage({params}:{params:Promise<{slug:string}>}){const {slug}=await params;const algorithm=algorithmBySlug(slug);if(!algorithm)notFound();return <div className="page-stack"><header className="playground-header"><div><p className="eyebrow">Interactive playground</p><h1>{algorithm.title}</h1><p>{algorithm.shortDescription}</p></div><div><Badge tone="indigo">{algorithm.timeComplexity}</Badge><Badge>{algorithm.category}</Badge></div></header><PlaygroundWorkbench algorithm={algorithm}/></div>}
