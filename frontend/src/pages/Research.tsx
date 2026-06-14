import React, { useState } from 'react';
import { Search, Loader2, Globe, ExternalLink } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { performResearch } from '../services/api';
import ReactMarkdown from 'react-markdown';
import { motion } from 'framer-motion';

export default function Research() {
  const [query, setQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [result, setResult] = useState<{ summary: string; sources: any[] } | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || isSearching) return;

    setIsSearching(true);
    setResult(null);

    try {
      const data = await performResearch(query);
      setResult(data);
    } catch (error) {
      console.error(error);
      setResult({
        summary: "An error occurred while performing research. Please check API keys and try again.",
        sources: []
      });
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto h-full flex flex-col gap-6">
      <div className="flex flex-col gap-2">
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          <Globe className="h-6 w-6 text-purple-400" />
          Autonomous Research Agent
        </h2>
        <p className="text-slate-400">Perform deep, multi-source web research with reasoning capabilities.</p>
      </div>

      <Card className="shrink-0">
        <form onSubmit={handleSearch} className="flex gap-4">
          <div className="relative flex-1">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-slate-400" />
            </div>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="What would you like to research today?"
              className="w-full bg-slate-900 border border-slate-700 focus:border-purple-500 rounded-xl py-3 pl-11 pr-4 text-white focus:outline-none transition-colors"
              disabled={isSearching}
            />
          </div>
          <Button
            type="submit"
            className="bg-purple-600 hover:bg-purple-700 text-white min-w-[120px]"
            disabled={!query.trim() || isSearching}
          >
            {isSearching ? <Loader2 className="h-5 w-5 animate-spin" /> : 'Research'}
          </Button>
        </form>
      </Card>

      {isSearching && (
        <div className="flex-1 flex flex-col items-center justify-center gap-4 text-slate-400">
          <div className="relative">
            <div className="absolute inset-0 bg-purple-500 blur-xl opacity-20 rounded-full animate-pulse"></div>
            <Loader2 className="h-12 w-12 animate-spin text-purple-400 relative z-10" />
          </div>
          <div className="flex flex-col items-center gap-1">
            <p className="text-lg font-medium text-slate-200">Analyzing query...</p>
            <p className="text-sm">Fetching and synthesizing sources</p>
          </div>
        </div>
      )}

      {result && !isSearching && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex-1 flex flex-col lg:flex-row gap-6 overflow-hidden"
        >
          {/* Main Report */}
          <Card className="flex-[2] overflow-y-auto bg-slate-900/80">
            <h3 className="text-lg font-semibold text-white mb-4 border-b border-slate-800 pb-4">Research Report</h3>
            <div className="prose prose-invert max-w-none">
              <ReactMarkdown>{result.summary}</ReactMarkdown>
            </div>
          </Card>

          {/* Sources Panel */}
          <div className="flex-1 flex flex-col gap-4 overflow-hidden">
            <h3 className="text-lg font-semibold text-white px-1">Sources Cited</h3>
            <div className="flex-1 overflow-y-auto flex flex-col gap-3 pr-2">
              {result.sources && result.sources.length > 0 ? (
                result.sources.map((source, idx) => (
                  <a
                    key={idx}
                    href={source.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block p-4 rounded-xl border border-slate-700 bg-slate-800/50 hover:bg-slate-800 transition-colors group"
                  >
                    <h4 className="font-medium text-slate-200 mb-2 line-clamp-2 group-hover:text-purple-400 transition-colors">
                      {source.title || new URL(source.url).hostname}
                    </h4>
                    {source.content && (
                      <p className="text-sm text-slate-400 line-clamp-3 mb-3">{source.content}</p>
                    )}
                    <div className="flex items-center text-xs text-slate-500 gap-1.5 font-medium">
                      <ExternalLink className="h-3 w-3" />
                      {new URL(source.url).hostname}
                    </div>
                  </a>
                ))
              ) : (
                <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/50 text-slate-500 text-sm text-center">
                  No explicit sources returned.
                </div>
              )}
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
}
