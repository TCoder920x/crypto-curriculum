/** Conversation Sidebar component for managing chat conversations */
import React, { useState } from 'react';
import {
  Box,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Typography,
  IconButton,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Divider,
  CircularProgress,
  Tooltip,
} from '@mui/material';
import {
  Add,
  Delete,
  Edit,
  Chat as ChatIcon,
} from '@mui/icons-material';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  aiAssistantService,
  type Conversation,
} from '../../services/aiAssistantService';
// Simple date formatter
const formatTimeAgo = (dateString: string): string => {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return 'just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  return date.toLocaleDateString();
};

interface ConversationSidebarProps {
  selectedConversationId: number | null;
  onSelectConversation: (conversationId: number | null) => void;
  onNewConversation: () => void;
}

export const ConversationSidebar: React.FC<ConversationSidebarProps> = ({
  selectedConversationId,
  onSelectConversation,
  onNewConversation,
}) => {
  const queryClient = useQueryClient();
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [conversationToDelete, setConversationToDelete] = useState<number | null>(null);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [conversationToEdit, setConversationToEdit] = useState<Conversation | null>(null);
  const [editTitle, setEditTitle] = useState('');

  const { data: conversationsData, isLoading } = useQuery({
    queryKey: ['ai-conversations'],
    queryFn: () => aiAssistantService.getConversations(50),
  });

  const deleteMutation = useMutation({
    mutationFn: (conversationId: number) =>
      aiAssistantService.deleteConversation(conversationId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ai-conversations'] });
      queryClient.invalidateQueries({ queryKey: ['ai-chat-history'] });
      if (selectedConversationId === conversationToDelete) {
        onSelectConversation(null);
      }
      setDeleteDialogOpen(false);
      setConversationToDelete(null);
    },
  });

  const updateTitleMutation = useMutation({
    mutationFn: ({ conversationId, title }: { conversationId: number; title: string }) =>
      aiAssistantService.updateConversationTitle(conversationId, title),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ai-conversations'] });
      setEditDialogOpen(false);
      setConversationToEdit(null);
      setEditTitle('');
    },
  });

  const handleDeleteClick = (e: React.MouseEvent, conversationId: number) => {
    e.stopPropagation();
    setConversationToDelete(conversationId);
    setDeleteDialogOpen(true);
  };

  const handleEditClick = (e: React.MouseEvent, conversation: Conversation) => {
    e.stopPropagation();
    setConversationToEdit(conversation);
    setEditTitle(conversation.title || '');
    setEditDialogOpen(true);
  };

  const handleDeleteConfirm = () => {
    if (conversationToDelete) {
      deleteMutation.mutate(conversationToDelete);
    }
  };

  const handleEditSave = () => {
    if (conversationToEdit && editTitle.trim()) {
      updateTitleMutation.mutate({
        conversationId: conversationToEdit.conversation_id,
        title: editTitle.trim(),
      });
    }
  };

  const conversations = conversationsData?.conversations || [];

  return (
    <>
      <Box
        sx={{
          width: 300,
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          borderRight: 1,
          borderColor: 'divider',
          bgcolor: 'background.paper',
        }}
      >
        {/* Header */}
        <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1 }}>
            <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <ChatIcon fontSize="small" />
              Conversations
            </Typography>
          </Box>
          <Button
            fullWidth
            variant="contained"
            startIcon={<Add />}
            onClick={onNewConversation}
            size="small"
          >
            New Chat
          </Button>
        </Box>

        {/* Conversations List */}
        <Box sx={{ flexGrow: 1, overflow: 'auto' }}>
          {isLoading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
              <CircularProgress size={24} />
            </Box>
          ) : conversations.length === 0 ? (
            <Box sx={{ p: 3, textAlign: 'center' }}>
              <Typography variant="body2" color="text.secondary">
                No conversations yet. Start a new chat!
              </Typography>
            </Box>
          ) : (
            <List dense>
              {conversations.map((conversation) => (
                <ListItem
                  key={conversation.conversation_id}
                  disablePadding
                  sx={{
                    bgcolor:
                      selectedConversationId === conversation.conversation_id
                        ? 'action.selected'
                        : 'transparent',
                  }}
                >
                  <ListItemButton
                    onClick={() => onSelectConversation(conversation.conversation_id)}
                    sx={{
                      '&:hover .conversation-actions': {
                        opacity: 1,
                      },
                    }}
                  >
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Typography
                            variant="body2"
                            sx={{
                              flexGrow: 1,
                              overflow: 'hidden',
                              textOverflow: 'ellipsis',
                              whiteSpace: 'nowrap',
                            }}
                          >
                            {conversation.title || 'New Conversation'}
                          </Typography>
                          <Box
                            className="conversation-actions"
                            sx={{
                              display: 'flex',
                              gap: 0.5,
                              opacity: 0,
                              transition: 'opacity 0.2s',
                            }}
                          >
                            <Tooltip title="Edit title">
                              <IconButton
                                size="small"
                                onClick={(e) => handleEditClick(e, conversation)}
                                sx={{ p: 0.5 }}
                              >
                                <Edit fontSize="small" />
                              </IconButton>
                            </Tooltip>
                            <Tooltip title="Delete">
                              <IconButton
                                size="small"
                                onClick={(e) => handleDeleteClick(e, conversation.conversation_id)}
                                sx={{ p: 0.5 }}
                              >
                                <Delete fontSize="small" />
                              </IconButton>
                            </Tooltip>
                          </Box>
                        </Box>
                      }
                      secondary={
                        <Typography variant="caption" color="text.secondary">
                          {conversation.last_message_at
                            ? formatTimeAgo(conversation.last_message_at)
                            : 'No messages'}
                          {' • '}
                          {conversation.message_count} message{conversation.message_count !== 1 ? 's' : ''}
                        </Typography>
                      }
                    />
                  </ListItemButton>
                </ListItem>
              ))}
            </List>
          )}
        </Box>
      </Box>

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Delete Conversation?</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete this conversation? This action cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={handleDeleteConfirm}
            color="error"
            variant="contained"
            disabled={deleteMutation.isPending}
          >
            {deleteMutation.isPending ? <CircularProgress size={20} /> : 'Delete'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Edit Title Dialog */}
      <Dialog open={editDialogOpen} onClose={() => setEditDialogOpen(false)}>
        <DialogTitle>Edit Conversation Title</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Title"
            fullWidth
            variant="outlined"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter' && editTitle.trim()) {
                handleEditSave();
              }
            }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={handleEditSave}
            variant="contained"
            disabled={!editTitle.trim() || updateTitleMutation.isPending}
          >
            {updateTitleMutation.isPending ? <CircularProgress size={20} /> : 'Save'}
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

