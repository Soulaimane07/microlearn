import React from 'react';
import { useNavigate } from 'react-router-dom';
import { PipelineFlow } from '../components/PipelineFlow';
import { MetricCard } from '../components/MetricCard';
import { StatusBadge } from '../components/StatusBadge';
import { Database, Brain, Activity, Play, Clock, FileText } from 'lucide-react';

export function Dashboard() {
  const navigate = useNavigate();

  const recentTasks = [
    { id: 1, name: 'Customer Churn Prediction', stage: 'Trainer', status: 'in-progress' as const, time: '2 min ago' },
    { id: 2, name: 'Sales Forecasting Model', stage: 'Evaluator', status: 'success' as const, time: '15 min ago' },
    { id: 3, name: 'Sentiment Analysis Pipeline', stage: 'Deployer', status: 'success' as const, time: '1 hour ago' },
    { id: 4, name: 'Fraud Detection System', stage: 'ModelSelector', status: 'failed' as const, time: '3 hours ago' },
  ];

  const recentDatasets = [
    { id: 'ds_001', name: 'customer_churn.csv', rows: 10000, columns: 23, date: '2025-12-04' },
    { id: 'ds_002', name: 'sales_data.csv', rows: 15000, columns: 18, date: '2025-12-03' },
    { id: 'ds_003', name: 'reviews.csv', rows: 50000, columns: 8, date: '2025-12-02' },
  ];

  const recentModels = [
    { id: 'mdl_501', name: 'RandomForest_v3', accuracy: 0.94, algorithm: 'RandomForest', date: '2025-12-04' },
    { id: 'mdl_502', name: 'XGBoost_v2', accuracy: 0.92, algorithm: 'XGBoost', date: '2025-12-03' },
    { id: 'mdl_503', name: 'LogisticReg_v1', accuracy: 0.89, algorithm: 'Logistic Regression', date: '2025-12-02' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-gray-900 mb-2">Welcome to MicroLearn</h1>
          <p className="text-gray-500">Orchestrate your machine learning pipelines with ease</p>
        </div>
        <button className="flex items-center gap-2 px-6 py-3 bg-[#2563EB] text-white rounded-lg hover:bg-[#1d4ed8] transition-colors shadow-sm">
          <Play className="w-4 h-4" />
          Start New Pipeline
        </button>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-4 gap-6 mb-8">
        <MetricCard
          title="Active Pipelines"
          value="3"
          icon={Activity}
          trend="+2 this week"
          trendUp={true}
        />
        <MetricCard
          title="Total Datasets"
          value="24"
          icon={Database}
          color="bg-teal-500"
        />
        <MetricCard
          title="Trained Models"
          value="67"
          icon={Brain}
          trend="+5 this month"
          trendUp={true}
          color="bg-purple-500"
        />
        <MetricCard
          title="Success Rate"
          value="94.2%"
          icon={Activity}
          trend="+2.1%"
          trendUp={true}
          color="bg-green-500"
        />
      </div>

      {/* Pipeline Flow */}
      <div className="mb-8">
        <PipelineFlow />
      </div>

      {/* Two Column Layout */}
      <div className="grid grid-cols-2 gap-6 mb-8">
        {/* Recent Tasks */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-gray-900">Recent Tasks</h3>
            <Clock className="w-5 h-5 text-gray-400" />
          </div>
          <div className="space-y-3">
            {recentTasks.map((task) => (
              <div key={task.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer">
                <div className="flex-1">
                  <div className="text-gray-900 text-sm mb-1">{task.name}</div>
                  <div className="text-gray-500 text-xs">{task.stage} • {task.time}</div>
                </div>
                <StatusBadge status={task.status} />
              </div>
            ))}
          </div>
        </div>

        {/* Recent Datasets */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-gray-900">Recent Datasets</h3>
            <button 
              onClick={() => navigate('/datasets')}
              className="text-sm text-[#2563EB] hover:underline"
            >
              View all
            </button>
          </div>
          <div className="space-y-3">
            {recentDatasets.map((dataset) => (
              <div key={dataset.id} className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <FileText className="w-4 h-4 text-teal-500" />
                    <span className="text-gray-900 text-sm">{dataset.name}</span>
                  </div>
                  <span className="text-xs text-gray-500">{dataset.id}</span>
                </div>
                <div className="flex items-center gap-4 text-xs text-gray-500">
                  <span>{dataset.rows.toLocaleString()} rows</span>
                  <span>{dataset.columns} columns</span>
                  <span>{dataset.date}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Models */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-gray-900">Recent Models</h3>
          <button 
            onClick={() => navigate('/models')}
            className="text-sm text-[#2563EB] hover:underline"
          >
            View all
          </button>
        </div>
        <div className="grid grid-cols-3 gap-4">
          {recentModels.map((model) => (
            <div key={model.id} className="p-4 bg-gradient-to-br from-white to-gray-50 border border-gray-200 rounded-lg hover:shadow-md transition-all cursor-pointer">
              <div className="flex items-start justify-between mb-3">
                <Brain className="w-5 h-5 text-[#2563EB]" />
                <span className="text-xs text-gray-500">{model.id}</span>
              </div>
              <div className="text-gray-900 mb-1">{model.name}</div>
              <div className="text-sm text-gray-500 mb-2">{model.algorithm}</div>
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-500">{model.date}</span>
                <span className="text-sm text-green-600">{(model.accuracy * 100).toFixed(1)}%</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
