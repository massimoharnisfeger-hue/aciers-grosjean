import { redirections } from "./lib/redirections.mjs";

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  // Les 652 anciennes URLs du site sont redirigées en 301 vers leur URL propre.
  // Sans cela, la refonte perdrait les 2 103 backlinks et les positions acquises.
  async redirects() {
    return redirections.map((r) => ({ ...r, permanent: true }));
  },
};

export default nextConfig;
