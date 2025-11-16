/** Reusable markdown renderer component with proper styling */
import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Box } from '@mui/material';
import { useThemeMode } from '../../contexts/ThemeContext';
import './MarkdownRenderer.css';

interface MarkdownRendererProps {
  content: string;
  className?: string;
}

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content, className = '' }) => {
  const { mode } = useThemeMode();

  // Ensure content is a string
  if (!content || typeof content !== 'string') {
    return null;
  }

  return (
    <Box
      className={`markdown-content ${className} ${mode === 'dark' ? 'markdown-dark' : 'markdown-light'}`}
      sx={{
        '& h1': {
          fontSize: '2rem',
          fontWeight: 'bold',
          marginTop: '1.5rem',
          marginBottom: '1rem',
          color: 'text.primary',
        },
        '& h2': {
          fontSize: '1.5rem',
          fontWeight: 'bold',
          marginTop: '1.25rem',
          marginBottom: '0.75rem',
          color: 'text.primary',
        },
        '& h3': {
          fontSize: '1.25rem',
          fontWeight: '600',
          marginTop: '1rem',
          marginBottom: '0.5rem',
          color: 'text.primary',
        },
        '& h4, & h5, & h6': {
          fontSize: '1rem',
          fontWeight: '600',
          marginTop: '0.75rem',
          marginBottom: '0.5rem',
          color: 'text.primary',
        },
        '& p': {
          marginBottom: '1rem',
          lineHeight: 1.6,
          color: 'text.primary',
        },
        '& ul, & ol': {
          marginBottom: '1rem',
          paddingLeft: '1.5rem',
          '& li': {
            marginBottom: '0.5rem',
            lineHeight: 1.6,
            color: 'text.primary',
          },
        },
        '& strong, & b': {
          fontWeight: 'bold',
          color: 'text.primary',
        },
        '& em, & i': {
          fontStyle: 'italic',
        },
        '& code': {
          backgroundColor: mode === 'light' ? 'rgba(0, 0, 0, 0.05)' : 'rgba(255, 255, 255, 0.1)',
          padding: '0.2rem 0.4rem',
          borderRadius: '0.25rem',
          fontSize: '0.9em',
          fontFamily: 'monospace',
          color: mode === 'light' ? '#d63384' : '#ff6b9d',
        },
        '& pre': {
          backgroundColor: mode === 'light' ? 'rgba(0, 0, 0, 0.05)' : 'rgba(255, 255, 255, 0.05)',
          padding: '1rem',
          borderRadius: '0.5rem',
          overflow: 'auto',
          marginBottom: '1rem',
          '& code': {
            backgroundColor: 'transparent',
            padding: 0,
          },
        },
        '& blockquote': {
          borderLeft: `4px solid ${mode === 'light' ? '#1976d2' : '#64b5f6'}`,
          paddingLeft: '1rem',
          marginLeft: 0,
          marginBottom: '1rem',
          fontStyle: 'italic',
          color: mode === 'light' ? 'rgba(0, 0, 0, 0.7)' : 'rgba(255, 255, 255, 0.7)',
        },
        '& a': {
          color: mode === 'light' ? '#1976d2' : '#64b5f6',
          textDecoration: 'none',
          '&:hover': {
            textDecoration: 'underline',
          },
        },
        '& hr': {
          border: 'none',
          borderTop: `1px solid ${mode === 'light' ? 'rgba(0, 0, 0, 0.1)' : 'rgba(255, 255, 255, 0.2)'}`,
          margin: '1.5rem 0',
        },
        '& table': {
          width: '100%',
          borderCollapse: 'collapse',
          marginBottom: '1rem',
          borderRadius: '0.5rem',
          border: `1px solid ${mode === 'light' ? 'rgba(0, 0, 0, 0.1)' : 'rgba(255, 255, 255, 0.2)'}`,
          tableLayout: 'auto',
          wordWrap: 'break-word',
          overflowWrap: 'break-word',
        },
        '& thead': {
          backgroundColor: mode === 'light' ? 'rgba(0, 0, 0, 0.05)' : 'rgba(255, 255, 255, 0.1)',
        },
        '& th': {
          padding: '0.75rem',
          textAlign: 'left',
          fontWeight: '600',
          borderBottom: `2px solid ${mode === 'light' ? 'rgba(0, 0, 0, 0.1)' : 'rgba(255, 255, 255, 0.2)'}`,
          color: 'text.primary',
          wordWrap: 'break-word',
          overflowWrap: 'break-word',
          whiteSpace: 'normal',
        },
        '& td': {
          padding: '0.75rem',
          borderBottom: `1px solid ${mode === 'light' ? 'rgba(0, 0, 0, 0.05)' : 'rgba(255, 255, 255, 0.1)'}`,
          color: 'text.primary',
          wordWrap: 'break-word',
          overflowWrap: 'break-word',
          whiteSpace: 'normal',
          verticalAlign: 'top',
        },
        '& tr:last-child td': {
          borderBottom: 'none',
        },
        '& tr:hover': {
          backgroundColor: mode === 'light' ? 'rgba(0, 0, 0, 0.02)' : 'rgba(255, 255, 255, 0.05)',
        },
      }}
    >
      <ReactMarkdown 
        remarkPlugins={[remarkGfm]}
        components={{
          p: ({ children }) => <p style={{ margin: 0, marginBottom: '0.5rem' }}>{children}</p>,
          strong: ({ children }) => <strong style={{ fontWeight: 'bold' }}>{children}</strong>,
          em: ({ children }) => <em style={{ fontStyle: 'italic' }}>{children}</em>,
        }}
      >
        {content}
      </ReactMarkdown>
    </Box>
  );
};

