import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { MainLayout } from './layouts/MainLayout';

// Lazy load pages for better performance (we'll implement these next)
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
const Chat = React.lazy(() => import('./pages/Chat'));
const Research = React.lazy(() => import('./pages/Research'));
const Documents = React.lazy(() => import('./pages/Documents'));
const Calendar = React.lazy(() => import('./pages/Calendar'));
const Analytics = React.lazy(() => import('./pages/Analytics'));

function App() {
  return (
    <React.Suspense fallback={
      <div className="flex h-screen items-center justify-center bg-slate-950 text-indigo-400">
        <span className="animate-spin h-8 w-8 border-4 border-current border-t-transparent rounded-full" />
      </div>
    }>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="chat" element={<Chat />} />
          <Route path="research" element={<Research />} />
          <Route path="documents" element={<Documents />} />
          <Route path="calendar" element={<Calendar />} />
          <Route path="analytics" element={<Analytics />} />
          <Route path="settings" element={<div className="p-6 text-slate-400">Settings page coming soon...</div>} />
        </Route>
      </Routes>
    </React.Suspense>
  );
}

export default App;
