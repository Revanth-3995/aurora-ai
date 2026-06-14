import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { MessageSquare, Search, FileText, Calendar, Activity, ArrowUpRight } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { getAnalytics } from '../services/api';
import { Link } from 'react-router-dom';

interface AnalyticsData {
  total_chats: number;
  research_queries: number;
  uploaded_documents: number;
  calendar_events: number;
  avg_response_time_ms: number;
  recent_activity: Array<{id: number, type: string, summary: string, time: string}>;
}

export default function Dashboard() {
  const [data, setData] = useState<AnalyticsData | null>(null);

  useEffect(() => {
    getAnalytics().then(setData).catch(console.error);
  }, []);

  const stats = [
    { label: 'Total Chats', value: data?.total_chats || '-', icon: MessageSquare, color: 'text-blue-500', bg: 'bg-blue-500/10' },
    { label: 'Research Queries', value: data?.research_queries || '-', icon: Search, color: 'text-purple-500', bg: 'bg-purple-500/10' },
    { label: 'Documents RAG', value: data?.uploaded_documents || '-', icon: FileText, color: 'text-emerald-500', bg: 'bg-emerald-500/10' },
    { label: 'Calendar Events', value: data?.calendar_events || '-', icon: Calendar, color: 'text-amber-500', bg: 'bg-amber-500/10' },
  ];

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white mb-1">Welcome back</h2>
          <p className="text-slate-400">Here's what your agents have been up to.</p>
        </div>
        <div className="flex items-center gap-2 text-sm text-emerald-400 bg-emerald-400/10 px-3 py-1.5 rounded-full border border-emerald-400/20">
          <Activity className="h-4 w-4" />
          <span>System Healthy</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, idx) => {
          const Icon = stat.icon;
          return (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1 }}
            >
              <Card className="flex flex-col gap-4">
                <div className="flex items-center justify-between">
                  <div className={`p-3 rounded-lg ${stat.bg}`}>
                    <Icon className={`h-6 w-6 ${stat.color}`} />
                  </div>
                </div>
                <div>
                  <h3 className="text-3xl font-bold text-white mb-1">{stat.value}</h3>
                  <p className="text-sm text-slate-400 font-medium">{stat.label}</p>
                </div>
              </Card>
            </motion.div>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2 flex flex-col">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-white">Quick Actions</h3>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Link to="/chat" className="group p-4 rounded-xl border border-slate-700 bg-slate-800/50 hover:bg-slate-800 transition-colors flex flex-col gap-3">
              <div className="h-10 w-10 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center">
                <MessageSquare className="h-5 w-5" />
              </div>
              <div>
                <h4 className="text-white font-medium mb-1 flex items-center justify-between">
                  New Chat <ArrowUpRight className="h-4 w-4 opacity-0 group-hover:opacity-100 transition-opacity" />
                </h4>
                <p className="text-sm text-slate-400">Start a new conversation with Aurora.</p>
              </div>
            </Link>
            <Link to="/research" className="group p-4 rounded-xl border border-slate-700 bg-slate-800/50 hover:bg-slate-800 transition-colors flex flex-col gap-3">
              <div className="h-10 w-10 rounded-lg bg-purple-500/20 text-purple-400 flex items-center justify-center">
                <Search className="h-5 w-5" />
              </div>
              <div>
                <h4 className="text-white font-medium mb-1 flex items-center justify-between">
                  Deep Research <ArrowUpRight className="h-4 w-4 opacity-0 group-hover:opacity-100 transition-opacity" />
                </h4>
                <p className="text-sm text-slate-400">Run an autonomous web research task.</p>
              </div>
            </Link>
            <Link to="/documents" className="group p-4 rounded-xl border border-slate-700 bg-slate-800/50 hover:bg-slate-800 transition-colors flex flex-col gap-3">
              <div className="h-10 w-10 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center">
                <FileText className="h-5 w-5" />
              </div>
              <div>
                <h4 className="text-white font-medium mb-1 flex items-center justify-between">
                  Upload PDF <ArrowUpRight className="h-4 w-4 opacity-0 group-hover:opacity-100 transition-opacity" />
                </h4>
                <p className="text-sm text-slate-400">Ingest a document to RAG memory.</p>
              </div>
            </Link>
            <Link to="/calendar" className="group p-4 rounded-xl border border-slate-700 bg-slate-800/50 hover:bg-slate-800 transition-colors flex flex-col gap-3">
              <div className="h-10 w-10 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center">
                <Calendar className="h-5 w-5" />
              </div>
              <div>
                <h4 className="text-white font-medium mb-1 flex items-center justify-between">
                  Schedule Event <ArrowUpRight className="h-4 w-4 opacity-0 group-hover:opacity-100 transition-opacity" />
                </h4>
                <p className="text-sm text-slate-400">Manage your Google Calendar.</p>
              </div>
            </Link>
          </div>
        </Card>

        <Card className="flex flex-col">
          <h3 className="text-lg font-semibold text-white mb-6">Recent Activity</h3>
          <div className="flex flex-col gap-4">
            {data?.recent_activity ? (
              data.recent_activity.map((activity) => (
                <div key={activity.id} className="flex gap-4">
                  <div className="mt-1 flex-shrink-0">
                    <div className="h-2 w-2 rounded-full bg-indigo-500" />
                  </div>
                  <div>
                    <p className="text-sm text-slate-200">{activity.summary}</p>
                    <p className="text-xs text-slate-500 mt-1">{activity.time}</p>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-sm text-slate-500">Loading activity...</div>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
}
