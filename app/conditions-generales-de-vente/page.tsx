import type { Metadata } from "next";
import PageLegale from "@/components/ui/PageLegale";

export const metadata: Metadata = {
  title: "Conditions générales de vente | Aciers Grosjean",
  description:
    "Devis, prix, tolérances de découpe, retrait en dépôt, paiement, garanties et réclamations — les conditions générales de vente d'Aciers Grosjean.",
  alternates: { canonical: "/conditions-generales-de-vente" },
};

export default function ConditionsGenerales() {
  return (
    <PageLegale
      surtitre="Conditions générales"
      titre="Conditions générales de vente"
      intro="Ce qui est convenu quand vous commandez : validité des prix, tolérances, retrait, paiement et réclamations."
      aCompleter={[
        "Validation par un conseil juridique avant publication",
        "Délais de paiement réellement pratiqués pour les comptes professionnels",
        "Taux de l'indemnité de retard et clause pénale retenus",
        "Tribunal compétent à désigner (arrondissement du siège)",
        "Durée de mise à disposition avant frais de gardiennage",
      ]}
      blocs={[
        {
          titre: "1. Champ d'application",
          paras: [
            "Les présentes conditions régissent toute vente de produits et toute prestation de service réalisée par Aciers Grosjean, auprès de clients professionnels comme de consommateurs. Elles prévalent sur les conditions d'achat du client, sauf accord écrit contraire.",
            "Les dispositions protectrices du droit belge de la consommation s'appliquent de plein droit aux clients consommateurs et priment sur toute clause contraire des présentes.",
          ],
        },
        {
          titre: "2. Devis et prix",
          paras: [
            "Les prix affichés sur le site sont indicatifs et hors TVA. Ils ne constituent pas une offre ferme : le marché de l'acier cote à la semaine.",
            "Seul le devis nominatif fait foi. Sauf mention contraire, un devis est valable quinze jours calendrier à compter de son émission.",
            "Les tarifs sont dégressifs selon la quantité. Les prestations de découpe, de pliage et de perçage sont facturées en sus, selon le nombre d'opérations.",
          ],
        },
        {
          titre: "3. Tolérances de fabrication",
          paras: [
            "Les produits sidérurgiques sont soumis aux tolérances dimensionnelles et pondérales des normes européennes applicables. Un écart compris dans ces tolérances ne constitue pas un défaut de conformité.",
            "Pour les prestations de découpe, la tolérance est de ± 2 mm. Pour le perçage, la tolérance d'entraxe est de ± 0,5 mm.",
            "Les produits laminés à chaud présentent naturellement une calamine de surface et une légère oxydation ; il ne s'agit pas d'un défaut.",
          ],
        },
        {
          titre: "4. Commande et retrait",
          paras: [
            "La vente s'effectue par retrait en dépôt (click & collect). Le client est informé dès que la commande est prête, et choisit le dépôt de retrait.",
            "Le chargement s'effectue aux heures d'ouverture, avec l'aide du personnel et des moyens de manutention disponibles. Il appartient au client de se présenter avec un véhicule adapté à la longueur et à la masse commandées, et d'assurer l'arrimage.",
            "Au-delà de la durée de mise à disposition convenue, des frais de gardiennage peuvent être appliqués.",
          ],
        },
        {
          titre: "5. Produits façonnés sur mesure",
          paras: [
            "Les pièces découpées, pliées, percées ou fabriquées d'après les cotes du client sont des biens confectionnés selon ses spécifications. Conformément au Code de droit économique, le droit de rétractation de quatorze jours ne s'y applique pas.",
            "Le client est seul responsable de l'exactitude des cotes, quantités et nuances qu'il communique. En cas de doute sur un plan, nous sollicitons une confirmation écrite avant lancement.",
          ],
        },
        {
          titre: "6. Paiement",
          paras: [
            "Sauf ouverture d'un compte professionnel, le paiement s'effectue au comptant lors du retrait.",
            "Les marchandises restent la propriété d'Aciers Grosjean jusqu'au paiement intégral du prix, le transfert des risques s'opérant en revanche dès le retrait.",
            "Tout retard de paiement d'un client professionnel donne lieu de plein droit à des intérêts de retard et à une indemnité forfaitaire de recouvrement, dans les conditions prévues par la loi relative à la lutte contre le retard de paiement.",
          ],
        },
        {
          titre: "7. Réclamations et garanties",
          paras: [
            "Les défauts apparents et les erreurs de quantité doivent être signalés lors du retrait ou, au plus tard, dans les deux jours ouvrables suivants, par écrit.",
            "Le client consommateur bénéficie de la garantie légale de conformité de deux ans prévue par le Code de droit économique.",
            "Notre responsabilité est limitée au remplacement ou au remboursement de la marchandise non conforme. Elle ne couvre pas les conséquences d'un dimensionnement inadapté, d'une mise en œuvre défectueuse, ni les dommages indirects.",
          ],
        },
        {
          titre: "8. Droit applicable et juridiction",
          paras: [
            "Les présentes conditions sont soumises au droit belge.",
            "Tout litige relève des juridictions de l'arrondissement du siège social. Le client consommateur conserve la faculté de saisir la juridiction de son domicile, ainsi que le Service de médiation pour le consommateur (mediationconsommateur.be).",
          ],
        },
      ]}
    />
  );
}
