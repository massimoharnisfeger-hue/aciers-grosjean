import { NextResponse } from "next/server";
import nodemailer from "nodemailer";
import { site } from "@/lib/content";

/**
 * Réception des demandes de devis (`components/sections/DevisForm.tsx`).
 *
 * Contrat, contrôlé par `tests/test_parcours.py` (P8) :
 * - GET → 405 ; corps illisible, incomplet ou trop long → 400 ;
 * - champ piège `site_web` rempli → 200 muet, rien n'est envoyé (robots) ;
 * - SMTP non configuré → 503 avec `erreur` : le formulaire bascule sur la
 *   messagerie du visiteur, comme avant l'existence de cette route ;
 * - envoi refusé par le serveur SMTP → 502 avec `erreur`, même bascule ;
 * - plus de 5 demandes valides, ou 30 requêtes, depuis la même adresse en
 *   10 minutes → 429 (P12).
 *
 * Variables (modèle dans `.env.example`) : SMTP_HOST, SMTP_PORT, SMTP_USER,
 * SMTP_PASSWORD, DEVIS_DESTINATAIRE. Sur Vercel : Settings → Environment
 * Variables. Jamais dans le dépôt, qui est public.
 */

// nodemailer a besoin de Node (sockets SMTP) : pas d'exécution Edge.
export const runtime = "nodejs";

const LIMITES = {
  profil: 40,
  nom: 120,
  email: 200,
  telephone: 40,
  produit: 120,
  depot: 80,
  details: 4000,
} as const;

/**
 * Plafond par adresse IP.
 *
 * Sans lui, l'adresse Microsoft 365 de l'entreprise relaie autant de messages
 * qu'on lui en demande : la boîte se remplit et le compte finit bridé ou
 * bloqué par Microsoft, ce qui coupe aussi les envois légitimes.
 *
 * Deux plafonds, parce qu'ils protègent deux choses différentes : ENVOIS
 * protège la boîte aux lettres et ne compte que les demandes qui vont
 * réellement partir ; REQUETES protège le quota d'exécutions et compte tout,
 * y compris les corps invalides qu'un robot envoie en rafale.
 *
 * Limite assumée : ce compteur vit dans la mémoire de l'instance. Vercel en
 * démarre plusieurs et les recycle ; un même visiteur peut donc tomber sur un
 * compteur neuf, et une attaque répartie sur de nombreuses adresses passe au
 * travers. Il arrête le flot naïf — une boucle depuis un poste — pas une
 * attaque distribuée. Un vrai plafond partagé demanderait un stockage externe
 * (Vercel KV, Upstash) : un service de plus, une clé de plus dans un dépôt
 * public. Ce n'est pas la bonne dépense tant que le site est en
 * préproduction ; c'est la marche suivante si le formulaire est abusé.
 */
const FENETRE_MS = 10 * 60 * 1000;
const PLAFOND_ENVOIS = 5;
const PLAFOND_REQUETES = 30;
// Un compteur par adresse ; au-delà, la mémoire est purgée entièrement plutôt
// que de croître sans fin sous une attaque qui change d'adresse à chaque coup.
const ADRESSES_MAX = 5000;

type Compteur = { envois: number[]; requetes: number[] };
const compteurs = new Map<string, Compteur>();

function adresseDe(requete: Request): string {
  const transmise = requete.headers.get("x-forwarded-for");
  // `x-forwarded-for` peut lister plusieurs relais : la première est le client.
  if (transmise) return transmise.split(",")[0].trim();
  return requete.headers.get("x-real-ip") ?? "inconnue";
}

function compteurDe(adresse: string, maintenant: number): Compteur {
  if (compteurs.size > ADRESSES_MAX) compteurs.clear();
  const compteur = compteurs.get(adresse) ?? { envois: [], requetes: [] };
  const recent = (horodatages: number[]) =>
    horodatages.filter((t) => maintenant - t < FENETRE_MS);
  compteur.envois = recent(compteur.envois);
  compteur.requetes = recent(compteur.requetes);
  compteurs.set(adresse, compteur);
  return compteur;
}

function refus(compteur: Compteur, maintenant: number) {
  const plusAncien = Math.min(...compteur.envois, ...compteur.requetes);
  const secondes = Math.max(1, Math.ceil((FENETRE_MS - (maintenant - plusAncien)) / 1000));
  return NextResponse.json(
    { erreur: "trop de demandes, réessayez dans quelques minutes" },
    { status: 429, headers: { "Retry-After": String(secondes) } },
  );
}

type Champ = keyof typeof LIMITES;
type Demande = Record<Champ, string>;

/** Un `\r\n` dans un nom ou une adresse injecterait un en-tête SMTP : une seule ligne. */
const uneLigne = (valeur: string) => valeur.replace(/[\r\n]+/g, " ").trim();

function lire(corps: unknown): Demande | null {
  if (typeof corps !== "object" || corps === null) return null;
  const source = corps as Record<string, unknown>;
  const demande = {} as Demande;
  for (const champ of Object.keys(LIMITES) as Champ[]) {
    const valeur = source[champ];
    if (valeur !== undefined && typeof valeur !== "string") return null;
    const texte = (valeur ?? "") as string;
    if (texte.length > LIMITES[champ]) return null;
    demande[champ] = champ === "details" ? texte.trim() : uneLigne(texte);
  }
  // Mêmes règles que `valide` dans DevisForm.tsx : le serveur ne fait pas confiance au client.
  if (demande.nom.length < 2) return null;
  if (!/.+@.+\..+/.test(demande.email)) return null;
  if (demande.details.length < 4) return null;
  return demande;
}

export async function POST(requete: Request) {
  const maintenant = Date.now();
  const compteur = compteurDe(adresseDe(requete), maintenant);
  if (compteur.requetes.length >= PLAFOND_REQUETES) return refus(compteur, maintenant);
  compteur.requetes.push(maintenant);

  let corps: unknown;
  try {
    corps = await requete.json();
  } catch {
    return NextResponse.json({ erreur: "corps illisible" }, { status: 400 });
  }

  // Champ piège : invisible pour un humain, rempli par les robots. On répond
  // comme à un succès pour ne pas leur apprendre à l'éviter.
  if (typeof corps === "object" && corps !== null && (corps as Record<string, unknown>).site_web) {
    return NextResponse.json({ ok: true });
  }

  const demande = lire(corps);
  if (!demande) {
    return NextResponse.json({ erreur: "demande incomplète ou invalide" }, { status: 400 });
  }

  // Comptabilisé ici seulement : un corps invalide ou un robot pris au piège
  // ne consomme pas le quota d'un visiteur qui partage son adresse (entreprise,
  // wifi public). Le 503 « SMTP non configuré » compte, lui : la demande était
  // valide et serait partie.
  if (compteur.envois.length >= PLAFOND_ENVOIS) return refus(compteur, maintenant);
  compteur.envois.push(maintenant);

  const { SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, DEVIS_DESTINATAIRE } = process.env;
  if (!SMTP_HOST || !SMTP_USER || !SMTP_PASSWORD) {
    return NextResponse.json({ erreur: "service d'envoi non configuré" }, { status: 503 });
  }

  const transport = nodemailer.createTransport({
    host: SMTP_HOST,
    port: Number(SMTP_PORT ?? 587),
    // Microsoft 365 : STARTTLS sur 587, pas de TLS implicite.
    secure: false,
    requireTLS: true,
    auth: { user: SMTP_USER, pass: SMTP_PASSWORD },
  });

  const texte = [
    `Profil : ${demande.profil || "—"}`,
    `Nom : ${demande.nom}`,
    `E-mail : ${demande.email}`,
    `Téléphone : ${demande.telephone || "—"}`,
    `Produit : ${demande.produit || "—"}`,
    `Dépôt de retrait : ${demande.depot || "—"}`,
    "",
    "Détails (dimensions, quantités, usage) :",
    demande.details,
    "",
    "— Envoyé par le formulaire de devis du site.",
  ].join("\n");

  try {
    await transport.sendMail({
      from: { name: "Site Aciers Grosjean", address: SMTP_USER },
      to: DEVIS_DESTINATAIRE || site.email,
      replyTo: { name: demande.nom, address: demande.email },
      subject: `Demande de devis — ${demande.nom} (${demande.produit || "produit non précisé"})`,
      text: texte,
    });
  } catch (erreur) {
    console.error("[devis] envoi SMTP refusé :", erreur instanceof Error ? erreur.message : erreur);
    return NextResponse.json({ erreur: "envoi impossible pour le moment" }, { status: 502 });
  }

  return NextResponse.json({ ok: true });
}
