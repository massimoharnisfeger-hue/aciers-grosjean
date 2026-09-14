import type { Metadata } from "next";
import PageHeader from "@/components/ui/PageHeader";
import DevisForm from "@/components/sections/DevisForm";
import { trust } from "@/lib/content";
import { univers } from "@/lib/catalogue";

export const metadata: Metadata = {
  title: "Demander un devis en 24h | Aciers Grosjean",
  description:
    "Décrivez votre projet acier : dimensions, quantités, usage. Devis sous 24h, sans engagement. Particuliers et professionnels.",
  alternates: { canonical: "/devis" },
};

export default function DevisPage() {
  return (
    <main>
      <PageHeader
        surtitre="Devis"
        titre={<>Votre devis en <span className="mark-jaune">24 heures</span></>}
        intro="Décrivez votre besoin, on revient vers vous sous 24h — sans engagement."
      />

      <section className="bg-white py-16 md:py-24">
        <div className="container-g grid gap-10 lg:grid-cols-[1fr_1.3fr]">
          <div>
            <h2 className="h-display text-2xl text-encre">Pourquoi nous demander un devis ?</h2>
            <ul className="mt-6 space-y-4">
              {trust.map((t) => (
                <li key={t.label} className="flex items-baseline gap-3">
                  <span className="h-title text-lg font-bold text-encre">{t.valeur}</span>
                  <span className="font-body text-soft">{t.label}</span>
                </li>
              ))}
            </ul>
            <div className="mt-8 rounded-2xl bg-nuage p-6">
              <p className="font-body text-sm text-soft">
                Besoin d'un conseil avant de chiffrer ? Appelez-nous, on vous oriente vers le bon produit sans jargon.
              </p>
            </div>
          </div>
          <DevisForm produits={univers.map((u) => u.nom)} />
        </div>
      </section>
    </main>
  );
}
