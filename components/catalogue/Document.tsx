import Image from "next/image";
import LogoSvg from "@/components/ui/LogoSvg";
import {
  SITE_URL,
  type Chapitre,
  type Famille,
  type SectionCatalogue,
  type Variante,
  type Visuel,
} from "@/lib/catalogue-visuel";
import { site, etapes, services } from "@/lib/content";
import { depotsDetail } from "@/lib/edito";

/**
 * Le catalogue en document : les pages A4 de la version imprimée
 * (app/catalogue/imprimer/page.tsx, exportée en PDF par
 * scripts/catalogue/exporter_pdf.py). Mêmes données que le catalogue web
 * (lib/catalogue-visuel.ts), mise en page papier : couverture, sommaire
 * paginé, ouverture par chapitre, fiches famille, quatre planches par
 * rangée, quatrième de couverture avec les dépôts.
 *
 * Tout est chargé d'emblée (`loading="eager"`) : un PDF n'a pas de défilement.
 * Les planches lient la fiche du produit sur le site actuel (`hrefSite`),
 * adresse valable hors du poste. Styles : app/globals.css, « CATALOGUE DOCUMENT ».
 */

const metres = (v: number) => `${v.toLocaleString("fr-BE")} m`;
const DOMAINE = SITE_URL.replace(/^https?:\/\//, "");

type Totaux = { produits: number; familles: number; visuels: number };

function Studio({ visuel, sizes }: { visuel: Visuel; sizes: string }) {
  return (
    <Image src={visuel.src} alt={visuel.alt} width={visuel.largeur} height={visuel.hauteur} sizes={sizes} loading="eager" />
  );
}

export function Couverture({ chapitres, totaux, edition }: { chapitres: Chapitre[]; totaux: Totaux; edition: string }) {
  return (
    <section className="page pdf-couv" aria-label="Couverture">
      <header className="pdf-couv-tete">
        <LogoSvg hauteur={54} couleur="#333642" anime={false} />
        <p className="pdf-h-sub pdf-soft">Édition {edition}</p>
      </header>
      <div className="pdf-couv-corps">
        <span className="pdf-barre" aria-hidden="true" />
        <h1 className="pdf-h-titre pdf-couv-titre">Catalogue produits</h1>
        <p className="pdf-h-sub pdf-couv-sous">
          Acier, aluminium, inox, toiture et bardage, jardin et clôture, quincaillerie.
        </p>
        <p className="pdf-soft pdf-couv-intro">
          {totaux.produits} produits en {totaux.familles} familles, {totaux.visuels} rendus 3D aux cotes. Chaque
          planche renvoie à la fiche du produit sur {DOMAINE}.
        </p>
      </div>
      <ul className="pdf-mosaique pdf-couv-mosaique">
        {chapitres.map((c) =>
          c.studios[0] ? (
            <li key={c.slug}>
              <figure>
                <Studio visuel={c.studios[0]} sizes="420px" />
                <figcaption>{c.nom}</figcaption>
              </figure>
            </li>
          ) : null
        )}
      </ul>
      <p className="pdf-soft pdf-mention">
        Illustrations non contractuelles : rendus 3D aux cotes nominales. Prix et disponibilités sur {DOMAINE} et
        sur devis.
      </p>
    </section>
  );
}

/** Les numéros de page sont écrits par l'export (data-page-de) : le HTML ne peut pas les connaître. */
export function Sommaire({ chapitres }: { chapitres: Chapitre[] }) {
  return (
    <section className="page" aria-label="Sommaire">
      <h2 className="pdf-h-titre pdf-titre-page">Sommaire</h2>
      <div className="pdf-sommaire">
        {chapitres.map((c) => (
          <div key={c.slug} className="pdf-sommaire-chapitre" data-chapitre-doc={c.slug} data-numero={c.numero}>
            <div className="pdf-ligne pdf-ligne-chapitre">
              <span className="pdf-onglet pdf-onglet-s" aria-hidden="true">{c.numero}</span>
              <span className="pdf-nom">{c.nom}</span>
              <span className="pdf-points" aria-hidden="true" />
              <span className="pdf-mono pdf-page" data-page-de={`chapitre-${c.slug}`} />
            </div>
            {c.sections.flatMap((s) =>
              s.familles.map((f) => (
                <div key={f.chemin} className="pdf-ligne" data-famille-doc={f.ancre} data-nom={f.nom}>
                  <span className="pdf-nom">{f.nom}</span>
                  <span className="pdf-mono pdf-soft pdf-nb">{f.variantes.length}</span>
                  <span className="pdf-points" aria-hidden="true" />
                  <span className="pdf-mono pdf-page" data-page-de={f.ancre} />
                </div>
              ))
            )}
          </div>
        ))}
      </div>
    </section>
  );
}

export function PageLecture() {
  return (
    <section className="page" aria-label="Lire ce catalogue">
      <h2 className="pdf-h-titre pdf-titre-page">Lire ce catalogue</h2>
      <dl className="pdf-lecture">
        <div>
          <dt>Les images</dt>
          <dd>
            Chaque variante est dessinée en 3D à ses cotes nominales ; la photo studio montre la famille.
            Illustrations non contractuelles.
          </dd>
        </div>
        <div>
          <dt>Les caractéristiques</dt>
          <dd>
            Celles des fiches du site {DOMAINE}, relevées le 14 septembre 2026. Ce qui vaut pour toute une famille
            se lit en tête de famille ; ce qui distingue une variante se lit sur sa planche.
          </dd>
        </div>
        <div>
          <dt>Les prix</dt>
          <dd>
            Sur la fiche de chaque produit, avec le calcul de votre quantité et la demande de devis. Le catalogue
            ne les reprend pas : ils se mettent à jour sur le site.
          </dd>
        </div>
      </dl>

      <h2 className="pdf-h-titre pdf-titre-page pdf-espace">Commander</h2>
      <ol className="pdf-etapes">
        {etapes.map((e) => (
          <li key={e.n}>
            <span className="pdf-onglet pdf-onglet-s" aria-hidden="true">{e.n.replace(/^0/, "")}</span>
            <div>
              <strong>{e.titre}</strong>
              <p className="pdf-soft">{e.texte}</p>
            </div>
          </li>
        ))}
      </ol>

      <h2 className="pdf-h-titre pdf-titre-page pdf-espace">Services</h2>
      <ul className="pdf-services">
        {services.map((s) => (
          <li key={s.nom}>
            <strong>{s.nom}</strong>
            <p className="pdf-soft">{s.detail ?? s.desc}</p>
          </li>
        ))}
      </ul>
    </section>
  );
}

export function DiviseurChapitre({ chapitre: c }: { chapitre: Chapitre }) {
  return (
    <section className="page pdf-chap" aria-label={`Ouverture du chapitre ${c.numero}`}>
      <div>
        <span className="pdf-onglet pdf-onglet-l" aria-hidden="true">{c.numero}</span>
        <p className="pdf-h-sub pdf-soft pdf-chap-sur">Chapitre {c.numero}</p>
        <h2 className="pdf-h-titre pdf-chap-nom">{c.nom}</h2>
        {c.accroche && <p className="pdf-h-sub pdf-chap-accroche">{c.accroche}</p>}
        {c.intro && <p className="pdf-soft pdf-chap-intro">{c.intro}</p>}
        <p className="pdf-soft pdf-chap-compte">
          {c.nbFamilles} familles, {c.nbProduits} produits, {c.nbVisuels} vues cotées.
        </p>
        <ul className="pdf-chap-familles">
          {c.sections.map((s, i) => (
            <li key={s.chemin ?? `direct-${i}`} style={{ display: "block", padding: 0, border: 0 }}>
              {s.nom && <p className="pdf-groupe">{s.nom}</p>}
              <ul>
                {s.familles.map((f) => (
                  <li key={f.chemin}>
                    <span>{f.nom}</span>
                    <span className="pdf-mono pdf-soft">{f.variantes.length}</span>
                  </li>
                ))}
              </ul>
            </li>
          ))}
        </ul>
      </div>
      {c.studios.length > 0 && (
        <ul className="pdf-mosaique pdf-mosaique-2">
          {c.studios.map((s) => (
            <li key={s.src}>
              <figure>
                <Studio visuel={s} sizes="700px" />
              </figure>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

function PlancheDocument({ variante: v }: { variante: Variante }) {
  return (
    <li className="pdf-planche">
      <a href={v.hrefSite}>
        <div className="pdf-plaque pdf-planche-image">
          {v.visuel ? (
            <Image src={v.visuel.src} alt={v.visuel.alt} width={v.visuel.largeur} height={v.visuel.hauteur} sizes="500px" loading="eager" />
          ) : (
            <p className="pdf-vide"><span>Visuel à compléter</span></p>
          )}
        </div>
        <div className="pdf-planche-texte">
          <p className="pdf-planche-nom">{v.nom}</p>
          {(v.specs.length > 0 || v.poids) && (
            <dl className="pdf-planche-specs">
              {v.specs.map((s) => (
                <div key={s.label}>
                  <dt className="pdf-soft">{s.label}</dt>
                  <dd className="pdf-mono">{s.valeur}</dd>
                </div>
              ))}
              {v.poids && (
                <div>
                  <dt className="pdf-soft">Poids</dt>
                  <dd className="pdf-mono">{v.poids}</dd>
                </div>
              )}
            </dl>
          )}
        </div>
      </a>
    </li>
  );
}

function FamilleDocument({ famille: f }: { famille: Famille }) {
  const nb = f.variantes.length;
  return (
    <section className="pdf-famille" id={`doc-${f.ancre}`} data-famille-doc={f.ancre} aria-labelledby={`doc-${f.ancre}-titre`}>
      <div className="pdf-famille-tete">
        <figure className="pdf-famille-studio">
          <div className="pdf-plaque">
            {f.studio ? <Studio visuel={f.studio} sizes="640px" /> : <p className="pdf-vide"><span>Photo studio à compléter</span></p>}
          </div>
          {f.studio && <figcaption>Photo studio, rendu 3D sur fond blanc</figcaption>}
        </figure>
        <div>
          <h4 id={`doc-${f.ancre}-titre`} className="pdf-famille-nom">{f.nom}</h4>
          {f.accroche && <p className="pdf-famille-accroche pdf-soft">{f.accroche}</p>}
          <dl className="pdf-caracteristiques">
            <div>
              <dt className="pdf-soft">Variantes</dt>
              <dd className="pdf-mono">{nb}</dd>
            </div>
            {f.communes.map((s) => (
              <div key={s.label}>
                <dt className="pdf-soft">{s.label}</dt>
                <dd className="pdf-mono">{s.valeur}</dd>
              </div>
            ))}
            {f.finition && (
              <div>
                <dt className="pdf-soft">Finition</dt>
                <dd className="pdf-mono">{f.finition}</dd>
              </div>
            )}
            {f.unite && (
              <div>
                <dt className="pdf-soft">Vente</dt>
                <dd className="pdf-mono">{f.unite}</dd>
              </div>
            )}
            {f.longueurs && (
              <div className="pdf-large">
                <dt className="pdf-soft">Longueurs standard</dt>
                <dd className="pdf-chips">
                  {f.longueurs.map((l) => (
                    <span key={l} className="pdf-mono">{metres(l)}</span>
                  ))}
                </dd>
              </div>
            )}
          </dl>
          {f.pdfs.length > 0 && (
            <p className="pdf-docs pdf-soft">
              Fiche technique sur le site : {f.pdfs.map((d) => d.titre).join(", ")}.
            </p>
          )}
        </div>
      </div>
      <p className="pdf-nb-variantes">
        {nb === 1 ? "Une variante" : `${nb} variantes`}
        {f.nbVisuels < nb && ` — ${nb - f.nbVisuels} sans visuel`}
      </p>
      <ul className="pdf-planches">
        {f.variantes.map((v) => (
          <PlancheDocument key={v.slug} variante={v} />
        ))}
      </ul>
    </section>
  );
}

export function SectionDocument({ section: s }: { section: SectionCatalogue }) {
  return (
    <div>
      {s.nom && (
        <div className="pdf-section">
          <span className="pdf-barre pdf-barre-s" aria-hidden="true" />
          <h3 className="pdf-h-titre pdf-section-nom">{s.nom}</h3>
          {s.accroche && <p className="pdf-h-sub pdf-soft pdf-section-accroche">{s.accroche}</p>}
        </div>
      )}
      {s.familles.map((f) => (
        <FamilleDocument key={f.chemin} famille={f} />
      ))}
    </div>
  );
}

export function QuatriemeDeCouverture({ edition }: { edition: string }) {
  return (
    <section className="page" aria-label="Quatrième de couverture">
      <LogoSvg hauteur={54} couleur="#333642" anime={false} />
      <p className="pdf-h-sub pdf-quatrieme-baseline">{site.baseline}</p>

      <h2 className="pdf-h-titre pdf-titre-page pdf-espace">Nos dépôts</h2>
      <ul className="pdf-depots">
        {depotsDetail.map((d) => (
          <li key={d.slug}>
            <strong>{d.nomComplet}</strong>
            <p>{d.adresse}</p>
            <p className="pdf-mono">{d.tel}</p>
            {d.horaires.map((h) => (
              <p key={h.jours} className="pdf-soft">
                {h.jours} : {h.heures}
              </p>
            ))}
          </li>
        ))}
      </ul>

      <h2 className="pdf-h-titre pdf-titre-page pdf-espace">Nous joindre</h2>
      <p className="pdf-contact">
        <span className="pdf-mono">{site.tel}</span>
        <br />
        {site.email}
        <br />
        {DOMAINE}
      </p>

      <p className="pdf-soft pdf-mention pdf-quatrieme-pied">
        Catalogue édité en {edition}. Caractéristiques relevées sur {DOMAINE} le 14 septembre 2026. Rendus 3D aux
        cotes nominales, illustrations non contractuelles. Prix et disponibilités sur le site et sur devis.
      </p>
    </section>
  );
}
