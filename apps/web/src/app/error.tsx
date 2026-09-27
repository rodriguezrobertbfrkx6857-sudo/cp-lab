"use client";
import { AlertTriangle, RotateCcw } from "lucide-react";
import { Button } from "@/components/ui";
export default function ErrorPage({reset}:{error:Error&{digest?:string};reset:()=>void}){return <div className="full-state"><AlertTriangle/><p className="eyebrow">Application error</p><h1>The view could not be rendered.</h1><p>Your data was not reported as successful. Retry the route or return to the dashboard.</p><Button onClick={reset}><RotateCcw size={17}/>Try again</Button></div>}
