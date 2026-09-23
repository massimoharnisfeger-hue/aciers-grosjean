import Link from "next/link";

export type OngletChapitre = { slug: string; nom: string; numero: number; href: string; nbProduits: number };

/**
 * Les six chapitres du catalogue, comme les onglets de tranche d'un catalogue
 * imprimé : un numéro, un nom, et l'onglet du chapitre ouvert en jaune.
 *
 * `prefetch={false}` : Next précharge sinon les six chapitres dès que les
 * onglets sont visibles, soit plusieurs centaines de cartes que le visiteur
 * n'a pas demandées (leçon L-046, même mécanisme).
 */
export default function OngletsChapitres({
  chapitres,
  actif,
}: {
  chapitres: OngletChapitre[];
  actif?: string;
}) {
  return (
    <nav aria-label="Chapitres du catalogue" className="print:hidden">
      <ol className="grid grid-cols-2 gap-2 sm:grid-cols-3 lg:grid-cols-6">
        {chapitres.map((c) => {
          const courant = c.slug === actif;
          return (
            <li key={c.slug} className="min-w-0">
              <Link
                href={c.href}
                prefetch={false}
                aria-current={courant ? "page" : undefined}
                className={`flex min-h-[3rem] items-center gap-3 rounded-lg border px-2.5 py-2 transition-colors ${
                  courant
                    ? "border-encre bg-white"
                    : "border-brume bg-white hover:border-encre"
                }`}
              >
                <span
                  className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-md font-title text-sm font-bold tabular-nums ${
                    courant ? "bg-jaune text-encre" : "bg-nuage text-encre"
                  }`}
                  aria-hidden="true"
                >
                  {c.numero}
                </span>
                <span className="min-w-0">
                  <span className="line-clamp-2 font-title text-sm font-semibold leading-tight text-encre">
                    <span className="sr-only">Chapitre {c.numero} : </span>
                    {c.nom}
                  </span>
                  <span className="block font-body text-xs leading-tight text-soft">{c.nbProduits} produits</span>
                </span>
              </Link>
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
