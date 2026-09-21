import type { Produit } from "@/lib/catalogue";

/**
 * Structure la description d'une fiche produit pour le gabarit.
 *
 * Entrée : les blocs relevés sur le site actuel (`lib/descriptions-site-actuel.json`,
 * produits par `scripts/inventaire/integrer.py`) — titres, listes, paragraphes,
 * dans l'ordre du site. Sortie : les mêmes textes, mot pour mot, rangés par
 * famille sémantique pour que chaque famille reçoive le traitement visuel qui
 * lui va (chips, liste à coches, grille libellé/valeur). Rien n'est inventé,
 * rien n'est retiré — sauf une ligne « Poids » qui répète le poids du catalogue
 * déjà affiché en chiffres clés.
 *
 * Pure et déterministe : appelée côté serveur à la construction.
 */

export type BlocDescription = { t: "p" | "h"; texte: string } | { t: "ul"; items: string[] };
export type Cote = { lettre: string; valeur: string };
export type DescriptionSiteActuel = {
  courte: string;
  blocs: BlocDescription[];
  cotes?: Cote[];
  supplementCoupe: boolean;
};

export type TypeSection =
  | "presentation"
  | "applications"
  | "atouts"
  | "caracteristiques"
  | "services"
  | "conseils"
  | "autre";

export type Paire = { label: string; valeur: string };
export type Section = {
  type: TypeSection;
  titre: string;
  paragraphes: string[];
  /** Items de liste sans forme « libellé : valeur ». */
  items: string[];
  /** Items de liste (ou rangées de tableau aplati) « libellé : valeur ». */
  paires: Paire[];
};
export type DescriptionStructuree = {
  courte: string;
  /** Paragraphes qui précèdent le premier intertitre. */
  introduction: string[];
  sections: Section[];
};

const FAMILLES: [TypeSection, RegExp][] = [
  ["services", /\bservices?\b|d[ée]coupe|livraison/i],
  ["conseils", /conseil|entretien|mise en [oœ]uvre|installation|points? techniques/i],
  ["applications", /utilisation|application|usage|exemple|domaine/i],
  ["atouts", /points? forts?|avantage|atout|pourquoi choisir|b[ée]n[ée]fice/i],
  ["caracteristiques", /caract[ée]ristique|sp[ée]cification|dimension|finition|composition|technique/i],
  ["presentation", /description|pr[ée]sentation|design/i],
];

/** « Libellé : valeur » dans un item de liste (libellé court, sans phrase). */
const PAIRE = /^([^:]{2,40}?)\s*:\s+(.{2,})$/;

/** Rangées d'un tableau à deux colonnes aplati par le site source (libellés relevés dans les données). */
const RANGEE = /^(Type de produit|Marque|Modèle|Nervures|Face externe|Face interne|Longueurs|Épaisseur|Largeur utile|Largeur|Couleur|Finition|Poids)\s+(.+)$/;

/** « Poids 0,17 kg/m », « Poids: 0,9 kg » : la valeur numérique, ou null. */
const POIDS = /^Poids\s*:?\s*([\d.,]+)\s*kg/i;

export function typeDeSection(titre: string): TypeSection {
  for (const [type, re] of FAMILLES) if (re.test(titre)) return type;
  return "autre";
}

/** « CARACTÉRISTIQUES TECHNIQUES » → « Caractéristiques techniques » ; le reste est laissé tel quel. */
export function titrePropre(titre: string): string {
  const t = titre.trim();
  if (t.length > 3 && t === t.toUpperCase() && /[A-ZÉ]/.test(t)) {
    return t.charAt(0) + t.slice(1).toLowerCase();
  }
  return t;
}

function nouvelleSection(titre: string): Section {
  return { type: typeDeSection(titre), titre: titrePropre(titre), paragraphes: [], items: [], paires: [] };
}

function repeteLePoids(texte: string, p: Produit): boolean {
  const m = POIDS.exec(texte.trim());
  if (!m || p.kg === null) return false;
  const v = parseFloat(m[1].replace(",", "."));
  return Number.isFinite(v) && Math.abs(v - p.kg) < 0.005;
}

/** Une phrase qui se termine par « : » juste avant une liste en est l'amorce : elle dit ce que la liste est. */
const AMORCE: [TypeSection, RegExp][] = [
  ["applications", /utilis|applic|adapt[ée]|projets|id[ée]al pour|convient|destin[ée]|usage|sert/i],
  ["atouts", /garantiss|avantage|atout|assur|offr|permet|b[ée]n[ée]fic|apport/i],
  ["caracteristiques", /caract[ée]ristique|sp[ée]cification|dimension|disponible en|propos[ée]/i],
  ["services", /service|d[ée]coupe|livraison|sur demande/i],
];

function typeDAmorce(texte: string): TypeSection {
  for (const [type, re] of AMORCE) if (re.test(texte)) return type;
  return "autre";
}

function vide(s: Section): boolean {
  return s.paragraphes.length + s.items.length + s.paires.length === 0;
}

export function structurerDescription(desc: DescriptionSiteActuel | undefined, p: Produit): DescriptionStructuree {
  const resultat: DescriptionStructuree = { courte: desc?.courte ?? "", introduction: [], sections: [] };
  if (!desc) return resultat;

  let courante: Section | null = null;
  const pousser = () => {
    if (courante && !vide(courante)) resultat.sections.push(courante);
    courante = null;
  };

  for (const [i, b] of desc.blocs.entries()) {
    if (b.t === "h") {
      pousser();
      courante = nouvelleSection(b.texte);
      continue;
    }
    if (b.t === "ul") {
      if (!courante) courante = { type: "autre", titre: "", paragraphes: [], items: [], paires: [] };
      for (const item of b.items) {
        const m = PAIRE.exec(item);
        if (m) courante.paires.push({ label: m[1].trim(), valeur: m[2].trim() });
        else courante.items.push(item);
      }
      continue;
    }
    // paragraphe
    const texte = b.texte.trim();
    if (!texte || repeteLePoids(texte, p)) continue;
    const suivant = desc.blocs[i + 1];
    // Une amorce ouvre sa propre section, sauf sous un vrai intertitre (qui garde ses listes).
    if (texte.endsWith(":") && suivant && suivant.t === "ul" && (!courante || courante.titre === "")) {
      pousser();
      courante = { type: typeDAmorce(texte), titre: "", paragraphes: [texte], items: [], paires: [] };
      continue;
    }
    if (!courante) {
      resultat.introduction.push(texte);
      continue;
    }
    const r = courante.type === "caracteristiques" ? RANGEE.exec(texte) : null;
    if (r) courante.paires.push({ label: r[1], valeur: r[2].trim() });
    else courante.paragraphes.push(texte);
  }
  pousser();
  return resultat;
}

/** Les sections d'une famille, dans l'ordre du site. */
export function sectionsDe(d: DescriptionStructuree, ...types: TypeSection[]): Section[] {
  return d.sections.filter((s) => types.includes(s.type));
}
