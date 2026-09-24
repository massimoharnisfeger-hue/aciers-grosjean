import Image from "next/image";
import Link from "next/link";
import type { Variante } from "@/lib/catalogue-visuel";

/**
 * La planche d'une variante : son rendu 3D aux cotes, son nom, ce qui la
 * distingue des autres variantes de la famille, et le lien vers sa fiche.
 *
 * L'image vient du manifeste (`lib/visuels-produits.json`), et de lui seul.
 * Sans entrée au manifeste, la planche montre un emplacement « visuel à
 * compléter » : le dessin SVG de la famille, que le site sert en repli sur la
 * fiche, n'est pas le produit et n'a pas sa place dans un catalogue.
 *
 * `unoptimized`, comme la galerie de la fiche : les rendus sont des fichiers
 * légers (25 à 70 Ko). Les passer par l'optimiseur coûterait des centaines de
 * transformations pour quelques kilo-octets (mesure du 22/09, GalerieProduit).
 * La boîte 4/5 est stable : le navigateur réserve la place avant que l'image
 * arrive, et les rendus, entiers en 4:3 depuis l'ADR-0012 (pièce et tableau),
 * s'y posent `object-contain`.
 */
export default function PlancheVariante({ variante, priorite = false }: { variante: Variante; priorite?: boolean }) {
  const v = variante;
  return (
    <li data-variante="" data-recherche={v.recherche} className="min-w-0 break-inside-avoid">
      <Link
        href={v.href}
        prefetch={false}
        className="group flex h-full flex-col overflow-hidden rounded-xl border border-brume bg-white transition-colors hover:border-encre focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-jaune"
      >
        <div className="relative aspect-[4/5] bg-nuage">
          <div className="grid-industrie absolute inset-0 opacity-60" aria-hidden="true" />
          {v.visuel ? (
            <Image
              src={v.visuel.src}
              alt={v.visuel.alt}
              width={v.visuel.largeur}
              height={v.visuel.hauteur}
              unoptimized
              priority={priorite}
              className="absolute inset-0 h-full w-full object-contain p-2"
            />
          ) : (
            <p className="absolute inset-3 flex items-center justify-center rounded-lg border border-dashed border-acier p-3 text-center font-body text-xs leading-snug text-soft sm:text-sm">
              Visuel à compléter
            </p>
          )}
        </div>
        <div className="flex flex-1 flex-col p-3 sm:p-4">
          <h4 className="h-title break-words font-title text-sm font-semibold leading-snug text-encre">{v.nom}</h4>
          {(v.specs.length > 0 || v.poids) && (
            <dl className="mt-2 space-y-1">
              {v.specs.map((s) => (
                <div key={s.label} className="flex items-baseline justify-between gap-2 font-body text-xs leading-snug">
                  <dt className="text-soft">{s.label}</dt>
                  <dd className="text-right font-mono tabular-nums text-encre">{s.valeur}</dd>
                </div>
              ))}
              {v.poids && (
                <div className="flex items-baseline justify-between gap-2 font-body text-xs leading-snug">
                  <dt className="text-soft">Poids</dt>
                  <dd className="text-right font-mono tabular-nums text-encre">{v.poids}</dd>
                </div>
              )}
            </dl>
          )}
          <span className="mt-auto pt-3 font-body text-xs font-medium text-encre underline decoration-brume underline-offset-4 transition-colors group-hover:decoration-jaune">
            Voir la fiche
          </span>
        </div>
      </Link>
    </li>
  );
}
