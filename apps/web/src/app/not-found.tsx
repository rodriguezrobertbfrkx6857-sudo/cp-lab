import { ArrowLeft, SearchX } from "lucide-react";
import { LinkButton } from "@/components/ui";
export default function NotFound(){return <div className="full-state"><SearchX/><p className="eyebrow">404 · route not found</p><h1>This path has no algorithm.</h1><p>Return to the catalog and choose a supported experiment.</p><LinkButton href="/algorithms"><ArrowLeft size={17}/>Browse algorithms</LinkButton></div>}
