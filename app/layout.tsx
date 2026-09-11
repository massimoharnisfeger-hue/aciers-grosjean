import type { Metadata, Viewport } from "next";
import { Poppins, Comfortaa, Questrial } from "next/font/google";
import "./globals.css";
import SmoothScroll from "@/components/fx/SmoothScroll";
import Nav from "@/components/ui/Nav";
import Footer from "@/components/sections/Footer";
import ScrollProgress from "@/components/fx/ScrollProgress";

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

export const metadata: Metadata = {
  title: "Aciers Grosjean — L'acier de pro, accessible à tous",
  description:
    "Négoce et transformation d'acier depuis 40 ans. Poutrelles, tôles, tubes, cornières, corten. Découpe sur mesure, devis en 24h, retrait le jour même. 4 dépôts en Wallonie et en France.",
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
      className={`${poppins.variable} ${comfortaa.variable} ${questrial.variable}`}
    >
      <body className="grain">
        <ScrollProgress />
        <SmoothScroll>
          <Nav />
          {children}
          <Footer />
        </SmoothScroll>
      </body>
    </html>
  );
}
