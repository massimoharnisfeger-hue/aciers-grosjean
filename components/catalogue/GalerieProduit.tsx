import Image from "next/image";

/** Visuel 3D d'une fiche ou d'une catégorie (lib/visuels-produits.json, scripts/rendu-3d/integrer_visuels.py). */
export type VisuelProduit = { src: string; largeur: number; hauteur: number; alt: string };
export type VueGalerie = VisuelProduit & { legende: string };

// Classes écrites en entier : Tailwind ne génère que les noms présents tels quels dans le code.
const CLASSES = [
  { bouton: "peer/v0", panneau: "peer-checked/v0:block", vignette: "peer-checked/v0:border-encre peer-focus-visible/v0:ring-2" },
  { bouton: "peer/v1", panneau: "peer-checked/v1:block", vignette: "peer-checked/v1:border-encre peer-focus-visible/v1:ring-2" },
  { bouton: "peer/v2", panneau: "peer-checked/v2:block", vignette: "peer-checked/v2:border-encre peer-focus-visible/v2:ring-2" },
];

/**
 * Galerie sans JavaScript : un bouton radio par vue, la vue cochée s'affiche (sélecteurs CSS « peer »).
 * La première vue est cochée dans le HTML, donc visible même si le JavaScript ne charge pas.
 * Les WebP sont déjà optimisés (< 200 Ko, 1600 px) : servis tels quels, sans redimensionnement.
 */
export default function GalerieProduit({ vues }: { vues: VueGalerie[] }) {
  const liste = vues.slice(0, CLASSES.length);
  return (
    <div className="grid grid-cols-3 gap-3">
      {liste.map((v, i) => (
        <input
          key={`bouton-${v.src}`}
          type="radio"
          name="vue-produit"
          id={`vue-produit-${i}`}
          defaultChecked={i === 0}
          aria-label={`Afficher : ${v.legende}`}
          className={`${CLASSES[i].bouton} sr-only`}
        />
      ))}
      {/*
        `unoptimized` est garde ici, a l'inverse de `VisuelFamille`. Mesure du
        22/09/2026 : les 466 rendus de fiche font 36 Ko en moyenne pour une vue
        principale affichee a 45vw, et la vignette reutilise le meme fichier
        (donc le meme cache, pas un second telechargement). Les faire passer par
        l'optimiseur couterait ~1 400 transformations pour quelques kilo-octets.
        Le defaut corrige dans `VisuelFamille` etait d'un autre ordre : une
        photo de 1600 x 1200 servie dans un carre de 80 px.
      */}
      {liste.map((v, i) => (
        <figure key={`vue-${v.src}`} className={`col-span-3 hidden ${CLASSES[i].panneau}`}>
          <div className="overflow-hidden rounded-2xl border border-brume bg-white">
            <Image
              src={v.src}
              alt={v.alt}
              width={v.largeur}
              height={v.hauteur}
              sizes="(min-width: 1024px) 45vw, 100vw"
              priority={i === 0}
              unoptimized
              className="h-auto w-full"
            />
          </div>
          <figcaption className="mt-2 font-mono text-[11px] uppercase tracking-[0.16em] text-soft">{v.legende}</figcaption>
        </figure>
      ))}
      {liste.length > 1 &&
        liste.map((v, i) => (
          <label
            key={`vignette-${v.src}`}
            htmlFor={`vue-produit-${i}`}
            className={`cursor-pointer overflow-hidden rounded-xl border-2 border-brume bg-white ring-jaune transition-colors hover:border-encre/40 ${CLASSES[i].vignette}`}
          >
            <Image src={v.src} alt="" width={v.largeur} height={v.hauteur} sizes="160px" unoptimized className="h-auto w-full" />
            <span className="sr-only">{v.legende}</span>
          </label>
        ))}
    </div>
  );
}
