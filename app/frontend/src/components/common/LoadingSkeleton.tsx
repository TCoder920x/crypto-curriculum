/** Loading skeleton components matching glass aesthetic */
import React from 'react';
import { Box, Skeleton, SkeletonProps } from '@mui/material';
import { useThemeMode } from '../../contexts/ThemeContext';

export interface LoadingSkeletonProps extends SkeletonProps {
  variant?: 'text' | 'rectangular' | 'rounded' | 'circular';
  width?: number | string;
  height?: number | string;
  count?: number;
}

/** Single skeleton with glass effect */
export const GlassSkeleton: React.FC<LoadingSkeletonProps> = ({
  variant = 'rectangular',
  width,
  height,
  ...skeletonProps
}) => {
  const { mode } = useThemeMode();
  const isDark = mode === 'dark';

  return (
    <Skeleton
      variant={variant}
      width={width}
      height={height}
      sx={{
        bgcolor: isDark
          ? 'rgba(255, 255, 255, 0.05)'
          : 'rgba(0, 0, 0, 0.05)',
        borderRadius: variant === 'rounded' ? '12px' : variant === 'circular' ? '50%' : '8px',
        '&::after': {
          background: isDark
            ? 'linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent)'
            : 'linear-gradient(90deg, transparent, rgba(0, 0, 0, 0.1), transparent)',
        },
      }}
      {...skeletonProps}
    />
  );
};

/** Card skeleton */
export const CardSkeleton: React.FC<{ count?: number }> = ({ count = 1 }) => {
  return (
    <>
      {Array.from({ length: count }).map((_, index) => (
        <Box
          key={index}
          className="glass-card"
          sx={{
            p: 3,
            mb: 2,
            borderRadius: '16px',
          }}
        >
          <GlassSkeleton variant="rectangular" width="60%" height={24} sx={{ mb: 2 }} />
          <GlassSkeleton variant="rectangular" width="100%" height={16} sx={{ mb: 1 }} />
          <GlassSkeleton variant="rectangular" width="80%" height={16} />
        </Box>
      ))}
    </>
  );
};

/** List skeleton */
export const ListSkeleton: React.FC<{ count?: number; showAvatar?: boolean }> = ({
  count = 3,
  showAvatar = false,
}) => {
  return (
    <>
      {Array.from({ length: count }).map((_, index) => (
        <Box
          key={index}
          sx={{
            display: 'flex',
            alignItems: 'center',
            gap: 2,
            p: 2,
            mb: 1,
          }}
        >
          {showAvatar && (
            <GlassSkeleton variant="circular" width={40} height={40} />
          )}
          <Box sx={{ flexGrow: 1 }}>
            <GlassSkeleton variant="rectangular" width="40%" height={20} sx={{ mb: 1 }} />
            <GlassSkeleton variant="rectangular" width="60%" height={16} />
          </Box>
        </Box>
      ))}
    </>
  );
};

/** Table skeleton */
export const TableSkeleton: React.FC<{ rows?: number; columns?: number }> = ({
  rows = 5,
  columns = 4,
}) => {
  return (
    <Box className="glass-card" sx={{ p: 2, borderRadius: '16px' }}>
      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        {Array.from({ length: columns }).map((_, index) => (
          <GlassSkeleton key={index} variant="rectangular" width="100%" height={24} />
        ))}
      </Box>
      {Array.from({ length: rows }).map((_, rowIndex) => (
        <Box key={rowIndex} sx={{ display: 'flex', gap: 2, mb: 1 }}>
          {Array.from({ length: columns }).map((_, colIndex) => (
            <GlassSkeleton key={colIndex} variant="rectangular" width="100%" height={20} />
          ))}
        </Box>
      ))}
    </Box>
  );
};

/** Page skeleton - full page loading state */
export const PageSkeleton: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <GlassSkeleton variant="rectangular" width="40%" height={32} sx={{ mb: 3 }} />
      <CardSkeleton count={3} />
    </Box>
  );
};

