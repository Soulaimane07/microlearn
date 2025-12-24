import React, { useEffect, useState } from 'react';
import { BarChart3, Download, ChevronDown } from 'lucide-react';
import {
  LineChart, Line, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import { EvaluatorUrl } from '../components/variables';

const API_BASE = EvaluatorUrl; // Evaluator microservice

export default function Evaluator() {
  const [models, setModels] = useState([]);
  const [datasets, setDatasets] = useState([]);
  const [selectedModel, setSelectedModel] = useState("");
  const [selectedDataset, setSelectedDataset] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  /* ---------------- LOAD MODELS & DATASETS ---------------- */

  useEffect(() => {
    fetch(`${API_BASE}/models`).then(r => r.json()).then(setModels);
    fetch(`${API_BASE}/datasets`).then(r => r.json()).then(setDatasets);
  }, []);

  /* ---------------- RUN EVALUATION ---------------- */

  const runEvaluation = async () => {
    setLoading(true);
    setResult(null);

    const res = await fetch(`${API_BASE}/evaluate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model_id: selectedModel,
        dataset_id: selectedDataset
      })
    });

    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

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
        <p className="text-gray-500">
          Evaluate trained models using real test datasets
        </p>
      </div>

      <div className="grid grid-cols-3 gap-6">

        {/* LEFT */}
        <div className="col-span-2 space-y-6">

          {/* CONFIG */}
          <div className="bg-white rounded-xl p-6 shadow-sm border">
            <h3 className="mb-4">Evaluation Configuration</h3>

            <div className="grid grid-cols-2 gap-4">
              <select
                className="input"
                onChange={e => setSelectedModel(e.target.value)}
              >
                <option value="">Select Model</option>
                {models.map(m => (
                  <option key={m.id} value={m.id}>
                    {m.name} ({m.algorithm})
                  </option>
                ))}
              </select>

              <select
                className="input"
                onChange={e => setSelectedDataset(e.target.value)}
              >
                <option value="">Select Dataset</option>
                {datasets.map(d => (
                  <option key={d.id} value={d.id}>
                    {d.name}
                  </option>
                ))}
              </select>
            </div>

            <button
              onClick={runEvaluation}
              disabled={!selectedModel || !selectedDataset || loading}
              className="mt-4 px-6 py-2 bg-[#2563EB] text-white rounded-lg"
            >
              {loading ? "Evaluating..." : "Run Evaluation"}
            </button>
          </div>

          {/* ROC */}
          {result && (
            <div className="bg-white rounded-xl p-6 shadow-sm border">
              <h3 className="mb-4">ROC Curve (AUC = {result.auc})</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={result.roc}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="fpr" />
                  <YAxis />
                  <Tooltip />
                  <Line dataKey="tpr" stroke="#2563EB" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* PR */}
          {result && (
            <div className="bg-white rounded-xl p-6 shadow-sm border">
              <h3 className="mb-4">Precision–Recall Curve</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={result.pr}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="recall" />
                  <YAxis />
                  <Tooltip />
                  <Line dataKey="precision" stroke="#14b8a6" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* FEATURE IMPORTANCE */}
          {result && (
            <div className="bg-white rounded-xl p-6 shadow-sm border">
              <h3 className="mb-4">Feature Importance</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={result.feature_importance} layout="vertical">
                  <XAxis type="number" />
                  <YAxis dataKey="feature" type="category" />
                  <Tooltip />
                  <Bar dataKey="importance" fill="#8b5cf6" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>

        {/* RIGHT */}
        <div className="space-y-6">

          {result && (
            <div className="bg-white rounded-xl p-6 shadow-sm border">
              <h3 className="mb-4">Evaluation Summary</h3>

              {Object.entries(result.metrics).map(([k, v]) => (
                <div key={k} className="mb-2">
                  <span className="text-xs text-gray-500">{k}</span>
                  <div className="font-bold">{(v * 100).toFixed(2)}%</div>
                </div>
              ))}
            </div>
          )}

          {result && (
            <div className="bg-white rounded-xl p-6 shadow-sm border">
              <h3 className="mb-4">Confusion Matrix</h3>

              <div className="grid grid-cols-2 gap-2 text-center">
                <div className="bg-green-100 p-4">TP: {result.confusion.tp}</div>
                <div className="bg-red-100 p-4">FP: {result.confusion.fp}</div>
                <div className="bg-red-100 p-4">FN: {result.confusion.fn}</div>
                <div className="bg-green-100 p-4">TN: {result.confusion.tn}</div>
              </div>
            </div>
          )}

          {result && (
            <button className="w-full flex gap-2 justify-center px-6 py-3 bg-[#2563EB] text-white rounded-lg">
              <Download className="w-4 h-4" /> Download Report
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
