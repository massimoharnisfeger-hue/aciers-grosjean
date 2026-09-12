import type { Metadata } from "next";
import PageEspace from "@/components/ui/PageEspace";

export const metadata: Metadata = {
  title: "Mot de passe oublié | Aciers Grosjean",
  description: "Récupération de mot de passe de l’espace client. Pour retrouver un devis ou une commande passée, appelez-nous : on la retrouve dans nos dossiers.",
  alternates: { canonical: "/compte/mot-de-passe-oublie" },
  robots: { index: false, follow: true },
};

export default function Page() {
  return (
    <PageEspace
      surtitre="Mon compte"
      titre={<>Mot de passe oublié</>}
      intro="L’espace client en ligne est en cours de déploiement : il n’y a pas encore de mot de passe à récupérer."
      maintenant="Si vous cherchez à retrouver un devis ou une commande passée, appelez-nous avec la date approximative : on la retrouve dans nos dossiers."
      aVenir={["Réinitialiser votre mot de passe par e-mail", "Sécuriser l’accès à vos documents"]}
    />
  );
}
