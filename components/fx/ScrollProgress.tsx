"use client";

import { motion, useScroll, useSpring } from "framer-motion";

/** Fine barre jaune indiquant la progression de lecture. */
export default function ScrollProgress() {
  const { scrollYProgress } = useScroll();
  const scaleX = useSpring(scrollYProgress, { stiffness: 120, damping: 25, restDelta: 0.001 });
  return <motion.div aria-hidden className="progress-bar w-full" style={{ scaleX }} />;
}
