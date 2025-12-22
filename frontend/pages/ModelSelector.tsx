import React, { useState } from 'react';
import { Search, Play, Trophy, ChevronDown } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function ModelSelector() {
  const [showResults, setShowResults] = useState(false);

  const algorithms = [
    { id: 'rf', name: 'RandomForest', selected: true },
    { id: 'lr', name: 'Logistic Regression', selected: true },
    { id: 'svm', name: 'SVM', selected: false },
    { id: 'xgb', name: 'XGBoost', selected: true },
  ];

  const comparisonData = [
    { name: 'RandomForest', accuracy: 0.94, f1: 0.92, precision: 0.93, recall: 0.91 },
    { name: 'XGBoost', accuracy: 0.92, f1: 0.90, precision: 0.91, recall: 0.89 },
    { name: 'LogisticReg', accuracy: 0.87, f1: 0.85, precision: 0.86, recall: 0.84 },
  ];

  const chartData = [
    { metric: 'Accuracy', RandomForest: 94, XGBoost: 92, LogisticReg: 87 },
    { metric: 'F1 Score', RandomForest: 92, XGBoost: 90, LogisticReg: 85 },
    { metric: 'Precision', RandomForest: 93, XGBoost: 91, LogisticReg: 86 },
    { metric: 'Recall', RandomForest: 91, XGBoost: 89, LogisticReg: 84 },
  ];

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 bg-[#2563EB] rounded-lg flex items-center justify-center">
            <Search className="w-5 h-5 text-white" />
          </div>
          <h1 className="text-gray-900">ModelSelector Microservice</h1>
        </div>
        <p className="text-gray-500">Compare ML algorithms and select the best performing model</p>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {/* Configuration */}
        <div className="col-span-2 space-y-6">
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Configuration</h3>
            
            <div className="space-y-4">
              {/* Dataset Selection */}
              <div>
                <label className="block text-sm text-gray-700 mb-2">Select Prepared Dataset</label>
                <div className="relative">
                  <select className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 appearance-none cursor-pointer hover:border-[#2563EB] transition-colors">
                    <option>ds_004 - customer_data_cleaned</option>
                    <option>ds_003 - sales_data_processed</option>
                    <option>ds_002 - reviews_transformed</option>
                  </select>
                  <ChevronDown className="w-4 h-4 text-gray-400 absolute right-3 top-3.5 pointer-events-none" />
                </div>
              </div>

              {/* Target Column */}
              <div>
                <label className="block text-sm text-gray-700 mb-2">Target Column</label>
                <div className="relative">
                  <select className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 appearance-none cursor-pointer hover:border-[#2563EB] transition-colors">
                    <option>churn</option>
                    <option>conversion</option>
                    <option>purchase</option>
                  </select>
                  <ChevronDown className="w-4 h-4 text-gray-400 absolute right-3 top-3.5 pointer-events-none" />
                </div>
              </div>

              {/* Algorithm Selection */}
              <div>
                <label className="block text-sm text-gray-700 mb-3">Select Algorithms to Compare</label>
                <div className="grid grid-cols-2 gap-3">
                  {algorithms.map((algo) => (
                    <label key={algo.id} className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 border border-gray-200">
                      <input 
                        type="checkbox" 
                        defaultChecked={algo.selected}
                        className="text-[#2563EB] rounded" 
                      />
                      <span className="text-sm text-gray-700">{algo.name}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Model Comparison Results */}
          {showResults && (
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <h3 className="text-gray-900 mb-4">Model Comparison</h3>
              
              {/* Chart */}
              <div className="mb-6">
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="metric" tick={{ fontSize: 12 }} />
                    <YAxis tick={{ fontSize: 12 }} />
                    <Tooltip />
                    <Bar dataKey="RandomForest" fill="#2563EB" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="XGBoost" fill="#14b8a6" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="LogisticReg" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Metrics Table */}
              <div className="overflow-x-auto border border-gray-200 rounded-lg">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs text-gray-600">Model</th>
                      <th className="px-4 py-3 text-left text-xs text-gray-600">Accuracy</th>
                      <th className="px-4 py-3 text-left text-xs text-gray-600">F1 Score</th>
                      <th className="px-4 py-3 text-left text-xs text-gray-600">Precision</th>
                      <th className="px-4 py-3 text-left text-xs text-gray-600">Recall</th>
                      <th className="px-4 py-3 text-left text-xs text-gray-600">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {comparisonData.map((model, idx) => (
                      <tr key={model.name} className={idx === 0 ? 'bg-green-50' : 'hover:bg-gray-50'}>
                        <td className="px-4 py-3 text-sm text-gray-900 flex items-center gap-2">
                          {model.name}
                          {idx === 0 && <Trophy className="w-4 h-4 text-yellow-500" />}
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-900">{(model.accuracy * 100).toFixed(1)}%</td>
                        <td className="px-4 py-3 text-sm text-gray-900">{(model.f1 * 100).toFixed(1)}%</td>
                        <td className="px-4 py-3 text-sm text-gray-900">{(model.precision * 100).toFixed(1)}%</td>
                        <td className="px-4 py-3 text-sm text-gray-900">{(model.recall * 100).toFixed(1)}%</td>
                        <td className="px-4 py-3">
                          {idx === 0 ? (
                            <span className="inline-flex items-center gap-1 px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs">
                              Winner
                            </span>
                          ) : (
                            <span className="text-xs text-gray-500">Evaluated</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Confusion Matrix Preview */}
              <div className="mt-6">
                <div className="text-sm text-gray-700 mb-3">Confusion Matrix - RandomForest (Winner)</div>
                <div className="grid grid-cols-2 gap-2 max-w-xs">
                  <div className="bg-green-100 border border-green-300 rounded p-3 text-center">
                    <div className="text-xs text-gray-600 mb-1">True Positive</div>
                    <div className="text-green-700">8,420</div>
                  </div>
                  <div className="bg-red-100 border border-red-300 rounded p-3 text-center">
                    <div className="text-xs text-gray-600 mb-1">False Positive</div>
                    <div className="text-red-700">542</div>
                  </div>
                  <div className="bg-red-100 border border-red-300 rounded p-3 text-center">
                    <div className="text-xs text-gray-600 mb-1">False Negative</div>
                    <div className="text-red-700">628</div>
                  </div>
                  <div className="bg-green-100 border border-green-300 rounded p-3 text-center">
                    <div className="text-xs text-gray-600 mb-1">True Negative</div>
                    <div className="text-green-700">410</div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Right Sidebar */}
        <div className="space-y-6">
          {/* Run Button */}
          <button 
            onClick={() => setShowResults(true)}
            className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-[#2563EB] text-white rounded-lg hover:bg-[#1d4ed8] transition-colors shadow-sm"
          >
            <Play className="w-4 h-4" />
            Run Model Selection
          </button>

          {/* Winner Card */}
          {showResults && (
            <div className="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-xl p-6 shadow-sm border border-yellow-200">
              <div className="flex items-center gap-2 mb-4">
                <Trophy className="w-6 h-6 text-yellow-600" />
                <h3 className="text-gray-900">Winner Model</h3>
              </div>
              
              <div className="space-y-3">
                <div>
                  <div className="text-xs text-gray-600 mb-1">Model ID</div>
                  <div className="text-sm text-gray-900 font-mono bg-white px-3 py-2 rounded">mdl_504</div>
                </div>
                
                <div>
                  <div className="text-xs text-gray-600 mb-1">Algorithm</div>
                  <div className="text-sm text-gray-900">RandomForest</div>
                </div>
                
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <div className="text-xs text-gray-600 mb-1">Accuracy</div>
                    <div className="text-green-600">94.0%</div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-600 mb-1">F1 Score</div>
                    <div className="text-green-600">92.0%</div>
                  </div>
                </div>
                
                <div>
                  <div className="text-xs text-gray-600 mb-1">MinIO Artifact</div>
                  <a href="#" className="text-xs text-[#2563EB] hover:underline break-all">
                    minio://models/mdl_504.pkl
                  </a>
                </div>
              </div>
            </div>
          )}

          {/* Info Card */}
          <div className="bg-blue-50 rounded-xl p-6 border border-blue-200">
            <h4 className="text-sm text-gray-900 mb-2">How it works</h4>
            <ul className="space-y-2 text-xs text-gray-600">
              <li>• Trains multiple models in parallel</li>
              <li>• Uses cross-validation for robust metrics</li>
              <li>• Automatically selects the best performer</li>
              <li>• Saves all models for comparison</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
