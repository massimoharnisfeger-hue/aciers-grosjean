import Image from "next/image";
import Link from "next/link";
import type { BlocOnglet, Onglet } from "@/lib/onglets";
import type { Paire } from "@/lib/description";
import { GrillePaires } from "@/components/catalogue/FicheModules";

/**
 * « Le produit en détail » en onglets, **sans une ligne de JavaScript**.
 *
 * Un bouton radio par onglet, le panneau coché s'affiche par sélecteur CSS
 * `peer` — exactement le mécanisme de `GalerieProduit`. Trois conséquences,
 * toutes voulues :
 *
 * - le contenu est dans le HTML et le premier onglet est coché à l'écriture :
 *   la page reste lisible si le JavaScript ne charge pas (règle du projet) ;
 * - la navigation au clavier est celle, native, d'un groupe de boutons radio —
 *   flèches pour changer d'onglet, Tab pour en sortir. Rien à réimplémenter,
 *   donc rien à casser. Un composant à état aurait exigé `"use client"`, donc
 *   d'embarquer du JavaScript sur 495 pages pour afficher du texte déjà
 *   présent dans le HTML ;
 * - aucune dépendance ajoutée : ni Radix, ni lucide — les icônes sont des SVG
 *   en ligne, comme partout ailleurs dans ce dépôt.
 *
 * Les classes sont écrites en entier : Tailwind ne génère que les noms qu'il
 * lit littéralement dans le code. D'où `CLASSES`, et le contrôle O3 qui refuse
 * qu'un onglet dépasse le dernier jeu déclaré — sinon il s'afficherait sans
 * pouvoir être sélectionné, comme la 4ᵉ vue de la galerie.
 *
 * Mise en valeur (22/09) : la barre d'onglets est un « segmented control »
 * (rail clair, pastille pleine pour l'onglet actif) plutôt que des pilules
 * flottantes — l'état courant se lit alors sans chercher. Mesure préalable :
 * la médiane d'un panneau est de 100 caractères, donc le contenu est court ;
 * le travail utile est la structure, pas le dégraissage. Les rares panneaux
 * bavards (13 sur 830 dépassent quatre paragraphes) replient leur surplus dans
 * un `<details>` natif : rien n'est supprimé, rien n'est réécrit.
 */
const CLASSES = [
  { bouton: "peer/o0", panneau: "peer-checked/o0:block", pastille: "peer-checked/o0:bg-encre peer-checked/o0:text-white peer-checked/o0:shadow-sm peer-focus-visible/o0:ring-2" },
  { bouton: "peer/o1", panneau: "peer-checked/o1:block", pastille: "peer-checked/o1:bg-encre peer-checked/o1:text-white peer-checked/o1:shadow-sm peer-focus-visible/o1:ring-2" },
  { bouton: "peer/o2", panneau: "peer-checked/o2:block", pastille: "peer-checked/o2:bg-encre peer-checked/o2:text-white peer-checked/o2:shadow-sm peer-focus-visible/o2:ring-2" },
];

/** Au-delà, le surplus se replie : le panneau doit s'embrasser d'un regard. */
const PARAGRAPHES_VISIBLES = 3;

/** Icônes en ligne : une par famille d'onglet, dessinée au trait comme le reste du site. */
const TRAITS: Record<string, string> = {
  caracteristiques: "M4 20V4M4 20h16M8 16V8M12 16v-4M16 16V6",
  usage: "M4 12l8-8 8 8-8 8z",
  documents: "M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8zM14 3v5h5M12 11v6M9.5 14.5L12 17l2.5-2.5",
};

function Icone({ cle }: { cle: string }) {
  return (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" className="shrink-0" aria-hidden="true">
      <path
        d={TRAITS[cle] ?? TRAITS.usage}
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

/** Un item court, sans ponctuation : il se lit mieux en pastille qu'en puce. */
const court = (s: string) => s.length <= 42 && !/[.;!?]/.test(s);

/** `Cote A` → `A`. La lettre renvoie à celle portée par le rendu 3D, à côté. */
const LETTRE = /^Cote\s+(.+)$/;

/**
 * Les cotes en tableau technique : la lettre en pastille, la valeur en chiffres
 * tabulaires. C'est la seule donnée de la fiche qui se lise en regard d'un
 * dessin — l'aligner sur le rendu vaut mieux que la noyer dans une liste.
 */
function TableauCotes({ paires }: { paires: Paire[] }) {
  const cotes = paires.filter((p) => LETTRE.test(p.label));
  const autres = paires.filter((p) => !LETTRE.test(p.label));
  return (
    <div className="mt-5">
      {cotes.length > 0 && (
        <dl className="grid grid-cols-2 gap-2 sm:grid-cols-3">
          {cotes.map((p) => (
            <div key={p.label} className="rounded-xl border border-brume bg-nuage px-3 py-3">
              <dt className="flex items-center gap-2">
                <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-md bg-encre font-mono text-[11px] font-bold text-white">
                  {p.label.replace(LETTRE, "$1")}
                </span>
                <span className="font-body text-[11px] uppercase tracking-[0.12em] text-soft">Cote</span>
              </dt>
              <dd className="h-title mt-2 font-mono text-lg font-semibold tabular-nums text-encre">{p.valeur}</dd>
            </div>
          ))}
        </dl>
      )}
      {autres.length > 0 && (
        <div className={cotes.length > 0 ? "mt-4" : ""}>
          <GrillePaires paires={autres} />
        </div>
      )}
    </div>
  );
}

/**
 * Un bloc de contenu, tel que le site source l'a ecrit.
 *
 * `data-module` porte le type d'origine : c'est le marqueur que le controle P9
 * cherche dans le HTML servi, et il survit donc a la mise en onglets.
 */
function Bloc({ b, premier }: { b: BlocOnglet; premier: boolean }) {
  if (b.repliable && b.titre) {
    return (
      <details data-module={b.type} className="group min-w-0 border-t border-brume first:border-0">
        <summary className="lien-tactile flex cursor-pointer list-none items-center justify-between gap-4 py-5 first:pt-0">
          <span className="h-title text-xs font-semibold uppercase tracking-[0.16em] text-soft">{b.titre}</span>
          <span
            className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full border border-brume text-soft transition-transform duration-200 group-open:rotate-180"
            aria-hidden="true"
          >
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none">
              <path d="M6 9l6 6 6-6" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </span>
        </summary>
        <div className="pb-6">
          <CorpsDeBloc b={b} premier={false} />
        </div>
      </details>
    );
  }
  return <BlocOuvert b={b} premier={premier} />;
}

function BlocOuvert({ b, premier }: { b: BlocOnglet; premier: boolean }) {
  return (
    <div data-module={b.type} className="min-w-0 border-t border-brume pt-6 first:border-0 first:pt-0">
      {b.titre && (
        <h4 className="h-title text-xs font-semibold uppercase tracking-[0.16em] text-soft">{b.titre}</h4>
      )}
      <CorpsDeBloc b={b} premier={premier} />
    </div>
  );
}

/** Le contenu d'un bloc, sans son enveloppe : il sert ouvert comme replie. */
function CorpsDeBloc({ b, premier }: { b: BlocOnglet; premier: boolean }) {
  const tousCourts = b.items.length > 0 && b.items.every(court);
  const [tete, ...suite] = b.paragraphes;
  const visibles = suite.slice(0, PARAGRAPHES_VISIBLES - 1);
  const replies = suite.slice(PARAGRAPHES_VISIBLES - 1);

  return (
    <>
      {tete && (
        <p
          className={`font-body leading-relaxed text-encre ${b.titre ? "mt-3" : ""} ${
            premier ? "text-lg md:text-xl" : "text-base"
          }`}
        >
          {tete}
        </p>
      )}
      {visibles.length > 0 && (
        <div className="mt-3 space-y-3 font-body text-sm leading-relaxed text-soft">
          {visibles.map((x) => (
            <p key={x}>{x}</p>
          ))}
        </div>
      )}
      {replies.length > 0 && (
        // `<details>` natif : pas de JavaScript, le texte reste dans le HTML.
        <details className="mt-3">
          <summary className="lien-tactile cursor-pointer list-none font-body text-sm font-medium text-encre underline decoration-jaune decoration-2 underline-offset-4">
            Lire la suite ({replies.length})
          </summary>
          <div className="mt-3 space-y-3 font-body text-sm leading-relaxed text-soft">
            {replies.map((x) => (
              <p key={x}>{x}</p>
            ))}
          </div>
        </details>
      )}

      {b.paires.length > 0 &&
        (b.paires.some((pa) => LETTRE.test(pa.label)) ? (
          <TableauCotes paires={b.paires} />
        ) : (
          <div className="mt-4">
            <GrillePaires paires={b.paires} />
          </div>
        ))}

      {b.items.length > 0 &&
        (tousCourts ? (
          <ul className="mt-4 flex flex-wrap gap-2">
            {b.items.map((it) => (
              <li key={it} className="rounded-full border border-brume bg-nuage px-3 py-1.5 font-body text-sm text-encre">
                {it}
              </li>
            ))}
          </ul>
        ) : (
          <ul className="mt-4 grid gap-2.5 sm:grid-cols-2">
            {b.items.map((it) => (
              <li
                key={it}
                className="flex items-start gap-2.5 rounded-xl border border-brume bg-nuage px-4 py-3 font-body text-sm leading-relaxed text-encre"
              >
                <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-jaune" aria-hidden="true" />
                <span className="min-w-0">{it}</span>
              </li>
            ))}
          </ul>
        ))}
    </>
  );
}

function Contenu({ o }: { o: Onglet }) {
  return (
    <div className="min-w-0 break-words">
      <div className="flex flex-wrap items-center gap-3">
        <span className="inline-flex items-center gap-2 rounded-full bg-jaune px-3 py-1 font-mono text-[11px] font-semibold uppercase tracking-[0.14em] text-encre">
          <Icone cle={o.cle} />
          {o.badge}
        </span>
      </div>
      <h3 className="h-display mt-3 text-xl leading-tight md:text-2xl">{o.titre}</h3>
      <div className="mt-5 h-px w-full bg-brume" />

      <div className="mt-5 space-y-6">
        {o.blocs.map((b, i) => (
          <Bloc key={`${b.type}-${i}`} b={b} premier={i === 0} />
        ))}
      </div>

      {o.pdfs && o.pdfs.length > 0 && (
        <ul className="mt-5 grid gap-2 sm:grid-cols-2">
          {o.pdfs.map((d) => (
            <li key={d.fichier}>
              <a
                href={d.fichier}
                target="_blank"
                rel="noopener"
                className="group flex items-center gap-3 rounded-xl border border-brume bg-nuage px-4 py-3 transition-colors hover:border-encre/30 hover:bg-white"
              >
                <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-encre">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" className="on-encre-jaune" aria-hidden="true">
                    <path
                      d="M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8zM14 3v5h5M12 11v6M9.5 14.5L12 17l2.5-2.5"
                      stroke="currentColor"
                      strokeWidth="1.7"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </span>
                <span className="min-w-0 flex-1 font-body text-sm text-encre">{d.titre}</span>
                <span className="font-mono text-[11px] uppercase text-soft">PDF</span>
              </a>
            </li>
          ))}
        </ul>
      )}

      {o.note && (
        <p className="mt-5 border-l-2 border-jaune pl-4 font-body text-xs leading-relaxed text-soft">{o.note}</p>
      )}

      {o.action && (
        <Link href={o.action.href} className="btn-cta mt-6 inline-flex">
          {o.action.libelle}
        </Link>
      )}
    </div>
  );
}

/** Le contenu d'un onglet, avec son visuel quand il en a un. */
function Panneau({ o }: { o: Onglet }) {
  if (!o.visuel) return <Contenu o={o} />;
  return (
    <div className="grid items-start gap-8 lg:grid-cols-[1fr_auto] lg:gap-12">
      <Contenu o={o} />
      <figure className="order-first w-full max-w-md lg:order-last lg:w-80 xl:w-96">
        {/* Meme presentation que la galerie : le rendu cote est servi entier,
            tableau des mesures compris (ADR-0012), en 4:3 comme cette boite ;
            un clic l'ouvre en grand (controle D14). */}
        <a
          href={o.visuel.src}
          target="_blank"
          rel="noopener"
          title="Ouvrir l'image en grand"
          className="relative block aspect-[4/3] overflow-hidden rounded-xl border border-brume bg-white [&>img]:h-full [&>img]:w-full [&>img]:object-contain"
        >
          <Image
            src={o.visuel.src}
            alt={o.visuel.alt}
            width={o.visuel.largeur}
            height={o.visuel.hauteur}
            sizes="(min-width: 1280px) 384px, (min-width: 1024px) 320px, (min-width: 640px) 28rem, 100vw"
          // Servi brut, comme dans la galerie : meme fichier, deja en cache.
          // L'optimiseur renvoyait ici une variante de 384 px la ou l'ecran
          // retina en demande 498 — mesure du 22/09, image floue sur la moitie
          // des ecrans. Un rendu entier pese 25 a 70 Ko (ADR-0012).
          unoptimized
            className="h-auto w-full"
          />
          <span className="pointer-events-none absolute bottom-2 right-2 rounded-md bg-encre/80 px-2 py-1 font-body text-xs text-white">
            Agrandir
          </span>
        </a>
        {o.legendeVisuel && (
          <figcaption className="mt-2 font-mono text-[11px] uppercase tracking-[0.14em] text-soft">
            {o.legendeVisuel}
          </figcaption>
        )}
      </figure>
    </div>
  );
}

/**
 * En-tête de la section : elle doit s'annoncer avant qu'on lise son contenu.
 *
 * Elle ne porte plus l'introduction : celle-ci est devenue le bloc de tête de
 * l'onglet « Présentation ». Sans cela, une fiche avec introduction n'avait pas
 * le même squelette qu'une fiche sans — demande du 22/09, « il faut qu'à chaque
 * fois ça garde la même structure ».
 */
function Entete() {
  return (
    <>
      <span className="inline-flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.2em] text-soft">
        <span className="h-px w-8 bg-jaune" aria-hidden="true" />
        Fiche détaillée
      </span>
      <h2 className="h-display mt-3 text-2xl md:text-3xl">Le produit en détail</h2>
    </>
  );
}

const SECTION = "border-y border-brume bg-nuage py-14 md:py-16";
const CARTE = "rounded-2xl border border-brume bg-white p-6 shadow-[0_18px_50px_-32px_rgba(51,54,66,.45)] md:p-10";

export default function DetailProduit({ onglets }: { onglets: Onglet[] }) {
  const liste = onglets.slice(0, CLASSES.length);
  if (liste.length === 0) return null;

  return (
    <section className={SECTION}>
      <div className="container-g">
        <Entete />

        {/* Un seul groupe radio : les flèches du clavier parcourent les onglets. */}
        <fieldset className="mt-8 min-w-0">
          <legend className="sr-only">Choisir une rubrique du produit</legend>

          {liste.map((o, i) => (
            <input
              key={`bouton-${o.cle}`}
              type="radio"
              name="detail-produit"
              id={`detail-${o.cle}`}
              defaultChecked={i === 0}
              className={`${CLASSES[i].bouton} sr-only`}
            />
          ))}

          {/* Rail clair, pastille pleine pour l'onglet actif : l'état courant se
              lit sans chercher. Il défile horizontalement sur mobile ; la page,
              elle, ne déborde pas (le fieldset porte `min-w-0`, contrôle R7). */}
          <div className="-mx-5 overflow-x-auto px-5 pb-1 md:mx-0 md:px-0">
            <div className="inline-flex w-max gap-1 rounded-full border border-brume bg-white p-1 md:w-auto md:flex-wrap">
              {liste.map((o, i) => (
                <label
                  key={`pastille-${o.cle}`}
                  htmlFor={`detail-${o.cle}`}
                  className={`flex cursor-pointer select-none items-center gap-2 whitespace-nowrap rounded-full px-4 py-2.5 font-body text-sm font-medium text-soft ring-jaune transition-all duration-200 hover:bg-nuage hover:text-encre active:scale-[.98] ${CLASSES[i].pastille}`}
                >
                  <Icone cle={o.cle} />
                  {o.libelle}
                </label>
              ))}
            </div>
          </div>

          {liste.map((o, i) => (
            <div key={`panneau-${o.cle}`} className={`mt-5 hidden ${CARTE} ${CLASSES[i].panneau}`}>
              <Panneau o={o} />
            </div>
          ))}
        </fieldset>
      </div>
    </section>
  );
}
