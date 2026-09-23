import type { Metadata, Viewport } from "next";
import { Poppins, Comfortaa, Questrial, IBM_Plex_Mono } from "next/font/google";
import "./globals.css";
import Nav from "@/components/ui/Nav";
import Footer from "@/components/sections/Footer";
import ScrollProgress from "@/components/fx/ScrollProgress";
import { menuCatalogue } from "@/lib/menu";
import { catalogueActif } from "@/lib/catalogue-visuel";

// Le site de préproduction (vercel.app) ne doit pas être indexé : il ferait
// doublon avec aciersgrosjean.be. Mettre SITE_INDEXABLE=oui sur Vercel le jour
// où ce site remplace l'actuel.
const indexable = process.env.SITE_INDEXABLE === "oui";

const poppins = Poppins({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-poppins",
  display: "swap",
});
const comfortaa = Comfortaa({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-comfortaa",
  display: "swap",
});
const questrial = Questrial({
  subsets: ["latin"],
  weight: ["400"],
  variable: "--font-questrial",
  display: "swap",
});
// Police technique : cotes, références, caractéristiques.
const plexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-mono",
  display: "swap",
});

export const metadata: Metadata = {
  metadataBase: new URL("https://www.aciersgrosjean.be"),
  title: "Aciers Grosjean — l'acier de pro, accessible à tous",
  description:
    "Poutrelles, tôles, tubes, cornières, corten. Découpe sur mesure, devis en 24 h, retrait le jour même dans nos 4 dépôts en Wallonie et en France.",
  alternates: { canonical: "/" },
  robots: indexable ? undefined : { index: false, follow: false },
  keywords: [
    "acier",
    "poutrelles",
    "tôles",
    "tubes acier",
    "cornières",
    "corten",
    "découpe sur mesure",
    "Charleroi",
    "La Louvière",
    "Tournai",
  ],
  openGraph: {
    title: "Aciers Grosjean — L'acier de pro, accessible à tous",
    description:
      "40 ans d'expertise acier. Découpe sur mesure, devis en 24h, retrait le jour même.",
    type: "website",
    locale: "fr_BE",
  },
};

export const viewport: Viewport = {
  themeColor: "#333642",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="fr"
      className={`${poppins.variable} ${comfortaa.variable} ${questrial.variable} ${plexMono.variable}`}
    >
      <body className="grain">
        <ScrollProgress />
        <Nav menu={menuCatalogue()} catalogueLocal={catalogueActif} />
        {children}
        <Footer />
      </body>
    </html>
  );
}
