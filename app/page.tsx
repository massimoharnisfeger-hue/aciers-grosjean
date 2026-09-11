import Hero from "@/components/sections/Hero";
import Marquee from "@/components/ui/Marquee";
import Counters from "@/components/fx/Counters";
import Produits from "@/components/sections/Produits";
import Comparaison from "@/components/sections/Comparaison";
import Publics from "@/components/sections/Publics";
import Services from "@/components/sections/Services";
import Etapes from "@/components/sections/Etapes";
import Realisations from "@/components/sections/Realisations";
import Guides from "@/components/sections/Guides";
import Depots from "@/components/sections/Depots";
import CtaBand from "@/components/sections/CtaBand";
import Faq from "@/components/sections/Faq";

export default function Home() {
  return (
    <main>
      <Hero />
      <Marquee />
      <Counters />
      <Produits />
      <Comparaison />
      <Publics />
      <Services />
      <Etapes />
      <Realisations />
      <Guides />
      <Depots />
      <CtaBand />
      <Faq />
    </main>
  );
}
