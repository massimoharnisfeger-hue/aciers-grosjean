"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { site, depots } from "@/lib/content";

/**
 * `text-base` (16 px) est obligatoire, pas cosmétique : sous 16 px, Safari iOS
 * agrandit la page dès qu'un champ reçoit le focus et n'en revient pas toujours.
 * Sans cette classe, les champs héritent du `text-sm` (14 px) porté par le
 * <label> parent. Contrôlé par `tests/test_mobile.py` (M1, M1bis).
 */
const champStyle =
  "mt-2 w-full rounded-xl border border-brume bg-white px-4 py-3 font-body text-base text-encre placeholder:text-soft focus:border-encre focus:outline-none";

/**
 * `saisie` → `envoi` → `envoye` quand `/api/devis` a accepté la demande.
 * Si la route est absente (503), refusée (502) ou injoignable, `messagerie` :
 * la messagerie du visiteur prend le relais, comme avant l'existence de la route.
 * Contrat de la route : `app/api/devis/route.ts`, contrôlé par P8.
 */
type Etat = "saisie" | "envoi" | "envoye" | "messagerie";

/** `produits` : noms des univers du catalogue, passés par la page (serveur). */
export default function DevisForm({ produits }: { produits: string[] }) {
  const [profil, setProfil] = useState("Particulier");
  const [nom, setNom] = useState("");
  const [email, setEmail] = useState("");
  const [tel, setTel] = useState("");
  const [produit, setProduit] = useState(produits[0] ?? "Autre / je ne sais pas");
  const [depot, setDepot] = useState(depots[0].ville);
  const [details, setDetails] = useState("");
  // Champ piège : invisible pour un humain, rempli par les robots (P8c).
  const [siteWeb, setSiteWeb] = useState("");
  const [etat, setEtat] = useState<Etat>("saisie");

  // Le calculateur d'une fiche produit arrive avec son estimation dans l'URL
  // (`/devis?details=...`). Lu au montage : la page reste statique.
  useEffect(() => {
    const prerempli = new URLSearchParams(window.location.search).get("details");
    if (prerempli) setDetails((actuel) => actuel || prerempli);
  }, []);

  const valide = nom.trim().length > 1 && /.+@.+\..+/.test(email) && details.trim().length > 3;

  const corps = () =>
    [
      `Profil : ${profil}`,
      `Nom : ${nom}`,
      `Email : ${email}`,
      `Téléphone : ${tel || "—"}`,
      `Produit : ${produit}`,
      `Dépôt de retrait : ${depot}`,
      "",
      "Détails (dimensions, quantités, usage) :",
      details,
    ].join("\n");

  const lienMessagerie = () =>
    `mailto:${site.email}?subject=${encodeURIComponent("Demande de devis — " + nom)}&body=${encodeURIComponent(corps())}`;

  const envoyer = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!valide || etat === "envoi") return;
    setEtat("envoi");
    try {
      const reponse = await fetch("/api/devis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ profil, nom, email, telephone: tel, produit, depot, details, site_web: siteWeb }),
      });
      if (reponse.ok) {
        setEtat("envoye");
        return;
      }
    } catch {
      // Réseau coupé : même secours que le service indisponible.
    }
    window.location.href = lienMessagerie();
    setEtat("messagerie");
  };

  if (etat === "envoye") {
    return (
      <div className="rounded-2xl border border-brume bg-white p-10 text-center">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-jaune">
          <svg width="30" height="30" viewBox="0 0 24 24" fill="none"><path d="M5 13l4 4L19 7" stroke="#333642" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" /></svg>
        </div>
        <h2 className="h-display mt-5 text-2xl text-encre">Demande envoyée</h2>
        <p className="mt-3 font-body text-soft">
          Merci {nom.trim()}. On revient vers vous sous 24h à <strong className="text-encre">{email.trim()}</strong>.
          Une précision à ajouter ? Écrivez-nous à {site.email}.
        </p>
      </div>
    );
  }

  if (etat === "messagerie") {
    return (
      <div className="rounded-2xl border border-brume bg-white p-10 text-center">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-jaune">
          <svg width="30" height="30" viewBox="0 0 24 24" fill="none"><path d="M5 13l4 4L19 7" stroke="#333642" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" /></svg>
        </div>
        <h2 className="h-display mt-5 text-2xl text-encre">Votre messagerie s’ouvre…</h2>
        <p className="mt-3 font-body text-soft">
          Notre service d’envoi est momentanément indisponible : votre messagerie prend le relais.
          Vérifiez que le message pré-rempli à <strong className="text-encre">{site.email}</strong> part bien.
          Si rien ne s’est ouvert, écrivez-nous directement — on répond sous 24h.
        </p>
        <a href={lienMessagerie()} className="btn-ghost mt-6 inline-flex">Ouvrir ma messagerie</a>
      </div>
    );
  }

  return (
    <form onSubmit={envoyer} className="rounded-2xl border border-brume bg-white p-6 md:p-8">
      <fieldset>
        <legend className="font-body text-sm font-medium text-encre">Je suis…</legend>
        <div className="mt-3 grid grid-cols-2 gap-3">
          {["Particulier", "Professionnel"].map((p) => (
            <button
              key={p}
              type="button"
              onClick={() => setProfil(p)}
              className={`rounded-xl border px-4 py-3 font-body text-sm transition-all ${
                profil === p ? "border-encre bg-encre text-white" : "border-brume text-encre hover:border-encre/40"
              }`}
            >
              {p}
            </button>
          ))}
        </div>
      </fieldset>

      <div className="mt-5 grid gap-4 sm:grid-cols-2">
        <label className="block font-body text-sm text-encre">Nom complet *
          <input name="nom" autoComplete="name" value={nom} onChange={(e) => setNom(e.target.value)} placeholder="Jean Dupont" className={champStyle} required />
        </label>
        <label className="block font-body text-sm text-encre">E-mail *
          <input type="email" name="email" autoComplete="email" inputMode="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="jean@email.com" className={champStyle} required />
        </label>
        <label className="block font-body text-sm text-encre">Téléphone
          <input type="tel" name="telephone" autoComplete="tel" inputMode="tel" value={tel} onChange={(e) => setTel(e.target.value)} placeholder="+32 …" className={champStyle} />
        </label>
        <label className="block font-body text-sm text-encre">Dépôt de retrait
          <select name="depot" value={depot} onChange={(e) => setDepot(e.target.value)} className={champStyle}>
            {depots.map((d) => <option key={d.ville}>{d.ville}</option>)}
          </select>
        </label>
      </div>

      <label className="mt-4 block font-body text-sm text-encre">Type de produit
        <select name="produit" value={produit} onChange={(e) => setProduit(e.target.value)} className={champStyle}>
          {produits.map((p) => <option key={p}>{p}</option>)}
          <option>Autre / je ne sais pas</option>
        </select>
      </label>

      <label className="mt-4 block font-body text-sm text-encre">Votre projet (dimensions, quantités, usage) *
        <textarea name="details" value={details} onChange={(e) => setDetails(e.target.value)} rows={4} placeholder="Ex. 12 m de tube carré 40×40×2, découpé en longueurs de 2 m, pour un garde-corps." className={champStyle} required />
      </label>

      {/* Champ piège, hors écran et hors tabulation : un humain ne le voit pas, un robot le remplit. */}
      <label className="hidden" aria-hidden="true">Site web
        <input name="site_web" autoComplete="off" tabIndex={-1} value={siteWeb} onChange={(e) => setSiteWeb(e.target.value)} />
      </label>

      <button type="submit" disabled={!valide || etat === "envoi"} className="btn-cta mt-6 w-full justify-center disabled:cursor-not-allowed disabled:opacity-40">
        {etat === "envoi" ? "Envoi en cours…" : "Envoyer ma demande de devis"}
      </button>
      <p className="mt-3 text-center font-body text-xs text-soft">
        Sans engagement · Réponse sous 24h · Vos coordonnées servent uniquement à traiter votre demande
        (<Link href="/protection-des-donnees" className="lien-tactile underline">protection des données</Link>).
      </p>
    </form>
  );
}
