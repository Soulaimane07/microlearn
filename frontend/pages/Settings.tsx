import React, { useState } from 'react';
import { Settings as SettingsIcon, Database, Server, Shield, Save } from 'lucide-react';

export function Settings() {
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="max-w-5xl mx-auto px-6 py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 bg-[#2563EB] rounded-lg flex items-center justify-center">
            <SettingsIcon className="w-5 h-5 text-white" />
          </div>
          <h1 className="text-gray-900">Settings</h1>
        </div>
        <p className="text-gray-500">Configure your MicroLearn platform settings</p>
      </div>

      <div className="space-y-6">
        {/* MinIO Configuration */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center gap-3 mb-4">
            <Database className="w-5 h-5 text-[#2563EB]" />
            <h3 className="text-gray-900">MinIO Configuration</h3>
          </div>
          
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-gray-700 mb-2">Endpoint URL</label>
                <input 
                  type="text" 
                  defaultValue="http://localhost:9000"
                  className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 hover:border-[#2563EB] transition-colors"
                />
              </div>
              
              <div>
                <label className="block text-sm text-gray-700 mb-2">Bucket Name</label>
                <input 
                  type="text" 
                  defaultValue="microlearn-storage"
                  className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 hover:border-[#2563EB] transition-colors"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-gray-700 mb-2">Access Key</label>
                <input 
                  type="text" 
                  defaultValue="minio_access_key"
                  className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 hover:border-[#2563EB] transition-colors"
                />
              </div>
              
              <div>
                <label className="block text-sm text-gray-700 mb-2">Secret Key</label>
                <input 
                  type="password" 
                  defaultValue="••••••••••••"
                  className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 hover:border-[#2563EB] transition-colors"
                />
              </div>
            </div>

            <div className="flex items-center justify-between pt-2">
              <span className="text-xs text-gray-500">Object storage for datasets and models</span>
              <button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm">
                Test Connection
              </button>
            </div>
          </div>
        </div>

        {/* PostgreSQL Configuration */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center gap-3 mb-4">
            <Server className="w-5 h-5 text-teal-500" />
            <h3 className="text-gray-900">PostgreSQL Configuration</h3>
          </div>
          
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-gray-700 mb-2">Host</label>
                <input 
                  type="text" 
                  defaultValue="localhost"
                  className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 hover:border-[#2563EB] transition-colors"
                />
              </div>
              
              <div>
                <label className="block text-sm text-gray-700 mb-2">Port</label>
                <input 
                  type="text" 
                  defaultValue="5432"
                  className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 hover:border-[#2563EB] transition-colors"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-gray-700 mb-2">Database Name</label>
                <input 
                  type="text" 
                  defaultValue="microlearn_db"
                  className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 hover:border-[#2563EB] transition-colors"
                />
              </div>
              
              <div>
                <label className="block text-sm text-gray-700 mb-2">Username</label>
                <input 
                  type="text" 
                  defaultValue="postgres"
                  className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 hover:border-[#2563EB] transition-colors"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm text-gray-700 mb-2">Password</label>
              <input 
                type="password" 
                defaultValue="••••••••••••"
                className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 hover:border-[#2563EB] transition-colors"
              />
            </div>

            <div className="flex items-center justify-between pt-2">
              <span className="text-xs text-gray-500">Metadata and pipeline state storage</span>
              <button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm">
                Test Connection
              </button>
            </div>
          </div>
        </div>

        {/* API Gateway Settings */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center gap-3 mb-4">
            <Shield className="w-5 h-5 text-purple-500" />
            <h3 className="text-gray-900">API Gateway Settings</h3>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-gray-700 mb-2">Gateway URL</label>
              <input 
                type="text" 
                defaultValue="http://localhost:8080"
                className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 hover:border-[#2563EB] transition-colors"
              />
            </div>

            <div>
              <label className="block text-sm text-gray-700 mb-2">API Key</label>
              <input 
                type="password" 
                defaultValue="••••••••-••••-••••-••••-••••••••••••"
                className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 hover:border-[#2563EB] transition-colors"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-gray-700 mb-2">Rate Limit (req/min)</label>
                <input 
                  type="number" 
                  defaultValue={100}
                  className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 hover:border-[#2563EB] transition-colors"
                />
              </div>
              
              <div>
                <label className="block text-sm text-gray-700 mb-2">Timeout (seconds)</label>
                <input 
                  type="number" 
                  defaultValue={30}
                  className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 hover:border-[#2563EB] transition-colors"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Microservice URLs */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <h3 className="text-gray-900 mb-4">Microservice URLs</h3>
          
          <div className="space-y-3">
            {[
              { name: 'DataPreparer', url: 'http://localhost:8001' },
              { name: 'ModelSelector', url: 'http://localhost:8002' },
              { name: 'Trainer', url: 'http://localhost:8003' },
              { name: 'Evaluator', url: 'http://localhost:8004' },
              { name: 'Deployer', url: 'http://localhost:8005' },
            ].map((service) => (
              <div key={service.name} className="grid grid-cols-3 gap-4 items-center">
                <label className="text-sm text-gray-700">{service.name}</label>
                <input 
                  type="text" 
                  defaultValue={service.url}
                  className="col-span-2 px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 hover:border-[#2563EB] transition-colors text-sm"
                />
              </div>
            ))}
          </div>
        </div>

        {/* Save Button */}
        <div className="flex items-center justify-end gap-3">
          <button className="px-6 py-3 bg-white text-gray-700 rounded-lg hover:bg-gray-50 transition-colors border border-gray-200">
            Reset to Defaults
          </button>
          <button 
            onClick={handleSave}
            className="flex items-center gap-2 px-6 py-3 bg-[#2563EB] text-white rounded-lg hover:bg-[#1d4ed8] transition-colors shadow-sm"
          >
            <Save className="w-4 h-4" />
            {saved ? 'Saved!' : 'Save Changes'}
          </button>
        </div>

        {saved && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <p className="text-sm text-green-700">✓ Settings saved successfully!</p>
          </div>
        )}
      </div>
    </div>
  );
}
