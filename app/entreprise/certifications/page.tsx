import type { Metadata } from "next";
import Link from "next/link";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";

export const metadata: Metadata = {
  title: "Certification EN 1090-Exc2 et traçabilité",
  description:
    "Certification EN 1090-Exc2 pour la fabrication des structures en acier : ce qu'elle couvre, pourquoi elle est exigée, et ce qu'elle change pour vos commandes.",
  alternates: { canonical: "/entreprise/certifications" },
};

export default function CertificationsPage() {
  return (
    <main>
      <PageHeader
        surtitre="Certifications"
        titre={
          <>
            Certifié <span className="mark-jaune">EN 1090-Exc2</span>
          </>
        }
        intro="La norme européenne qui encadre l'exécution des structures en acier. Peu d'acteurs de notre taille la détiennent — et sur un chantier soumis à contrôle, elle n'est pas négociable."
      />

      <section className="bg-white py-16 md:py-20">
        <div className="container-g grid gap-12 lg:grid-cols-[minmax(0,1fr)_20rem] lg:gap-16">
          <div className="max-w-[46rem]">
            <Reveal>
              <h2 className="h-display text-2xl md:text-3xl">Ce que couvre la norme</h2>
              <p className="mt-5 font-body text-lg leading-[1.75] text-soft">
                L'EN 1090 encadre l'exécution des structures en acier et en aluminium destinées à
                la construction. Elle impose un système de contrôle de production en usine, la
                qualification des soudeurs et des modes opératoires de soudage, et la traçabilité
                des matériaux employés.
              </p>
              <p className="mt-4 font-body text-lg leading-[1.75] text-soft">
                La mention <strong className="text-encre">Exc2</strong> désigne la classe
                d'exécution. C'est celle qui couvre la grande majorité des ouvrages courants de
                bâtiment, au-dessus de l'Exc1 réservée aux structures les moins sollicitées.
              </p>
            </Reveal>

            <Reveal delay={0.06}>
              <h2 className="h-display mt-14 text-2xl md:text-3xl">Ce que ça change pour vous</h2>
              <ul className="mt-6 space-y-3">
                {[
                  "Sur un chantier soumis à contrôle, un ouvrage porteur doit provenir d'un atelier certifié. Sans certification, la pièce est refusée à la réception — et c'est le poseur qui le découvre.",
                  "Les certificats matière sont disponibles sur demande pour les produits concernés : vous pouvez remonter la filière jusqu'à la coulée.",
                  "Les soudures suivent des modes opératoires qualifiés et sont réalisées par des soudeurs certifiés. Ce n'est pas l'habitude qui décide des paramètres.",
                  "Le marquage CE des ensembles structurels est assuré, avec la déclaration de performance qui l'accompagne.",
                ].map((t) => (
                  <li key={t} className="flex gap-3 font-body text-lg leading-[1.7] text-soft">
                    <span className="mt-[0.62em] h-1.5 w-1.5 shrink-0 rounded-full bg-jaune" aria-hidden="true" />
                    <span>{t}</span>
                  </li>
                ))}
              </ul>
            </Reveal>

            <Reveal delay={0.06}>
              <aside className="mt-12 rounded-2xl border-l-4 border-jaune bg-nuage p-6">
                <p className="h-title font-semibold text-encre">Un point d'honnêteté</p>
                <p className="mt-2 font-body leading-relaxed text-soft">
                  La certification couvre notre atelier de transformation. Elle ne remplace pas la
                  note de calcul : dès qu'une pièce reprend une charge de structure, le
                  dimensionnement relève d'un bureau d'études ou d'un architecte. Nous fournissons
                  la matière, les cotes et la traçabilité ; le calcul, c'est leur métier.
                </p>
              </aside>
            </Reveal>
          </div>

          <aside className="lg:sticky lg:top-28 lg:self-start">
            <div className="rounded-2xl border border-brume bg-nuage p-6">
              <span className="tag-stock">EN 1090-Exc2</span>
              <dl className="mt-5 divide-y divide-brume border-y border-brume">
                {[
                  ["Portée", "Exécution de structures en acier"],
                  ["Classe", "Exc2"],
                  ["Soudage", "Modes opératoires qualifiés"],
                  ["Soudeurs", "Certifiés"],
                  ["Traçabilité", "Certificat matière sur demande"],
                  ["Marquage", "CE des ensembles structurels"],
                ].map(([k, v]) => (
                  <div key={k} className="py-3">
                    <dt className="font-body text-xs uppercase tracking-[0.1em] text-soft">{k}</dt>
                    <dd className="mt-0.5 font-body text-sm text-encre">{v}</dd>
                  </div>
                ))}
              </dl>
              <Link href="/devis" className="btn-cta mt-6 w-full justify-center">
                Demander un certificat
              </Link>
            </div>

            <div className="mt-5 rounded-2xl border border-brume p-6">
              <h2 className="h-title text-sm font-semibold uppercase tracking-[0.14em] text-soft">
                Services concernés
              </h2>
              <ul className="mt-4 space-y-2">
                {[
                  ["Soudure & assemblage", "/services/soudure"],
                  ["Coupé-plié armatures", "/services/coupe-plie-armatures"],
                  ["Forage & poinçonnage", "/services/forage-poinconnage"],
                ].map(([l, h]) => (
                  <li key={h}>
                    <Link href={h} className="font-body text-sm text-encre hover:text-jaune">{l}</Link>
                  </li>
                ))}
              </ul>
            </div>
          </aside>
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
