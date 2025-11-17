/** AI Assistant service for API calls */
import { apiClient } from './api';

export interface ChatMessage {
  id: number;
  user_id: number;
  message: string;
  response: string | null;
  context: Record<string, any> | null;
  suggested_lessons: number[] | null;
  escalated: boolean;
  conversation_id: number | null;
  created_at: string;
}

export interface ChatHistoryResponse {
  messages: ChatMessage[];
  total: number;
}

export interface ChatMessageCreate {
  message: string;
  conversation_id?: number | null;
  context?: Record<string, any> | null;
}

export interface Conversation {
  conversation_id: number;
  title: string | null;
  last_message_at: string | null;
  message_count: number;
  created_at: string;
}

export interface ConversationListResponse {
  conversations: Conversation[];
  total: number;
}

export interface ConversationDetail {
  conversation_id: number;
  title: string | null;
  created_at: string;
  last_message_at: string | null;
  message_count: number;
  messages: ChatMessage[];
}

export interface ConversationTitleUpdate {
  title: string;
}

export const aiAssistantService = {
  /** Send a message to the AI assistant (non-streaming) */
  sendMessage: async (messageData: ChatMessageCreate): Promise<ChatMessage> => {
    const response = await apiClient.post('/chat', messageData);
    return response.data;
  },

  /** Send a message with streaming response */
  sendMessageStream: async function* (
    messageData: ChatMessageCreate
  ): AsyncGenerator<{ type: string; content?: string; conversation_id?: number; message?: string }, void, unknown> {
    // Get token from localStorage
    const token = localStorage.getItem('access_token');
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${apiClient.defaults.baseURL}/chat/stream`, {
      method: 'POST',
      headers,
      body: JSON.stringify(messageData),
    });

    if (!response.ok) {
      throw new Error(`Stream request failed: ${response.statusText}`);
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('No response body reader available');
    }

    const decoder = new TextDecoder();
    let buffer = '';

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              yield data;
            } catch (e) {
              console.error('Error parsing SSE data:', e);
            }
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
  },

  /** Get chat history */
  getHistory: async (limit: number = 50, conversationId?: number): Promise<ChatHistoryResponse> => {
    const params: any = { limit };
    if (conversationId) {
      params.conversation_id = conversationId;
    }
    const response = await apiClient.get('/chat/history', { params });
    return response.data;
  },

  /** Get list of all conversations */
  getConversations: async (limit: number = 50, offset: number = 0): Promise<ConversationListResponse> => {
    const response = await apiClient.get('/conversations', {
      params: { limit, offset },
    });
    return response.data;
  },

  /** Get conversation details with messages */
  getConversation: async (conversationId: number): Promise<ConversationDetail> => {
    const response = await apiClient.get(`/conversations/${conversationId}`);
    return response.data;
  },

  /** Delete a conversation */
  deleteConversation: async (conversationId: number): Promise<void> => {
    await apiClient.delete(`/conversations/${conversationId}`);
  },

  /** Update conversation title */
  updateConversationTitle: async (
    conversationId: number,
    title: string
  ): Promise<Conversation> => {
    const response = await apiClient.patch(`/conversations/${conversationId}/title`, {
      title,
    });
    return response.data;
  },
};
