import type { Metadata } from "next";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Recherche, { type EntreeRecherche } from "@/components/catalogue/Recherche";
import { noeuds, totalProduits, tousProduits } from "@/lib/catalogue";

export const metadata: Metadata = {
  title: "Rechercher dans le catalogue | Aciers Grosjean",
  description: `Cherchez parmi ${totalProduits} produits et toutes les catégories : cornières, poutrelles, tubes, tôles, inox, aluminium, corten.`,
  alternates: { canonical: "/recherche" },
  robots: { index: false, follow: true },
};

/**
 * L'index de recherche, construit ICI, sur le serveur.
 *
 * Il vivait dans `Recherche.tsx`, un composant « use client » : le catalogue
 * entier partait donc dans le navigateur, et Next le prechargait depuis chaque
 * page a cause du lien de recherche de l'en-tete — 485 Ko sur chaque visite,
 * mesures du 22/09. L'index ne retient que sept champs par entree ; le reste
 * (specifications, PDF, longueurs, finitions) n'a jamais besoin de traverser
 * le reseau. Regle de `CLAUDE.md` ligne 19, controle C1.
 */
const norm = (s: string) =>
  s
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, " ")
    .trim();

const INDEX: EntreeRecherche[] = [
  ...tousProduits.map((p) => ({
    type: "produit" as const,
    titre: p.nom,
    href: `/p/${p.slug}`,
    contexte: noeuds[p.categorie]?.nom ?? p.univers,
    prix: p.prix,
    unite: p.uniteCourte,
    cle: norm(p.nom + " " + p.specs.map((s) => s.valeur).join(" ")),
  })),
  ...Object.values(noeuds).map((n) => ({
    type: "categorie" as const,
    titre: n.nom,
    href: n.chemin,
    contexte: n.chemin.split("/")[1],
    prix: null as number | null,
    unite: "",
    cle: norm(n.nom + " " + n.accroche),
  })),
];

export default function RecherchePage() {
  return (
    <main>
      <PageHeader
        surtitre="Recherche"
        titre={<>Cherchez une <span className="mark-jaune">cote</span></>}
        intro={`${totalProduits} produits indexés. Tapez une section, une épaisseur, une nuance ou un usage — la recherche répond pendant que vous écrivez.`}
      />
      <section className="bg-white py-14 md:py-20">
        <div className="container-g max-w-3xl">
          <Recherche entrees={INDEX} />
        </div>
      </section>
      <CtaBand />
    </main>
  );
}
