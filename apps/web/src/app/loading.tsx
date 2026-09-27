import { Skeleton } from "@/components/ui";
export default function Loading(){return <div className="page-stack"><Skeleton className="title-skeleton"/><div className="metric-grid">{Array.from({length:4},(_,index)=><Skeleton className="card-skeleton" key={index}/>)}</div><Skeleton className="content-skeleton"/></div>}
