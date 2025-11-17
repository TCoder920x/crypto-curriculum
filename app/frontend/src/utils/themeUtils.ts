/** Theme utility functions for glass effects and adaptive styling */

import { ThemeMode } from '../contexts/ThemeContext';

/**
 * Get glass effect styles based on theme mode
 */
export const getGlassStyles = (
  mode: ThemeMode,
  variant: 'surface' | 'card' | 'button' | 'nav' = 'surface',
  opacity: number = 0.7
): React.CSSProperties => {
  const isDark = mode === 'dark';

  const baseStyles: React.CSSProperties = {
    backdropFilter: 'blur(20px) saturate(180%)',
    WebkitBackdropFilter: 'blur(20px) saturate(180%)',
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  };

  const variantStyles: Record<string, React.CSSProperties> = {
    surface: {
      background: isDark
        ? `rgba(22, 27, 34, ${opacity})`
        : `rgba(255, 255, 255, ${opacity})`,
      border: isDark
        ? '1px solid rgba(255, 255, 255, 0.1)'
        : '1px solid rgba(255, 255, 255, 0.3)',
      boxShadow: isDark
        ? '0 8px 32px 0 rgba(0, 0, 0, 0.4), inset 0 1px 0 0 rgba(255, 255, 255, 0.1)'
        : '0 8px 32px 0 rgba(0, 0, 0, 0.1), inset 0 1px 0 0 rgba(255, 255, 255, 0.5)',
    },
    card: {
      background: isDark
        ? `rgba(22, 27, 34, ${Math.min(opacity + 0.05, 1)})`
        : `rgba(255, 255, 255, ${Math.min(opacity + 0.05, 1)})`,
      border: isDark
        ? '1px solid rgba(255, 255, 255, 0.1)'
        : '1px solid rgba(255, 255, 255, 0.3)',
      boxShadow: isDark
        ? '0 8px 32px 0 rgba(0, 0, 0, 0.4), inset 0 1px 0 0 rgba(255, 255, 255, 0.1)'
        : '0 8px 32px 0 rgba(0, 0, 0, 0.1), inset 0 1px 0 0 rgba(255, 255, 255, 0.5)',
    },
    button: {
      background: isDark
        ? `rgba(22, 27, 34, ${opacity * 0.8})`
        : `rgba(255, 255, 255, ${opacity * 0.8})`,
      border: isDark
        ? '1px solid rgba(255, 255, 255, 0.1)'
        : '1px solid rgba(255, 255, 255, 0.3)',
      boxShadow: isDark
        ? '0 4px 16px 0 rgba(0, 0, 0, 0.4), inset 0 1px 0 0 rgba(255, 255, 255, 0.1)'
        : '0 4px 16px 0 rgba(0, 0, 0, 0.1), inset 0 1px 0 0 rgba(255, 255, 255, 0.5)',
    },
    nav: {
      background: isDark
        ? `rgba(10, 14, 39, ${Math.min(opacity + 0.1, 1)})`
        : `rgba(255, 255, 255, ${Math.min(opacity + 0.1, 1)})`,
      border: isDark
        ? '1px solid rgba(255, 255, 255, 0.1)'
        : '1px solid rgba(255, 255, 255, 0.3)',
      boxShadow: isDark
        ? '0 8px 32px 0 rgba(0, 0, 0, 0.4), inset 0 1px 0 0 rgba(255, 255, 255, 0.1)'
        : '0 8px 32px 0 rgba(0, 0, 0, 0.1), inset 0 1px 0 0 rgba(255, 255, 255, 0.5)',
    },
  };

  return {
    ...baseStyles,
    ...variantStyles[variant],
  };
};

/**
 * Calculate adaptive opacity based on scroll position
 * @param scrollY Current scroll position
 * @param maxScroll Maximum scroll position
 * @param minOpacity Minimum opacity (default 0.5)
 * @param maxOpacity Maximum opacity (default 0.9)
 * @returns Calculated opacity value
 */
export const calculateAdaptiveOpacity = (
  scrollY: number,
  maxScroll: number = 500,
  minOpacity: number = 0.5,
  maxOpacity: number = 0.9
): number => {
  const scrollRatio = Math.min(scrollY / maxScroll, 1);
  return minOpacity + (maxOpacity - minOpacity) * scrollRatio;
};

/**
 * Get focus ring color based on theme
 */
export const getFocusRingColor = (mode: ThemeMode): string => {
  return mode === 'dark' ? 'rgba(77, 171, 247, 0.8)' : 'rgba(25, 118, 210, 0.8)';
};

