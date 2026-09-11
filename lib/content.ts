// Contenu Aciers Grosjean — issu de la charte officielle.
// Prix à titre d'exemple (charte) — à confirmer/mettre à jour.

export const site = {
  nom: "Aciers Grosjean",
  baseline: "L'acier de pro, accessible à tous",
  tel: "+32 (0)71 00 00 00",
  email: "info@aciersgrosjean.be",
};

export const trust = [
  { valeur: "40 ans", label: "d'expertise acier" },
  { valeur: "4 dépôts", label: "Wallonie + France" },
  { valeur: "EN1090", label: "certifié Exc2" },
  { valeur: "500+", label: "références en stock" },
  { valeur: "24h", label: "devis sans engagement" },
];

// Bandeau défilant (marquee)
export const arguments_ = [
  "Découpe sur mesure",
  "Retrait le jour même",
  "Devis en 24h",
  "Particuliers & pros",
  "Certifié EN1090-Exc2",
  "Entreprise familiale wallonne",
  "500+ références en stock",
  "Sans engagement",
];

// Compteurs animés
export const chiffres = [
  { valeur: 40, suffixe: " ans", label: "d'expertise" },
  { valeur: 4, suffixe: "", label: "dépôts" },
  { valeur: 500, suffixe: "+", label: "références en stock" },
  { valeur: 24, suffixe: "h", label: "pour votre devis" },
];

export type Produit = {
  nom: string;
  desc: string;
  prix: string;
  usages: string;
  stock: boolean;
};

export const produits: Produit[] = [
  { nom: "Poutrelles IPE · HEA · HEB", desc: "Profilés normalisés pour structures et charpentes métalliques.", prix: "Sur devis", usages: "Structure, charpente, mezzanine", stock: true },
  { nom: "Tôles", desc: "Tôles laminées, profilées et nervurées, plusieurs épaisseurs.", prix: "dès 14,71 €/m²", usages: "Bardage, toiture, habillage", stock: true },
  { nom: "Tubes ronds & carrés", desc: "Tubes acier pour ossatures, garde-corps et mobilier.", prix: "dès 3,20 €/m", usages: "Garde-corps, ossature, portail", stock: true },
  { nom: "Cornières", desc: "Cornières égales à ailes, idéales pour renforts et assemblages.", prix: "dès 2,85 €/m", usages: "Renfort, cadre, support", stock: true },
  { nom: "Acier corten", desc: "L'acier à la patine rouille, pour l'aménagement extérieur.", prix: "Sur devis", usages: "Terrasse, déco jardin, bardage", stock: true },
  { nom: "Plats & treillis", desc: "Plats laminés et treillis soudés pour le bâtiment.", prix: "dès 1,95 €/m", usages: "Béton armé, renfort, ferronnerie", stock: true },
];

// Catalogue détaillé (page Produits) — catégories avec références
export type Categorie = {
  slug: string;
  titre: string;
  intro: string;
  refs: { nom: string; dim: string; prix: string }[];
};

export const categories: Categorie[] = [
  {
    slug: "poutrelles",
    titre: "Poutrelles & profilés",
    intro: "Profilés normalisés pour la structure : charpentes, mezzanines, planchers.",
    refs: [
      { nom: "IPE 80", dim: "80 × 46 mm", prix: "Sur devis" },
      { nom: "IPE 120", dim: "120 × 64 mm", prix: "Sur devis" },
      { nom: "HEA 100", dim: "96 × 100 mm", prix: "Sur devis" },
      { nom: "HEB 120", dim: "120 × 120 mm", prix: "Sur devis" },
    ],
  },
  {
    slug: "tubes",
    titre: "Tubes ronds & carrés",
    intro: "Pour ossatures, garde-corps, portails et mobilier métallique.",
    refs: [
      { nom: "Tube carré 40×40×2", dim: "2 mm", prix: "3,20 €/m" },
      { nom: "Tube carré 50×50×3", dim: "3 mm", prix: "5,90 €/m" },
      { nom: "Tube rond Ø33,7×2", dim: "2 mm", prix: "sur devis" },
      { nom: "Tube rond Ø48,3×3", dim: "3 mm", prix: "sur devis" },
    ],
  },
  {
    slug: "toles",
    titre: "Tôles",
    intro: "Laminées, profilées, nervurées — bardage, toiture, habillage.",
    refs: [
      { nom: "Tôle lisse 2 mm", dim: "au m²", prix: "18,50 €/m²" },
      { nom: "Tôle nervurée", dim: "au m²", prix: "dès 14,71 €/m²" },
      { nom: "Tôle larmée 3 mm", dim: "au m²", prix: "sur devis" },
      { nom: "Tôle galvanisée", dim: "plusieurs ép.", prix: "sur devis" },
    ],
  },
  {
    slug: "cornieres-plats",
    titre: "Cornières & plats",
    intro: "Renforts, cadres, supports et ferronnerie.",
    refs: [
      { nom: "Cornière 40×40×4", dim: "4 mm", prix: "2,85 €/m" },
      { nom: "Cornière 50×50×5", dim: "5 mm", prix: "sur devis" },
      { nom: "Plat 30×3", dim: "3 mm", prix: "1,95 €/m" },
      { nom: "Plat 50×5", dim: "5 mm", prix: "sur devis" },
    ],
  },
  {
    slug: "corten",
    titre: "Acier corten",
    intro: "La patine rouille pour l'aménagement extérieur : terrasses, déco, bardage.",
    refs: [
      { nom: "Tôle corten 2 mm", dim: "au m²", prix: "Sur devis" },
      { nom: "Bac corten déco", dim: "sur mesure", prix: "Sur devis" },
      { nom: "Bardage corten", dim: "sur mesure", prix: "Sur devis" },
      { nom: "Bordure jardin", dim: "sur mesure", prix: "Sur devis" },
    ],
  },
  {
    slug: "treillis",
    titre: "Treillis & armatures",
    intro: "Treillis soudés et aciers pour béton armé.",
    refs: [
      { nom: "Treillis soudé", dim: "panneaux std", prix: "Sur devis" },
      { nom: "Rond à béton", dim: "Ø6 à Ø16", prix: "Sur devis" },
      { nom: "Fil recuit", dim: "bobine", prix: "Sur devis" },
      { nom: "Écarteurs", dim: "sachet", prix: "Sur devis" },
    ],
  },
];

export type Service = { nom: string; desc: string; detail?: string };

export const services: Service[] = [
  { nom: "Découpe sur mesure", desc: "Vos pièces coupées aux bonnes dimensions, prêtes à l'emploi.", detail: "Sciage et cisaillage aux cotes exactes. Vous ne payez que ce dont vous avez besoin, et vous gagnez du temps sur le chantier." },
  { nom: "Transformation & façonnage", desc: "Pliage, perçage, mise en forme selon votre plan.", detail: "Pliage, perçage, poinçonnage : on prépare la matière selon votre plan pour qu'elle arrive prête à assembler." },
  { nom: "Conseil technique", desc: "Un doute sur la nuance ou l'épaisseur ? On vous oriente.", detail: "40 ans d'expérience à votre service : nuance, épaisseur, protection anticorrosion — on vous guide vers le bon produit." },
  { nom: "Click & collect", desc: "Vous commandez, vous retirez en dépôt — souvent le jour même.", detail: "Commande simple, retrait rapide dans le dépôt de votre choix. Souvent disponible le jour même." },
];

export const publics = [
  { titre: "Vous êtes un particulier", texte: "Terrasse, portail, clôture, garde-corps, déco de jardin… On rend l'acier de qualité pro accessible, sans jargon et sans intimidation. Prix clairs, retrait rapide.", points: ["Sans compte pro", "Petites quantités acceptées", "Retrait en dépôt"] },
  { titre: "Vous êtes un professionnel", texte: "Artisan, métallier, entrepreneur : un partenaire réactif, un stock profond et des services de transformation pour tenir vos délais de chantier.", points: ["Devis en 24h", "Accompagnement dédié", "Découpe & façonnage"] },
];

// Comparaison qualité pro vs grande surface
export const comparaison = {
  titre: "Pourquoi pas la grande surface ?",
  intro: "Le rayon métal d'un magasin de bricolage dépanne. Pour un projet qui doit tenir, la différence se voit — et se paie moins cher au mètre.",
  lignes: [
    { critere: "Choix & épaisseurs", grosjean: "500+ références, toutes épaisseurs", autre: "Quelques formats standard" },
    { critere: "Découpe sur mesure", grosjean: "Oui, aux cotes exactes", autre: "Rarement, longueurs fixes" },
    { critere: "Conseil technique", grosjean: "40 ans d'expertise", autre: "Vendeur généraliste" },
    { critere: "Prix au mètre", grosjean: "Tarif négociant", autre: "Marge grande distribution" },
    { critere: "Certification", grosjean: "EN1090-Exc2", autre: "Non communiquée" },
  ],
};

export const etapes = [
  { n: "01", titre: "Choisissez", texte: "Parcourez le catalogue ou décrivez votre projet." },
  { n: "02", titre: "Devis en 24h", texte: "On chiffre votre demande sous 24h, sans engagement." },
  { n: "03", titre: "Découpe", texte: "On prépare et découpe vos pièces sur mesure." },
  { n: "04", titre: "Retrait", texte: "Vous retirez en dépôt, souvent le jour même." },
];

export type Depot = { ville: string; pays: string; adresse: string; tel: string; horaires: string };

export const depots: Depot[] = [
  { ville: "Charleroi", pays: "Belgique", adresse: "Zoning industriel — Charleroi", tel: "+32 (0)71 00 00 00", horaires: "Lun–Ven 7h–17h · Sam 8h–12h" },
  { ville: "La Louvière", pays: "Belgique", adresse: "Zoning — La Louvière", tel: "+32 (0)64 00 00 00", horaires: "Lun–Ven 7h–17h" },
  { ville: "Tournai", pays: "Belgique", adresse: "Zoning — Tournai", tel: "+32 (0)69 00 00 00", horaires: "Lun–Ven 7h–17h" },
  { ville: "Marville", pays: "France", adresse: "Zone d'activité — Marville", tel: "+33 (0)3 00 00 00 00", horaires: "Lun–Ven 8h–17h" },
];

// Réalisations (placeholders — à remplacer par de vraies photos de projets)
export const realisations = [
  { titre: "Garde-corps sur mesure", tag: "Ferronnerie" },
  { titre: "Structure de mezzanine", tag: "Charpente" },
  { titre: "Terrasse en corten", tag: "Aménagement" },
  { titre: "Portail acier", tag: "Particulier" },
  { titre: "Bardage atelier", tag: "Bâtiment" },
  { titre: "Escalier métallique", tag: "Métallerie" },
];

// À propos
export const histoire = {
  intro: "Depuis près de 40 ans, la famille Grosjean transforme et distribue l'acier en Wallonie. D'un dépôt à quatre, une conviction n'a pas bougé : l'acier de qualité professionnelle doit être accessible à tous, du grand chantier au projet de week-end.",
  valeurs: [
    { titre: "Expertise", texte: "Quatre décennies à connaître la matière, les nuances et les usages." },
    { titre: "Proximité", texte: "Une entreprise familiale, quatre dépôts, un accueil sans intimidation." },
    { titre: "Efficacité", texte: "Devis en 24h, découpe sur mesure, retrait rapide. On ne vous fait pas attendre." },
    { titre: "Exigence", texte: "Certification EN1090-Exc2 : la rigueur du pro sur chaque commande." },
  ],
};

export const faq = [
  { q: "Faut-il être un professionnel pour commander ?", r: "Non. Les particuliers sont les bienvenus, même pour de petites quantités. Vous bénéficiez des mêmes prix pro accessibles." },
  { q: "Galvanisé, inox ou acier brut : comment choisir ?", r: "Pour l'extérieur exposé, préférez le galvanisé (protégé contre la rouille) ou l'inox. L'acier brut convient en intérieur ou s'il est peint. En cas de doute, notre équipe vous conseille." },
  { q: "Proposez-vous la livraison à domicile ?", r: "Le modèle est le retrait en dépôt (click & collect), souvent disponible le jour même. Cela garde des prix serrés et un retrait rapide." },
  { q: "En combien de temps ai-je un devis ?", r: "Sous 24h, sans engagement. Décrivez votre besoin (dimensions, quantités, usage) et nous revenons vers vous rapidement." },
  { q: "Découpez-vous aux dimensions demandées ?", r: "Oui, la découpe sur mesure fait partie de nos services, tout comme le pliage, le perçage et le façonnage selon votre plan." },
  { q: "Qu'est-ce que la certification EN1090-Exc2 ?", r: "C'est une norme européenne qui encadre la fabrication des structures en acier. L'obtenir atteste d'un niveau d'exigence que peu d'acteurs de notre secteur affichent." },
];
