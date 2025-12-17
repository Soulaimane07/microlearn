import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Database, Search, Zap, BarChart3, Rocket, Activity, ExternalLink } from 'lucide-react';
import { StatusBadge } from '../components/StatusBadge';

export function Microservices() {
  const navigate = useNavigate();

  const services = [
    {
      id: 'data-preparer',
      name: 'DataPreparer',
      icon: Database,
      status: 'success' as const,
      version: 'v2.1.0',
      lastActivity: '2 min ago',
      health: 'Healthy',
      uptime: '99.8%',
      requests: '1,234',
      path: '/data-preparer',
      color: 'bg-[#2563EB]',
    },
    {
      id: 'model-selector',
      name: 'ModelSelector',
      icon: Search,
      status: 'success' as const,
      version: 'v1.8.3',
      lastActivity: '5 min ago',
      health: 'Healthy',
      uptime: '99.9%',
      requests: '856',
      path: '/model-selector',
      color: 'bg-teal-500',
    },
    {
      id: 'trainer',
      name: 'Trainer',
      icon: Zap,
      status: 'in-progress' as const,
      version: 'v3.0.1',
      lastActivity: '1 min ago',
      health: 'Training',
      uptime: '99.7%',
      requests: '432',
      path: '/trainer',
      color: 'bg-yellow-500',
    },
    {
      id: 'evaluator',
      name: 'Evaluator',
      icon: BarChart3,
      status: 'success' as const,
      version: 'v1.5.2',
      lastActivity: '10 min ago',
      health: 'Healthy',
      uptime: '99.9%',
      requests: '678',
      path: '/evaluator',
      color: 'bg-purple-500',
    },
    {
      id: 'deployer',
      name: 'Deployer',
      icon: Rocket,
      status: 'success' as const,
      version: 'v2.3.0',
      lastActivity: '3 min ago',
      health: 'Healthy',
      uptime: '99.6%',
      requests: '234',
      path: '/deployer',
      color: 'bg-green-500',
    },
  ];

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-gray-900 mb-2">Microservices Overview</h1>
        <p className="text-gray-500">Monitor and manage all ML pipeline microservices</p>
      </div>

      {/* Overall Health */}
      <div className="grid grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-500">Overall Status</span>
            <Activity className="w-5 h-5 text-green-500" />
          </div>
          <div className="text-green-600">All Systems Operational</div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-500">Active Services</span>
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          </div>
          <div className="text-gray-900">5 / 5</div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-500">Avg Uptime</span>
          </div>
          <div className="text-gray-900">99.8%</div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-500">Total Requests</span>
          </div>
          <div className="text-gray-900">3,434</div>
        </div>
      </div>

      {/* Service Cards */}
      <div className="grid grid-cols-2 gap-6">
        {services.map((service) => {
          const Icon = service.icon;
          return (
            <div key={service.id} className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 hover:shadow-md transition-all">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className={`w-12 h-12 ${service.color} rounded-lg flex items-center justify-center`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-gray-900">{service.name}</h3>
                    <p className="text-sm text-gray-500">{service.version}</p>
                  </div>
                </div>
                <StatusBadge status={service.status} />
              </div>

              <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <div className="text-xs text-gray-500 mb-1">Health</div>
                  <div className="text-sm text-gray-900">{service.health}</div>
                </div>
                <div>
                  <div className="text-xs text-gray-500 mb-1">Last Activity</div>
                  <div className="text-sm text-gray-900">{service.lastActivity}</div>
                </div>
                <div>
                  <div className="text-xs text-gray-500 mb-1">Uptime</div>
                  <div className="text-sm text-green-600">{service.uptime}</div>
                </div>
                <div>
                  <div className="text-xs text-gray-500 mb-1">Requests (24h)</div>
                  <div className="text-sm text-gray-900">{service.requests}</div>
                </div>
              </div>

              <div className="flex gap-2">
                <button 
                  onClick={() => navigate(service.path)}
                  className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-[#2563EB] text-white rounded-lg hover:bg-[#1d4ed8] transition-colors text-sm"
                >
                  <ExternalLink className="w-4 h-4" />
                  Open Service
                </button>
                <button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm">
                  Logs
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Service Endpoints */}
      <div className="mt-8 bg-white rounded-xl p-6 shadow-sm border border-gray-200">
        <h3 className="text-gray-900 mb-4">Service Endpoints</h3>
        <div className="space-y-3">
          {services.map((service) => (
            <div key={service.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div>
                <div className="text-sm text-gray-900 mb-1">{service.name}</div>
                <div className="text-xs text-gray-500 font-mono">http://localhost:800{services.indexOf(service)}/{service.id}</div>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs text-green-600">✓ Reachable</span>
                <button className="p-1.5 hover:bg-gray-200 rounded transition-colors">
                  <ExternalLink className="w-4 h-4 text-gray-600" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
