import Link from "next/link";
import type { ButtonHTMLAttributes, HTMLAttributes, ReactNode } from "react";

export function Card({ className = "", ...props }: HTMLAttributes<HTMLDivElement>) {
  return <div className={`card ${className}`} {...props} />;
}

export function Badge({ children, tone = "neutral" }: { children: ReactNode; tone?: "neutral" | "indigo" | "cyan" | "green" | "amber" | "rose" }) {
  return <span className={`badge badge-${tone}`}>{children}</span>;
}

export function Button({ className = "", ...props }: ButtonHTMLAttributes<HTMLButtonElement>) {
  return <button className={`button ${className}`} {...props} />;
}

export function LinkButton({ href, children, secondary = false }: { href: string; children: ReactNode; secondary?: boolean }) {
  return <Link className={`button ${secondary ? "button-secondary" : ""}`} href={href}>{children}</Link>;
}

export function PageHeader({ eyebrow, title, description, actions }: { eyebrow?: string; title: string; description: string; actions?: ReactNode }) {
  return <header className="page-header">
    <div>{eyebrow && <p className="eyebrow">{eyebrow}</p>}<h1>{title}</h1><p>{description}</p></div>
    {actions && <div className="page-actions">{actions}</div>}
  </header>;
}

export function EmptyState({ title, description }: { title: string; description: string }) {
  return <Card className="empty-state"><div className="empty-icon">∅</div><h3>{title}</h3><p>{description}</p></Card>;
}

export function InlineError({ message, retry }: { message: string; retry?: () => void }) {
  return <div className="inline-error" role="alert"><strong>Couldn&apos;t complete that request.</strong><span>{message}</span>{retry && <Button onClick={retry}>Retry</Button>}</div>;
}

export function Skeleton({ className = "" }: { className?: string }) {
  return <span className={`skeleton ${className}`} aria-hidden="true" />;
}
