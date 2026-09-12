import type { Metadata } from "next";
import Link from "next/link";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";

export const metadata: Metadata = {
  title: "Engagement ESG — nos chiffres et nos objectifs",
  description:
    "112 points de contrôle, 993 heures de formation, une feuille de route jusqu'en 2030. Ce que nous mesurons et ce que nous nous engageons à améliorer.",
  alternates: { canonical: "/entreprise/engagement-esg" },
};

const piliers = [
  {
    titre: "Environnement",
    chiffre: "100 %",
    legende: "recyclable, indéfiniment",
    texte:
      "L'acier se recycle sans perte de propriétés — c'est l'un des rares matériaux dans ce cas. Notre levier réel est ailleurs : la consommation énergétique des sites, l'optimisation des transferts entre dépôts, et la réduction des chutes par la découpe à la demande. Chaque coupe optimisée est de la matière qui ne part pas en ferraille.",
  },
  {
    titre: "Social",
    chiffre: "993 h",
    legende: "de formation dispensées",
    texte:
      "Dont une part majoritaire en sécurité et en conduite d'engins de manutention. Dans un métier où l'on déplace des charges lourdes tous les jours, c'est la ligne la moins discutable du budget. S'y ajoutent l'ancrage local de l'emploi et la stabilité des équipes, qui font la qualité du conseil au comptoir.",
  },
  {
    titre: "Gouvernance",
    chiffre: "112",
    legende: "points de contrôle évalués",
    texte:
      "De la traçabilité des approvisionnements aux règles de décision d'une entreprise familiale. Chaque point est documenté ou ne compte pas — c'est la seule façon de rendre un rapport utile plutôt que décoratif.",
  },
];

export default function EsgPage() {
  return (
    <main>
      <PageHeader
        surtitre="Engagement ESG"
        titre={
          <>
            Ce qu'on mesure, <span className="mark-jaune">et ce qu'on améliore</span>
          </>
        }
        intro="Premier exercice de transparence formalisé. Trois piliers, 112 points de contrôle, et une feuille de route datée jusqu'en 2030."
      />

      <section className="bg-white py-16 md:py-24">
        <div className="container-g grid gap-6 md:grid-cols-3">
          {piliers.map((p, i) => (
            <Reveal key={p.titre} delay={i * 0.07}>
              <div className="flex h-full flex-col rounded-2xl border border-brume bg-white p-7">
                <span className="font-body text-xs uppercase tracking-[0.16em] text-soft">{p.titre}</span>
                <span className="h-title mt-3 text-4xl font-bold tabular-nums text-encre">{p.chiffre}</span>
                <span className="mt-1 font-body text-sm text-soft">{p.legende}</span>
                <p className="mt-5 flex-1 border-t border-brume pt-5 font-body leading-relaxed text-soft">
                  {p.texte}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      <section className="border-y border-brume bg-nuage py-16 md:py-20">
        <div className="container-g max-w-[46rem]">
          <h2 className="h-display text-2xl md:text-3xl">Feuille de route 2022-2030</h2>
          <p className="mt-4 font-body text-lg leading-relaxed text-soft">
            Des objectifs datés plutôt que des intentions : réduction de l'intensité énergétique
            des sites, amélioration continue du taux de valorisation des chutes, et extension de
            la certification à l'ensemble des activités de transformation.
          </p>
          <p className="mt-4 font-body text-lg leading-relaxed text-soft">
            Le rapport est réévalué chaque exercice. Un engagement qu'on ne peut pas mesurer
            n'est pas un engagement.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link href="/conseils/rapport-esg-aciers-grosjean-2023" className="btn-cta">
              Lire le rapport ESG 2023
            </Link>
            <Link href="/entreprise/certifications" className="btn-ghost">Nos certifications</Link>
          </div>
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
