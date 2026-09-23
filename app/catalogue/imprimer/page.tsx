import type { Metadata } from "next";
import { Fragment } from "react";
import { notFound } from "next/navigation";
import { chapitres, totauxCatalogue, catalogueActif } from "@/lib/catalogue-visuel";
import {
  Couverture,
  Sommaire,
  PageLecture,
  DiviseurChapitre,
  SectionDocument,
  QuatriemeDeCouverture,
} from "@/components/catalogue/Document";

/**
 * Le catalogue en un seul document A4 : couverture, sommaire, mode d'emploi,
 * puis chaque chapitre (ouverture, sections, familles, planches), et la
 * quatrième de couverture. Relisible à l'écran page par page ; exporté en PDF
 * par scripts/catalogue/exporter_pdf.py. Comme le reste du catalogue, la page
 * n'existe que derrière le drapeau local (ADR-0010).
 */

const EDITION = new Intl.DateTimeFormat("fr-BE", { month: "long", year: "numeric" }).format(new Date());

export const metadata: Metadata = {
  title: "Catalogue produits — document | Aciers Grosjean",
  robots: { index: false, follow: false },
};

export default function CatalogueDocument() {
  if (!catalogueActif) notFound();
  const tous = chapitres();
  const totaux = totauxCatalogue();

  return (
    <main className="catalogue-pdf">
      <Couverture chapitres={tous} totaux={totaux} edition={EDITION} />
      <Sommaire chapitres={tous} />
      <PageLecture />
      {tous.map((c) => (
        <Fragment key={c.slug}>
          <DiviseurChapitre chapitre={c} />
          <section className="page" aria-label={`Chapitre ${c.numero} : ${c.nom}`}>
            {c.sections.map((s, i) => (
              <SectionDocument key={s.chemin ?? `direct-${i}`} section={s} />
            ))}
          </section>
        </Fragment>
      ))}
      <QuatriemeDeCouverture edition={EDITION} />
    </main>
  );
}
