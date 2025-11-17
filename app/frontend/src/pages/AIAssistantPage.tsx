import React, { Fragment, useEffect, useMemo, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { CSSTransition, TransitionGroup } from 'react-transition-group';
import { FileOpen, UploadFile } from '@mui/icons-material';
import { AIChat } from '../components/ai/AIChat';
import { ConversationSidebar } from '../components/ai/ConversationSidebar';
import { documentService, type ReferenceDocument } from '../services/documentService';

interface LocationState {
  initialQuery?: string;
  conversationId?: number;
}

const groupDocuments = (documents: ReferenceDocument[]) => {
  const standard = documents.filter((doc) => doc.category !== 'user-upload');
  const uploads = documents.filter((doc) => doc.category === 'user-upload');
  return { standard, uploads };
};

export const AIAssistantPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const locationState = (location.state as LocationState) || {};
  const [documents, setDocuments] = useState<ReferenceDocument[]>([]);
  const [isLoadingDocs, setIsLoadingDocs] = useState(false);
  const [docError, setDocError] = useState<string | null>(null);
  const [selectedConversationId, setSelectedConversationId] = useState<number | null>(
    locationState.conversationId ?? null
  );

  useEffect(() => {
    let mounted = true;
    const loadDocs = async () => {
      setIsLoadingDocs(true);
      try {
        const list = await documentService.listDocuments();
        if (mounted) {
          setDocuments(list);
        }
      } catch (error) {
        setDocError('Unable to load reference documents.');
      } finally {
        setIsLoadingDocs(false);
      }
    };
    loadDocs();
    return () => {
      mounted = false;
    };
  }, []);

  const groupedDocs = useMemo(() => groupDocuments(documents), [documents]);

  const renderDocumentCard = (doc: ReferenceDocument) => (
    <div
      key={doc.id}
      className="rounded-2xl border border-white/30 bg-white/20 p-4 text-sm shadow-lg backdrop-blur-xl dark:border-slate-700 dark:bg-slate-800/60"
    >
      <p className="text-sm font-semibold text-slate-900 dark:text-white">{doc.title}</p>
      <p className="mt-1 text-[11px] uppercase tracking-wide text-slate-500">
        {doc.category === 'user-upload' ? 'User Upload' : doc.category}
      </p>
      <p className="mt-1 text-xs text-slate-500">Updated {new Date(doc.updated_at).toLocaleDateString()}</p>
      <button
        className="mt-3 inline-flex items-center gap-2 rounded-full border border-slate-300/70 px-3 py-1 text-xs font-semibold text-slate-600 transition hover:bg-white/70 dark:border-slate-600 dark:text-slate-200"
        onClick={() => documentService.openDocumentInNewTab(doc.id)}
      >
        <FileOpen fontSize="inherit" /> View
      </button>
    </div>
  );

  return (
    <div className="relative h-[calc(100vh-4rem)] w-full overflow-hidden px-4 pb-6 pt-2">
      <div className="absolute inset-0 -z-10 bg-gradient-to-br from-indigo-100/70 via-white to-blue-50 dark:from-slate-900 dark:via-slate-950 dark:to-blue-950" />
      <div className="mx-auto flex h-full max-w-6xl flex-col">
        <div className="mb-4 flex flex-col gap-2 rounded-3xl border border-white/50 bg-white/70 px-6 py-4 backdrop-blur-xl dark:border-slate-700 dark:bg-slate-900/60">
          <p className="text-sm font-semibold uppercase tracking-wide text-slate-500">Learning workspace</p>
          <h1 className="text-2xl font-semibold text-slate-900 dark:text-white">AI Reference Studio</h1>
          <p className="text-sm text-slate-600 dark:text-slate-300">
            Collect study guides, attach module notes, and explore AI answers with inline citations.
          </p>
        </div>
        <div className="grid flex-1 grid-cols-1 gap-6 overflow-hidden md:grid-cols-3">
          <div className="flex flex-col rounded-3xl border border-white/40 bg-white/65 p-4 backdrop-blur-xl dark:border-slate-800 dark:bg-slate-900/60">
            <div className="flex items-center justify-between">
              <p className="text-sm font-semibold text-slate-700 dark:text-slate-200">Reference documents</p>
              <button className="inline-flex items-center gap-1 rounded-full border border-slate-200/80 px-3 py-1 text-xs font-semibold text-slate-600 transition hover:bg-white/80 dark:border-slate-700 dark:text-slate-300">
                <UploadFile fontSize="inherit" /> Upload
              </button>
            </div>
            {docError && <p className="mt-3 text-xs text-red-500">{docError}</p>}
            <div className="mt-4 max-h-[200px] overflow-y-auto pr-1">
              {isLoadingDocs ? (
                <p className="text-xs text-slate-500">Loading documents…</p>
              ) : (
                <TransitionGroup component={null}>
                  {[{ title: 'Standard Library', data: groupedDocs.standard }, { title: 'User Uploads', data: groupedDocs.uploads }].map(
                    (section) => (
                      <CSSTransition key={section.title} timeout={250} classNames="fade">
                        <Fragment>
                          <p className="mb-2 text-[11px] font-semibold uppercase tracking-wide text-slate-500">
                            {section.title}
                          </p>
                          <div className="mb-4 space-y-3">
                            {section.data.length === 0 ? (
                              <p className="text-xs text-slate-400">No documents yet.</p>
                            ) : (
                              section.data.map(renderDocumentCard)
                            )}
                          </div>
                        </Fragment>
                      </CSSTransition>
                    ),
                  )}
                </TransitionGroup>
              )}
            </div>
            <div className="mt-6 border-t border-slate-200/50 pt-4 dark:border-slate-700">
              <div className="flex h-[400px] flex-col overflow-hidden">
                <ConversationSidebar
                  selectedConversationId={selectedConversationId}
                  onSelectConversation={(id) => {
                    setSelectedConversationId(id);
                  }}
                  onNewConversation={() => {
                    setSelectedConversationId(null);
                  }}
                />
              </div>
            </div>
          </div>
          <div className="md:col-span-2">
            <AIChat
              className="h-full"
              initialQuery={locationState.initialQuery}
              initialConversationIdProp={selectedConversationId}
              navigateTo={navigate}
              onConversationChange={(id) => {
                setSelectedConversationId(id);
              }}
        />
          </div>
        </div>
      </div>
    </div>
  );
};
