import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Database, Search, Zap, BarChart3, Rocket, ArrowRight } from 'lucide-react';
import { StatusBadge } from './StatusBadge';

export function PipelineFlow() {
  const navigate = useNavigate();
  
  const stages = [
    {
      id: 'data-preparer',
      title: 'DataPreparer',
      icon: Database,
      status: 'success' as const,
      description: 'Clean & transform data',
      path: '/data-preparer',
    },
    {
      id: 'model-selector',
      title: 'ModelSelector',
      icon: Search,
      status: 'success' as const,
      description: 'Compare algorithms',
      path: '/model-selector',
    },
    {
      id: 'trainer',
      title: 'Trainer',
      icon: Zap,
      status: 'in-progress' as const,
      description: 'Train best model',
      path: '/trainer',
    },
    {
      id: 'evaluator',
      title: 'Evaluator',
      icon: BarChart3,
      status: 'pending' as const,
      description: 'Evaluate performance',
      path: '/evaluator',
    },
    {
      id: 'deployer',
      title: 'Deployer',
      icon: Rocket,
      status: 'pending' as const,
      description: 'Deploy to production',
      path: '/deployer',
    },
  ];

  return (
    <div className="bg-white rounded-xl p-8 shadow-sm border border-gray-200">
      <h2 className="text-gray-900 mb-6">Pipeline Flow</h2>
      
      <div className="flex items-center justify-between gap-4">
        {stages.map((stage, index) => {
          const Icon = stage.icon;
          return (
            <React.Fragment key={stage.id}>
              <button
                onClick={() => navigate(stage.path)}
                className="flex-1 bg-gradient-to-br from-white to-gray-50 border border-gray-200 rounded-xl p-6 hover:shadow-md transition-all hover:scale-105 cursor-pointer group"
              >
                <div className="flex flex-col items-center gap-3">
                  <div className="w-14 h-14 bg-[#2563EB] rounded-xl flex items-center justify-center group-hover:bg-[#1d4ed8] transition-colors">
                    <Icon className="w-7 h-7 text-white" />
                  </div>
                  <div className="text-center">
                    <div className="text-gray-900 mb-1">{stage.title}</div>
                    <div className="text-sm text-gray-500 mb-2">{stage.description}</div>
                    <StatusBadge status={stage.status} />
                  </div>
                </div>
              </button>
              
              {index < stages.length - 1 && (
                <ArrowRight className="w-6 h-6 text-gray-300 flex-shrink-0" />
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
}
