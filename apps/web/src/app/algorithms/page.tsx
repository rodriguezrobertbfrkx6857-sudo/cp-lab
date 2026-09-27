import { Suspense } from "react";
import { AlgorithmExplorer } from "@/components/algorithm-explorer";
import { PageHeader, Skeleton } from "@/components/ui";
export default function AlgorithmsPage() { return <div className="page-stack"><PageHeader eyebrow="Catalog" title="Algorithm Explorer" description="Twenty complete implementations, organized for focused study and experimentation."/><Suspense fallback={<Skeleton className="explorer-skeleton"/>}><AlgorithmExplorer/></Suspense></div>; }
