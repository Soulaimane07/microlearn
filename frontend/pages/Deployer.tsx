import React, { useState } from 'react';
import { Rocket, Play, CheckCircle2, Copy } from 'lucide-react';
import { StatusBadge } from '../components/StatusBadge';

export function Deployer() {
  const [deployed, setDeployed] = useState(false);
  const [deploymentTarget, setDeploymentTarget] = useState('local');

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 bg-[#2563EB] rounded-lg flex items-center justify-center">
            <Rocket className="w-5 h-5 text-white" />
          </div>
          <h1 className="text-gray-900">Deployer Microservice</h1>
        </div>
        <p className="text-gray-500">Deploy your trained models to production environments</p>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="col-span-2 space-y-6">
          {/* Model Selection */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Select Model to Deploy</h3>
            
            <div className="space-y-3">
              {[
                { id: 'mdl_505', name: 'RandomForest_v3', accuracy: 94.7, status: 'trained' },
                { id: 'mdl_504', name: 'RandomForest_v2', accuracy: 94.0, status: 'deployed' },
                { id: 'mdl_503', name: 'XGBoost_v2', accuracy: 92.0, status: 'trained' },
              ].map((model) => (
                <label key={model.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 border border-gray-200">
                  <div className="flex items-center gap-3">
                    <input type="radio" name="model" defaultChecked={model.id === 'mdl_505'} className="text-[#2563EB]" />
                    <div>
                      <div className="text-sm text-gray-900">{model.name}</div>
                      <div className="text-xs text-gray-500">{model.id}</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-sm text-green-600">{model.accuracy}%</span>
                    {model.status === 'deployed' && (
                      <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs">
                        Currently Deployed
                      </span>
                    )}
                  </div>
                </label>
              ))}
            </div>
          </div>

          {/* Deployment Target */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Deployment Target</h3>
            
            <div className="grid grid-cols-3 gap-4">
              <label 
                className={`p-6 rounded-lg border-2 cursor-pointer transition-all ${
                  deploymentTarget === 'local' 
                    ? 'border-[#2563EB] bg-blue-50' 
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <input 
                  type="radio" 
                  name="target" 
                  value="local"
                  checked={deploymentTarget === 'local'}
                  onChange={(e) => setDeploymentTarget(e.target.value)}
                  className="sr-only" 
                />
                <div className="text-center">
                  <div className="w-12 h-12 bg-[#2563EB] rounded-lg flex items-center justify-center mx-auto mb-3">
                    <Rocket className="w-6 h-6 text-white" />
                  </div>
                  <div className="text-sm text-gray-900 mb-1">Local API</div>
                  <div className="text-xs text-gray-500">REST endpoint</div>
                </div>
              </label>

              <label 
                className={`p-6 rounded-lg border-2 cursor-pointer transition-all ${
                  deploymentTarget === 'docker' 
                    ? 'border-[#2563EB] bg-blue-50' 
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <input 
                  type="radio" 
                  name="target" 
                  value="docker"
                  checked={deploymentTarget === 'docker'}
                  onChange={(e) => setDeploymentTarget(e.target.value)}
                  className="sr-only" 
                />
                <div className="text-center">
                  <div className="w-12 h-12 bg-teal-500 rounded-lg flex items-center justify-center mx-auto mb-3">
                    <Rocket className="w-6 h-6 text-white" />
                  </div>
                  <div className="text-sm text-gray-900 mb-1">Docker</div>
                  <div className="text-xs text-gray-500">Container</div>
                </div>
              </label>

              <label 
                className={`p-6 rounded-lg border-2 cursor-pointer transition-all ${
                  deploymentTarget === 'cloud' 
                    ? 'border-[#2563EB] bg-blue-50' 
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <input 
                  type="radio" 
                  name="target" 
                  value="cloud"
                  checked={deploymentTarget === 'cloud'}
                  onChange={(e) => setDeploymentTarget(e.target.value)}
                  className="sr-only" 
                />
                <div className="text-center">
                  <div className="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center mx-auto mb-3">
                    <Rocket className="w-6 h-6 text-white" />
                  </div>
                  <div className="text-sm text-gray-900 mb-1">Cloud</div>
                  <div className="text-xs text-gray-500">AWS/GCP/Azure</div>
                </div>
              </label>
            </div>
          </div>

          {/* API Documentation Preview */}
          {deployed && (
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <h3 className="text-gray-900 mb-4">API Documentation</h3>
              
              <div className="space-y-4">
                {/* Endpoint */}
                <div>
                  <div className="text-sm text-gray-700 mb-2">Endpoint</div>
                  <div className="flex items-center gap-2 p-3 bg-gray-900 rounded-lg font-mono text-sm text-green-400">
                    <span>POST</span>
                    <span className="text-gray-400">http://localhost:8000/predict</span>
                    <button className="ml-auto p-1 hover:bg-gray-800 rounded">
                      <Copy className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {/* Request Body */}
                <div>
                  <div className="text-sm text-gray-700 mb-2">Request Body</div>
                  <div className="bg-gray-900 rounded-lg p-4 font-mono text-xs text-gray-300 overflow-x-auto">
                    <pre>{`{
  "features": {
    "age": 35,
    "income": 65000,
    "tenure": 24,
    "usage": 450,
    "support_calls": 2,
    "region": "North"
  }
}`}</pre>
                  </div>
                </div>

                {/* Response */}
                <div>
                  <div className="text-sm text-gray-700 mb-2">Response</div>
                  <div className="bg-gray-900 rounded-lg p-4 font-mono text-xs text-gray-300 overflow-x-auto">
                    <pre>{`{
  "prediction": 0,
  "probability": 0.847,
  "model_id": "mdl_505",
  "timestamp": "2025-12-04T10:30:45Z"
}`}</pre>
                  </div>
                </div>

                {/* Example cURL */}
                <div>
                  <div className="text-sm text-gray-700 mb-2">Example cURL</div>
                  <div className="bg-gray-900 rounded-lg p-4 font-mono text-xs text-gray-300 overflow-x-auto">
                    <pre>{`curl -X POST http://localhost:8000/predict \\
  -H "Content-Type: application/json" \\
  -d '{"features": {...}}'`}</pre>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Deployment Logs */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Deployment Logs</h3>
            <div className="bg-gray-900 rounded-lg p-4 font-mono text-xs text-green-400 h-48 overflow-y-auto">
              {deployed ? (
                <>
                  <div>[INFO] Loading model mdl_505 from MinIO...</div>
                  <div>[INFO] Model loaded successfully</div>
                  <div>[INFO] Initializing FastAPI server...</div>
                  <div>[INFO] Creating /predict endpoint...</div>
                  <div>[INFO] Creating /health endpoint...</div>
                  <div>[SUCCESS] Server started on http://localhost:8000</div>
                  <div>[INFO] API documentation available at /docs</div>
                  <div>[SUCCESS] Deployment complete!</div>
                </>
              ) : (
                <div className="text-gray-500">[INFO] Ready to deploy...</div>
              )}
            </div>
          </div>
        </div>

        {/* Right Sidebar */}
        <div className="space-y-6">
          {/* Deploy Button */}
          <button 
            onClick={() => setDeployed(true)}
            disabled={deployed}
            className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-[#2563EB] text-white rounded-lg hover:bg-[#1d4ed8] transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {deployed ? (
              <>
                <CheckCircle2 className="w-4 h-4" />
                Deployed
              </>
            ) : (
              <>
                <Play className="w-4 h-4" />
                Deploy Model
              </>
            )}
          </button>

          {/* Deployment Status */}
          {deployed && (
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <div className="flex items-center gap-2 mb-4">
                <StatusBadge status="success" label="Live" />
              </div>
              
              <div className="space-y-3">
                <div>
                  <div className="text-xs text-gray-500 mb-1">Status</div>
                  <div className="text-sm text-green-600">Running</div>
                </div>
                
                <div>
                  <div className="text-xs text-gray-500 mb-1">Endpoint</div>
                  <div className="text-xs text-gray-900 break-all">localhost:8000</div>
                </div>
                
                <div>
                  <div className="text-xs text-gray-500 mb-1">Model Version</div>
                  <div className="text-sm text-gray-900">mdl_505</div>
                </div>
                
                <div>
                  <div className="text-xs text-gray-500 mb-1">Uptime</div>
                  <div className="text-sm text-gray-900">2m 34s</div>
                </div>
                
                <div>
                  <div className="text-xs text-gray-500 mb-1">Requests</div>
                  <div className="text-sm text-gray-900">47</div>
                </div>
              </div>
            </div>
          )}

          {/* Health Check */}
          {deployed && (
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <h4 className="text-sm text-gray-900 mb-3">Health Check</h4>
              <div className="space-y-2">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-gray-600">API Status</span>
                  <span className="text-green-600">✓ Healthy</span>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-gray-600">Model Loaded</span>
                  <span className="text-green-600">✓ Yes</span>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-gray-600">Avg Response</span>
                  <span className="text-gray-900">24ms</span>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-gray-600">Memory Usage</span>
                  <span className="text-gray-900">342 MB</span>
                </div>
              </div>
            </div>
          )}

          {/* Quick Actions */}
          {deployed && (
            <div className="space-y-2">
              <button className="w-full px-4 py-2 bg-white text-gray-700 rounded-lg hover:bg-gray-50 transition-colors border border-gray-200 text-sm">
                View Logs
              </button>
              <button className="w-full px-4 py-2 bg-white text-gray-700 rounded-lg hover:bg-gray-50 transition-colors border border-gray-200 text-sm">
                Test Endpoint
              </button>
              <button className="w-full px-4 py-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-colors border border-red-200 text-sm">
                Stop Deployment
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
