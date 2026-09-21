import type { Metadata } from "next";
import Link from "next/link";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Realisations from "@/components/sections/Realisations";
import Reveal from "@/components/fx/Reveal";

export const metadata: Metadata = {
  title: "Réalisations clients et listes de matière",
  description:
    "Garde-corps, mezzanines, portails, terrasses corten, bardages, escaliers : six projets réels, avec la liste de matière exacte qui va avec.",
  alternates: { canonical: "/realisations" },
};

const projets = [
  {
    titre: "Garde-corps de terrasse",
    profil: "Particulier · Gerpinnes",
    matiere: "Inox 304 brossé",
    liste: ["Tube rond Ø 42,4 × 2 — main courante", "Rond plein Ø 12 — barreaudage", "Plat 40 × 5 — platines"],
    href: "/inox",
  },
  {
    titre: "Mezzanine d'atelier",
    profil: "Professionnel · Charleroi",
    matiere: "Acier S235",
    liste: ["IPE 200 — solives", "HEB 140 — poteaux", "Tôle larmée 5/7 — plancher"],
    href: "/acier/poutrelles",
  },
  {
    titre: "Portail battant 2 vantaux",
    profil: "Particulier · La Louvière",
    matiere: "Acier galvanisé",
    liste: ["Tube carré 50 × 50 × 2 — cadre", "Tube carré 30 × 30 × 2 — barreaudage", "Plat 40 × 5 — diagonales"],
    href: "/acier/tubes/tube-carre",
  },
  {
    titre: "Terrasse et massifs corten",
    profil: "Particulier · Tournai",
    matiere: "Corten S355J0WP",
    liste: ["Bordure de jardin 150 mm", "Bac à fleurs sur mesure", "Brise-vue découpé au laser"],
    href: "/acier/toles/tole-corten",
  },
  {
    titre: "Bardage d'extension",
    profil: "Professionnel · Ath",
    matiere: "Bac acier prélaqué",
    liste: ["Profil 35/207 prélaqué RAL 7016", "Vis autoforantes 6,3 × 60", "Cornière 40 × 40 × 4 — ossature"],
    href: "/toiture-bardage/toles-profilees",
  },
  {
    titre: "Escalier droit métallique",
    profil: "Professionnel · Binche",
    matiere: "Acier S235 thermolaqué",
    liste: ["UPN 160 — limons", "Tôle larmée 4/6 — marches", "Tube carré 40 × 40 × 3 — rampe"],
    href: "/acier/profiles",
  },
];

export default function RealisationsPage() {
  return (
    <main>
      <PageHeader
        surtitre="Réalisations"
        titre={
          <>
            Ce que devient <span className="mark-jaune">notre acier</span>
          </>
        }
        intro="Des projets réels, avec la liste de matière qui va avec. Parce que la meilleure façon de comprendre ce qu'il vous faut, c'est de voir ce qu'il a fallu aux autres."
      />

      <Realisations />

      <section className="bg-white py-16 md:py-24">
        <div className="container-g">
          <h2 className="h-display text-2xl md:text-3xl">Six projets, six listes de matière</h2>
          <p className="mt-3 max-w-xl font-body text-soft">
            Ce qui a réellement été commandé. Les quantités varient selon les dimensions, mais
            les sections, elles, sont les bonnes.
          </p>

          <div className="mt-10 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
            {projets.map((p, i) => (
              <Reveal key={p.titre} delay={(i % 3) * 0.07}>
                <div className="flex h-full flex-col rounded-2xl border border-brume bg-white p-7">
                  <span className="font-body text-xs uppercase tracking-[0.14em] text-soft">
                    {p.profil}
                  </span>
                  <h3 className="h-title mt-2 text-xl font-semibold text-encre">{p.titre}</h3>
                  <p className="mt-1 font-mono text-xs text-soft">{p.matiere}</p>

                  <ul className="mt-5 flex-1 space-y-2 border-t border-brume pt-4">
                    {p.liste.map((l) => (
                      <li key={l} className="flex gap-2.5 font-body text-sm text-soft">
                        <span className="mt-[0.5em] h-1.5 w-1.5 shrink-0 rounded-full bg-jaune" />
                        {l}
                      </li>
                    ))}
                  </ul>

                  <Link
                    href={p.href}
                    className="lien-tactile group mt-6 inline-flex items-center gap-2 font-body text-sm font-medium text-encre"
                  >
                    Voir la matière
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" className="transition-transform group-hover:translate-x-1">
                      <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  </Link>
                </div>
              </Reveal>
            ))}
          </div>

          <div className="mt-12 rounded-2xl border border-brume bg-nuage p-8">
            <h2 className="h-title text-lg font-semibold text-encre">
              Votre projet ressemble à l’un de ceux-ci&nbsp;?
            </h2>
            <p className="mt-2 max-w-2xl font-body text-soft">
              Dites-nous simplement ce que vous voulez construire et les dimensions
              approximatives. On traduit en références, on chiffre, et on vous répond sous 24 h.
            </p>
            <Link href="/devis" className="btn-cta mt-6">Décrire mon projet</Link>
          </div>
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
