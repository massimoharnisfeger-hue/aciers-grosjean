import type { MetadataRoute } from "next";
import { univers, noeuds, tousProduits } from "@/lib/catalogue";
import { articles, servicesDetail, depotsDetail, pagesAide } from "@/lib/edito";

const BASE = "https://www.aciersgrosjean.be";

export const dynamic = "force-static";

type Freq = "daily" | "weekly" | "monthly" | "yearly";

export default function sitemap(): MetadataRoute.Sitemap {
  const maj = new Date();
  const e = (path: string, priority: number, changeFrequency: Freq = "monthly") => ({
    url: `${BASE}${path}`,
    lastModified: maj,
    changeFrequency,
    priority,
  });

  return [
    e("", 1, "weekly"),
    e("/produits", 0.9, "weekly"),
    e("/catalogue", 0.8),
    e("/devis", 0.9),
    e("/services", 0.8),
    e("/depots", 0.8),
    e("/conseils", 0.8, "weekly"),
    e("/entreprise", 0.6),
    e("/entreprise/engagement-esg", 0.5),
    e("/entreprise/certifications", 0.6),
    e("/pro", 0.7),
    e("/pro/demande-de-compte", 0.6),
    e("/contact", 0.7),
    e("/realisations", 0.6),
    e("/a-propos", 0.5),
    e("/nouveautes", 0.6, "weekly"),
    e("/documentation", 0.5),
    e("/plan-du-site", 0.4),
    e("/faq", 0.5),
    e("/conditions-generales-de-vente", 0.2, "yearly"),
    e("/protection-des-donnees", 0.2, "yearly"),
    e("/cookies", 0.2, "yearly"),
    e("/mentions-legales", 0.2, "yearly"),

    ...univers.map((u) => e(`/${u.slug}`, 0.9, "weekly")),
    ...univers.map((u) => e(`/catalogue/${u.slug}`, 0.7)),
    ...Object.keys(noeuds)
      .filter((c) => c.split("/").length > 2)
      .map((c) => e(c, c.split("/").length === 3 ? 0.85 : 0.8, "weekly")),
    ...tousProduits.map((p) => e(`/p/${p.slug}`, 0.7, "weekly")),

    ...servicesDetail.map((s) => e(`/services/${s.slug}`, 0.7)),
    ...depotsDetail.map((d) => e(`/depots/${d.slug}`, 0.7)),
    ...articles.map((a) => e(`/conseils/${a.slug}`, 0.65)),
    ...pagesAide.map((p) => e(`/aide/${p.slug}`, 0.5)),
  ];
}
