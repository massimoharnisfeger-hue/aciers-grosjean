"use client";

import { useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";

/** Déplacement vertical léger au scroll — profondeur sans désorientation. */
export default function Parallax({
  children,
  className = "",
  amount = 12,
  scale = false,
}: {
  children: React.ReactNode;
  className?: string;
  amount?: number;
  scale?: boolean;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start end", "end start"] });
  const y = useTransform(scrollYProgress, [0, 1], [`${amount}%`, `${-amount}%`]);
  const s = useTransform(scrollYProgress, [0, 0.5, 1], [1.12, 1, 1.12]);

  return (
    <div ref={ref} className={`overflow-hidden ${className}`}>
      <motion.div style={scale ? { y, scale: s } : { y }} className="h-full w-full">
        {children}
      </motion.div>
    </div>
  );
}
