import type { Metadata } from "next";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Recherche from "@/components/catalogue/Recherche";
import { totalProduits } from "@/lib/catalogue";

export const metadata: Metadata = {
  title: "Rechercher dans le catalogue | Aciers Grosjean",
  description: `Cherchez parmi ${totalProduits} produits et toutes les catégories : cornières, poutrelles, tubes, tôles, inox, aluminium, corten.`,
  alternates: { canonical: "/recherche" },
  robots: { index: false, follow: true },
};

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
          <Recherche />
        </div>
      </section>
      <CtaBand />
    </main>
  );
}
