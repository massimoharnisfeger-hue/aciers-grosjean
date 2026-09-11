import type { Metadata } from "next";
import PageLegale from "@/components/ui/PageLegale";
import { site } from "@/lib/content";

export const metadata: Metadata = {
  title: "Mentions légales | Aciers Grosjean",
  description:
    "Éditeur du site, hébergeur, propriété intellectuelle et responsabilité — les mentions légales du site Aciers Grosjean.",
  alternates: { canonical: "/mentions-legales" },
};

export default function MentionsLegales() {
  return (
    <PageLegale
      surtitre="Mentions légales"
      titre="Mentions légales"
      intro="Qui édite ce site, qui l'héberge, et ce que vous pouvez en faire."
      aCompleter={[
        "Dénomination sociale exacte et forme juridique (SA, SRL…)",
        "Adresse du siège social",
        "Numéro d'entreprise BCE et numéro de TVA",
        "Nom du représentant légal / directeur de la publication",
        "Nom et adresse de l'hébergeur retenu",
      ]}
      blocs={[
        {
          titre: "1. Éditeur du site",
          paras: [
            "Le présent site est édité par le Groupe Aciers Grosjean, entreprise active dans la transformation et la distribution d'acier, de métal et d'aluminium, disposant de quatre dépôts à Charleroi, La Louvière, Tournai et Marville.",
            `Contact : ${site.email} — ${site.tel}.`,
            "Les mentions d'identification complètes exigées par le Code de droit économique belge (dénomination, forme juridique, siège social, numéro d'entreprise BCE et numéro de TVA) doivent être renseignées ci-dessus avant la mise en ligne publique du site.",
          ],
        },
        {
          titre: "2. Hébergement",
          paras: [
            "Le site est hébergé sur une infrastructure de diffusion de contenu. Les coordonnées complètes de l'hébergeur seront précisées ici une fois l'hébergement définitif retenu.",
          ],
        },
        {
          titre: "3. Propriété intellectuelle",
          paras: [
            "L'ensemble des éléments de ce site — structure, textes, illustrations techniques, schémas, mise en page et code — est protégé par le droit d'auteur. Toute reproduction ou représentation, totale ou partielle, sans autorisation écrite préalable est interdite.",
            "Les marques, logos et signes distinctifs reproduits sur le site sont la propriété de leurs titulaires respectifs.",
          ],
        },
        {
          titre: "4. Données techniques et prix",
          paras: [
            "Les dimensions, poids et caractéristiques mécaniques indiqués sur les fiches produits correspondent aux valeurs normalisées des normes européennes applicables (EN 10025, EN 10056, EN 10219, EN 10346 notamment) ou à des valeurs calculées à partir de la masse volumique du matériau. Ils sont donnés à titre indicatif.",
            "Les prix affichés sont indicatifs, exprimés hors TVA, et ne constituent pas une offre contractuelle. Le marché de l'acier évoluant de façon hebdomadaire, seul le devis nominatif fait foi.",
            "Les informations techniques publiées dans les guides ne remplacent en aucun cas une note de calcul de structure établie par un bureau d'études ou un architecte, laquelle reste obligatoire pour tout ouvrage porteur.",
          ],
        },
        {
          titre: "5. Responsabilité",
          paras: [
            "L'éditeur met tout en œuvre pour assurer l'exactitude des informations diffusées, sans garantir qu'elles soient exemptes d'erreur. Sa responsabilité ne saurait être engagée en cas de dommage résultant d'une utilisation des informations du site, en particulier d'un dimensionnement réalisé sans validation technique.",
            "Le site peut contenir des liens vers des sites tiers, sur le contenu desquels l'éditeur n'exerce aucun contrôle.",
          ],
        },
        {
          titre: "6. Droit applicable",
          paras: [
            "Le présent site est soumis au droit belge. Tout litige relatif à son utilisation relève de la compétence des juridictions belges.",
          ],
        },
      ]}
    />
  );
}
