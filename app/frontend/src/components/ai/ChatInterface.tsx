/** AI Chat Interface component */
import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  TextField,
  IconButton,
  Typography,
  CircularProgress,
  Alert,
  Avatar,
  Paper,
  IconButton as MuiIconButton,
  Tooltip,
} from '@mui/material';
import { Send, SmartToy, Delete, Edit } from '@mui/icons-material';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  aiAssistantService,
  type ChatMessage,
} from '../../services/aiAssistantService';
import { useAuth } from '../../contexts/AuthContext';

interface ChatInterfaceProps {
  moduleId?: number;
  lessonId?: number;
  conversationId?: number | null;
  onConversationChange?: (conversationId: number | null) => void;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  moduleId,
  lessonId,
  conversationId: propConversationId,
  onConversationChange,
}) => {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [message, setMessage] = useState('');
  const [currentConversationId, setCurrentConversationId] = useState<number | null>(
    propConversationId || null
  );
  const [streamingResponse, setStreamingResponse] = useState<string>('');
  const [isStreaming, setIsStreaming] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  // Update local conversation ID when prop changes
  useEffect(() => {
    if (propConversationId !== undefined) {
      setCurrentConversationId(propConversationId);
    }
  }, [propConversationId]);

  // Load conversation messages when conversation changes
  const { data: conversationData, isLoading: isLoadingConversation } = useQuery({
    queryKey: ['ai-conversation', currentConversationId],
    queryFn: () => {
      if (!currentConversationId) return null;
      return aiAssistantService.getConversation(currentConversationId);
    },
    enabled: !!currentConversationId && !!user,
  });

  // Fallback to history if no conversation selected
  const { data: chatHistory } = useQuery({
    queryKey: ['ai-chat-history', currentConversationId],
    queryFn: () =>
      aiAssistantService.getHistory(50, currentConversationId || undefined),
    enabled: !currentConversationId && !!user,
  });

  const sendMutation = useMutation({
    mutationFn: (messageText: string) =>
      aiAssistantService.sendMessage({
        message: messageText,
        conversation_id: currentConversationId,
        context: moduleId
          ? { current_module_id: moduleId, current_lesson_id: lessonId }
          : undefined,
      }),
    onSuccess: (data) => {
      // Update conversation ID if it was generated
      if (data.conversation_id && data.conversation_id !== currentConversationId) {
        setCurrentConversationId(data.conversation_id);
        onConversationChange?.(data.conversation_id);
      }
      queryClient.invalidateQueries({ queryKey: ['ai-chat-history'] });
      queryClient.invalidateQueries({ queryKey: ['ai-conversation'] });
      queryClient.invalidateQueries({ queryKey: ['ai-conversations'] });
      setMessage('');
    },
  });

  const streamMutation = useMutation({
    mutationFn: async (messageText: string) => {
      setIsStreaming(true);
      setStreamingResponse('');
      let newConversationId = currentConversationId;

      try {
        for await (const chunk of aiAssistantService.sendMessageStream({
          message: messageText,
          conversation_id: currentConversationId,
          context: moduleId
            ? { current_module_id: moduleId, current_lesson_id: lessonId }
            : undefined,
        })) {
          if (chunk.type === 'conversation_id' && chunk.conversation_id) {
            newConversationId = chunk.conversation_id;
            setCurrentConversationId(newConversationId);
            onConversationChange?.(newConversationId);
          } else if (chunk.type === 'chunk' && chunk.content) {
            setStreamingResponse((prev) => prev + chunk.content);
          } else if (chunk.type === 'error') {
            throw new Error(chunk.message || 'Streaming error');
          } else if (chunk.type === 'done') {
            // Invalidate queries to refresh data
            queryClient.invalidateQueries({ queryKey: ['ai-chat-history'] });
            queryClient.invalidateQueries({ queryKey: ['ai-conversation'] });
            queryClient.invalidateQueries({ queryKey: ['ai-conversations'] });
          }
        }
      } finally {
        setIsStreaming(false);
        setStreamingResponse('');
      }

      return newConversationId;
    },
  });

  useEffect(() => {
    scrollToBottom();
  }, [conversationData, chatHistory, streamingResponse]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim() || sendMutation.isPending || streamMutation.isPending) return;

    // Use streaming by default
    streamMutation.mutate(message.trim());
    setMessage('');
  };

  if (!user) {
    return (
      <Alert severity="info">Please log in to use the AI assistant.</Alert>
    );
  }

  // Get messages from conversation or history
  const messages: ChatMessage[] = currentConversationId
    ? conversationData?.messages || []
    : chatHistory?.messages || [];

  const conversationTitle = conversationData?.title;

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      {currentConversationId && (
        <Box
          sx={{
            p: 1.5,
            borderBottom: 1,
            borderColor: 'divider',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            bgcolor: 'background.paper',
          }}
        >
          <Typography variant="subtitle1" sx={{ fontWeight: 500 }}>
            {conversationTitle || 'Conversation'}
          </Typography>
          <Box sx={{ display: 'flex', gap: 0.5 }}>
            <Tooltip title="Delete conversation">
              <MuiIconButton size="small" onClick={() => onConversationChange?.(null)}>
                <Delete fontSize="small" />
              </MuiIconButton>
            </Tooltip>
          </Box>
        </Box>
      )}

      {/* Messages */}
      <Box
        ref={chatContainerRef}
        sx={{
          flexGrow: 1,
          overflow: 'auto',
          p: 2,
          display: 'flex',
          flexDirection: 'column',
          gap: 2,
        }}
      >
        {isLoadingConversation ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
            <CircularProgress />
          </Box>
        ) : messages.length === 0 && !isStreaming ? (
          <Box sx={{ textAlign: 'center', mt: 4 }}>
            <SmartToy sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
            <Typography variant="body1" color="text.secondary">
              Start a conversation! Ask me about blockchain concepts, definitions, or how
              things work.
            </Typography>
          </Box>
        ) : (
          <>
        {messages.map((msg) => (
          <Box
            key={msg.id}
            sx={{
              display: 'flex',
              gap: 1,
              flexDirection: msg.user_id === user.id ? 'row-reverse' : 'row',
            }}
          >
            <Avatar sx={{ width: 32, height: 32 }}>
                  {msg.user_id === user.id
                    ? user.email?.[0].toUpperCase()
                    : 'AI'}
            </Avatar>
            <Box
              sx={{
                maxWidth: '70%',
                    bgcolor:
                      msg.user_id === user.id ? 'primary.main' : 'grey.200',
                color: msg.user_id === user.id ? 'white' : 'text.primary',
                p: 1.5,
                borderRadius: 2,
              }}
            >
              <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                {msg.message}
              </Typography>
              {msg.response && (
                    <Box
                      sx={{
                        mt: 1,
                        pt: 1,
                        borderTop: 1,
                        borderColor: 'rgba(255,255,255,0.2)',
                      }}
                    >
                  <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                    {msg.response}
                  </Typography>
                </Box>
              )}
            </Box>
          </Box>
        ))}

            {/* Streaming response */}
            {isStreaming && (
              <Box sx={{ display: 'flex', gap: 1 }}>
            <Avatar sx={{ width: 32, height: 32 }}>AI</Avatar>
                <Box
                  sx={{
                    maxWidth: '70%',
                    bgcolor: 'grey.200',
                    color: 'text.primary',
                    p: 1.5,
                    borderRadius: 2,
                  }}
                >
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
              <CircularProgress size={16} />
                    <Typography variant="caption" color="text.secondary">
                Thinking...
              </Typography>
                  </Box>
                  {streamingResponse && (
                    <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                      {streamingResponse}
                    </Typography>
                  )}
            </Box>
          </Box>
        )}

            {streamMutation.isError && (
          <Alert severity="error" sx={{ mt: 1 }}>
                {streamMutation.error instanceof Error
                  ? streamMutation.error.message
              : 'Failed to send message. Please try again.'}
          </Alert>
            )}
          </>
        )}

        <div ref={messagesEndRef} />
      </Box>

      {/* Input */}
      <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
        <form onSubmit={handleSubmit}>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              fullWidth
              size="small"
              placeholder="Ask a question about the curriculum..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              disabled={sendMutation.isPending || streamMutation.isPending}
            />
            <IconButton
              type="submit"
              color="primary"
              disabled={!message.trim() || sendMutation.isPending || streamMutation.isPending}
            >
              <Send />
            </IconButton>
          </Box>
        </form>
      </Box>
    </Box>
  );
};
