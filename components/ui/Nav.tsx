"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import Logo from "@/components/ui/Logo";
import type { MenuUnivers } from "@/lib/menu";

const secondaires = [
  { label: "Services", href: "/services" },
  { label: "Conseils", href: "/conseils" },
  { label: "Dépôts", href: "/depots" },
  { label: "Entreprise", href: "/entreprise" },
];

export default function Nav({ menu }: { menu: MenuUnivers[] }) {
  const pathname = usePathname();
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  const [mega, setMega] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    setOpen(false);
    setMega(false);
  }, [pathname]);

  const catalogueActif =
    pathname === "/produits" ||
    pathname.startsWith("/catalogue") ||
    menu.some((u) => pathname === `/${u.slug}` || pathname.startsWith(`/${u.slug}/`)) ||
    pathname.startsWith("/p/");

  return (
    <header
      className={`fixed inset-x-0 top-0 z-[9000] transition-all duration-300 ${
        scrolled
          ? "bg-white/90 py-3 shadow-[0_1px_0_rgba(51,54,66,0.08)] backdrop-blur"
          : "bg-white/70 py-5 backdrop-blur-sm"
      }`}
      onMouseLeave={() => setMega(false)}
    >
      <div className="container-g flex items-center justify-between">
        <Link href="/" aria-label="Accueil"><Logo hauteur={scrolled ? 40 : 48} /></Link>

        <nav className="hidden items-center gap-1 lg:flex" aria-label="Navigation principale">
          {/* catalogue : méga-menu */}
          <button
            type="button"
            onMouseEnter={() => setMega(true)}
            onClick={() => setMega((m) => !m)}
            aria-expanded={mega}
            className={`flex items-center gap-1.5 rounded-md px-4 py-2 font-body text-sm transition-colors ${
              catalogueActif ? "text-encre" : "text-soft hover:bg-nuage hover:text-encre"
            }`}
          >
            Catalogue
            <svg
              width="12" height="12" viewBox="0 0 24 24" fill="none" aria-hidden="true"
              className={`transition-transform ${mega ? "rotate-180" : ""}`}
            >
              <path d="M6 9l6 6 6-6" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </button>

          {secondaires.map((l) => {
            const actif = pathname === l.href || pathname.startsWith(l.href + "/");
            return (
              <Link
                key={l.href}
                href={l.href}
                className={`rounded-md px-4 py-2 font-body text-sm transition-colors ${
                  actif ? "text-encre" : "text-soft hover:bg-nuage hover:text-encre"
                }`}
              >
                {l.label}
                {actif && <span className="mx-auto mt-0.5 block h-0.5 w-4 rounded-full bg-jaune" />}
              </Link>
            );
          })}
        </nav>

        <div className="flex items-center gap-2">
          <Link
            href="/recherche"
            aria-label="Rechercher"
            className="hidden h-10 w-10 items-center justify-center rounded-md text-soft transition-colors hover:bg-nuage hover:text-encre lg:flex"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <circle cx="11" cy="11" r="7" stroke="currentColor" strokeWidth="2" />
              <path d="M20 20l-3.5-3.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
            </svg>
          </Link>
          <Link href="/pro" className="hidden font-body text-sm text-soft transition-colors hover:text-encre lg:block">
            Espace pro
          </Link>
          <Link href="/devis" className="btn-cta hidden text-sm lg:inline-flex">Devis en 24h</Link>

          <button
            onClick={() => setOpen((o) => !o)}
            aria-label={open ? "Fermer le menu" : "Ouvrir le menu"}
            aria-expanded={open}
            className="flex h-11 w-11 items-center justify-center rounded-md border border-brume lg:hidden"
          >
            <div className="space-y-1.5">
              <span className={`block h-0.5 w-5 bg-encre transition-transform ${open ? "translate-y-2 rotate-45" : ""}`} />
              <span className={`block h-0.5 w-5 bg-encre transition-opacity ${open ? "opacity-0" : ""}`} />
              <span className={`block h-0.5 w-5 bg-encre transition-transform ${open ? "-translate-y-2 -rotate-45" : ""}`} />
            </div>
          </button>
        </div>
      </div>

      {/* ---- méga-menu catalogue (desktop) ---- */}
      {mega && (
        <div className="absolute inset-x-0 top-full hidden border-t border-brume bg-white shadow-[0_24px_48px_-24px_rgba(51,54,66,.3)] lg:block">
          <div className="container-g grid grid-cols-6 gap-6 py-8">
            {menu.map((u) => (
              <div key={u.slug}>
                <Link
                  href={`/${u.slug}`}
                  className="h-title block font-semibold leading-snug text-encre hover:text-jaune"
                >
                  {u.nom}
                </Link>
                <span className="mt-0.5 block font-mono text-[11px] text-soft">
                  {u.total} produits
                </span>
                <ul className="mt-3 space-y-1.5">
                  {u.familles.map((f) => (
                    <li key={f.chemin}>
                      <Link href={f.chemin} className="font-body text-sm text-soft hover:text-encre">
                        {f.nom}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
          <div className="border-t border-brume bg-nuage">
            <div className="container-g flex flex-wrap items-center gap-x-6 gap-y-2 py-3.5">
              <Link href="/produits" className="font-body text-sm font-medium text-encre hover:text-jaune">
                Tout le catalogue
              </Link>
              <Link href="/catalogue" prefetch={false} className="font-body text-sm text-soft hover:text-encre">
                Catalogue en images
              </Link>
              <Link href="/nouveautes" className="font-body text-sm text-soft hover:text-encre">Nouveautés</Link>
              <Link href="/recherche" className="font-body text-sm text-soft hover:text-encre">Recherche</Link>
              <Link href="/documentation" className="font-body text-sm text-soft hover:text-encre">Documentation</Link>
            </div>
          </div>
        </div>
      )}

      {/* ---- menu mobile ---- */}
      <div
        className={`container-g overflow-y-auto transition-all duration-300 lg:hidden ${
          open ? "mt-3 max-h-[75vh]" : "max-h-0"
        }`}
      >
        <div className="rounded-xl border border-brume bg-white p-3">
          <p className="px-4 pb-1 pt-2 font-body text-xs uppercase tracking-[0.14em] text-soft">Catalogue</p>
          {menu.map((u) => (
            <Link
              key={u.slug}
              href={`/${u.slug}`}
              className="flex items-center justify-between rounded-lg px-4 py-2.5 text-left font-body text-encre hover:bg-nuage"
            >
              {u.nom}
              <span className="font-mono text-xs text-soft">{u.total}</span>
            </Link>
          ))}
          <Link href="/produits" className="block rounded-lg px-4 py-2.5 font-body text-sm text-soft hover:bg-nuage">
            Tout le catalogue
          </Link>
          <Link href="/catalogue" prefetch={false} className="block rounded-lg px-4 py-2.5 font-body text-sm text-soft hover:bg-nuage">
            Catalogue en images
          </Link>

          <p className="mt-2 border-t border-brume px-4 pb-1 pt-3 font-body text-xs uppercase tracking-[0.14em] text-soft">
            Le reste
          </p>
          {[...secondaires, { label: "Recherche", href: "/recherche" }, { label: "Espace pro", href: "/pro" }].map((l) => (
            <Link
              key={l.href}
              href={l.href}
              className="block rounded-lg px-4 py-2.5 text-left font-body text-encre hover:bg-nuage"
            >
              {l.label}
            </Link>
          ))}
          <Link href="/devis" className="btn-cta mt-3 w-full justify-center">Devis en 24h</Link>
        </div>
      </div>
    </header>
  );
}
