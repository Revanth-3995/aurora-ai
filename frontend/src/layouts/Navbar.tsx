import React from 'react';
import { useLocation } from 'react-router-dom';
import { Activity, User } from 'lucide-react';
import { Badge } from '../components/ui/Badge';

export const Navbar = () => {
  const location = useLocation();

  const getPageTitle = () => {
    switch (location.pathname) {
      case '/': return 'Dashboard';
      case '/chat': return 'Chat';
      case '/research': return 'Research Agent';
      case '/documents': return 'Document Intelligence';
      case '/calendar': return 'Calendar Agent';
      case '/analytics': return 'Analytics';
      default: return 'Aurora AI';
    }
  };

  return (
    <header className="h-16 border-b border-slate-800 bg-slate-950/50 backdrop-blur flex items-center justify-between px-6 shrink-0 sticky top-0 z-10">
      <div className="flex items-center gap-4">
        <h1 className="text-lg font-semibold text-white">{getPageTitle()}</h1>
        <Badge variant="success" className="gap-1.5 hidden sm:flex">
          <Activity className="h-3 w-3" />
          Agents Online
        </Badge>
      </div>

      <div className="flex items-center gap-4">
        <div className="h-8 w-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-300">
          <User className="h-4 w-4" />
        </div>
      </div>
    </header>
  );
};
