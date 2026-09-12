import type { Metadata } from "next";
import Link from "next/link";
import PageHeader from "@/components/ui/PageHeader";
import CtaBand from "@/components/sections/CtaBand";
import Counters from "@/components/fx/Counters";
import Reveal from "@/components/fx/Reveal";
import { ArtAtelier, ArtStock, ArtDecoupe } from "@/components/art/ProductArt";
import { histoire } from "@/lib/content";
import { depotsDetail } from "@/lib/edito";

export const metadata: Metadata = {
  title: "L'entreprise — 40 ans de négoce acier",
  description:
    "Entreprise familiale, quatre dépôts en Belgique et en France, certification EN 1090-Exc2. Quarante ans à rendre l'acier de qualité professionnelle accessible à tous.",
  alternates: { canonical: "/entreprise" },
};

export default function EntreprisePage() {
  return (
    <main>
      <PageHeader
        surtitre="L'entreprise"
        titre={
          <>
            40 ans d'acier, <span className="mark-jaune">une famille</span>
          </>
        }
        intro={histoire.intro}
      />

      <Counters />

      <section className="bg-white py-16 md:py-24">
        <div className="container-g">
          <h2 className="h-display text-2xl md:text-3xl">Ce qui ne bouge pas</h2>
          <div className="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {histoire.valeurs.map((v, i) => (
              <Reveal key={v.titre} delay={(i % 4) * 0.06}>
                <div className="flex h-full flex-col rounded-2xl border border-brume bg-white p-7">
                  <span className="font-mono text-xs text-soft">{String(i + 1).padStart(2, "0")}</span>
                  <h3 className="h-title mt-3 text-lg font-semibold text-encre">{v.titre}</h3>
                  <p className="mt-2 font-body leading-relaxed text-soft">{v.texte}</p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      <section className="border-y border-brume bg-nuage py-16 md:py-20">
        <div className="container-g">
          <h2 className="h-display text-2xl md:text-3xl">Quatre dépôts, deux pays</h2>
          <p className="mt-3 max-w-xl font-body text-soft">
            Charleroi est le dépôt historique et le plus profond en stock. Les trois autres
            couvrent le Centre, l'ouest wallon et le Grand Est.
          </p>
          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {depotsDetail.map((d, i) => (
              <Reveal key={d.slug} delay={i * 0.06}>
                <Link
                  href={`/depots/${d.slug}`}
                  className="group flex h-full flex-col rounded-2xl border border-brume bg-white p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_26px_60px_-34px_rgba(51,54,66,.5)]"
                >
                  <h3 className="h-title text-lg font-semibold text-encre">{d.ville}</h3>
                  <p className="mt-0.5 font-body text-xs text-soft">{d.region} · {d.pays}</p>
                  <p className="mt-4 flex-1 font-body text-sm leading-relaxed text-soft">
                    {d.intro.split(". ")[0]}.
                  </p>
                </Link>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-white py-16 md:py-20">
        <div className="container-g grid gap-5 md:grid-cols-3">
          {[
            { A: ArtStock, t: "Le stock", d: "Des centaines de références tenues en permanence, c'est ce qui permet le retrait le jour même." },
            { A: ArtDecoupe, t: "L'atelier", d: "Découpe, pliage, perçage, soudure. La matière part préparée, pas brute." },
            { A: ArtAtelier, t: "La certification", d: "EN 1090-Exc2 : la norme des structures en acier, que peu d'acteurs de notre taille détiennent." },
          ].map(({ A, t, d }, i) => (
            <Reveal key={t} delay={i * 0.07}>
              <div className="group overflow-hidden rounded-2xl border border-brume bg-white">
                <div className="shine relative aspect-[4/3] overflow-hidden bg-nuage">
                  <div className="grid-industrie absolute inset-0 opacity-70" />
                  <A className="absolute inset-0 h-full w-full transition-transform duration-700 group-hover:scale-105" />
                </div>
                <div className="p-6">
                  <h3 className="h-title font-semibold text-encre">{t}</h3>
                  <p className="mt-2 font-body text-sm leading-relaxed text-soft">{d}</p>
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      <section className="border-t border-brume bg-nuage py-14">
        <div className="container-g flex flex-wrap gap-3">
          <Link href="/entreprise/engagement-esg" className="btn-ghost">Notre engagement ESG</Link>
          <Link href="/entreprise/certifications" className="btn-ghost">Nos certifications</Link>
          <Link href="/conseils/une-entreprise-tournee-vers-lavenir" className="btn-ghost">
            40 ans en Wallonie
          </Link>
        </div>
      </section>

      <CtaBand />
    </main>
  );
}
