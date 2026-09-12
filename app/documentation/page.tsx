import type { Metadata } from "next";
import Link from "next/link";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import { univers } from "@/lib/catalogue";

export const metadata: Metadata = {
  title: "Documentation technique et fiches produits",
  description:
    "Fiches techniques, notices de pose et certificats matière par famille de produits. Demandez le document qui vous manque, on vous l'envoie.",
  alternates: { canonical: "/documentation" },
};

const familles = [
  { nom: "Toiture & bardage", desc: "Fiches techniques des profils, notices de pose, abaques de portée et teintes RAL disponibles.", href: "/toiture-bardage" },
  { nom: "Panneaux isolés", desc: "Performances thermiques, longueurs standard, détails de raccord et accessoires de finition.", href: "/toiture-bardage/panneaux-isoles" },
  { nom: "Clôtures", desc: "Notices de pose des panneaux rigides, entraxes de poteaux, nuanciers RAL.", href: "/jardin-cloture/clotures" },
  { nom: "Protection & chimie", desc: "Fiches de données de sécurité, fiches techniques ZINGA, primaires et mastics.", href: "/quincaillerie/protection-chimie" },
  { nom: "Caillebotis", desc: "Abaques de charge, hauteurs de porteur, modes de fixation.", href: "/quincaillerie/caillebotis-marches" },
  { nom: "Certificats matière", desc: "Certificats de conformité 3.1 sur demande, pour les produits qui le permettent.", href: "/entreprise/certifications" },
];

export default function DocumentationPage() {
  return (
    <main>
      <PageHeader
        surtitre="Documentation"
        titre={<>Les documents <span className="mark-jaune">techniques</span></>}
        intro="Fiches techniques, notices de pose, abaques et certificats. Si le document que vous cherchez n'est pas listé, demandez-le : il existe presque toujours."
      />

      <section className="bg-white py-14 md:py-20">
        <div className="container-g">
          <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
            {familles.map((f, i) => (
              <Reveal key={f.nom} delay={(i % 3) * 0.06}>
                <Link
                  href={f.href}
                  className="group flex h-full flex-col rounded-2xl border border-brume bg-white p-7 transition-all duration-300 hover:-translate-y-1 hover:border-encre/20 hover:shadow-[0_28px_64px_-36px_rgba(51,54,66,.55)]"
                >
                  <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-encre">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" className="on-encre-jaune" aria-hidden="true">
                      <path d="M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8zM14 3v5h5M9 13h6M9 17h4" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  </span>
                  <h2 className="h-title mt-5 text-lg font-semibold text-encre">{f.nom}</h2>
                  <p className="mt-2 flex-1 font-body text-sm leading-relaxed text-soft">{f.desc}</p>
                  <span className="mt-5 h-px w-6 bg-jaune transition-all duration-300 group-hover:w-12" />
                </Link>
              </Reveal>
            ))}
          </div>

          <div className="mt-12 rounded-2xl border-l-4 border-jaune bg-nuage p-8">
            <h2 className="h-title text-lg font-semibold text-encre">Un document vous manque&nbsp;?</h2>
            <p className="mt-2 max-w-2xl font-body text-soft">
              Donnez-nous la référence du produit et le type de document recherché. On vous
              l&apos;envoie par e-mail, généralement dans la journée.
            </p>
            <Link href="/contact" className="btn-cta mt-6">Demander un document</Link>
          </div>

          <div className="mt-14">
            <h2 className="h-title text-sm font-semibold uppercase tracking-[0.14em] text-soft">
              Parcourir par univers
            </h2>
            <div className="mt-5 flex flex-wrap gap-3">
              {univers.map((u) => (
                <Link
                  key={u.slug}
                  href={`/${u.slug}`}
                  className="rounded-full border border-brume px-4 py-2 font-body text-sm text-encre transition-colors hover:border-encre hover:bg-nuage"
                >
                  {u.nom}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
