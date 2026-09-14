"use client";

import { useState } from "react";
import { site, depots } from "@/lib/content";

const champStyle =
  "mt-2 w-full rounded-xl border border-brume bg-white px-4 py-3 font-body text-encre placeholder:text-soft focus:border-encre focus:outline-none";

/** `produits` : noms des univers du catalogue, passés par la page (serveur). */
export default function DevisForm({ produits }: { produits: string[] }) {
  const [profil, setProfil] = useState("Particulier");
  const [nom, setNom] = useState("");
  const [email, setEmail] = useState("");
  const [tel, setTel] = useState("");
  const [produit, setProduit] = useState(produits[0] ?? "Autre / je ne sais pas");
  const [depot, setDepot] = useState(depots[0].ville);
  const [details, setDetails] = useState("");
  const [sent, setSent] = useState(false);

  const valide = nom.trim().length > 1 && /.+@.+\..+/.test(email) && details.trim().length > 3;

  const envoyer = (e: React.FormEvent) => {
    e.preventDefault();
    if (!valide) return;
    const corps = [
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
    const url = `mailto:${site.email}?subject=${encodeURIComponent(
      "Demande de devis — " + nom
    )}&body=${encodeURIComponent(corps)}`;
    window.location.href = url;
    setSent(true);
  };

  if (sent) {
    return (
      <div className="rounded-2xl border border-brume bg-white p-10 text-center">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-jaune">
          <svg width="30" height="30" viewBox="0 0 24 24" fill="none"><path d="M5 13l4 4L19 7" stroke="#333642" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" /></svg>
        </div>
        <h2 className="h-display mt-5 text-2xl text-encre">Votre messagerie s'ouvre…</h2>
        <p className="mt-3 font-body text-soft">
          Vérifiez que le message pré-rempli à <strong className="text-encre">{site.email}</strong> part bien.
          Si rien ne s'est ouvert, écrivez-nous directement — on répond sous 24h.
        </p>
        <a href={`mailto:${site.email}`} className="btn-ghost mt-6 inline-flex">Ouvrir ma messagerie</a>
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
          <input value={nom} onChange={(e) => setNom(e.target.value)} placeholder="Jean Dupont" className={champStyle} required />
        </label>
        <label className="block font-body text-sm text-encre">E-mail *
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="jean@email.com" className={champStyle} required />
        </label>
        <label className="block font-body text-sm text-encre">Téléphone
          <input value={tel} onChange={(e) => setTel(e.target.value)} placeholder="+32 …" className={champStyle} />
        </label>
        <label className="block font-body text-sm text-encre">Dépôt de retrait
          <select value={depot} onChange={(e) => setDepot(e.target.value)} className={champStyle}>
            {depots.map((d) => <option key={d.ville}>{d.ville}</option>)}
          </select>
        </label>
      </div>

      <label className="mt-4 block font-body text-sm text-encre">Type de produit
        <select value={produit} onChange={(e) => setProduit(e.target.value)} className={champStyle}>
          {produits.map((p) => <option key={p}>{p}</option>)}
          <option>Autre / je ne sais pas</option>
        </select>
      </label>

      <label className="mt-4 block font-body text-sm text-encre">Votre projet (dimensions, quantités, usage) *
        <textarea value={details} onChange={(e) => setDetails(e.target.value)} rows={4} placeholder="Ex. 12 m de tube carré 40×40×2, découpé en longueurs de 2 m, pour un garde-corps." className={champStyle} required />
      </label>

      <button type="submit" disabled={!valide} className="btn-cta mt-6 w-full justify-center disabled:cursor-not-allowed disabled:opacity-40">
        Envoyer ma demande de devis
      </button>
      <p className="mt-3 text-center font-body text-xs text-soft">
        Sans engagement · Réponse sous 24h · Aucune donnée n'est stockée sur ce site (le message part par votre messagerie).
      </p>
    </form>
  );
}
