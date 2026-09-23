import {
  univers as tousUnivers,
  noeuds,
  produits as tousProduits,
  type Produit,
  type Noeud,
  type Spec,
  type DocumentPdf,
} from "@/lib/catalogue";
import visuelsBruts from "@/lib/visuels-produits.json";
import { specsParImportance } from "@/lib/specs";
import { parCotes } from "@/lib/tri-produits";
import { normaliserRecherche } from "@/lib/recherche-texte";

/**
 * Le catalogue visuel : les mêmes données que le site, lues comme un catalogue.
 *
 * Un chapitre par univers, une section par sous-catégorie, une famille par
 * catégorie qui porte des produits, une variante par fiche produit. Rien n'est
 * calculé ici qui ne soit déjà dans `lib/catalogue.ts` (généré) et dans le
 * manifeste des visuels (`lib/visuels-produits.json`, généré) : ce module
 * range, il n'invente pas.
 *
 * Deux règles qui font le catalogue :
 *  - une caractéristique identique sur toutes les variantes d'une famille se
 *    lit une fois, en tête de famille ; les autres se lisent sur chaque carte ;
 *  - une variante sans visuel dans le manifeste n'a PAS d'image. Le site sert
 *    alors le dessin SVG de la famille ; le catalogue, lui, montre un emplacement
 *    « visuel à compléter », parce qu'un dessin générique n'est pas le produit.
 *
 * Module serveur uniquement : il embarque le catalogue entier.
 */

export type Visuel = { src: string; largeur: number; hauteur: number; alt: string };

const visuels = visuelsBruts as unknown as {
  produits: Record<string, Visuel>;
  categories: Record<string, Visuel>;
};

export type Variante = {
  slug: string;
  nom: string;
  /** Fiche produit du site : la seule route d'un produit. */
  href: string;
  visuel: Visuel | null;
  /** Ce qui distingue cette variante des autres de la famille, par importance. */
  specs: Spec[];
  /** « 2,42 kg/m », ou null quand le poids n'est pas connu. */
  poids: string | null;
  /** Texte normalisé sur lequel porte le filtre du chapitre. */
  recherche: string;
};

export type Famille = {
  chemin: string;
  nom: string;
  accroche: string;
  /** Identifiant d'ancre dans la page du chapitre : `acier-profiles-carre-plein`. */
  ancre: string;
  /** Photo studio de la catégorie, telle que servie par le manifeste. */
  studio: Visuel | null;
  /** Caractéristiques identiques sur toutes les variantes. */
  communes: Spec[];
  finition: string | null;
  /** Longueurs standard, en mètres, quand elles sont les mêmes pour toute la famille. */
  longueurs: number[] | null;
  /** « au mètre », « à la plaque »… quand l'unité de vente est commune. */
  unite: string | null;
  /** Fiches techniques PDF rattachées à toutes les variantes. */
  pdfs: DocumentPdf[];
  variantes: Variante[];
  nbVisuels: number;
};

export type SectionCatalogue = {
  /** Sous-catégorie (nœud intermédiaire), ou null pour les familles rangées directement sous l'univers. */
  chemin: string | null;
  nom: string | null;
  accroche: string;
  familles: Famille[];
};

export type Chapitre = {
  slug: string;
  nom: string;
  /** Rang dans le catalogue, 1 à 6 : l'ordre des univers de lib/catalogue.ts. */
  numero: number;
  href: string;
  accroche: string;
  intro: string;
  sections: SectionCatalogue[];
  nbFamilles: number;
  nbProduits: number;
  nbVisuels: number;
  /** Jusqu'à quatre photos studio du chapitre, dans l'ordre du catalogue : l'ouverture visuelle. */
  studios: Visuel[];
};

export const ancreDeFamille = (chemin: string) => chemin.replace(/^\//, "").replace(/\//g, "-");

const poidsDe = (p: Produit) =>
  p.kg === null
    ? null
    : `${p.kg.toLocaleString("fr-BE", { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ${p.unitePoids || "kg"}`;

const memes = <T,>(valeurs: T[]) =>
  valeurs.length > 0 && valeurs.every((v) => JSON.stringify(v) === JSON.stringify(valeurs[0]));

/** Le poids est porté à part (`kg`) : il ne compte ni comme commun ni comme distinctif. */
const sansPoids = (specs: Spec[]) => specs.filter((s) => s.label !== "Poids");

function famille(n: Noeud, contexte: string[]): Famille {
  const produits = n.produits
    .map((s) => tousProduits[s])
    .filter((p): p is Produit => Boolean(p))
    .sort(parCotes);

  const communes: Spec[] = [];
  if (produits.length > 0) {
    for (const s of sansPoids(produits[0].specs)) {
      const partout = produits.every((p) => p.specs.some((x) => x.label === s.label && x.valeur === s.valeur));
      if (partout) communes.push(s);
    }
  }
  const communsLabels = new Set(communes.map((s) => s.label));

  const finitions = produits.map((p) => p.finition ?? null);
  const longueurs = produits.map((p) => p.longueurs ?? []);
  const unites = produits.map((p) => p.unite);
  const premiersPdfs = produits[0]?.pdfs ?? [];
  const pdfs = premiersPdfs.filter((d) => produits.every((p) => (p.pdfs ?? []).some((x) => x.fichier === d.fichier)));

  const variantes: Variante[] = produits.map((p) => ({
    slug: p.slug,
    nom: p.nom,
    href: `/p/${p.slug}`,
    visuel: visuels.produits[p.slug] ?? null,
    specs: specsParImportance(sansPoids(p.specs).filter((s) => !communsLabels.has(s.label))).slice(0, 3),
    poids: poidsDe(p),
    recherche: normaliserRecherche(
      [p.nom, ...p.specs.map((s) => `${s.label} ${s.valeur}`), n.nom, ...contexte].join(" ")
    ),
  }));

  return {
    chemin: n.chemin,
    nom: n.nom,
    accroche: n.accroche,
    ancre: ancreDeFamille(n.chemin),
    studio: visuels.categories[n.chemin] ?? null,
    communes: specsParImportance(communes),
    finition: memes(finitions) && finitions[0] ? finitions[0] : null,
    longueurs: memes(longueurs) && longueurs[0].length > 0 ? longueurs[0] : null,
    unite: memes(unites) && unites[0] ? unites[0] : null,
    pdfs,
    variantes,
    nbVisuels: variantes.filter((v) => v.visuel).length,
  };
}

/** Les familles d'un nœud, dans l'ordre du catalogue : lui-même s'il porte des produits, puis ses enfants. */
function famillesSous(n: Noeud, contexte: string[]): Famille[] {
  const propres = n.produits.length > 0 ? [famille(n, contexte)] : [];
  const enfants = n.enfants
    .map((c) => noeuds[c])
    .filter((e): e is Noeud => Boolean(e))
    .flatMap((e) => famillesSous(e, [...contexte, e.nom]));
  return [...propres, ...enfants];
}

function chapitre(numero: number, u: (typeof tousUnivers)[number]): Chapitre {
  const sections: SectionCatalogue[] = [];
  for (const chemin of u.enfants) {
    const n = noeuds[chemin];
    if (!n) continue;
    if (n.enfants.length === 0) {
      // Famille rangée directement sous l'univers : elle rejoint la section sans titre en cours.
      const derniere = sections[sections.length - 1];
      const f = famille(n, [u.nom]);
      if (derniere && derniere.chemin === null) derniere.familles.push(f);
      else sections.push({ chemin: null, nom: null, accroche: "", familles: [f] });
      continue;
    }
    sections.push({
      chemin: n.chemin,
      nom: n.nom,
      accroche: n.accroche,
      familles: famillesSous(n, [u.nom, n.nom]),
    });
  }
  const familles = sections.flatMap((s) => s.familles);
  return {
    slug: u.slug,
    nom: u.nom,
    numero,
    href: `/catalogue/${u.slug}`,
    accroche: u.accroche,
    intro: u.intro,
    sections,
    nbFamilles: familles.length,
    nbProduits: familles.reduce((t, f) => t + f.variantes.length, 0),
    nbVisuels: familles.reduce((t, f) => t + f.nbVisuels, 0),
    studios: familles.map((f) => f.studio).filter((s): s is Visuel => Boolean(s)).slice(0, 4),
  };
}

let cache: Chapitre[] | null = null;

/** Les six chapitres du catalogue, calculés une fois par processus de construction. */
export function chapitres(): Chapitre[] {
  if (!cache) cache = tousUnivers.map((u, i) => chapitre(i + 1, u));
  return cache;
}

export const chapitreParSlug = (slug: string) => chapitres().find((c) => c.slug === slug);

/** Les totaux de la couverture, recalculés depuis les chapitres : jamais écrits en dur. */
export function totauxCatalogue() {
  const tous = chapitres();
  return {
    chapitres: tous.length,
    familles: tous.reduce((t, c) => t + c.nbFamilles, 0),
    produits: tous.reduce((t, c) => t + c.nbProduits, 0),
    visuels: tous.reduce((t, c) => t + c.nbVisuels, 0),
  };
}
