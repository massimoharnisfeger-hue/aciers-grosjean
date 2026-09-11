import type { Config } from "tailwindcss";

// Palette 100 % charte officielle Aciers Grosjean (e-identite, avril 2024).
const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Couleurs charte
        jaune: "#FFD500", // signal, CTA, accents — ≤10% de la surface
        encre: "#333642", // gris bleuté — texte principal, fonds sombres, logo
        acier: "#AAB0B3", // gris moyen — aplats, séparateurs
        brume: "#D1D6DA", // gris clair — fonds alternatifs, bordures
        nuage: "#F4F6F7", // blanc cassé dérivé (fonds de respiration)
      },
      fontFamily: {
        // Poppins = substitut de Code Bold (titres) ; Comfortaa (sous-titres) ; Questrial ≈ Century Gothic (corps)
        title: ["var(--font-poppins)", "Poppins", "sans-serif"],
        sub: ["var(--font-comfortaa)", "Comfortaa", "sans-serif"],
        body: ["var(--font-questrial)", "Questrial", "sans-serif"],
        mono: ["var(--font-mono)", "IBM Plex Mono", "ui-monospace", "monospace"],
      },
      keyframes: {
        "beam-pan": {
          "0%,100%": { backgroundPosition: "0% 50%" },
          "50%": { backgroundPosition: "100% 50%" },
        },
        marquee: {
          from: { transform: "translateX(0)" },
          to: { transform: "translateX(-50%)" },
        },
      },
      animation: {
        "beam-pan": "beam-pan 14s ease infinite",
        marquee: "marquee 28s linear infinite",
      },
    },
  },
  plugins: [],
};

export default config;
