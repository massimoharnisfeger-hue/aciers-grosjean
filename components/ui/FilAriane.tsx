import Link from "next/link";

export type Miette = { label: string; href?: string };

export default function FilAriane({ items, sombre = false }: { items: Miette[]; sombre?: boolean }) {
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [{ label: "Accueil", href: "/" }, ...items].map((m, i) => ({
      "@type": "ListItem",
      position: i + 1,
      name: m.label,
      ...(m.href ? { item: `https://www.aciersgrosjean.be${m.href}` } : {}),
    })),
  };

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <nav aria-label="Fil d'Ariane" className="overflow-x-auto">
        <ol className={`flex whitespace-nowrap font-body text-xs ${sombre ? "text-white/60" : "text-soft"}`}>
          <li>
            <Link href="/" className={`lien-tactile ${sombre ? "hover:text-jaune" : "hover:text-encre"}`}>Accueil</Link>
          </li>
          {items.map((m, i) => (
            <li key={i} className="flex items-center">
              <span className={`mx-2 ${sombre ? "text-white/25" : "text-brume"}`} aria-hidden="true">/</span>
              {m.href && i < items.length - 1 ? (
                <Link href={m.href} className={`lien-tactile ${sombre ? "hover:text-jaune" : "hover:text-encre"}`}>
                  {m.label}
                </Link>
              ) : (
                <span className={sombre ? "text-white" : "text-encre"} aria-current="page">{m.label}</span>
              )}
            </li>
          ))}
        </ol>
      </nav>
    </>
  );
}
