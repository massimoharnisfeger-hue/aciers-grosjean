"use client";

import { useState } from "react";
import Link from "next/link";
import type { Produit } from "@/lib/catalogue";

const eur = (v: number) =>
  v.toLocaleString("fr-BE", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " €";
const kgf = (v: number) =>
  v.toLocaleString("fr-BE", { minimumFractionDigits: 1, maximumFractionDigits: 1 });

function champ(p: Produit) {
  if (p.unite === "au mètre") return { label: "Longueur", suffixe: "m", pas: 0.1, defaut: 6, coupable: true };
  if (p.unite === "au m²") return { label: "Surface", suffixe: "m²", pas: 0.5, defaut: 2, coupable: true };
  if (p.unite === "à la plaque") return { label: "Nombre de plaques", suffixe: "plaques", pas: 1, defaut: 1, coupable: true };
  if (p.unite === "au panneau") return { label: "Nombre de panneaux", suffixe: "panneaux", pas: 1, defaut: 1, coupable: false };
  return { label: "Quantité", suffixe: "pièces", pas: 1, defaut: 1, coupable: false };
}

export default function Calculateur({ p }: { p: Produit }) {
  const c = champ(p);
  const [qte, setQte] = useState<number>(c.defaut);
  const [coupes, setCoupes] = useState(0);

  const quantite = Number.isFinite(qte) && qte > 0 ? qte : 0;
  const poids = p.kg !== null ? quantite * p.kg : null;
  // Prix du catalogue du site actuel ; la découpe est un supplément dont le montant dépend du profil.
  const total = p.prix !== null ? quantite * p.prix : null;
  const totalTtc = p.prixTtc != null ? quantite * p.prixTtc : null;

  const corps = [
    `Produit : ${p.nom}`,
    `${c.label} : ${quantite} ${c.suffixe}`,
    c.coupable ? `Découpes : ${coupes}` : "",
    poids !== null ? `Poids estimé : ${kgf(poids)} kg` : "",
    total !== null
      ? `Estimation en ligne : ${eur(total)} HTVA${totalTtc !== null ? ` (${eur(totalTtc)} TVAC)` : ""}, hors découpe`
      : "Prix : sur devis",
    "",
    "Merci de me confirmer le prix exact, la disponibilité et le dépôt de retrait.",
  ]
    .filter(Boolean)
    .join("\n");

  // L'estimation part au formulaire de devis, qui l'envoie par le serveur (ADR-0006) :
  // ouvrir la messagerie du visiteur perdait la demande sur un telephone sans client mail.

  return (
    <div className="rounded-2xl border border-brume bg-nuage p-6">
      <h2 className="h-title text-sm font-semibold uppercase tracking-[0.14em] text-soft">
        Estimez votre besoin
      </h2>

      <div className={`mt-5 grid gap-4 ${c.coupable ? "sm:grid-cols-2" : ""}`}>
        <label className="block font-body text-sm text-encre">
          {c.label} ({c.suffixe})
          <input
            id={`qte-${p.slug}`}
            type="number"
            min={0}
            step={c.pas}
            value={Number.isNaN(qte) ? "" : qte}
            onChange={(e) => setQte(parseFloat(e.target.value))}
            className="mt-2 w-full rounded-xl border border-brume bg-white px-4 py-3 font-mono text-lg tabular-nums text-encre focus:border-encre focus:outline-none"
          />
        </label>

        {c.coupable && (
          <label className="block font-body text-sm text-encre">
            Nombre de découpes
            <input
              id={`coupes-${p.slug}`}
              type="number"
              min={0}
              step={1}
              value={Number.isNaN(coupes) ? "" : coupes}
              onChange={(e) => setCoupes(Math.max(0, parseInt(e.target.value || "0", 10)))}
              className="mt-2 w-full rounded-xl border border-brume bg-white px-4 py-3 font-mono text-lg tabular-nums text-encre focus:border-encre focus:outline-none"
            />
          </label>
        )}
      </div>

      <dl className="mt-6 divide-y divide-brume border-y border-brume">
        {poids !== null && (
          <div className="flex items-baseline justify-between gap-4 py-2.5">
            <dt className="font-body text-sm text-soft">Poids total</dt>
            <dd className="font-mono text-sm tabular-nums text-encre">{kgf(poids)} kg</dd>
          </div>
        )}
        {c.coupable && (
          <div className="flex items-baseline justify-between gap-4 py-2.5">
            <dt className="font-body text-sm text-soft">
              Découpe <span className="text-xs">· supplément selon le profil</span>
            </dt>
            <dd className="font-mono text-sm tabular-nums text-encre">
              {coupes > 0 ? "sur devis" : "—"}
            </dd>
          </div>
        )}
        <div className="flex items-baseline justify-between gap-4 py-3.5">
          <dt className="h-title font-semibold text-encre">Estimation HTVA</dt>
          <dd className="h-title text-2xl font-bold tabular-nums text-encre">
            {total !== null ? eur(total) : "Sur devis"}
          </dd>
        </div>
        {totalTtc !== null && (
          <div className="flex items-baseline justify-between gap-4 py-2.5">
            <dt className="font-body text-sm text-soft">Soit TVAC (21&nbsp;%)</dt>
            <dd className="font-mono text-sm tabular-nums text-encre">{eur(totalTtc)}</dd>
          </div>
        )}
      </dl>

      <Link href={`/devis?details=${encodeURIComponent(corps)}`} className="btn-cta mt-6 w-full justify-center">
        Confirmer ce prix en 24 h
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </Link>

      <p className="mt-3 font-body text-xs leading-relaxed text-soft">
        Estimation calculée sur le prix du catalogue, hors supplément de découpe. L&apos;acier
        cote à la semaine&nbsp;: le devis fait foi.
      </p>
    </div>
  );
}
