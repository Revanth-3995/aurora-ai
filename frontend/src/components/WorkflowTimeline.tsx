import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle2, Circle, Clock, AlertCircle } from 'lucide-react';

export interface WorkflowStep {
  step: number;
  tool: string;
  instruction: string;
  result?: string;
  status: 'pending' | 'active' | 'success' | 'error';
}

interface WorkflowTimelineProps {
  intent?: string;
  reasoning?: string;
  steps: WorkflowStep[];
}

export const WorkflowTimeline = ({ intent, reasoning, steps }: WorkflowTimelineProps) => {
  return (
    <div className="flex flex-col gap-6">
      {intent && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-slate-900/50 rounded-lg p-4 border border-slate-800"
        >
          <h4 className="text-sm font-semibold text-slate-300 uppercase tracking-wider mb-2 flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-indigo-500"></span>
            Intent Analysis
          </h4>
          <p className="text-white font-medium mb-1">Detected: <span className="text-indigo-400">{intent}</span></p>
          <p className="text-sm text-slate-400">{reasoning}</p>
        </motion.div>
      )}

      {steps.length > 0 && (
        <div className="relative border-l-2 border-slate-800 ml-3 py-2">
          {steps.map((step, index) => {
            const isSuccess = step.status === 'success';
            const isActive = step.status === 'active';
            const isError = step.status === 'error';

            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="mb-8 last:mb-0 relative pl-8"
              >
                <span className="absolute -left-[11px] top-1 bg-slate-950">
                  {isSuccess ? (
                    <CheckCircle2 className="h-5 w-5 text-emerald-500 bg-slate-950 rounded-full" />
                  ) : isError ? (
                    <AlertCircle className="h-5 w-5 text-red-500 bg-slate-950 rounded-full" />
                  ) : isActive ? (
                    <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 2, ease: "linear" }}>
                       <Clock className="h-5 w-5 text-indigo-400 bg-slate-950 rounded-full" />
                    </motion.div>
                  ) : (
                    <Circle className="h-5 w-5 text-slate-600 bg-slate-950 rounded-full" />
                  )}
                </span>

                <div className="flex flex-col gap-1.5">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-medium px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                      Step {step.step}
                    </span>
                    <span className="text-sm font-semibold text-indigo-300 bg-indigo-900/20 px-2 py-0.5 rounded border border-indigo-800/30">
                      {step.tool !== 'none' ? step.tool : 'Direct Reasoning'}
                    </span>
                  </div>

                  <p className="text-sm text-slate-200 mt-1">{step.instruction}</p>

                  {(isSuccess || isError) && step.result && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      className={`mt-2 p-3 rounded-md text-xs font-mono overflow-x-auto border ${
                        isSuccess ? 'bg-slate-900/80 border-slate-800 text-slate-400' : 'bg-red-950/30 border-red-900/50 text-red-200'
                      }`}
                    >
                      {step.result.length > 300 ? step.result.substring(0, 300) + '...' : step.result}
                    </motion.div>
                  )}
                </div>
              </motion.div>
            );
          })}
        </div>
      )}
    </div>
  );
};
