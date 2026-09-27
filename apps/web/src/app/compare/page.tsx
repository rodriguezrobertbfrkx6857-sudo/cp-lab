import { Suspense } from "react";
import { CompareLab } from "@/components/compare-lab";
import { PageHeader, Skeleton } from "@/components/ui";
export default function ComparePage(){return <div className="page-stack"><PageHeader eyebrow="Trade-off analysis" title="Compare algorithms" description="Put two approaches side by side, then measure only when both support the same trusted workload."/><Suspense fallback={<Skeleton className="benchmark-skeleton"/>}><CompareLab/></Suspense></div>}
