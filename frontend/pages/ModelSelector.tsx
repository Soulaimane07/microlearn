import React, { useState, useEffect } from 'react';
import { Search, Play, Trophy, ChevronDown } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { getModelCandidates } from './api';
import { useDispatch, useSelector } from 'react-redux';
import { storemodelselection } from "../store/slices/pipelineSlice";  

export default function ModelSelector({ pipelineId, targetColumn }) {
  const dataset = useSelector((state) => state.pipeline?.datapreparer?.minio_object);
  
  const [algorithms, setAlgorithms] = useState([
    { id: 'rf', name: 'RandomForest', selected: true },
    { id: 'lr', name: 'Logistic Regression', selected: true },
    { id: 'svm', name: 'SVM', selected: false },
    { id: 'xgb', name: 'XGBoost', selected: true },
  ]);

  const [results, setResults] = useState([]);
  const [showResults, setShowResults] = useState(false);
  const [loading, setLoading] = useState(false);
  
  const dispatch = useDispatch();


  const runModelSelection = async () => {
    setLoading(true);
    try {
      const selectedCategories = algorithms.filter(a => a.selected).map(a => a.id);
      const data = await getModelCandidates(pipelineId, dataset, targetColumn, selectedCategories);
      console.log(data);
      
      dispatch(storemodelselection(data));
      setResults(data.candidates || []);
      setShowResults(true);
    } catch (err) {
      console.error(err);
      alert('Error fetching model candidates');
    }
    setLoading(false);
  };

  const chartData = results.map(model => ({
    name: model.model_name,
    Compatibility: (model.compatibility_score || 0) * 100
  }));

  const winnerModel = results.reduce((prev, curr) => {
    return (curr.compatibility_score || 0) > (prev.compatibility_score || 0) ? curr : prev;
  }, results[0] || {});


  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      {/* Header */}
      <div className="mb-8 flex items-center gap-3">
        <div className="w-10 h-10 bg-[#2563EB] rounded-lg flex items-center justify-center">
          <Search className="w-5 h-5 text-white" />
        </div>
        <h1 className="text-gray-900">ModelSelector Microservice</h1>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {/* Config */}
        <div className="col-span-2 space-y-6 min-h-screen">
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Configuration</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-700 mb-2">Prepared Dataset</label>
                <input
                  type="text"
                  value={dataset}
                  disabled
                  className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-700 mb-3">Allowed Algorithm Families</label>
                <div className="grid grid-cols-2 gap-3">
                  {algorithms.map((algo, idx) => (
                    <label
                      key={algo.id}
                      className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 border border-gray-200"
                    >
                      <span className="text-sm text-gray-700">{algo.name}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Results */}
          {showResults && results.length > 0 && (
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <h3 className="text-gray-900 mb-4">Recommended Models</h3>

              <div className="mb-6">
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                    <YAxis tick={{ fontSize: 12 }} />
                    <Tooltip formatter={(value) => `${value.toFixed(1)}%`} />
                    <Bar dataKey="Compatibility" fill="#2563EB" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="overflow-x-auto border border-gray-200 rounded-lg">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs text-gray-600">Model</th>
                      <th className="px-4 py-3 text-left text-xs text-gray-600">Expected Accuracy</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {results.map((model, idx) => (
                      <tr key={model.model_id} className={model === winnerModel ? 'bg-green-50' : 'hover:bg-gray-50'}>
                        <td className="px-4 py-3 text-sm text-gray-900 flex items-center gap-2">
                          {model.model_name}
                          {model === winnerModel && <Trophy className="w-4 h-4 text-yellow-500" />}
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-900">{(model.compatibility_score*100).toFixed(1)}%</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          <button
            onClick={runModelSelection}
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-[#2563EB] text-white rounded-lg hover:bg-[#1d4ed8] transition-colors shadow-sm"
          >
            <Play className="w-4 h-4" />
            {loading ? 'Selecting...' : 'Run Model Selection'}
          </button>
        </div>
      </div>
    </div>
  );
}
