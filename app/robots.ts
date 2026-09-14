import type { MetadataRoute } from "next";

export const dynamic = "force-static";

// Préproduction non indexée tant que SITE_INDEXABLE n'est pas à « oui » (voir app/layout.tsx).
const indexable = process.env.SITE_INDEXABLE === "oui";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: indexable ? { userAgent: "*", allow: "/" } : { userAgent: "*", disallow: "/" },
    sitemap: "https://www.aciersgrosjean.be/sitemap.xml",
    host: "https://www.aciersgrosjean.be",
  };
}
