import type { Metadata } from "next";
import Link from "next/link";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Reveal from "@/components/fx/Reveal";
import { univers } from "@/lib/catalogue";
import documentsBruts from "@/lib/documents.json";

export const metadata: Metadata = {
  title: "Documentation technique et fiches produits",
  description:
    "Fiches techniques, notices de pose et documentation des fabricants en PDF : tôles, tubes, poutrelles, clôtures, toiture et bardage.",
  alternates: { canonical: "/documentation" },
};

/** Documents publiés dans public/documents (scripts/inventaire/integrer.py). */
type Doc = { fichier: string; titre: string; groupe: string; tailleKo: number; produits: number };
const documents = documentsBruts as Doc[];

const GROUPES = [
  {
    cle: "fiches-produits",
    titre: "Fiches techniques des produits",
    intro: "Les fiches liées au catalogue : dimensions, tolérances, poids et nuances. Chacune est aussi proposée sur les fiches produits concernées.",
  },
  {
    cle: "toiture-bardage",
    titre: "Toiture & bardage",
    intro: "Documentation des fabricants : profils, panneaux isolés, accessoires, nuancier et manuel technique.",
  },
  { cle: "entreprise", titre: "L'entreprise", intro: "" },
];

const taille = (ko: number) =>
  ko >= 1024 ? `${(ko / 1024).toLocaleString("fr-BE", { maximumFractionDigits: 1 })} Mo` : `${ko} Ko`;

export default function DocumentationPage() {
  return (
    <main>
      <PageHeader
        surtitre="Documentation"
        titre={<>Les documents <span className="mark-jaune">techniques</span></>}
        intro={`${documents.length} documents à télécharger en PDF. Si celui que vous cherchez n'est pas listé, demandez-le : il existe presque toujours.`}
      />

      <section className="bg-white py-14 md:py-20">
        <div className="container-g space-y-14">
          {GROUPES.map((g) => {
            const liste = documents.filter((d) => d.groupe === g.cle);
            if (!liste.length) return null;
            return (
              <div key={g.cle}>
                <Reveal>
                  <h2 className="h-display text-2xl md:text-3xl">{g.titre}</h2>
                  {g.intro && <p className="mt-2 max-w-2xl font-body text-soft">{g.intro}</p>}
                </Reveal>
                <ul className="mt-6 grid gap-3 md:grid-cols-2">
                  {liste.map((d) => (
                    <li key={d.fichier}>
                      <a
                        href={d.fichier}
                        target="_blank"
                        rel="noopener"
                        className="group flex h-full items-center gap-4 rounded-2xl border border-brume bg-white px-5 py-4 transition-all duration-300 hover:-translate-y-0.5 hover:border-encre/20 hover:shadow-[0_20px_48px_-32px_rgba(51,54,66,.5)]"
                      >
                        <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-encre">
                          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" className="on-encre-jaune" aria-hidden="true">
                            <path d="M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8zM14 3v5h5M12 11v6M9.5 14.5L12 17l2.5-2.5" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" />
                          </svg>
                        </span>
                        <span className="min-w-0 flex-1">
                          <span className="h-title block font-semibold leading-snug text-encre">
                            {d.titre.replace(/^(Fiche technique|Notice de pose) — /, "")}
                          </span>
                          <span className="mt-0.5 block font-body text-xs text-soft">
                            {d.titre.startsWith("Notice de pose") ? "Notice de pose" : g.cle === "fiches-produits" ? "Fiche technique" : "PDF"}
                            {" · "}
                            {taille(d.tailleKo)}
                            {d.produits > 0 && ` · ${d.produits} produit${d.produits > 1 ? "s" : ""}`}
                          </span>
                        </span>
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            );
          })}

          <div className="rounded-2xl border-l-4 border-jaune bg-nuage p-8">
            <h2 className="h-title text-lg font-semibold text-encre">Un document vous manque&nbsp;?</h2>
            <p className="mt-2 max-w-2xl font-body text-soft">
              Certificats matière, fiches de sécurité, abaques : donnez-nous la référence du produit et le
              type de document recherché. On vous l&apos;envoie par e-mail, généralement dans la journée.
            </p>
            <Link href="/contact" className="btn-cta mt-6">Demander un document</Link>
          </div>

          <div>
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
