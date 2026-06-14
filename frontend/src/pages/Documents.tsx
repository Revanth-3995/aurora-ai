import React, { useState, useRef } from 'react';
import { Upload, FileText, Send, Bot, User, Loader2, AlertCircle, CheckCircle2 } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { uploadDocument, askDocument } from '../services/api';
import ReactMarkdown from 'react-markdown';
import { motion, AnimatePresence } from 'framer-motion';

export default function Documents() {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [uploadMessage, setUploadMessage] = useState('');

  const [question, setQuestion] = useState('');
  const [isAsking, setIsAsking] = useState(false);
  const [chatHistory, setChatHistory] = useState<Array<{role: 'user'|'assistant', text: string}>>([]);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setUploadStatus('idle');
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setIsUploading(true);
    setUploadStatus('idle');

    try {
      const res = await uploadDocument(file);
      setUploadStatus('success');
      setUploadMessage(res.status);
    } catch (err: any) {
      setUploadStatus('error');
      setUploadMessage(err.response?.data?.detail || "Upload failed");
    } finally {
      setIsUploading(false);
    }
  };

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || isAsking) return;

    const currentQ = question;
    setChatHistory(prev => [...prev, { role: 'user', text: currentQ }]);
    setQuestion('');
    setIsAsking(true);

    try {
      const res = await askDocument(currentQ);
      setChatHistory(prev => [...prev, { role: 'assistant', text: res.answer }]);
    } catch (err: any) {
      setChatHistory(prev => [...prev, { role: 'assistant', text: err.response?.data?.detail || "Error querying documents." }]);
    } finally {
      setIsAsking(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto h-full flex gap-6">

      {/* Upload Panel */}
      <div className="w-1/3 flex flex-col gap-6">
        <div className="flex flex-col gap-2">
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <FileText className="h-6 w-6 text-emerald-400" />
            Document Base
          </h2>
          <p className="text-sm text-slate-400">Upload PDFs to augment the agent's knowledge.</p>
        </div>

        <Card className="flex flex-col gap-4">
          <h3 className="font-semibold text-white">Upload New Document</h3>

          <div
            className={`border-2 border-dashed rounded-xl p-6 flex flex-col items-center justify-center text-center transition-colors cursor-pointer
              ${file ? 'border-emerald-500/50 bg-emerald-500/5' : 'border-slate-700 bg-slate-800/50 hover:bg-slate-800 hover:border-slate-600'}`}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              type="file"
              accept=".pdf"
              className="hidden"
              ref={fileInputRef}
              onChange={handleFileSelect}
            />
            <Upload className={`h-10 w-10 mb-3 ${file ? 'text-emerald-400' : 'text-slate-500'}`} />

            {file ? (
              <div>
                <p className="text-sm font-medium text-slate-200">{file.name}</p>
                <p className="text-xs text-slate-500 mt-1">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
              </div>
            ) : (
              <div>
                <p className="text-sm font-medium text-slate-300">Click to browse or drag and drop</p>
                <p className="text-xs text-slate-500 mt-1">PDF documents only</p>
              </div>
            )}
          </div>

          <Button
            className="w-full bg-emerald-600 hover:bg-emerald-700 text-white"
            disabled={!file || isUploading}
            onClick={handleUpload}
          >
            {isUploading ? <Loader2 className="h-5 w-5 animate-spin mr-2" /> : null}
            {isUploading ? 'Ingesting to FAISS...' : 'Upload & Process'}
          </Button>

          <AnimatePresence>
            {uploadStatus !== 'idle' && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className={`p-3 rounded-lg flex items-center gap-2 text-sm ${
                  uploadStatus === 'success' ? 'bg-emerald-900/30 text-emerald-400 border border-emerald-800/50' : 'bg-red-900/30 text-red-400 border border-red-800/50'
                }`}
              >
                {uploadStatus === 'success' ? <CheckCircle2 className="h-4 w-4 shrink-0" /> : <AlertCircle className="h-4 w-4 shrink-0" />}
                {uploadMessage}
              </motion.div>
            )}
          </AnimatePresence>
        </Card>
      </div>

      {/* Chat Interface */}
      <Card className="flex-1 flex flex-col p-0 overflow-hidden bg-slate-900/50">
        <div className="p-4 border-b border-slate-800 bg-slate-900/80 shrink-0">
          <h3 className="font-semibold text-white">Document Q&A</h3>
          <p className="text-xs text-slate-400 mt-1">Ask questions about the ingested context.</p>
        </div>

        <div className="flex-1 overflow-y-auto p-6 flex flex-col gap-6">
          {chatHistory.length === 0 ? (
             <div className="flex flex-col items-center justify-center h-full text-slate-500 gap-4">
               <FileText className="h-12 w-12 text-slate-700" />
               <p className="text-center max-w-sm">Upload a document on the left, then ask questions about its contents here.</p>
             </div>
          ) : (
            chatHistory.map((msg, i) => (
              <div key={i} className={`flex gap-4 max-w-[90%] ${msg.role === 'user' ? 'ml-auto flex-row-reverse' : ''}`}>
                 <div className={`shrink-0 h-8 w-8 rounded-full flex items-center justify-center ${
                    msg.role === 'user' ? 'bg-emerald-600' : 'bg-slate-800 border border-slate-700 text-emerald-400'
                  }`}>
                    {msg.role === 'user' ? <User size={14} /> : <Bot size={14} />}
                  </div>

                  <div className={`px-4 py-3 rounded-2xl ${
                      msg.role === 'user'
                        ? 'bg-emerald-600 text-white rounded-tr-none'
                        : 'bg-slate-800 border border-slate-700 text-slate-200 rounded-tl-none prose prose-invert max-w-none'
                    }`}>
                      {msg.role === 'assistant' ? (
                        <ReactMarkdown>{msg.text}</ReactMarkdown>
                      ) : (
                        msg.text
                      )}
                  </div>
              </div>
            ))
          )}

          {isAsking && (
             <div className="flex gap-4">
               <div className="shrink-0 h-8 w-8 rounded-full bg-slate-800 border border-slate-700 text-emerald-400 flex items-center justify-center">
                  <Bot size={14} />
                </div>
                <div className="bg-slate-800 border border-slate-700 px-4 py-4 rounded-2xl rounded-tl-none flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin text-emerald-400" />
                  <span className="text-sm text-slate-400">Retrieving context...</span>
                </div>
            </div>
          )}
        </div>

        <div className="p-4 bg-slate-900 border-t border-slate-800 shrink-0">
          <form onSubmit={handleAsk} className="relative flex items-center gap-2">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask about your documents..."
              className="flex-1 bg-slate-950 border border-slate-700 focus:border-emerald-500 rounded-xl px-4 py-3 text-white focus:outline-none transition-colors"
              disabled={isAsking}
            />
            <Button
              type="submit"
              disabled={!question.trim() || isAsking}
              className="bg-emerald-600 hover:bg-emerald-700 text-white"
            >
              <Send className="h-5 w-5" />
            </Button>
          </form>
        </div>
      </Card>

    </div>
  );
}
