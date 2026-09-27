"use client";

import dynamic from "next/dynamic";
import { Check, Clock3, Cpu, Database, Gauge, HardDrive, History, Play, ShieldCheck } from "lucide-react";
import { useSearchParams } from "next/navigation";
import { useCallback, useEffect, useMemo, useState } from "react";
import { apiRequest } from "@/lib/api";
import { benchmarkAlgorithms } from "@/lib/catalog";
import { Badge, Button, Card, EmptyState, InlineError } from "./ui";

const Chart = dynamic(() => import("echarts-for-react"), {
  ssr: false,
  loading: () => <div className="chart-loading">Preparing chart…</div>,
});

type Result = { algorithm:string; language:string; samplesMs:number[]; medianMs:number; minMs:number; maxMs:number; p95Ms:number; operations:number|null; memoryBytes:number|null; memoryNote:string };
type Run = { id:string; status:string; results:Result[]; environment:Record<string,unknown>; dataset:Record<string,unknown> };

const kinds = ["random", "sorted", "reverse-sorted", "nearly-sorted", "duplicate-heavy", "sparse-graph", "dense-graph", "chain-graph", "random-tree"];
const suites: Record<string, string[]> = {
  "Custom selection": [],
  "Naive GCD vs Euclidean": ["naive-gcd", "euclidean-gcd"],
  "Naive power vs binary exponentiation": ["naive-power", "binary-exponentiation"],
  "Trial prime vs Eratosthenes": ["trial-prime", "eratosthenes-sieve"],
  "Eratosthenes vs Euler sieve": ["eratosthenes-sieve", "euler-linear-sieve"],
  "BFS vs DFS": ["bfs", "dfs"],
  "DSU path compression": ["dsu-basic", "dsu"],
  "Fenwick vs naive prefix": ["naive-prefix", "fenwick-tree"],
  "Merge Sort vs Quick Sort": ["merge-sort", "quick-sort"],
};

export function BenchmarkLab() {
  const params = useSearchParams();
  const preferred = params.get("algorithm");
  const [selected, setSelected] = useState<string[]>([preferred && benchmarkAlgorithms.some((item) => item.slug === preferred) ? preferred : "merge-sort", "quick-sort"]);
  const [suite, setSuite] = useState("Custom selection");
  const [language, setLanguage] = useState("python");
  const [size, setSize] = useState(1000);
  const [runs, setRuns] = useState(10);
  const [warmups, setWarmups] = useState(3);
  const [seed, setSeed] = useState(42);
  const [kind, setKind] = useState("random");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<Run | null>(null);
  const [history, setHistory] = useState<Run[]>([]);

  const refreshHistory = useCallback(() => {
    apiRequest<Run[]>("/benchmark-history/recent?limit=5").then(setHistory).catch(() => setHistory([]));
  }, []);
  useEffect(() => { refreshHistory(); }, [refreshHistory]);

  const submit = async () => {
    setLoading(true); setError("");
    try {
      const completed = await apiRequest<Run>("/benchmark", { method:"POST", body:JSON.stringify({ algorithms:selected, language, dataset:{ kind, size, min_value:0, max_value:1_000_000, density:0.15 }, warmups, measured_runs:runs, seed }) });
      setResult(completed); refreshHistory();
    } catch (problem) {
      setError(problem instanceof Error ? problem.message : "Benchmark failed");
    } finally { setLoading(false); }
  };
  const toggle = (slug:string) => { setSuite("Custom selection"); setSelected((items) => items.includes(slug) ? items.filter((item) => item !== slug) : items.length < 4 ? [...items, slug] : items); };

  const runtimeChart = useMemo(() => ({
    color:["#6558d9", "#2f99a5", "#31a36b", "#d88636"],
    tooltip:{trigger:"axis",backgroundColor:"#fff",borderColor:"#e5e8ee",textStyle:{color:"#111318"}},
    legend:{top:0,textStyle:{color:"#69717d"}}, grid:{left:48,right:20,top:42,bottom:40},
    xAxis:{type:"category",data:Array.from({length:Math.max(0,...(result?.results.map((item) => item.samplesMs.length) ?? [0]))},(_,index)=>`Run ${index+1}`),axisLine:{lineStyle:{color:"#dfe3ea"}}},
    yAxis:{type:"value",name:"ms",splitLine:{lineStyle:{color:"#eef0f4"}}},
    series:result?.results.map((item)=>({name:item.algorithm,type:"line",smooth:true,symbolSize:7,data:item.samplesMs,lineStyle:{width:2}})) ?? [],
  }), [result]);
  const operationResults = useMemo(() => result?.results.filter((item) => item.operations !== null) ?? [], [result]);
  const operationsChart = useMemo(() => ({
    grid:{left:55,right:20,top:20,bottom:55}, xAxis:{type:"category",data:operationResults.map((item)=>item.algorithm),axisLabel:{rotate:18}},
    yAxis:{type:"value",name:"operations",splitLine:{lineStyle:{color:"#eef0f4"}}},
    series:[{type:"bar",barMaxWidth:54,data:operationResults.map((item,index)=>({value:item.operations,itemStyle:{color:["#6558d9","#2f99a5","#31a36b","#d88636"][index],borderRadius:[8,8,0,0]}}))}],
  }), [operationResults]);

  return <div className="benchmark-layout">
    <Card className="benchmark-config">
      <div className="panel-title"><div><p className="eyebrow">Configuration</p><h2>Trusted benchmark</h2></div><ShieldCheck size={22}/></div>
      <label className="field suite-select"><span>Built-in comparison suite</span><select value={suite} onChange={(event) => { const value=event.target.value; setSuite(value); if (suites[value].length) setSelected(suites[value]); }}>{Object.keys(suites).map((item)=><option key={item}>{item}</option>)}</select></label>
      <fieldset><legend>Algorithms <small>choose up to 4</small></legend><div className="algorithm-checks">{benchmarkAlgorithms.map((item)=><label key={item.slug} className={selected.includes(item.slug)?"selected":""}><input type="checkbox" checked={selected.includes(item.slug)} onChange={()=>toggle(item.slug)}/><span>{selected.includes(item.slug)&&<Check size={13}/>}</span>{item.title}</label>)}</div></fieldset>
      <div className="form-grid">
        <label className="field"><span>Language</span><select value={language} onChange={(event)=>setLanguage(event.target.value)}><option value="python">Python · backend</option><option value="cpp">C++20 · -O2 backend</option></select></label>
        <label className="field"><span>Generator</span><select value={kind} onChange={(event)=>setKind(event.target.value)}>{kinds.map((item)=><option key={item}>{item}</option>)}</select></label>
        <label className="field"><span>Input size</span><input type="number" min="1" max="100000" value={size} onChange={(event)=>setSize(Number(event.target.value))}/></label>
        <label className="field"><span>Seed</span><input type="number" min="0" value={seed} onChange={(event)=>setSeed(Number(event.target.value))}/></label>
        <label className="field"><span>Warmups</span><input type="number" min="0" max="10" value={warmups} onChange={(event)=>setWarmups(Number(event.target.value))}/></label>
        <label className="field"><span>Measured runs</span><input type="number" min="3" max="30" value={runs} onChange={(event)=>setRuns(Number(event.target.value))}/></label>
      </div>
      <Button onClick={submit} disabled={loading||!selected.length}><Play size={16}/>{loading?"Running trusted code…":"Run benchmark"}</Button>
      <p className="fine-print">Warmups are excluded. Timing uses a monotonic backend clock; memory stays unavailable unless it can be measured honestly.</p>
    </Card>
    <div className="benchmark-results">
      {error&&<InlineError message={error} retry={submit}/>} 
      {!result&&!error&&!loading&&<EmptyState title="No measured run yet" description="Configure the dataset and run trusted repository code to populate results."/>}
      {loading&&<Card className="benchmark-running"><span className="spinner"/><h3>Benchmark in progress</h3><p>Generating a seeded dataset, warming the runtime, and collecting measured samples.</p></Card>}
      {result&&<>
        <div className="result-cards">{result.results.map((item)=><Card key={item.algorithm} className="result-card"><div><Badge tone="indigo">{item.language}</Badge><span>{item.algorithm}</span></div><strong>{item.medianMs.toFixed(3)} <small>ms median</small></strong><dl><div><dt>Min</dt><dd>{item.minMs.toFixed(3)}</dd></div><div><dt>P95</dt><dd>{item.p95Ms.toFixed(3)}</dd></div><div><dt>Max</dt><dd>{item.maxMs.toFixed(3)}</dd></div></dl></Card>)}</div>
        <Card className="chart-card"><div className="panel-title"><div><p className="eyebrow">Measured samples</p><h2>Runtime by run</h2></div><Badge tone="green">backend timing</Badge></div><Chart option={runtimeChart} style={{height:330}}/></Card>
        <div className="benchmark-analysis-grid">
          <Card className="chart-card"><div className="panel-title"><div><p className="eyebrow">Instrumentation</p><h2>Operations</h2></div><Gauge size={20}/></div>{operationResults.length?<Chart option={operationsChart} style={{height:250}}/>:<p className="unavailable-state">Operation counts are not instrumented for this selection.</p>}</Card>
          <Card className="chart-card"><div className="panel-title"><div><p className="eyebrow">Memory</p><h2>Measurement status</h2></div><HardDrive size={20}/></div><div className="memory-unavailable"><Badge tone="amber">Unavailable</Badge><p>{result.results[0]?.memoryNote}</p><small>No value is estimated or fabricated.</small></div></Card>
        </div>
        <Card className="environment-card"><div><Cpu/><span><small>Runtime</small><strong>{String(result.environment.runtime)}</strong></span></div><div><Clock3/><span><small>Method</small><strong>{String(result.environment.warmupRuns)} warmup · {String(result.environment.measuredRuns)} measured</strong></span></div><div><Database/><span><small>Dataset</small><strong>{String(result.dataset.kind)} · n={String(result.dataset.size)}</strong></span></div></Card>
      </>}
      <Card className="benchmark-history"><div className="panel-title"><div><p className="eyebrow">SQLite history</p><h2>Recent measured runs</h2></div><History size={20}/></div>{history.length?<div>{history.map((run)=><div className="history-row" key={run.id}><span><strong>{run.results.map((item)=>item.algorithm).join(" · ")}</strong><small>{String(run.environment.language)} · seed {String(run.environment.seed)}</small></span><time>{new Date(String(run.environment.timestamp)).toLocaleString()}</time></div>)}</div>:<p className="unavailable-state">No persisted benchmark runs yet.</p>}</Card>
    </div>
  </div>;
}
