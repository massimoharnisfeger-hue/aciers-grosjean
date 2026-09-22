import type { Metadata } from "next";
import PageLegale from "@/components/ui/PageLegale";

export const metadata: Metadata = {
  title: "Cookies et traceurs — ce site ne vous suit pas",
  description:
    "Ce site ne dépose aucun cookie publicitaire ni traceur de réseau social. Voici ce qu'il utilise réellement.",
  alternates: { canonical: "/cookies" },
};

export default function CookiesPage() {
  return (
    <PageLegale
      surtitre="Cookies"
      titre="Cookies et traceurs"
      intro="La version courte : ce site ne vous suit pas."
      blocs={[
        {
          titre: "1. Aucun cookie publicitaire",
          paras: [
            "Ce site ne dépose aucun cookie publicitaire, aucun pixel de réseau social et aucun traceur tiers. Il n'y a donc pas de bandeau de consentement, parce qu'il n'y a rien à consentir.",
            "Les pages sont générées à l'avance et servies en statique : il n'y a ni session, ni identifiant de suivi, ni profilage.",
          ],
        },
        {
          titre: "2. Stockage local",
          paras: [
            "À ce jour, le site n'écrit rien dans le stockage de votre navigateur : ni cookie, ni stockage local, ni session. Les filtres et les onglets du catalogue fonctionnent sans rien retenir d'une visite à l'autre.",
            "Si cela devait changer — pour retenir un filtre ou un onglet, par exemple — ces données resteraient sur votre appareil et ne nous seraient pas transmises.",
            "Vous pouvez les effacer à tout moment en vidant les données de site dans votre navigateur, sans aucune conséquence sur le fonctionnement des pages.",
          ],
        },
        {
          titre: "3. Polices et ressources externes",
          paras: [
            "Les polices de caractères sont servies depuis le même domaine que le site, et non depuis un service tiers : votre navigateur ne contacte donc aucun serveur externe pour les afficher.",
          ],
        },
        {
          titre: "4. Si cela change",
          paras: [
            "Si une mesure d'audience est ajoutée à l'avenir, elle sera mentionnée ici et une solution sans cookie, sans identifiant persistant et sans transfert hors de l'Union européenne sera privilégiée.",
          ],
        },
      ]}
    />
  );
}
