import React, { useState, useRef, useEffect } from 'react';
import { Send, User, Bot, Loader2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { motion, AnimatePresence } from 'framer-motion';
import { sendChatMessage } from '../services/api';
import { WorkflowTimeline, WorkflowStep } from '../components/WorkflowTimeline';
import { Card } from '../components/ui/Card';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  intent?: string;
  reasoning?: string;
  workflow?: WorkflowStep[];
  toolUsed?: string;
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await sendChatMessage(userMessage.content);

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.response,
        intent: response.intent,
        reasoning: response.reasoning,
        workflow: response.workflow,
        toolUsed: response.tool_used,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Chat error:", error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: "Sorry, I encountered an error while processing your request.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-full gap-6">
      {/* Chat Area */}
      <div className="flex-1 flex flex-col glass rounded-2xl overflow-hidden border border-slate-800">
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-slate-500 gap-4">
              <Bot className="h-16 w-16 text-slate-700" />
              <p className="text-lg">How can I assist you today?</p>
            </div>
          ) : (
            messages.map((msg) => (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                key={msg.id}
                className={`flex gap-4 max-w-[90%] ${msg.role === 'user' ? 'ml-auto flex-row-reverse' : ''}`}
              >
                <div className={`shrink-0 h-8 w-8 rounded-full flex items-center justify-center ${
                  msg.role === 'user' ? 'bg-indigo-600' : 'bg-slate-800 border border-slate-700 text-indigo-400'
                }`}>
                  {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                </div>

                <div className={`flex flex-col gap-2 ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                  <div className={`px-4 py-3 rounded-2xl ${
                    msg.role === 'user'
                      ? 'bg-indigo-600 text-white rounded-tr-none'
                      : 'bg-slate-800 border border-slate-700 text-slate-200 rounded-tl-none prose prose-invert max-w-none'
                  }`}>
                    {msg.role === 'assistant' ? (
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                    ) : (
                      msg.content
                    )}
                  </div>

                  {msg.role === 'assistant' && msg.toolUsed && msg.toolUsed !== 'None' && (
                    <div className="flex items-center gap-1.5 text-xs text-slate-500 font-medium px-1">
                      <span>Tools used:</span>
                      <span className="text-indigo-400 bg-indigo-400/10 px-1.5 py-0.5 rounded">{msg.toolUsed}</span>
                    </div>
                  )}
                </div>
              </motion.div>
            ))
          )}

          {isLoading && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-4">
               <div className="shrink-0 h-8 w-8 rounded-full bg-slate-800 border border-slate-700 text-indigo-400 flex items-center justify-center">
                  <Bot size={16} />
                </div>
                <div className="bg-slate-800 border border-slate-700 px-4 py-4 rounded-2xl rounded-tl-none flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin text-indigo-400" />
                  <span className="text-sm text-slate-400">Agent is thinking...</span>
                </div>
            </motion.div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="p-4 bg-slate-900 border-t border-slate-800">
          <form onSubmit={handleSubmit} className="relative flex items-end gap-2 max-w-4xl mx-auto">
            <div className="relative flex-1 bg-slate-950 border border-slate-700 focus-within:border-indigo-500 rounded-xl overflow-hidden transition-colors">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask Aurora AI anything..."
                className="w-full bg-transparent text-white p-4 max-h-48 min-h-[56px] focus:outline-none resize-none"
                rows={1}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSubmit(e);
                  }
                }}
              />
            </div>
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="h-14 w-14 shrink-0 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl flex items-center justify-center transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="h-5 w-5" />
            </button>
          </form>
        </div>
      </div>

      {/* Workflow Panel (Explainable AI) */}
      <AnimatePresence>
        {messages.length > 0 && messages[messages.length - 1].role === 'assistant' && (
          <motion.div
            initial={{ opacity: 0, width: 0 }}
            animate={{ opacity: 1, width: 380 }}
            exit={{ opacity: 0, width: 0 }}
            className="hidden xl:flex flex-col gap-4 overflow-hidden shrink-0"
          >
            <h3 className="font-semibold text-slate-200 px-1 shrink-0">Why this answer?</h3>
            <Card className="flex-1 overflow-y-auto bg-slate-950/50">
              <WorkflowTimeline
                intent={messages[messages.length - 1].intent}
                reasoning={messages[messages.length - 1].reasoning}
                steps={messages[messages.length - 1].workflow || []}
              />
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
