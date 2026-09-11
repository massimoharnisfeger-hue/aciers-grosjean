import type { MetadataRoute } from "next";
import { familles, matieres } from "@/lib/catalogue";
import { guides, servicesDetail, depotsDetail } from "@/lib/edito";

const BASE = "https://www.aciersgrosjean.be";

export const dynamic = "force-static";

export default function sitemap(): MetadataRoute.Sitemap {
  const maj = new Date();

  const fixes: [string, number][] = [
    ["", 1],
    ["/produits", 0.9],
    ["/services", 0.8],
    ["/depots", 0.8],
    ["/guides", 0.8],
    ["/realisations", 0.6],
    ["/a-propos", 0.5],
    ["/devis", 0.9],
    ["/contact", 0.7],
    ["/faq", 0.6],
    ["/mentions-legales", 0.2],
    ["/confidentialite", 0.2],
    ["/conditions-generales", 0.2],
  ];

  return [
    ...fixes.map(([path, priority]) => ({
      url: `${BASE}${path}`,
      lastModified: maj,
      changeFrequency: "monthly" as const,
      priority,
    })),
    ...matieres.map((m) => ({
      url: `${BASE}/materiaux/${m.slug}`,
      lastModified: maj,
      changeFrequency: "monthly" as const,
      priority: 0.8,
    })),
    ...familles.map((f) => ({
      url: `${BASE}/produits/${f.slug}`,
      lastModified: maj,
      changeFrequency: "weekly" as const,
      priority: 0.85,
    })),
    ...familles.flatMap((f) =>
      f.refs.map((r) => ({
        url: `${BASE}/produits/${f.slug}/${r.ref}`,
        lastModified: maj,
        changeFrequency: "weekly" as const,
        priority: 0.7,
      }))
    ),
    ...servicesDetail.map((s) => ({
      url: `${BASE}/services/${s.slug}`,
      lastModified: maj,
      changeFrequency: "monthly" as const,
      priority: 0.7,
    })),
    ...depotsDetail.map((d) => ({
      url: `${BASE}/depots/${d.slug}`,
      lastModified: maj,
      changeFrequency: "monthly" as const,
      priority: 0.7,
    })),
    ...guides.map((g) => ({
      url: `${BASE}/guides/${g.slug}`,
      lastModified: maj,
      changeFrequency: "monthly" as const,
      priority: 0.65,
    })),
  ];
}
