"use client";

import { Check, Copy } from "lucide-react";
import { useState } from "react";
import { Badge, Button } from "./ui";

export function CodeTabs({ python, cpp }: { python: string; cpp: string }) {
  const [language, setLanguage] = useState<"python" | "cpp">("cpp"); const [copied, setCopied] = useState(false); const source = language === "cpp" ? cpp : python;
  const copy = async () => { await navigator.clipboard.writeText(source); setCopied(true); window.setTimeout(() => setCopied(false), 1400); };
  return <div className="code-viewer"><div className="code-toolbar"><div className="segmented"><button className={language === "cpp" ? "active" : ""} onClick={() => setLanguage("cpp")}>C++20</button><button className={language === "python" ? "active" : ""} onClick={() => setLanguage("python")}>Python</button></div><div><Badge tone="green">Tested</Badge><Button onClick={copy} aria-label="Copy code">{copied ? <Check size={16}/> : <Copy size={16}/>} {copied ? "Copied" : "Copy"}</Button></div></div><pre><code>{source.split("\n").map((line,index) => <span className="code-line" key={index}><i>{index+1}</i><b>{line || " "}</b></span>)}</code></pre></div>;
}
