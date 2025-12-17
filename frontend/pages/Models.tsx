import React, { useState } from 'react';
import { Brain, Download, ExternalLink, Trophy, TrendingUp } from 'lucide-react';
import { StatusBadge } from '../components/StatusBadge';

export function Models() {
  const [selectedModel, setSelectedModel] = useState<string | null>(null);

  const models = [
    {
      id: 'mdl_505',
      name: 'RandomForest_v3',
      algorithm: 'RandomForest',
      accuracy: 0.947,
      f1Score: 0.932,
      precision: 0.928,
      recall: 0.936,
      trainingDate: '2025-12-04',
      status: 'best',
      trainingTime: '5m 23s',
      size: '24.3 MB',
    },
    {
      id: 'mdl_504',
      name: 'RandomForest_v2',
      algorithm: 'RandomForest',
      accuracy: 0.940,
      f1Score: 0.920,
      precision: 0.930,
      recall: 0.910,
      trainingDate: '2025-12-03',
      status: 'old',
      trainingTime: '4m 56s',
      size: '22.1 MB',
    },
    {
      id: 'mdl_503',
      name: 'XGBoost_v2',
      algorithm: 'XGBoost',
      accuracy: 0.920,
      f1Score: 0.900,
      precision: 0.910,
      recall: 0.890,
      trainingDate: '2025-12-03',
      status: 'old',
      trainingTime: '7m 12s',
      size: '31.5 MB',
    },
    {
      id: 'mdl_502',
      name: 'XGBoost_v1',
      algorithm: 'XGBoost',
      accuracy: 0.915,
      f1Score: 0.895,
      precision: 0.905,
      recall: 0.885,
      trainingDate: '2025-12-02',
      status: 'old',
      trainingTime: '6m 45s',
      size: '29.8 MB',
    },
    {
      id: 'mdl_501',
      name: 'LogisticReg_v1',
      algorithm: 'Logistic Regression',
      accuracy: 0.870,
      f1Score: 0.850,
      precision: 0.860,
      recall: 0.840,
      trainingDate: '2025-12-01',
      status: 'old',
      trainingTime: '2m 34s',
      size: '8.4 MB',
    },
  ];

  const confusionMatrix = {
    tp: 1872,
    fp: 144,
    fn: 128,
    tn: 856,
  };

  const selected = models.find(m => m.id === selectedModel);

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-gray-900 mb-2">Models</h1>
            <p className="text-gray-500">Browse and manage your trained machine learning models</p>
          </div>
          <button className="flex items-center gap-2 px-6 py-3 bg-[#2563EB] text-white rounded-lg hover:bg-[#1d4ed8] transition-colors shadow-sm">
            <Brain className="w-4 h-4" />
            Train New Model
          </button>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {/* Models List */}
        <div className="col-span-2 bg-white rounded-xl shadow-sm border border-gray-200">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-gray-900">All Models</h3>
          </div>
          
          <div className="divide-y divide-gray-200">
            {models.map((model) => (
              <div 
                key={model.id}
                onClick={() => setSelectedModel(model.id)}
                className={`p-6 cursor-pointer transition-colors ${
                  selectedModel === model.id ? 'bg-blue-50' : 'hover:bg-gray-50'
                }`}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-start gap-3">
                    <div className={`w-10 h-10 ${model.status === 'best' ? 'bg-yellow-500' : 'bg-[#2563EB]'} rounded-lg flex items-center justify-center flex-shrink-0`}>
                      {model.status === 'best' ? (
                        <Trophy className="w-5 h-5 text-white" />
                      ) : (
                        <Brain className="w-5 h-5 text-white" />
                      )}
                    </div>
                    <div>
                      <div className="text-gray-900 mb-1">{model.name}</div>
                      <div className="text-sm text-gray-500">{model.algorithm}</div>
                      <div className="text-xs text-gray-400 font-mono mt-1">{model.id}</div>
                    </div>
                  </div>
                  <div className="text-right">
                    {model.status === 'best' ? (
                      <span className="inline-flex items-center gap-1 px-3 py-1 bg-yellow-100 text-yellow-700 rounded-full text-xs mb-2">
                        <Trophy className="w-3 h-3" />
                        Best Model
                      </span>
                    ) : (
                      <span className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-xs mb-2 inline-block">
                        Previous
                      </span>
                    )}
                    <div className="text-green-600 flex items-center gap-1 justify-end mt-1">
                      <TrendingUp className="w-3 h-3" />
                      <span>{(model.accuracy * 100).toFixed(1)}%</span>
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-5 gap-4 text-sm">
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Accuracy</div>
                    <div className="text-gray-900">{(model.accuracy * 100).toFixed(1)}%</div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 mb-1">F1 Score</div>
                    <div className="text-gray-900">{(model.f1Score * 100).toFixed(1)}%</div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Precision</div>
                    <div className="text-gray-900">{(model.precision * 100).toFixed(1)}%</div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Recall</div>
                    <div className="text-gray-900">{(model.recall * 100).toFixed(1)}%</div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Trained</div>
                    <div className="text-gray-900">{model.trainingDate}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Model Details */}
        <div className="space-y-6">
          {selected ? (
            <>
              <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                <h3 className="text-gray-900 mb-4">Model Details</h3>
                
                <div className="space-y-3">
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Model ID</div>
                    <div className="text-sm text-gray-900 font-mono bg-gray-50 px-3 py-2 rounded">{selected.id}</div>
                  </div>
                  
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Algorithm</div>
                    <div className="text-sm text-gray-900">{selected.algorithm}</div>
                  </div>
                  
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Training Time</div>
                    <div className="text-sm text-gray-900">{selected.trainingTime}</div>
                  </div>
                  
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Model Size</div>
                    <div className="text-sm text-gray-900">{selected.size}</div>
                  </div>

                  <div>
                    <div className="text-xs text-gray-500 mb-1">Status</div>
                    {selected.status === 'best' ? (
                      <StatusBadge status="success" label="Best Model" />
                    ) : (
                      <span className="text-sm text-gray-600">Previous Version</span>
                    )}
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                <h4 className="text-sm text-gray-900 mb-3">Performance Metrics</h4>
                <div className="space-y-3">
                  <div className="p-3 bg-green-50 rounded-lg border border-green-200">
                    <div className="text-xs text-gray-600 mb-1">Accuracy</div>
                    <div className="text-green-600">{(selected.accuracy * 100).toFixed(1)}%</div>
                  </div>

                  <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
                    <div className="text-xs text-gray-600 mb-1">F1 Score</div>
                    <div className="text-blue-600">{(selected.f1Score * 100).toFixed(1)}%</div>
                  </div>

                  <div className="p-3 bg-purple-50 rounded-lg border border-purple-200">
                    <div className="text-xs text-gray-600 mb-1">Precision</div>
                    <div className="text-purple-600">{(selected.precision * 100).toFixed(1)}%</div>
                  </div>

                  <div className="p-3 bg-teal-50 rounded-lg border border-teal-200">
                    <div className="text-xs text-gray-600 mb-1">Recall</div>
                    <div className="text-teal-600">{(selected.recall * 100).toFixed(1)}%</div>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                <h4 className="text-sm text-gray-900 mb-3">Confusion Matrix</h4>
                
                <div className="space-y-2">
                  <div className="grid grid-cols-2 gap-2">
                    <div className="bg-green-100 border border-green-300 rounded-lg p-3 text-center">
                      <div className="text-xs text-gray-600 mb-1">True Positive</div>
                      <div className="text-green-700">{confusionMatrix.tp}</div>
                    </div>
                    <div className="bg-red-100 border border-red-300 rounded-lg p-3 text-center">
                      <div className="text-xs text-gray-600 mb-1">False Positive</div>
                      <div className="text-red-700">{confusionMatrix.fp}</div>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-2">
                    <div className="bg-red-100 border border-red-300 rounded-lg p-3 text-center">
                      <div className="text-xs text-gray-600 mb-1">False Negative</div>
                      <div className="text-red-700">{confusionMatrix.fn}</div>
                    </div>
                    <div className="bg-green-100 border border-green-300 rounded-lg p-3 text-center">
                      <div className="text-xs text-gray-600 mb-1">True Negative</div>
                      <div className="text-green-700">{confusionMatrix.tn}</div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="space-y-2">
                <button className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-[#2563EB] text-white rounded-lg hover:bg-[#1d4ed8] transition-colors text-sm">
                  <Download className="w-4 h-4" />
                  Download Model
                </button>
                <button className="w-full px-4 py-2.5 bg-white text-gray-700 rounded-lg hover:bg-gray-50 transition-colors border border-gray-200 text-sm">
                  View Training Logs
                </button>
                <a 
                  href="#" 
                  className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-white text-gray-700 rounded-lg hover:bg-gray-50 transition-colors border border-gray-200 text-sm"
                >
                  <ExternalLink className="w-4 h-4" />
                  MinIO Artifact
                </a>
              </div>
            </>
          ) : (
            <div className="bg-gray-50 rounded-xl p-8 text-center border border-gray-200">
              <Brain className="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-500 text-sm">Select a model to view details</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
