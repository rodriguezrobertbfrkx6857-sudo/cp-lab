import { Suspense } from "react";
import { BenchmarkLab } from "@/components/benchmark-lab";
import { PageHeader, Skeleton } from "@/components/ui";
export default function BenchmarkPage(){return <div className="page-stack"><PageHeader eyebrow="Performance laboratory" title="Benchmark trusted implementations" description="Seeded datasets, explicit warmups, measured samples, and transparent runtime metadata—never fabricated numbers."/><Suspense fallback={<Skeleton className="benchmark-skeleton"/>}><BenchmarkLab/></Suspense></div>}
