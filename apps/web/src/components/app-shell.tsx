"use client";

import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import { Activity, BarChart3, BookOpen, Braces, Code2, Command, Github, Home, Info, Menu, Search, Scale, X } from "lucide-react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { algorithms } from "@/lib/catalog";
import { GITHUB_URL, PRODUCT_NAME } from "@/lib/config";

const primary = [
  { href: "/", label: "Dashboard", icon: Home }, { href: "/algorithms", label: "Algorithms", icon: Braces },
  { href: "/playground", label: "Playground", icon: Activity }, { href: "/benchmark", label: "Benchmark", icon: BarChart3 },
  { href: "/compare", label: "Compare", icon: Scale },
];
const secondary = [{ href: "/docs", label: "Documentation", icon: BookOpen }, { href: "/about", label: "About", icon: Info }];

export function AppShell({ children }: { children: React.ReactNode }) {
  const path = usePathname(); const router = useRouter(); const reduceMotion = useReducedMotion();
  const [menuOpen, setMenuOpen] = useState(false); const [paletteOpen, setPaletteOpen] = useState(false); const [query, setQuery] = useState("");
  useEffect(() => {
    const keydown = (event: KeyboardEvent) => {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") { event.preventDefault(); setPaletteOpen((value) => !value); }
      if (event.key === "Escape") { setPaletteOpen(false); setMenuOpen(false); }
    };
    window.addEventListener("keydown", keydown); return () => window.removeEventListener("keydown", keydown);
  }, []);
  const matches = useMemo(() => {
    const routes = [...primary, ...secondary].map((item) => ({ ...item, type: "Page" }));
    const items = algorithms.map((algorithm) => ({ href: `/algorithms/${algorithm.slug}`, label: algorithm.title, type: algorithm.category }));
    const needle = query.trim().toLowerCase(); return [...routes, ...items].filter((item) => !needle || `${item.label} ${item.type}`.toLowerCase().includes(needle)).slice(0, 9);
  }, [query]);
  const title = [...primary, ...secondary].find((item) => item.href === path)?.label ?? (path.includes("playground") ? "Playground" : path.includes("algorithms") ? "Algorithm" : PRODUCT_NAME);
  const navigate = (href: string) => { setPaletteOpen(false); setMenuOpen(false); router.push(href); };
  return <div className="app-shell">
    <aside className={`sidebar ${menuOpen ? "sidebar-open" : ""}`} aria-label="Primary navigation">
      <Link href="/" className="brand" aria-label={`${PRODUCT_NAME} home`}><span className="brand-mark"><Code2 size={20}/></span><span>{PRODUCT_NAME}</span></Link>
      <nav>{primary.map((item) => <NavItem key={item.href} item={item} active={path === item.href || (item.href !== "/" && path.startsWith(item.href))} />)}</nav>
      <nav className="secondary-nav">{secondary.map((item) => <NavItem key={item.href} item={item} active={path === item.href} />)}
        <a href={GITHUB_URL} target="_blank" rel="noreferrer"><Github size={19}/><span>GitHub</span></a>
      </nav>
    </aside>
    {menuOpen && <button className="nav-scrim" aria-label="Close navigation" onClick={() => setMenuOpen(false)} />}
    <div className="app-content">
      <header className="top-header"><div className="header-title"><button className="mobile-menu" onClick={() => setMenuOpen(true)} aria-label="Open navigation"><Menu/></button><span>{title}</span></div>
        <button className="search-trigger" onClick={() => setPaletteOpen(true)}><Search size={17}/><span>Search algorithms and tools</span><kbd><Command size={12}/> K</kbd></button>
        <a className="icon-link" href={GITHUB_URL} aria-label="Open GitHub repository"><Github size={19}/></a>
      </header>
      <main className="main-content">{children}</main>
    </div>
    <AnimatePresence>{paletteOpen && <motion.div className="palette-backdrop" initial={reduceMotion ? false : { opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onMouseDown={() => setPaletteOpen(false)}>
      <motion.div className="command-palette" role="dialog" aria-modal="true" aria-label="Command palette" initial={reduceMotion ? false : { opacity: 0, y: -12 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }} onMouseDown={(event) => event.stopPropagation()}>
        <div className="palette-input"><Search/><input autoFocus value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search algorithms, categories, and pages…" aria-label="Search commands"/><button onClick={() => setPaletteOpen(false)} aria-label="Close"><X/></button></div>
        <div className="palette-results">{matches.map((item) => <button key={item.href} onClick={() => navigate(item.href)}><span>{item.label}</span><small>{item.type}</small></button>)}</div>
      </motion.div>
    </motion.div>}</AnimatePresence>
  </div>;
}

function NavItem({ item, active }: { item: { href: string; label: string; icon: typeof Home }; active: boolean }) {
  const Icon = item.icon; return <Link href={item.href} className={active ? "active" : ""}><Icon size={19}/><span>{item.label}</span></Link>;
}
