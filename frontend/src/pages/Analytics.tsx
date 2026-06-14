import React, { useEffect, useState } from 'react';
import { BarChart2, Activity, Clock, Layers } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { getAnalytics } from '../services/api';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

export default function Analytics() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    getAnalytics().then(setData).catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="flex items-center justify-center h-full">
        <span className="animate-spin h-8 w-8 border-4 border-indigo-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-slate-900 border border-slate-700 p-3 rounded-lg shadow-xl">
          <p className="text-white font-medium mb-2">{label}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.name}: <span className="font-bold">{entry.value}</span>
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="max-w-6xl mx-auto h-full flex flex-col gap-6">
      <div className="flex flex-col gap-2">
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          <BarChart2 className="h-6 w-6 text-indigo-500" />
          System Analytics
        </h2>
        <p className="text-slate-400">Monitor agent performance, usage trends, and system health.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-slate-900/50">
          <div className="flex items-center gap-3 mb-2">
            <Activity className="h-5 w-5 text-indigo-400" />
            <h3 className="text-sm font-medium text-slate-400">Total Interactions</h3>
          </div>
          <p className="text-2xl font-bold text-white">{data.total_chats}</p>
        </Card>
        <Card className="bg-slate-900/50">
          <div className="flex items-center gap-3 mb-2">
            <Layers className="h-5 w-5 text-emerald-400" />
            <h3 className="text-sm font-medium text-slate-400">RAG Documents</h3>
          </div>
          <p className="text-2xl font-bold text-white">{data.uploaded_documents}</p>
        </Card>
        <Card className="bg-slate-900/50">
          <div className="flex items-center gap-3 mb-2">
            <BarChart2 className="h-5 w-5 text-purple-400" />
            <h3 className="text-sm font-medium text-slate-400">Research Tasks</h3>
          </div>
          <p className="text-2xl font-bold text-white">{data.research_queries}</p>
        </Card>
        <Card className="bg-slate-900/50">
          <div className="flex items-center gap-3 mb-2">
            <Clock className="h-5 w-5 text-amber-400" />
            <h3 className="text-sm font-medium text-slate-400">Avg. Response Time</h3>
          </div>
          <p className="text-2xl font-bold text-white">{data.avg_response_time_ms}ms</p>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 flex-1 min-h-[400px]">
        <Card className="flex flex-col">
          <h3 className="text-lg font-semibold text-white mb-6">Interaction Trends</h3>
          <div className="flex-1 w-full min-h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data.chart_data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorChats" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                <XAxis dataKey="name" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip content={<CustomTooltip />} />
                <Area type="monotone" dataKey="chats" name="Chat Queries" stroke="#6366f1" strokeWidth={2} fillOpacity={1} fill="url(#colorChats)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card className="flex flex-col">
          <h3 className="text-lg font-semibold text-white mb-6">Agent Execution Distribution</h3>
          <div className="flex-1 w-full min-h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.chart_data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                <XAxis dataKey="name" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip content={<CustomTooltip />} cursor={{ fill: '#1e293b' }} />
                <Bar dataKey="research" name="Research Tasks" fill="#a855f7" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>
    </div>
  );
}
