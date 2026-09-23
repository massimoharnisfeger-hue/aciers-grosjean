/**
 * Recherche dans le catalogue visuel : la même lecture des deux côtés.
 *
 * L'index est bâti sur le serveur (lib/catalogue-visuel.ts) et la saisie est
 * lue dans le navigateur (components/catalogue/FiltreCatalogue.tsx). Si les
 * deux ne normalisaient pas le texte de la même façon, ils ne se
 * rencontreraient jamais : ce module n'importe rien et sert aux deux.
 *
 * Les cotes s'écrivent « 40x40x4mm » dans les noms de produits et « 40 × 40 mm »
 * dans les spécifications. Les deux deviennent « 40 40 4 mm », et une requête
 * tapée « 40x40 » retrouve les deux écritures.
 */
export function normaliserRecherche(texte: string): string {
  return texte
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/(\d)\s*[x×*]\s*(?=\d)/g, "$1 ") // 40x40, 40 × 40 → 40 40
    .replace(/(\d)([a-z])/g, "$1 $2") // 4mm → 4 mm
    .replace(/(\d)[.,](?=\d)/g, "$1.") // 2,5 → 2.5 : une seule écriture décimale
    .replace(/[^a-z0-9.]+/g, " ")
    .replace(/(^|\s)\.+|\.+(?=\s|$)/g, "$1") // points isolés ou finaux (« S235JR. »)
    .trim();
}

/**
 * La requête correspond-elle à une entrée ? Les deux textes sont déjà normalisés.
 *
 * Chaque jeton de la requête consomme un jeton distinct de l'entrée : « 40 40 »
 * exige deux « 40 », donc un tube 40 × 20 ne répond pas à « 40x40 ». Un nombre
 * se compare entièrement (« 4 » ne trouve pas « 40 ») ; un mot se compare par
 * son début (« corn » trouve « corniere »).
 */
export function correspondALaRecherche(entree: string, requete: string): boolean {
  const voulus = requete.split(" ").filter(Boolean);
  if (voulus.length === 0) return true;
  const disponibles = entree.split(" ").filter(Boolean);
  const pris = new Array<boolean>(disponibles.length).fill(false);
  for (const jeton of voulus) {
    const numerique = /^\d/.test(jeton);
    const i = disponibles.findIndex(
      (d, k) => !pris[k] && (numerique ? d === jeton : d.startsWith(jeton))
    );
    if (i === -1) return false;
    pris[i] = true;
  }
  return true;
}
