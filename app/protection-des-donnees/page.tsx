import type { Metadata } from "next";
import PageLegale from "@/components/ui/PageLegale";
import { site } from "@/lib/content";

export const metadata: Metadata = {
  title: "Politique de confidentialité | Aciers Grosjean",
  description:
    "Quelles données ce site collecte (très peu), pourquoi, combien de temps, et comment exercer vos droits RGPD.",
  alternates: { canonical: "/protection-des-donnees" },
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
          titre: "1. Le principe : rien n'est stocké",
          paras: [
            "Ce site ne dispose d'aucune base de données de prospects. Aucun formulaire n'enregistre quoi que ce soit : ni base, ni fichier, ni journal. Une saisie abandonnée ne laisse donc aucune trace chez nous.",
            "Le formulaire de demande de devis transmet ce que vous avez saisi à notre serveur, qui le relaie immédiatement par e-mail à notre boîte commerciale, puis l'oublie. Votre demande n'existe ensuite que dans cette boîte aux lettres, comme si vous nous aviez écrit vous-même.",
            "Les autres formulaires — contact, demande de compte professionnel — ne passent pas par notre serveur du tout : ils composent un message dans votre propre logiciel de messagerie, que vous relisez et envoyez vous-même. Tant que vous n'avez pas cliqué sur « envoyer », aucune donnée ne nous parvient. Le formulaire de devis bascule sur ce même fonctionnement si notre service d'envoi est indisponible.",
          ],
        },
        {
          titre: "2. Les données que nous recevons par e-mail",
          paras: [
            "Lorsque vous nous écrivez, nous recevons les informations que vous avez choisi d'inclure : nom, adresse e-mail, éventuellement numéro de téléphone, et la description de votre projet. Le formulaire de devis y ajoute les champs que vous avez remplis : profil (particulier ou professionnel), produit recherché et dépôt de retrait souhaité.",
            "Sous-traitants : l'hébergeur du site, qui achemine la demande sans la conserver, et notre fournisseur de messagerie professionnelle, chez qui le message est reçu et stocké. Aucun autre tiers n'y a accès.",
            "Base légale : l'exécution de mesures précontractuelles prises à votre demande (article 6.1.b du RGPD), c'est-à-dire l'établissement du devis que vous sollicitez.",
            "Finalité : répondre à votre demande, établir un devis, et assurer le suivi commercial de ce devis. Ces données ne sont ni vendues, ni louées, ni transmises à des tiers à des fins de prospection.",
            "Durée de conservation : trois ans à compter du dernier contact pour les demandes sans suite ; la durée légale de conservation comptable pour les commandes effectivement passées.",
          ],
        },
        {
          titre: "3. Cookies et mesure d'audience",
          paras: [
            "Le site ne dépose aucun cookie publicitaire et n'utilise aucun traceur de réseau social.",
            "À ce jour, le site n'écrit rien dans le stockage de votre navigateur. Si des préférences d'affichage devaient y être conservées, elles ne quitteraient jamais votre appareil et ne nous seraient pas transmises.",
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
