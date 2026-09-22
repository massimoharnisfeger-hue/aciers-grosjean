import type { DocumentPdf, Produit } from "@/lib/catalogue";
import type { Cote, DescriptionStructuree, Paire, Section, TypeSection } from "@/lib/description";
import { usageDe } from "@/lib/usages";

/**
 * Construit les onglets de la section « Le produit en détail » d'une fiche.
 *
 * Module pur : aucun React, aucun `use client`. Il se teste et se relit sans
 * rendu (contrôle O1).
 *
 * **Trois onglets, pas plus** (demande du propriétaire, 22/09 : « il y a
 * beaucoup trop d'onglets »). La première version en proposait neuf, et les
 * fiches en portaient quatre à six : on ne savait plus où regarder, et certains
 * onglets ne contenaient que trois lignes. Les neuf familles se replient donc
 * en trois, sans qu'aucun contenu ne disparaisse :
 *
 * - **Caractéristiques** — tout ce qui se mesure : la fiche technique, les
 *   cotes relevées, et ce que le site officiel dit des caractéristiques ;
 * - **Usage** — tout ce qui explique : à quoi ça sert, les points forts, la
 *   mise en œuvre, et le complément « à savoir » ;
 * - **Documents** — les PDF, quand la fiche en a.
 *
 * Trois règles gouvernent le contenu.
 *
 * 1. **Rien n'est inventé.** Chaque valeur vient de `lib/catalogue.ts` ou de la
 *    description relevée sur le site officiel. Un onglet sans contenu réel
 *    n'est pas produit — pas d'onglet vide, pas de texte de remplissage.
 *
 * 2. **Rien n'est doublé.** Les spécifications et les documents ont quitté la
 *    colonne de droite de la fiche pour vivre ici ; le contrôle O4 refuse les
 *    deux emplacements à la fois.
 *
 * 3. **Rien n'est perdu.** Les sept `TypeSection` de `lib/description.ts` sont
 *    toutes acheminées : `MAP` en est la preuve lisible, et le contrôle O2
 *    échoue si l'une d'elles disparaît.
 */

/** Visuel d'une fiche ou d'une catégorie (`lib/visuels-produits.json`). */
export type Visuel = { src: string; largeur: number; hauteur: number; alt: string };

/**
 * Un bloc de contenu d'origine, tel que le site source l'a écrit.
 *
 * Un onglet en porte plusieurs : « Caractéristiques » réunit la fiche
 * technique, les cotes et la prose du site. Les garder séparés conserve leur
 * titre d'origine — les aplatir en une seule liste le perdait — et permet à
 * chacun de porter son `data-module`, le marqueur que le contrôle P9 vérifie
 * dans le HTML servi.
 */
export type BlocOnglet = {
  type: TypeSection;
  /** Titre affiché au-dessus du bloc, vide s'il n'en faut pas. */
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
  /**
   * Ce que le visuel montre, dit au visiteur sous l'image.
   *
   * La légende suit l'IMAGE, pas l'onglet : le 22/09 elle se déduisait de la
   * clé d'onglet, et le rendu 3D coté de l'onglet Caractéristiques s'affichait
   * sous la mention « photo studio ». Un visiteur lisait une légende fausse.
   */
  legendeVisuel?: string;
  /** Action réelle du site, ou absente : jamais un bouton décoratif. */
  action?: { libelle: string; href: string };
  /** Mention de la découpe, seulement si la fiche la porte. */
  note?: string;
  /** Documents PDF de la fiche, rendus en liens de téléchargement. */
  pdfs?: DocumentPdf[];
};

/**
 * Où va chaque type de section. Les sept types du site source se répartissent
 * entre deux onglets seulement : ce qui se mesure, et ce qui s'explique.
 */
const MAP: Record<TypeSection, string> = {
  "caracteristiques": "caracteristiques",
  "applications": "usage",
  "atouts": "usage",
  "conseils": "usage",
  "services": "usage",
  "presentation": "usage",
  "autre": "usage",
};

/** Ordre d'apparition : le technique d'abord, le contexte ensuite, les pièces jointes en dernier. */
const ORDRE = ["caracteristiques", "usage", "documents"] as const;

const LIBELLES: Record<string, { libelle: string; badge: string; titre: string }> = {
  caracteristiques: { libelle: "Caractéristiques", badge: "Fiche technique", titre: "Ce qui définit ce produit" },
  usage: { libelle: "Usage", badge: "À quoi ça sert", titre: "Où l'employer" },
  documents: { libelle: "Documents", badge: "À télécharger", titre: "Les documents de ce produit" },
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

/** `Cote A` : la lettre renvoie à celle que porte le rendu 3D, affiché à côté. */
function blocCotes(p: Produit, cotes: Cote[]): BlocOnglet | null {
  const paires: Paire[] = cotes.map((c) => ({ label: `Cote ${c.lettre}`, valeur: c.valeur }));
  if (p.longueurs && p.longueurs.length > 0) {
    paires.push({
      label: "Longueurs standard",
      valeur: p.longueurs.map((l) => `${l.toLocaleString("fr-BE")} m`).join(" · "),
    });
  }
  if (paires.length === 0) return null;
  return { type: "caracteristiques", titre: "Les cotes", paragraphes: [], items: [], paires };
}

/**
 * La fiche technique : matière, spécifications relevées, poids, finition.
 *
 * Ces données étaient dans la colonne de droite de la fiche ; elles vivent ici
 * depuis le 22/09, pour que chaque fiche porte les mêmes rubriques — 472 fiches
 * sur 495 en ont. Elles ne sont plus rendues ailleurs (contrôle O4).
 */
function blocTechnique(p: Produit, matiere: string): BlocOnglet | null {
  const paires: Paire[] = [{ label: "Matière", valeur: matiere }];
  for (const s of p.specs) paires.push({ label: s.label, valeur: s.valeur });
  if (p.kg !== null) {
    paires.push({ label: "Poids", valeur: `${p.kg.toString().replace(".", ",")} ${p.unitePoids || "kg"}` });
  }
  if (p.finition) paires.push({ label: "Finition", valeur: p.finition });
  if (paires.length <= 1) return null;

  // Un même libellé peut venir des specs et du calcul : la première valeur gagne.
  const vus = new Set<string>();
  const uniques = paires.filter((pa) => (vus.has(pa.label) ? false : (vus.add(pa.label), true)));
  return { type: "caracteristiques", titre: "", paragraphes: [], items: [], paires: uniques };
}

/**
 * L'usage de la famille, en complément de ce que le site officiel dit déjà.
 *
 * Constat du 22/09 sur la cornière 40x40x4 : l'onglet Usage disait trois fois
 * la même chose. Le site écrivait « un profil en L dont les deux ailes ont la
 * même largeur », puis « utilisée pour assembler, renforcer ou consolider des
 * structures » ; et le texte de famille rajoutait « sert à former un angle
 * rigide : renfort d'assemblage… À ailes égales, les deux faces jouent le même
 * rôle ». La règle d'alors n'écartait le texte de famille que si la fiche avait
 * une SECTION « Applications » titrée — or ici l'usage vivait dans les
 * paragraphes d'introduction.
 *
 * La règle tient maintenant compte de ce que le site dit vraiment, où qu'il le
 * dise. Quand il parle déjà d'usage, on ne garde du texte de famille que les
 * **exemples** : la seule chose qu'il n'apporte jamais, et la seule qui se
 * balaie du regard. Quand il ne dit rien, le texte de famille passe en entier.
 *
 * Le relevé prime donc toujours, et aucune fiche ne reçoit un usage inventé
 * pour elle : le texte parle de la famille, jamais de la référence précise.
 */
function blocUsageDeFamille(categorie: string, leSiteParleDejaDUsage: boolean): BlocOnglet | null {
  const usage = usageDe(categorie);
  if (!usage) return null;
  return {
    type: "applications",
    titre: "Emplois courants",
    paragraphes: leSiteParleDejaDUsage ? [] : [usage.texte],
    items: usage.exemples,
    paires: [],
  };
}

export function ongletsDe(
  p: Produit,
  ds: DescriptionStructuree,
  cotes: Cote[],
  supplementCoupe: boolean,
  visuels: { fiche?: Visuel; categorie?: Visuel },
  matiere: string,
): Onglet[] {
  const groupes = new Map<string, Section[]>();
  for (const section of ds.sections) {
    const cle = MAP[section.type];
    const deja = groupes.get(cle);
    if (deja) deja.push(section);
    else groupes.set(cle, [section]);
  }

  // --- Caractéristiques : la fiche technique, les cotes, puis la prose du site.
  const technique = blocTechnique(p, matiere);
  const lesCotes = blocCotes(p, cotes);
  const blocsTechniques = [
    ...(technique ? [technique] : []),
    ...(lesCotes ? [lesCotes] : []),
    ...enBlocs(groupes.get("caracteristiques") ?? []),
  ];

  // --- Usage : l'introduction en tête, puis ce que le site en dit, sinon la famille.
  // Le site parle d'usage s'il a une section « Applications », ou simplement
  // s'il a une introduction : c'est là que la cornière expliquait son emploi.
  const sections = groupes.get("usage") ?? [];
  const leSiteParleDejaDUsage =
    ds.introduction.length > 0 || sections.some((s) => s.type === "applications");
  const repli = blocUsageDeFamille(p.categorie, leSiteParleDejaDUsage);
  const blocsUsage = [
    ...(ds.introduction.length > 0
      ? [{ type: "presentation" as TypeSection, titre: "", paragraphes: ds.introduction, items: [], paires: [] }]
      : []),
    ...enBlocs(sections),
    ...(repli ? [repli] : []),
  ];

  const details =
    `${p.nom}\n` +
    cotes.map((c) => `Cote ${c.lettre} : ${c.valeur}`).join("\n") +
    `\n\nLongueur souhaitée : `;

  const parCle: Record<string, Onglet | null> = {
    caracteristiques:
      blocsTechniques.length > 0
        ? {
            cle: "caracteristiques",
            ...LIBELLES.caracteristiques,
            blocs: blocsTechniques,
            visuel: visuels.fiche,
            legendeVisuel: visuels.fiche ? "Rendu 3D aux cotes" : undefined,
            note: supplementCoupe
              ? "Les cotes sont celles du profil. La longueur se coupe à la demande ; un supplément de coupe s’ajoute au prix affiché."
              : undefined,
            action:
              supplementCoupe && cotes.length > 0
                ? { libelle: "Demander cette découpe", href: `/devis?details=${encodeURIComponent(details)}` }
                : undefined,
          }
        : null,
    usage:
      blocsUsage.length > 0
        ? {
            cle: "usage",
            ...LIBELLES.usage,
            blocs: blocsUsage,
            // La photo studio de la catégorie montre la famille : elle éclaire
            // l'usage. C'est ici que viendra la mise en situation.
            visuel: visuels.categorie,
            legendeVisuel: visuels.categorie ? "Photo studio" : undefined,
          }
        : null,
    documents:
      p.pdfs && p.pdfs.length > 0
        ? { cle: "documents", ...LIBELLES.documents, blocs: [], pdfs: p.pdfs }
        : null,
  };

  return ORDRE.map((cle) => parCle[cle]).filter((o): o is Onglet => o !== null);
}
