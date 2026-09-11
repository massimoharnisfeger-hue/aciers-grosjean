import type { Metadata } from "next";
import PageLegale from "@/components/ui/PageLegale";
import { site } from "@/lib/content";

export const metadata: Metadata = {
  title: "Politique de confidentialité | Aciers Grosjean",
  description:
    "Quelles données ce site collecte (très peu), pourquoi, combien de temps, et comment exercer vos droits RGPD.",
  alternates: { canonical: "/confidentialite" },
};

export default function Confidentialite() {
  return (
    <PageLegale
      surtitre="Confidentialité"
      titre="Politique de confidentialité"
      intro="Ce site ne collecte presque rien. Voici exactement quoi, pourquoi, et comment le faire effacer."
      aCompleter={[
        "Identité et coordonnées du responsable du traitement (raison sociale, siège, BCE)",
        "Coordonnées d'un éventuel délégué à la protection des données",
        "Confirmation de l'outil de mesure d'audience retenu, le cas échéant",
      ]}
      blocs={[
        {
          titre: "1. Le principe : aucun formulaire stocké",
          paras: [
            "Ce site ne dispose d'aucune base de données de prospects. Les formulaires de devis et de contact n'enregistrent rien : ils composent un message dans votre propre logiciel de messagerie, que vous relisez et envoyez vous-même. Tant que vous n'avez pas cliqué sur « envoyer » dans votre messagerie, aucune donnée ne nous parvient.",
            "Concrètement, cela signifie qu'une saisie abandonnée ne laisse aucune trace chez nous.",
          ],
        },
        {
          titre: "2. Les données que nous recevons par e-mail",
          paras: [
            "Lorsque vous nous écrivez, nous recevons les informations que vous avez choisi d'inclure : nom, adresse e-mail, éventuellement numéro de téléphone, et la description de votre projet.",
            "Base légale : l'exécution de mesures précontractuelles prises à votre demande (article 6.1.b du RGPD), c'est-à-dire l'établissement du devis que vous sollicitez.",
            "Finalité : répondre à votre demande, établir un devis, et assurer le suivi commercial de ce devis. Ces données ne sont ni vendues, ni louées, ni transmises à des tiers à des fins de prospection.",
            "Durée de conservation : trois ans à compter du dernier contact pour les demandes sans suite ; la durée légale de conservation comptable pour les commandes effectivement passées.",
          ],
        },
        {
          titre: "3. Cookies et mesure d'audience",
          paras: [
            "Le site ne dépose aucun cookie publicitaire et n'utilise aucun traceur de réseau social.",
            "Certaines préférences d'affichage peuvent être conservées localement dans votre navigateur. Elles ne quittent jamais votre appareil et ne nous sont pas transmises.",
            "Si une mesure d'audience est ajoutée ultérieurement, elle sera mentionnée ici, et une solution sans cookie et sans transfert hors de l'Union européenne sera privilégiée.",
          ],
        },
        {
          titre: "4. Vos droits",
          paras: [
            "Conformément au Règlement général sur la protection des données, vous disposez d'un droit d'accès, de rectification, d'effacement, de limitation et d'opposition au traitement de vos données, ainsi que d'un droit à la portabilité.",
            `Pour exercer ces droits, écrivez à ${site.email}. Nous répondons dans un délai d'un mois.`,
            "Si vous estimez que vos droits ne sont pas respectés, vous pouvez introduire une réclamation auprès de l'Autorité de protection des données (Rue de la Presse 35, 1000 Bruxelles — autoriteprotectiondonnees.be).",
          ],
        },
        {
          titre: "5. Sécurité",
          paras: [
            "Le site est diffusé exclusivement en HTTPS : les échanges entre votre navigateur et le serveur sont chiffrés.",
            "Les pages du site sont générées à l'avance et servies de façon statique, ce qui réduit considérablement la surface d'attaque : il n'y a ni base de données publique, ni interface d'administration exposée.",
          ],
        },
      ]}
    />
  );
}
