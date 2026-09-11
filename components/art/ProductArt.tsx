/**
 * Illustrations produits — dessinées à la main en SVG.
 * Libres de droit par construction, aucune dépendance réseau.
 * Palette charte : gris acier (#AAB0B3 / #D1D6DA), encre (#333642), jaune (#FFD500).
 */

type ArtProps = { className?: string };

/* Dégradés métal réutilisables, ids uniques par composant */
function MetalDefs({ id }: { id: string }) {
  return (
    <defs>
      <linearGradient id={`${id}-face`} x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stopColor="#E8ECEF" />
        <stop offset="45%" stopColor="#C3CACE" />
        <stop offset="100%" stopColor="#9AA2A7" />
      </linearGradient>
      <linearGradient id={`${id}-top`} x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stopColor="#F2F5F6" />
        <stop offset="100%" stopColor="#CFD5D9" />
      </linearGradient>
      <linearGradient id={`${id}-side`} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#8D9499" />
        <stop offset="100%" stopColor="#666D73" />
      </linearGradient>
      <linearGradient id={`${id}-shine`} x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stopColor="#fff" stopOpacity="0" />
        <stop offset="50%" stopColor="#fff" stopOpacity="0.55" />
        <stop offset="100%" stopColor="#fff" stopOpacity="0" />
      </linearGradient>
    </defs>
  );
}

/* ---------------- POUTRELLE IPE / HEA (isométrique) ---------------- */
export function ArtPoutrelle({ className }: ArtProps) {
  const id = "ipe";
  return (
    <svg viewBox="0 0 400 300" className={className} aria-hidden>
      <MetalDefs id={id} />
      {/* extrusion (profondeur) */}
      <g>
        <polygon points="120,80 190,45 190,62 155,79 155,79 120,97" fill={`url(#${id}-top)`} />
        <polygon points="240,80 310,45 310,62 240,97" fill={`url(#${id}-top)`} />
        <polygon points="310,45 310,62 240,97 240,80" fill={`url(#${id}-side)`} opacity="0.9" />
        <polygon points="120,220 190,185 310,185 240,220" fill={`url(#${id}-side)`} />
        <polygon points="240,80 310,45 310,185 240,220" fill={`url(#${id}-side)`} />
      </g>
      {/* face avant en I */}
      <path
        d="M120,80 H240 V100 H190 V200 H240 V220 H120 V200 H170 V100 H120 Z"
        fill={`url(#${id}-face)`}
        stroke="#333642"
        strokeWidth="2.5"
        strokeLinejoin="round"
      />
      {/* face supérieure */}
      <polygon points="120,80 190,45 310,45 240,80" fill={`url(#${id}-top)`} stroke="#333642" strokeWidth="2.5" strokeLinejoin="round" />
      {/* reflet */}
      <rect x="128" y="86" width="104" height="6" rx="3" fill={`url(#${id}-shine)`} />
      <rect x="176" y="110" width="8" height="80" rx="4" fill={`url(#${id}-shine)`} opacity="0.7" />
      {/* cote jaune */}
      <line x1="100" y1="80" x2="100" y2="220" stroke="#FFD500" strokeWidth="4" strokeLinecap="round" />
    </svg>
  );
}

/* ---------------- TÔLE NERVURÉE ---------------- */
export function ArtTole({ className }: ArtProps) {
  const id = "tole";
  const waves = Array.from({ length: 9 });
  return (
    <svg viewBox="0 0 400 300" className={className} aria-hidden>
      <MetalDefs id={id} />
      {/* plaque en perspective */}
      <g transform="translate(30,78) skewY(-6)">
        <rect x="0" y="20" width="340" height="170" fill={`url(#${id}-face)`} stroke="#333642" strokeWidth="2.5" />
        {waves.map((_, i) => (
          <g key={i}>
            <rect x={10 + i * 37} y="20" width="16" height="170" fill="#9AA2A7" opacity="0.55" />
            <rect x={26 + i * 37} y="20" width="4" height="170" fill="#fff" opacity="0.5" />
          </g>
        ))}
        {/* tranche */}
        <rect x="0" y="8" width="340" height="12" fill={`url(#${id}-top)`} stroke="#333642" strokeWidth="2.5" />
      </g>
      <rect x="30" y="236" width="120" height="5" rx="2.5" fill="#FFD500" />
    </svg>
  );
}

/* ---------------- TUBES rond + carré ---------------- */
export function ArtTube({ className }: ArtProps) {
  const id = "tube";
  return (
    <svg viewBox="0 0 400 300" className={className} aria-hidden>
      <MetalDefs id={id} />
      {/* tube carré (isométrique) */}
      <g>
        <polygon points="60,120 130,85 230,85 160,120" fill={`url(#${id}-top)`} stroke="#333642" strokeWidth="2.5" strokeLinejoin="round" />
        <rect x="60" y="120" width="100" height="110" fill={`url(#${id}-face)`} stroke="#333642" strokeWidth="2.5" />
        <polygon points="160,120 230,85 230,195 160,230" fill={`url(#${id}-side)`} stroke="#333642" strokeWidth="2.5" strokeLinejoin="round" />
        {/* creux */}
        <polygon points="82,132 137,105 208,105 153,132" fill="#5C6369" />
        <rect x="76" y="128" width="12" height="96" fill={`url(#${id}-shine)`} opacity="0.6" />
      </g>
      {/* tube rond */}
      <g transform="translate(255,150)">
        <ellipse cx="0" cy="0" rx="52" ry="52" fill={`url(#${id}-face)`} stroke="#333642" strokeWidth="2.5" />
        <ellipse cx="0" cy="0" rx="30" ry="30" fill="#5C6369" stroke="#333642" strokeWidth="2" />
        <path d="M-38,-24 A46,46 0 0 1 -8,-45" stroke="#fff" strokeWidth="6" fill="none" opacity="0.65" strokeLinecap="round" />
      </g>
      <circle cx="255" cy="150" r="66" fill="none" stroke="#FFD500" strokeWidth="3" strokeDasharray="6 10" opacity="0.9" />
    </svg>
  );
}

/* ---------------- CORNIÈRE (L) ---------------- */
export function ArtCorniere({ className }: ArtProps) {
  const id = "corn";
  return (
    <svg viewBox="0 0 400 300" className={className} aria-hidden>
      <MetalDefs id={id} />
      <g>
        {/* dessus */}
        <polygon points="110,90 180,55 300,55 230,90" fill={`url(#${id}-top)`} stroke="#333642" strokeWidth="2.5" strokeLinejoin="round" />
        <polygon points="110,90 130,90 130,210 250,210 250,230 110,230" fill={`url(#${id}-face)`} stroke="#333642" strokeWidth="2.5" strokeLinejoin="round" />
        <polygon points="230,90 300,55 300,75 250,102" fill={`url(#${id}-side)`} stroke="#333642" strokeWidth="2" strokeLinejoin="round" />
        <polygon points="250,210 320,175 320,195 250,230" fill={`url(#${id}-side)`} stroke="#333642" strokeWidth="2.5" strokeLinejoin="round" />
      </g>
      <rect x="116" y="96" width="8" height="108" rx="4" fill={`url(#${id}-shine)`} opacity="0.7" />
      <path d="M110,250 H250" stroke="#FFD500" strokeWidth="4" strokeLinecap="round" />
    </svg>
  );
}

/* ---------------- ACIER CORTEN (patine) ---------------- */
export function ArtCorten({ className }: ArtProps) {
  return (
    <svg viewBox="0 0 400 300" className={className} aria-hidden>
      <defs>
        <linearGradient id="corten-g" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#A9825F" />
          <stop offset="45%" stopColor="#8E6A4C" />
          <stop offset="100%" stopColor="#6E523C" />
        </linearGradient>
        <filter id="corten-rough">
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" />
          <feColorMatrix type="saturate" values="0" />
          <feComposite operator="in" in2="SourceGraphic" />
        </filter>
      </defs>
      {/* panneaux */}
      <g transform="translate(40,45)">
        <rect x="0" y="0" width="150" height="200" rx="3" fill="url(#corten-g)" stroke="#333642" strokeWidth="2.5" />
        <rect x="0" y="0" width="150" height="200" rx="3" fill="#3b2a1d" opacity="0.35" filter="url(#corten-rough)" />
        <rect x="165" y="20" width="150" height="200" rx="3" fill="url(#corten-g)" stroke="#333642" strokeWidth="2.5" />
        <rect x="165" y="20" width="150" height="200" rx="3" fill="#3b2a1d" opacity="0.28" filter="url(#corten-rough)" />
        {/* joints */}
        <line x1="0" y1="66" x2="150" y2="66" stroke="#5C4433" strokeWidth="2" opacity="0.7" />
        <line x1="0" y1="133" x2="150" y2="133" stroke="#5C4433" strokeWidth="2" opacity="0.7" />
        <line x1="165" y1="86" x2="315" y2="86" stroke="#5C4433" strokeWidth="2" opacity="0.7" />
        <line x1="165" y1="153" x2="315" y2="153" stroke="#5C4433" strokeWidth="2" opacity="0.7" />
      </g>
      <rect x="40" y="260" width="90" height="5" rx="2.5" fill="#FFD500" />
    </svg>
  );
}

/* ---------------- TREILLIS SOUDÉ ---------------- */
export function ArtTreillis({ className }: ArtProps) {
  const cols = Array.from({ length: 7 });
  const rows = Array.from({ length: 5 });
  return (
    <svg viewBox="0 0 400 300" className={className} aria-hidden>
      <MetalDefs id="tre" />
      <g transform="translate(45,50) skewY(-6)">
        {rows.map((_, r) => (
          <rect key={`r${r}`} x="0" y={r * 45} width="310" height="9" rx="4.5" fill="url(#tre-face)" stroke="#333642" strokeWidth="1.6" />
        ))}
        {cols.map((_, c) => (
          <rect key={`c${c}`} x={c * 50} y="0" width="9" height="190" rx="4.5" fill="url(#tre-face)" stroke="#333642" strokeWidth="1.6" />
        ))}
        {/* points de soudure */}
        {rows.map((_, r) =>
          cols.map((_, c) => (
            <circle key={`w${r}-${c}`} cx={c * 50 + 4.5} cy={r * 45 + 4.5} r="3.4" fill="#FFD500" opacity="0.9" />
          ))
        )}
      </g>
    </svg>
  );
}

/* ---------------- PLAT ACIER ---------------- */
export function ArtPlat({ className }: ArtProps) {
  const id = "plat";
  return (
    <svg viewBox="0 0 400 300" className={className} aria-hidden>
      <MetalDefs id={id} />
      {[0, 1, 2].map((i) => (
        <g key={i} transform={`translate(${i * 18},${i * 34})`}>
          <polygon points="70,120 140,85 320,85 250,120" fill={`url(#${id}-top)`} stroke="#333642" strokeWidth="2.2" strokeLinejoin="round" />
          <rect x="70" y="120" width="180" height="18" fill={`url(#${id}-face)`} stroke="#333642" strokeWidth="2.2" />
          <polygon points="250,120 320,85 320,103 250,138" fill={`url(#${id}-side)`} stroke="#333642" strokeWidth="2.2" strokeLinejoin="round" />
          <rect x="78" y="124" width="70" height="4" rx="2" fill={`url(#${id}-shine)`} />
        </g>
      ))}
      <rect x="70" y="245" width="100" height="5" rx="2.5" fill="#FFD500" />
    </svg>
  );
}

/* ---------------- SCÈNE : STOCK / DÉPÔT ---------------- */
export function ArtStock({ className }: ArtProps) {
  const id = "stock";
  return (
    <svg viewBox="0 0 400 300" className={className} aria-hidden>
      <MetalDefs id={id} />
      <rect width="400" height="300" fill="#EEF1F3" />
      {/* racks */}
      <g stroke="#333642" strokeWidth="3" fill="none" opacity="0.35">
        <path d="M40,40 V270 M200,40 V270 M360,40 V270 M40,120 H360 M40,195 H360" />
      </g>
      {/* piles de profilés */}
      {[0, 1, 2].map((r) =>
        [0, 1, 2, 3].map((c) => (
          <circle key={`${r}-${c}`} cx={68 + c * 34 + r * 8} cy={95 + r * 75} r="13" fill={`url(#${id}-face)`} stroke="#333642" strokeWidth="2" />
        ))
      )}
      {[0, 1].map((r) =>
        [0, 1, 2].map((c) => (
          <rect key={`t${r}-${c}`} x={225 + c * 40} y={70 + r * 75} width="32" height="26" rx="3" fill={`url(#${id}-face)`} stroke="#333642" strokeWidth="2" />
        ))
      )}
      <rect x="225" y="220" width="110" height="26" rx="3" fill="#FFD500" />
      <text x="280" y="238" textAnchor="middle" fontSize="14" fontWeight="700" fill="#333642" fontFamily="sans-serif">STOCK</text>
    </svg>
  );
}

/* ---------------- SCÈNE : DÉCOUPE ---------------- */
export function ArtDecoupe({ className }: ArtProps) {
  const id = "coupe";
  return (
    <svg viewBox="0 0 400 300" className={className} aria-hidden>
      <MetalDefs id={id} />
      <rect width="400" height="300" fill="#333642" />
      <g opacity="0.12" stroke="#fff" strokeWidth="1">
        {Array.from({ length: 9 }).map((_, i) => <line key={i} x1="0" y1={i * 36} x2="400" y2={i * 36} />)}
      </g>
      {/* barre */}
      <rect x="30" y="140" width="340" height="34" rx="4" fill={`url(#${id}-face)`} stroke="#0f1115" strokeWidth="2" />
      {/* disque */}
      <circle cx="230" cy="157" r="56" fill="none" stroke="#AAB0B3" strokeWidth="6" opacity="0.85" />
      <circle cx="230" cy="157" r="10" fill="#AAB0B3" />
      {/* étincelles */}
      {Array.from({ length: 14 }).map((_, i) => {
        const a = (-40 + i * 11) * (Math.PI / 180);
        const len = 40 + (i % 4) * 22;
        return (
          <line
            key={i}
            x1="230" y1="157"
            x2={230 + Math.cos(a) * len} y2={157 + Math.sin(a) * len}
            stroke="#FFD500" strokeWidth={i % 3 === 0 ? 3 : 1.6} strokeLinecap="round" opacity={0.9 - (i % 5) * 0.12}
          />
        );
      })}
      <circle cx="230" cy="157" r="16" fill="#FFD500" opacity="0.35" />
    </svg>
  );
}

/* ---------------- SCÈNE : ATELIER / STRUCTURE ---------------- */
export function ArtAtelier({ className }: ArtProps) {
  const id = "atel";
  return (
    <svg viewBox="0 0 400 300" className={className} aria-hidden>
      <MetalDefs id={id} />
      <rect width="400" height="300" fill="#EEF1F3" />
      {/* charpente */}
      <g stroke="#333642" strokeWidth="7" strokeLinecap="round" fill="none">
        <path d="M50,250 V110 M350,250 V110 M40,110 L200,40 L360,110" />
        <path d="M50,150 H350" strokeWidth="5" />
      </g>
      <g stroke="#AAB0B3" strokeWidth="4" fill="none">
        <path d="M60,150 L200,55 M340,150 L200,55 M60,250 L200,150 M340,250 L200,150" />
      </g>
      {/* gousset jaune */}
      <circle cx="200" cy="150" r="16" fill="#FFD500" />
      <circle cx="200" cy="55" r="9" fill="#FFD500" />
      <rect x="0" y="250" width="400" height="50" fill="#D1D6DA" />
    </svg>
  );
}

/* ---------------- VISSERIE (vis autoforante) ---------------- */
export function ArtVisserie({ className }: ArtProps) {
  const id = "vis";
  return (
    <svg viewBox="0 0 400 300" className={className} aria-hidden>
      <MetalDefs id={id} />
      <g transform="translate(0,10)">
        {/* tête hexagonale */}
        <polygon points="72,104 96,88 134,88 158,104 134,120 96,120" fill={`url(#${id}-face)`} stroke="#333642" strokeWidth="2.5" strokeLinejoin="round" />
        <polygon points="72,104 96,120 96,146 72,130" fill={`url(#${id}-side)`} stroke="#333642" strokeWidth="2.5" strokeLinejoin="round" />
        <polygon points="158,104 134,120 134,146 158,130" fill={`url(#${id}-side)`} stroke="#333642" strokeWidth="2.5" strokeLinejoin="round" />
        <polygon points="96,120 134,120 134,146 96,146" fill={`url(#${id}-face)`} stroke="#333642" strokeWidth="2.5" strokeLinejoin="round" />
        {/* rondelle */}
        <ellipse cx="115" cy="150" rx="34" ry="9" fill="#AAB0B3" stroke="#333642" strokeWidth="2.2" />
        {/* tige filetée */}
        <rect x="101" y="150" width="28" height="96" fill={`url(#${id}-face)`} stroke="#333642" strokeWidth="2.4" />
        {Array.from({ length: 8 }).map((_, i) => (
          <line key={i} x1="101" y1={162 + i * 11} x2="129" y2={156 + i * 11} stroke="#333642" strokeWidth="2" opacity="0.75" />
        ))}
        {/* pointe autoforante */}
        <polygon points="101,246 129,246 118,274 112,274" fill={`url(#${id}-side)`} stroke="#333642" strokeWidth="2.4" strokeLinejoin="round" />
        <rect x="106" y="112" width="7" height="26" rx="3" fill={`url(#${id}-shine)`} opacity="0.7" />
      </g>
      {/* cote jaune */}
      <g stroke="#FFD500" strokeWidth="3.5" strokeLinecap="round">
        <line x1="215" y1="100" x2="215" y2="284" />
        <line x1="207" y1="100" x2="223" y2="100" />
        <line x1="207" y1="284" x2="223" y2="284" />
      </g>
      <text x="236" y="198" fontSize="19" fontWeight="700" fill="#333642" fontFamily="sans-serif">100</text>
      <text x="284" y="198" fontSize="13" fill="#333642" opacity="0.6" fontFamily="sans-serif">mm</text>
    </svg>
  );
}

/* Table d'accès par clé produit */
export const productArt: Record<string, (p: ArtProps) => JSX.Element> = {
  poutrelles: ArtPoutrelle,
  toles: ArtTole,
  tubes: ArtTube,
  "cornieres-plats": ArtCorniere,
  corten: ArtCorten,
  treillis: ArtTreillis,
  plats: ArtPlat,
  visserie: ArtVisserie,
  "poteaux-cloture": ArtTube,
};
