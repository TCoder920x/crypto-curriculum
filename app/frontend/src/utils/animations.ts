/** Animation utilities and spring presets for Framer Motion */

export const springPresets = {
  /** Gentle, smooth animation */
  gentle: {
    type: 'spring' as const,
    stiffness: 100,
    damping: 20,
    mass: 1,
  },
  /** Bouncy, playful animation */
  bouncy: {
    type: 'spring' as const,
    stiffness: 300,
    damping: 15,
    mass: 0.8,
  },
  /** Snappy, quick animation */
  snappy: {
    type: 'spring' as const,
    stiffness: 400,
    damping: 25,
    mass: 0.6,
  },
  /** Subtle, minimal animation */
  subtle: {
    type: 'spring' as const,
    stiffness: 80,
    damping: 25,
    mass: 1.2,
  },
};

/** Fade in animation */
export const fadeIn = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
  exit: { opacity: 0 },
  transition: springPresets.gentle,
};

/** Slide up animation */
export const slideUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
  transition: springPresets.gentle,
};

/** Scale in animation */
export const scaleIn = {
  initial: { opacity: 0, scale: 0.9 },
  animate: { opacity: 1, scale: 1 },
  exit: { opacity: 0, scale: 0.9 },
  transition: springPresets.snappy,
};

/** Stagger children animation */
export const staggerContainer = {
  initial: {},
  animate: {
    transition: {
      staggerChildren: 0.1,
    },
  },
};

/** Morphing button animation variants */
export const morphButtonVariants = {
  initial: {
    borderRadius: '12px',
    scale: 1,
  },
  hover: {
    borderRadius: '16px',
    scale: 1.02,
    transition: springPresets.snappy,
  },
  tap: {
    scale: 0.98,
    transition: springPresets.snappy,
  },
};

/** Card hover animation */
export const cardHover = {
  initial: { y: 0 },
  hover: {
    y: -4,
    transition: springPresets.gentle,
  },
};

/** Page transition animation */
export const pageTransition = {
  initial: { opacity: 0, x: 20 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: -20 },
  transition: springPresets.gentle,
};

