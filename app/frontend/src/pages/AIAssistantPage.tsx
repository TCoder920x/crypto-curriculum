/** AI Assistant page */
import React, { useState } from 'react';
import { Box, useTheme, useMediaQuery } from '@mui/material';
import { ChatInterface } from '../components/ai/ChatInterface';
import { ConversationSidebar } from '../components/ai/ConversationSidebar';

export const AIAssistantPage: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [selectedConversationId, setSelectedConversationId] = useState<number | null>(null);

  const handleSelectConversation = (conversationId: number | null) => {
    setSelectedConversationId(conversationId);
  };

  const handleNewConversation = () => {
    setSelectedConversationId(null);
  };

  return (
    <Box
      sx={{
        height: 'calc(100vh - 64px)', // Adjust for app bar height
        width: '100%',
        display: 'flex',
        flexDirection: { xs: 'column', md: 'row' },
        overflow: 'hidden',
      }}
    >
      {/* Sidebar - Always visible on desktop, can be toggled on mobile */}
      <Box
        sx={{
          width: { xs: '100%', md: 300 },
          height: { xs: 'auto', md: '100%' },
          flexShrink: 0,
          borderRight: { md: 1 },
          borderColor: { md: 'divider' },
        }}
      >
        <ConversationSidebar
          selectedConversationId={selectedConversationId}
          onSelectConversation={handleSelectConversation}
          onNewConversation={handleNewConversation}
        />
      </Box>

      {/* Chat Interface */}
      <Box
        sx={{
          flexGrow: 1,
          height: { xs: 'calc(100vh - 64px - 200px)', md: '100%' },
          display: 'flex',
          flexDirection: 'column',
          minWidth: 0, // Prevent overflow
          overflow: 'hidden',
        }}
      >
        <ChatInterface
          conversationId={selectedConversationId}
          onConversationChange={handleSelectConversation}
        />
      </Box>
    </Box>
  );
};
