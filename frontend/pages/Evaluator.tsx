import React from 'react';
import { BarChart3, Download, ChevronDown } from 'lucide-react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export function Evaluator() {
  const rocData = [
    { fpr: 0, tpr: 0 },
    { fpr: 0.1, tpr: 0.75 },
    { fpr: 0.2, tpr: 0.88 },
    { fpr: 0.3, tpr: 0.93 },
    { fpr: 0.4, tpr: 0.96 },
    { fpr: 0.5, tpr: 0.98 },
    { fpr: 1, tpr: 1 },
  ];

  const prData = [
    { recall: 0, precision: 1 },
    { recall: 0.2, precision: 0.98 },
    { recall: 0.4, precision: 0.95 },
    { recall: 0.6, precision: 0.92 },
    { recall: 0.8, precision: 0.88 },
    { recall: 1, precision: 0.82 },
  ];

  const featureImportance = [
    { feature: 'income', importance: 0.28 },
    { feature: 'age', importance: 0.22 },
    { feature: 'tenure', importance: 0.18 },
    { feature: 'usage', importance: 0.15 },
    { feature: 'support_calls', importance: 0.10 },
    { feature: 'region', importance: 0.07 },
  ];

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 bg-[#2563EB] rounded-lg flex items-center justify-center">
            <BarChart3 className="w-5 h-5 text-white" />
          </div>
          <h1 className="text-gray-900">Evaluator Microservice</h1>
        </div>
        <p className="text-gray-500">Evaluate model performance with comprehensive metrics and visualizations</p>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="col-span-2 space-y-6">
          {/* Test Data Selection */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Evaluation Configuration</h3>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-gray-700 mb-2">Select Trained Model</label>
                <div className="relative">
                  <select className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 appearance-none cursor-pointer hover:border-[#2563EB] transition-colors">
                    <option>mdl_505 - RandomForest (Latest)</option>
                    <option>mdl_504 - RandomForest</option>
                    <option>mdl_503 - XGBoost</option>
                  </select>
                  <ChevronDown className="w-4 h-4 text-gray-400 absolute right-3 top-3.5 pointer-events-none" />
                </div>
              </div>

              <div>
                <label className="block text-sm text-gray-700 mb-2">Test Dataset</label>
                <div className="relative">
                  <select className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 appearance-none cursor-pointer hover:border-[#2563EB] transition-colors">
                    <option>Validation Split (20%)</option>
                    <option>Upload Test Set</option>
                    <option>ds_005 - test_data.csv</option>
                  </select>
                  <ChevronDown className="w-4 h-4 text-gray-400 absolute right-3 top-3.5 pointer-events-none" />
                </div>
              </div>
            </div>
          </div>

          {/* ROC Curve */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">ROC Curve (AUC = 0.96)</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={rocData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="fpr" label={{ value: 'False Positive Rate', position: 'insideBottom', offset: -5 }} tick={{ fontSize: 12 }} />
                <YAxis label={{ value: 'True Positive Rate', angle: -90, position: 'insideLeft' }} tick={{ fontSize: 12 }} />
                <Tooltip />
                <Line type="monotone" dataKey="tpr" stroke="#2563EB" strokeWidth={2} dot={false} />
                <Line type="monotone" data={[{ fpr: 0, tpr: 0 }, { fpr: 1, tpr: 1 }]} dataKey="tpr" stroke="#e5e7eb" strokeDasharray="5 5" dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Precision-Recall Curve */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Precision-Recall Curve</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={prData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="recall" label={{ value: 'Recall', position: 'insideBottom', offset: -5 }} tick={{ fontSize: 12 }} />
                <YAxis label={{ value: 'Precision', angle: -90, position: 'insideLeft' }} tick={{ fontSize: 12 }} />
                <Tooltip />
                <Line type="monotone" dataKey="precision" stroke="#14b8a6" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Feature Importance */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Feature Importance</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={featureImportance} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis type="number" tick={{ fontSize: 12 }} />
                <YAxis dataKey="feature" type="category" tick={{ fontSize: 12 }} width={100} />
                <Tooltip />
                <Bar dataKey="importance" fill="#8b5cf6" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Right Sidebar */}
        <div className="space-y-6">
          {/* Evaluation Summary */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Evaluation Summary</h3>
            
            <div className="space-y-4">
              <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                <div className="text-xs text-gray-600 mb-1">Accuracy</div>
                <div className="text-green-600">94.7%</div>
              </div>

              <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                <div className="text-xs text-gray-600 mb-1">F1 Score</div>
                <div className="text-blue-600">93.2%</div>
              </div>

              <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
                <div className="text-xs text-gray-600 mb-1">Precision</div>
                <div className="text-purple-600">92.8%</div>
              </div>

              <div className="p-4 bg-teal-50 rounded-lg border border-teal-200">
                <div className="text-xs text-gray-600 mb-1">Recall</div>
                <div className="text-teal-600">93.6%</div>
              </div>

              <div className="p-4 bg-orange-50 rounded-lg border border-orange-200">
                <div className="text-xs text-gray-600 mb-1">AUC-ROC</div>
                <div className="text-orange-600">0.96</div>
              </div>
            </div>
          </div>

          {/* Confusion Matrix */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Confusion Matrix</h3>
            
            <div className="space-y-2">
              <div className="grid grid-cols-2 gap-2">
                <div className="bg-green-100 border border-green-300 rounded-lg p-4 text-center">
                  <div className="text-xs text-gray-600 mb-1">True Positive</div>
                  <div className="text-green-700">1,872</div>
                </div>
                <div className="bg-red-100 border border-red-300 rounded-lg p-4 text-center">
                  <div className="text-xs text-gray-600 mb-1">False Positive</div>
                  <div className="text-red-700">144</div>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-2">
                <div className="bg-red-100 border border-red-300 rounded-lg p-4 text-center">
                  <div className="text-xs text-gray-600 mb-1">False Negative</div>
                  <div className="text-red-700">128</div>
                </div>
                <div className="bg-green-100 border border-green-300 rounded-lg p-4 text-center">
                  <div className="text-xs text-gray-600 mb-1">True Negative</div>
                  <div className="text-green-700">856</div>
                </div>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="space-y-3">
            <button className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-[#2563EB] text-white rounded-lg hover:bg-[#1d4ed8] transition-colors shadow-sm">
              <Download className="w-4 h-4" />
              Download Report
            </button>

            <button className="w-full px-6 py-3 bg-white text-gray-700 rounded-lg hover:bg-gray-50 transition-colors border border-gray-200">
              Export Metrics
            </button>
          </div>

          {/* Info */}
          <div className="bg-teal-50 rounded-xl p-6 border border-teal-200">
            <h4 className="text-sm text-gray-900 mb-2">Report Includes</h4>
            <ul className="space-y-1 text-xs text-gray-600">
              <li>• All performance metrics</li>
              <li>• ROC and PR curves</li>
              <li>• Confusion matrix</li>
              <li>• Feature importance</li>
              <li>• Model metadata</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
