import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import type { Components } from 'react-markdown';

interface TokenFadeTyperProps {
  text: string;
  isStreaming?: boolean;
  components?: Components;
}

export const TokenFadeTyper: React.FC<TokenFadeTyperProps> = ({ text, isStreaming, components }) => {
  return (
    <div className="prose prose-sm max-w-none dark:prose-invert">
      <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
        {text}
      </ReactMarkdown>
      {isStreaming && <span className="ml-1 inline-block h-4 w-2 animate-pulse rounded bg-blue-500" />}
    </div>
  );
};
