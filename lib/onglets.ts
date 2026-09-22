import type { Produit } from "@/lib/catalogue";
import type { Cote, DescriptionStructuree, Paire, Section, TypeSection } from "@/lib/description";

/**
 * Construit les onglets de la section « Le produit en détail » d'une fiche.
 *
 * Module pur : aucun React, aucun `use client`. Il se teste et se relit sans
 * rendu (contrôle O1).
 *
 * Trois règles le gouvernent.
 *
 * 1. **Rien n'est inventé.** Chaque valeur affichée vient de `lib/catalogue.ts`
 *    ou de la description relevée sur le site officiel. Un onglet sans contenu
 *    réel n'est pas produit — il n'y a pas d'onglet vide, pas de texte de
 *    remplissage.
 *
 * 2. **Rien n'est doublé.** La colonne de droite de la fiche rend déjà les
 *    spécifications (`p.specs`) et les documents (`p.pdfs`). Les onglets ne les
 *    reprennent pas : ils portent ce que cette section possède en propre — la
 *    description structurée — et ce qui n'était affiché nulle part : les
 *    **cotes** (contrôle O4).
 *
 * 3. **Rien n'est perdu.** Les sept `TypeSection` de `lib/description.ts` sont
 *    toutes acheminées vers un onglet ; `MAP` ci-dessous en est la preuve
 *    lisible, et le contrôle O2 échoue si l'une d'elles disparaît.
 */

/** Visuel d'une fiche ou d'une catégorie (`lib/visuels-produits.json`). */
export type Visuel = { src: string; largeur: number; hauteur: number; alt: string };

/**
 * Un bloc de contenu d'origine, tel que le site source l'a écrit.
 *
 * Un onglet en porte un ou plusieurs : « Mise en œuvre » réunit les conseils
 * et les services. Les garder séparés conserve leur titre d'origine — les
 * aplatir en une seule liste le perdait — et permet à chacun de porter son
 * `data-module`, le marqueur que le contrôle P9 vérifie dans le HTML servi.
 */
export type BlocOnglet = {
  type: TypeSection;
  /** Titre écrit par le site source, vide s'il n'en avait pas. */
  titre: string;
  paragraphes: string[];
  items: string[];
  paires: Paire[];
};

export type Onglet = {
  cle: string;
  /** Libellé de l'onglet, court : il doit tenir dans une pastille sur mobile. */
  libelle: string;
  /** Nature du contenu, affichée en pastille au-dessus du titre. */
  badge: string;
  titre: string;
  blocs: BlocOnglet[];
  /** Visuel réellement lié à ce contenu, ou absent : jamais une image d'emprunt. */
  visuel?: Visuel;
  /** Action réelle du site, ou absente : jamais un bouton décoratif. */
  action?: { libelle: string; href: string };
  /** Mention de la découpe, seulement si la fiche la porte. */
  note?: string;
};

/**
 * Où va chaque type de section. Deux types partagent l'onglet « Mise en
 * œuvre » : `conseils` (12 fiches) et `services` (16) sont trop rares pour
 * mériter chacun sa pastille, et parlent tous deux de ce qui se passe après
 * l'achat. `presentation` rejoint « À savoir » : son contenu est du complément,
 * l'accroche étant déjà servie en tête de fiche.
 */
const MAP: Record<TypeSection, string> = {
  "caracteristiques": "caracteristiques",
  "applications": "applications",
  "atouts": "atouts",
  "conseils": "mise-en-oeuvre",
  "services": "mise-en-oeuvre",
  "presentation": "presentation",
  "autre": "a-savoir",
};

/** Ordre d'apparition : du plus technique au plus contextuel. */
const ORDRE = ["presentation", "dimensions", "caracteristiques", "applications", "atouts", "mise-en-oeuvre", "a-savoir"] as const;

const LIBELLES: Record<string, { libelle: string; badge: string; titre: string }> = {
  presentation: { libelle: "Présentation", badge: "En bref", titre: "Ce qu'il faut retenir" },
  dimensions: { libelle: "Dimensions", badge: "Cotes relevées", titre: "Les cotes de ce produit" },
  caracteristiques: { libelle: "Caractéristiques", badge: "Fiche technique", titre: "Ce qui définit ce produit" },
  applications: { libelle: "Applications", badge: "Usages", titre: "À quoi il sert" },
  atouts: { libelle: "Points forts", badge: "Atouts", titre: "Pourquoi ce produit" },
  "mise-en-oeuvre": { libelle: "Mise en œuvre", badge: "Pose et services", titre: "Avant et après l'achat" },
  "a-savoir": { libelle: "À savoir", badge: "Complément", titre: "Bon à savoir" },
};

const blocVide = (b: BlocOnglet) =>
  b.paragraphes.length === 0 && b.items.length === 0 && b.paires.length === 0;

function enBlocs(sections: Section[]): BlocOnglet[] {
  return sections
    .map((s) => ({
      type: s.type,
      titre: s.titre,
      paragraphes: s.paragraphes,
      items: s.items,
      paires: s.paires,
    }))
    .filter((b) => !blocVide(b));
}

/**
 * L'onglet des cotes : 355 fiches en portent, et elles n'étaient affichées
 * nulle part. Le rendu 3D de la fiche montre ces mêmes lettres — c'est donc le
 * seul visuel qui explique vraiment le tableau, et il n'est pas emprunté à un
 * autre produit.
 */
function ongletDimensions(p: Produit, cotes: Cote[], visuel: Visuel | undefined, coupe: boolean): Onglet | null {
  const paires: Paire[] = cotes.map((c) => ({ label: `Cote ${c.lettre}`, valeur: c.valeur }));
  if (p.longueurs && p.longueurs.length > 0) {
    paires.push({
      label: "Longueurs standard",
      valeur: p.longueurs.map((l) => `${l.toLocaleString("fr-BE")} m`).join(" · "),
    });
  }
  if (paires.length === 0) return null;

  const details =
    `${p.nom}\n` +
    cotes.map((c) => `Cote ${c.lettre} : ${c.valeur}`).join("\n") +
    `\n\nLongueur souhaitée : `;

  return {
    cle: "dimensions",
    ...LIBELLES.dimensions,
    blocs: [{ type: "caracteristiques", titre: "", paragraphes: [], items: [], paires }],
    visuel,
    note: coupe
      ? "Ces cotes sont celles du profil. La longueur se coupe à la demande ; un supplément de coupe s’ajoute au prix affiché."
      : undefined,
    action: coupe
      ? { libelle: "Demander cette découpe", href: `/devis?details=${encodeURIComponent(details)}` }
      : undefined,
  };
}

export function ongletsDe(
  p: Produit,
  ds: DescriptionStructuree,
  cotes: Cote[],
  supplementCoupe: boolean,
  visuels: { fiche?: Visuel; categorie?: Visuel },
): Onglet[] {
  const groupes = new Map<string, Section[]>();
  for (const section of ds.sections) {
    const cle = MAP[section.type];
    const deja = groupes.get(cle);
    if (deja) deja.push(section);
    else groupes.set(cle, [section]);
  }

  // L'introduction devient le bloc de tete de l'onglet « Presentation » plutot
  // qu'un texte libre au-dessus des onglets : sans cela, la fiche change de
  // squelette selon qu'elle a ou non une introduction. Demande du 22/09 :
  // « il faut qu'a chaque fois ca garde la meme structure ».
  if (ds.introduction.length > 0) {
    const deja = groupes.get("presentation") ?? [];
    groupes.set("presentation", [
      { type: "presentation", titre: "", paragraphes: ds.introduction, items: [], paires: [] },
      ...deja,
    ]);
  }

  const onglets: Onglet[] = [];
  const dimensions = ongletDimensions(p, cotes, visuels.fiche, supplementCoupe);

  for (const cle of ORDRE) {
    if (cle === "dimensions") {
      if (dimensions) onglets.push(dimensions);
      continue;
    }
    const sections = groupes.get(cle);
    if (!sections) continue;
    const blocs = enBlocs(sections);
    if (blocs.length === 0) continue;
    onglets.push({
      cle,
      ...LIBELLES[cle],
      blocs,
      // La photo studio de la catégorie montre la famille en situation : elle
      // éclaire les usages, pas les cotes. Ailleurs, pas de visuel du tout.
      visuel: cle === "applications" ? visuels.categorie : undefined,
    });
  }

  return onglets;
}
