import React, { useState } from 'react';
import { Calendar as CalendarIcon, Clock, Link as LinkIcon, Loader2, CheckCircle2, AlertCircle } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { scheduleEvent } from '../services/api';

export default function Calendar() {
  const [title, setTitle] = useState('');
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');
  const [description, setDescription] = useState('');
  const [isScheduling, setIsScheduling] = useState(false);
  const [status, setStatus] = useState<{ type: 'success' | 'error', message: string } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !date || !time) return;

    setIsScheduling(true);
    setStatus(null);

    try {
      const res = await scheduleEvent(title, date, time, description);
      if (res.status === 'Success') {
        setStatus({ type: 'success', message: `Event scheduled successfully. ${res.message}` });
        setTitle('');
        setDate('');
        setTime('');
        setDescription('');
      } else {
         setStatus({ type: 'error', message: res.message || 'Failed to schedule event.' });
      }
    } catch (err: any) {
      setStatus({ type: 'error', message: err.response?.data?.detail || 'An error occurred connecting to Google Calendar.' });
    } finally {
      setIsScheduling(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto h-full flex flex-col gap-6">
      <div className="flex flex-col gap-2">
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          <CalendarIcon className="h-6 w-6 text-amber-500" />
          Calendar Agent
        </h2>
        <p className="text-slate-400">Autonomous meeting scheduling and availability checking via Google Calendar.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="md:col-span-2 flex flex-col gap-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
             <h3 className="text-lg font-semibold text-white">Schedule New Event</h3>
          </div>

          <form onSubmit={handleSubmit} className="flex flex-col gap-5">
            <div className="flex flex-col gap-2">
              <label className="text-sm font-medium text-slate-300">Event Title</label>
              <input
                type="text"
                value={title}
                onChange={e => setTitle(e.target.value)}
                placeholder="E.g. Team Sync"
                className="bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-white focus:border-amber-500 focus:outline-none"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="flex flex-col gap-2">
                <label className="text-sm font-medium text-slate-300">Date (YYYY-MM-DD)</label>
                <div className="relative">
                  <CalendarIcon className="absolute left-3 top-3 h-4 w-4 text-slate-500" />
                  <input
                    type="date"
                    value={date}
                    onChange={e => setDate(e.target.value)}
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg pl-10 pr-4 py-2.5 text-white focus:border-amber-500 focus:outline-none"
                    required
                  />
                </div>
              </div>
              <div className="flex flex-col gap-2">
                <label className="text-sm font-medium text-slate-300">Time (HH:MM)</label>
                <div className="relative">
                  <Clock className="absolute left-3 top-3 h-4 w-4 text-slate-500" />
                  <input
                    type="time"
                    value={time}
                    onChange={e => setTime(e.target.value)}
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg pl-10 pr-4 py-2.5 text-white focus:border-amber-500 focus:outline-none"
                    required
                  />
                </div>
              </div>
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-sm font-medium text-slate-300">Description (Optional)</label>
              <textarea
                value={description}
                onChange={e => setDescription(e.target.value)}
                placeholder="Meeting agenda..."
                className="bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-white focus:border-amber-500 focus:outline-none resize-none h-24"
              />
            </div>

            {status && (
              <div className={`p-3 rounded-lg flex items-start gap-2 text-sm ${
                status.type === 'success' ? 'bg-emerald-900/30 text-emerald-400 border border-emerald-800/50' : 'bg-red-900/30 text-red-400 border border-red-800/50'
              }`}>
                {status.type === 'success' ? <CheckCircle2 className="h-4 w-4 mt-0.5 shrink-0" /> : <AlertCircle className="h-4 w-4 mt-0.5 shrink-0" />}
                <p>{status.message}</p>
              </div>
            )}

            <div className="flex justify-end pt-2">
              <Button
                type="submit"
                className="bg-amber-600 hover:bg-amber-700 text-white min-w-[140px]"
                disabled={isScheduling}
              >
                {isScheduling ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
                {isScheduling ? 'Scheduling...' : 'Schedule Event'}
              </Button>
            </div>
          </form>
        </Card>

        <div className="flex flex-col gap-6">
          <Card className="flex flex-col gap-4">
            <h3 className="font-semibold text-white">Connection Status</h3>
            <div className="flex items-center gap-3 bg-slate-900 border border-slate-800 p-3 rounded-lg">
              <div className="h-10 w-10 bg-slate-800 rounded flex items-center justify-center border border-slate-700">
                <LinkIcon className="h-5 w-5 text-emerald-500" />
              </div>
              <div>
                <p className="text-sm font-medium text-white">Google Calendar</p>
                <p className="text-xs text-emerald-400">Connected</p>
              </div>
            </div>
          </Card>

          <Card className="flex-1 flex flex-col gap-4 bg-slate-900/50">
            <h3 className="font-semibold text-white">Upcoming Events</h3>
            <div className="flex-1 flex flex-col items-center justify-center text-center p-4 border-2 border-dashed border-slate-800 rounded-xl bg-slate-900/20">
              <CalendarIcon className="h-8 w-8 text-slate-600 mb-2" />
              <p className="text-sm text-slate-400">Syncing with calendar...</p>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
