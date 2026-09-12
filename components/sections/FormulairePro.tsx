"use client";

import { useState } from "react";
import { site } from "@/lib/content";
import { depotsDetail } from "@/lib/edito";

const champ =
  "mt-2 w-full rounded-xl border border-brume bg-white px-4 py-3 font-body text-encre placeholder:text-soft focus:border-encre focus:outline-none";

export default function FormulairePro() {
  const [societe, setSociete] = useState("");
  const [tva, setTva] = useState("");
  const [contact, setContact] = useState("");
  const [email, setEmail] = useState("");
  const [tel, setTel] = useState("");
  const [metier, setMetier] = useState("Métallier / ferronnier");
  const [depot, setDepot] = useState(depotsDetail[0].nomComplet);
  const [volume, setVolume] = useState("Moins de 5 t / an");
  const [besoins, setBesoins] = useState("");
  const [envoye, setEnvoye] = useState(false);

  const valide =
    societe.trim().length > 1 && tva.trim().length > 3 && /.+@.+\..+/.test(email) && contact.trim().length > 1;

  const envoyer = (e: React.FormEvent) => {
    e.preventDefault();
    if (!valide) return;
    const corps = [
      "DEMANDE D'OUVERTURE DE COMPTE PROFESSIONNEL",
      "",
      `Société : ${societe}`,
      `Numéro de TVA : ${tva}`,
      `Contact : ${contact}`,
      `E-mail : ${email}`,
      `Téléphone : ${tel || "—"}`,
      `Activité : ${metier}`,
      `Dépôt principal : ${depot}`,
      `Volume annuel estimé : ${volume}`,
      "",
      "Besoins particuliers :",
      besoins || "—",
    ].join("\n");
    window.location.href = `mailto:${site.email}?subject=${encodeURIComponent(
      "Demande de compte pro — " + societe
    )}&body=${encodeURIComponent(corps)}`;
    setEnvoye(true);
  };

  if (envoye) {
    return (
      <div className="rounded-2xl border border-brume bg-white p-10 text-center">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-jaune">
          <svg width="30" height="30" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M5 13l4 4L19 7" stroke="#333642" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </div>
        <h2 className="h-display mt-5 text-2xl text-encre">Votre messagerie s&apos;ouvre…</h2>
        <p className="mx-auto mt-3 max-w-md font-body text-soft">
          Vérifiez que le message pré-rempli à <strong className="text-encre">{site.email}</strong> part
          bien. Réponse sous quelques jours ouvrables.
        </p>
        <a href={`mailto:${site.email}`} className="btn-ghost mt-6 inline-flex">Ouvrir ma messagerie</a>
      </div>
    );
  }

  return (
    <form onSubmit={envoyer} className="rounded-2xl border border-brume bg-white p-6 md:p-8">
      <div className="grid gap-4 sm:grid-cols-2">
        <label className="block font-body text-sm text-encre">
          Raison sociale *
          <input id="pro-societe" value={societe} onChange={(e) => setSociete(e.target.value)}
            placeholder="Métallerie Dupont SRL" className={champ} required />
        </label>
        <label className="block font-body text-sm text-encre">
          Numéro de TVA *
          <input id="pro-tva" value={tva} onChange={(e) => setTva(e.target.value)}
            placeholder="BE 0123.456.789" className={champ} required />
        </label>
        <label className="block font-body text-sm text-encre">
          Personne de contact *
          <input id="pro-contact" value={contact} onChange={(e) => setContact(e.target.value)}
            placeholder="Jean Dupont" className={champ} required />
        </label>
        <label className="block font-body text-sm text-encre">
          E-mail *
          <input id="pro-email" type="email" value={email} onChange={(e) => setEmail(e.target.value)}
            placeholder="jean@metallerie-dupont.be" className={champ} required />
        </label>
        <label className="block font-body text-sm text-encre">
          Téléphone
          <input id="pro-tel" value={tel} onChange={(e) => setTel(e.target.value)}
            placeholder="+32 …" className={champ} />
        </label>
        <label className="block font-body text-sm text-encre">
          Activité
          <select id="pro-metier" value={metier} onChange={(e) => setMetier(e.target.value)} className={champ}>
            {["Métallier / ferronnier", "Entreprise de construction", "Charpentier métallique",
              "Couvreur", "Paysagiste", "Serrurier", "Industrie / maintenance", "Autre"].map((m) => (
              <option key={m}>{m}</option>
            ))}
          </select>
        </label>
        <label className="block font-body text-sm text-encre">
          Dépôt principal
          <select id="pro-depot" value={depot} onChange={(e) => setDepot(e.target.value)} className={champ}>
            {depotsDetail.map((d) => <option key={d.slug}>{d.nomComplet}</option>)}
          </select>
        </label>
        <label className="block font-body text-sm text-encre">
          Volume annuel estimé
          <select id="pro-volume" value={volume} onChange={(e) => setVolume(e.target.value)} className={champ}>
            {["Moins de 5 t / an", "5 à 20 t / an", "20 à 100 t / an", "Plus de 100 t / an"].map((v) => (
              <option key={v}>{v}</option>
            ))}
          </select>
        </label>
      </div>

      <label className="mt-4 block font-body text-sm text-encre">
        Besoins particuliers
        <textarea id="pro-besoins" value={besoins} onChange={(e) => setBesoins(e.target.value)} rows={4}
          placeholder="Ex. découpe systématique, enlèvements hebdomadaires, certificats matière sur les poutrelles."
          className={champ} />
      </label>

      <button type="submit" disabled={!valide}
        className="btn-cta mt-6 w-full justify-center disabled:cursor-not-allowed disabled:opacity-40">
        Envoyer ma demande
      </button>
      <p className="mt-3 text-center font-body text-xs leading-relaxed text-soft">
        Réponse sous quelques jours ouvrables · Aucune donnée n&apos;est stockée sur ce site&nbsp;: le
        message part par votre propre messagerie.
      </p>
    </form>
  );
}
