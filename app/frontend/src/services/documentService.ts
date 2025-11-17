import { apiClient } from './api';

export interface ReferenceDocument {
  id: number;
  title: string;
  category: 'standard' | 'user-upload' | 'policy' | string;
  updated_at: string;
  tags?: string[];
  owner?: string;
  type?: string;
}

class DocumentService {
  private cache: ReferenceDocument[] | null = null;
  private lastFetchedAt: number | null = null;
  private readonly ttl = 1000 * 60 * 5; // five minutes

  async listDocuments(force = false): Promise<ReferenceDocument[]> {
    const now = Date.now();

    if (!force && this.cache && this.lastFetchedAt && now - this.lastFetchedAt < this.ttl) {
      return this.cache;
    }

    const response = await apiClient.get('/documents/list');
    this.cache = response.data?.documents ?? response.data ?? [];
    this.lastFetchedAt = now;
    return this.cache;
  }

  openDocumentInNewTab(documentId: number): void {
    const token = localStorage.getItem('access_token');
    const url = `${apiClient.defaults.baseURL}/documents/download/${documentId}` + (token ? `?token=${token}` : '');
    window.open(url, '_blank', 'noopener');
  }
}

export const documentService = new DocumentService();
