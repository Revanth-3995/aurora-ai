import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, MessageSquare, Search, FileText, Calendar, BarChart2, Settings, ChevronLeft, ChevronRight, Zap } from 'lucide-react';
import { motion } from 'framer-motion';

const navItems = [
  { name: 'Dashboard', path: '/', icon: LayoutDashboard },
  { name: 'Chat', path: '/chat', icon: MessageSquare },
  { name: 'Research Agent', path: '/research', icon: Search },
  { name: 'Documents (RAG)', path: '/documents', icon: FileText },
  { name: 'Calendar Agent', path: '/calendar', icon: Calendar },
  { name: 'Analytics', path: '/analytics', icon: BarChart2 },
];

export const Sidebar = () => {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <motion.aside
      initial={false}
      animate={{ width: collapsed ? 80 : 260 }}
      className="h-screen bg-slate-950 border-r border-slate-800 flex flex-col relative shrink-0"
    >
      <div className="p-4 flex items-center justify-between h-16 border-b border-slate-800 shrink-0">
        {!collapsed && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex items-center gap-2 font-bold text-xl tracking-tight text-white">
            <Zap className="h-6 w-6 text-indigo-500" />
            AURORA AI
          </motion.div>
        )}
        {collapsed && (
          <div className="mx-auto w-full flex justify-center">
            <Zap className="h-6 w-6 text-indigo-500" />
          </div>
        )}

      </div>

      <button
        onClick={() => setCollapsed(!collapsed)}
        className="absolute -right-4 top-5 bg-slate-800 border border-slate-700 rounded-full p-1.5 text-slate-400 hover:text-white z-10"
      >
        {collapsed ? <ChevronRight size={14} /> : <ChevronLeft size={14} />}
      </button>

      <div className="flex-1 overflow-y-auto py-6 flex flex-col gap-2 px-3">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors group ${
                  isActive
                    ? 'bg-indigo-600/10 text-indigo-400 font-medium'
                    : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-100'
                }`
              }
            >
              <Icon className="h-5 w-5 shrink-0" />
              {!collapsed && <span>{item.name}</span>}
            </NavLink>
          );
        })}
      </div>

      <div className="p-4 border-t border-slate-800 shrink-0">
        <NavLink
          to="/settings"
          className={({ isActive }) =>
            `flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${
              isActive
                ? 'bg-slate-800 text-white font-medium'
                : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-100'
            }`
          }
        >
          <Settings className="h-5 w-5 shrink-0" />
          {!collapsed && <span>Settings</span>}
        </NavLink>
      </div>
    </motion.aside>
  );
};
