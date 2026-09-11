"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { label: "Accueil", href: "/" },
  { label: "Produits", href: "/produits" },
  { label: "Services", href: "/services" },
  { label: "Dépôts", href: "/depots" },
  { label: "À propos", href: "/a-propos" },
];

function Wordmark() {
  return (
    <span className="flex items-baseline gap-1.5 leading-none">
      <span className="h-title text-xl font-bold tracking-tight text-encre">GROSJEAN</span>
      <span className="h-sub text-xs text-soft">aciers</span>
    </span>
  );
}

export default function Nav() {
  const pathname = usePathname();
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => setOpen(false), [pathname]);

  return (
    <header
      className={`fixed inset-x-0 top-0 z-[9000] transition-all duration-300 ${
        scrolled ? "bg-white/90 py-3 shadow-[0_1px_0_rgba(51,54,66,0.08)] backdrop-blur" : "bg-white/70 py-5 backdrop-blur-sm"
      }`}
    >
      <div className="container-g flex items-center justify-between">
        <Link href="/" aria-label="Accueil"><Wordmark /></Link>

        <nav className="hidden items-center gap-1 md:flex">
          {links.map((l) => {
            const active = l.href === "/" ? pathname === "/" : pathname.startsWith(l.href);
            return (
              <Link
                key={l.href}
                href={l.href}
                className={`rounded-md px-4 py-2 font-body text-sm transition-colors ${
                  active ? "text-encre" : "text-soft hover:bg-nuage hover:text-encre"
                }`}
              >
                {l.label}
                {active && <span className="mx-auto mt-0.5 block h-0.5 w-4 rounded-full bg-jaune" />}
              </Link>
            );
          })}
        </nav>

        <div className="flex items-center gap-3">
          <Link href="/devis" className="btn-cta hidden text-sm md:inline-flex">Devis en 24h</Link>
          <button
            onClick={() => setOpen((o) => !o)}
            aria-label="Menu"
            className="flex h-11 w-11 items-center justify-center rounded-md border border-brume md:hidden"
          >
            <div className="space-y-1.5">
              <span className={`block h-0.5 w-5 bg-encre transition-transform ${open ? "translate-y-2 rotate-45" : ""}`} />
              <span className={`block h-0.5 w-5 bg-encre transition-opacity ${open ? "opacity-0" : ""}`} />
              <span className={`block h-0.5 w-5 bg-encre transition-transform ${open ? "-translate-y-2 -rotate-45" : ""}`} />
            </div>
          </button>
        </div>
      </div>

      <div className={`container-g overflow-hidden transition-all duration-300 md:hidden ${open ? "mt-3 max-h-96" : "max-h-0"}`}>
        <div className="rounded-xl border border-brume bg-white p-3">
          {links.map((l) => (
            <Link key={l.href} href={l.href} className="block w-full rounded-lg px-4 py-3 text-left font-body text-encre hover:bg-nuage">
              {l.label}
            </Link>
          ))}
          <Link href="/devis" className="btn-cta mt-2 w-full justify-center">Devis en 24h</Link>
        </div>
      </div>
    </header>
  );
}
