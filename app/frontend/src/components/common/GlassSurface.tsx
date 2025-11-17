/** Reusable glass surface wrapper component with configurable props */
import React from 'react';
import { Box, BoxProps } from '@mui/material';
import { useThemeMode } from '../../contexts/ThemeContext';

export interface GlassSurfaceProps extends Omit<BoxProps, 'sx'> {
  /** Opacity level (0-1) */
  opacity?: number;
  /** Blur intensity in pixels */
  blur?: number;
  /** Border radius: 'sm' | 'md' | 'lg' | 'xl' */
  radius?: 'sm' | 'md' | 'lg' | 'xl';
  /** Variant: 'surface' | 'card' | 'button' | 'nav' */
  variant?: 'surface' | 'card' | 'button' | 'nav';
  /** Enable hover lensing effect */
  enableHover?: boolean;
  /** Children to render inside glass surface */
  children?: React.ReactNode;
}

const radiusMap = {
  sm: '8px',
  md: '12px',
  lg: '16px',
  xl: '24px',
};

export const GlassSurface: React.FC<GlassSurfaceProps> = ({
  opacity = 0.7,
  blur = 20,
  radius = 'md',
  variant = 'surface',
  enableHover = true,
  children,
  ...boxProps
}) => {
  const { mode } = useThemeMode();
  const isDark = mode === 'dark';

  // Base glass styles
  const baseStyles: React.CSSProperties = {
    backdropFilter: `blur(${blur}px) saturate(180%)`,
    WebkitBackdropFilter: `blur(${blur}px) saturate(180%)`,
    borderRadius: radiusMap[radius],
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  };

  // Variant-specific styles
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
      minHeight: '44px',
      minWidth: '44px',
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

  const hoverStyles = enableHover
    ? {
        '&:hover': {
          backdropFilter: `blur(${blur + 4}px) saturate(200%)`,
          WebkitBackdropFilter: `blur(${blur + 4}px) saturate(200%)`,
          transform: variant === 'button' ? 'translateY(-1px)' : 'translateY(-2px)',
          boxShadow: isDark
            ? '0 12px 48px 0 rgba(0, 0, 0, 0.5), inset 0 1px 0 0 rgba(255, 255, 255, 0.2)'
            : '0 12px 48px 0 rgba(0, 0, 0, 0.15), inset 0 1px 0 0 rgba(255, 255, 255, 0.6)',
        },
        '&:active': variant === 'button' ? { transform: 'translateY(0)' } : {},
      }
    : {};

  return (
    <Box
      {...boxProps}
      sx={{
        ...baseStyles,
        ...variantStyles[variant],
        ...hoverStyles,
        '&:focus-visible': {
          outline: `2px solid ${isDark ? 'rgba(77, 171, 247, 0.8)' : 'rgba(25, 118, 210, 0.8)'}`,
          outlineOffset: '2px',
        },
        ...boxProps.sx,
      }}
    >
      {children}
    </Box>
  );
};

