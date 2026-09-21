import FilAriane, { type Miette } from "@/components/ui/FilAriane";

export default function PageHeader({
  surtitre,
  titre,
  intro,
  miettes,
}: {
  surtitre: string;
  titre: React.ReactNode;
  intro?: string;
  /** Fil d'Ariane complet quand la page en a un ; sinon « Accueil / surtitre ». */
  miettes?: Miette[];
}) {
  return (
    <section className="relative overflow-hidden border-b border-brume bg-nuage pt-32 md:pt-40">
      <div className="grid-industrie pointer-events-none absolute inset-0 opacity-60" />
      <div className="pointer-events-none absolute -right-16 top-16 h-64 w-64 rounded-full bg-jaune/10 blur-[110px]" />
      <div className="container-g relative pb-14 md:pb-20">
        <div className="mb-5">
          <FilAriane items={miettes ?? [{ label: surtitre }]} />
        </div>
        <h1 className="h-display max-w-3xl text-4xl md:text-6xl">{titre}</h1>
        {intro && <p className="mt-5 max-w-xl font-body text-lg text-soft">{intro}</p>}
      </div>
    </section>
  );
}
