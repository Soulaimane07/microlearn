import React, { useState } from 'react';
import { FileText, ExternalLink, Database, Calendar, Download } from 'lucide-react';

export function Datasets() {
  const [selectedDataset, setSelectedDataset] = useState<string | null>(null);

  const datasets = [
    {
      id: 'ds_001',
      name: 'customer_churn.csv',
      rawFile: 'customer_churn_raw.csv',
      preparedFile: 'customer_churn_cleaned.parquet',
      rows: 10000,
      columns: 23,
      dateUploaded: '2025-12-04',
      size: '2.4 MB',
      status: 'processed',
    },
    {
      id: 'ds_002',
      name: 'sales_data.csv',
      rawFile: 'sales_data_raw.csv',
      preparedFile: 'sales_data_processed.parquet',
      rows: 15000,
      columns: 18,
      dateUploaded: '2025-12-03',
      size: '3.1 MB',
      status: 'processed',
    },
    {
      id: 'ds_003',
      name: 'reviews.csv',
      rawFile: 'reviews_raw.csv',
      preparedFile: 'reviews_transformed.parquet',
      rows: 50000,
      columns: 8,
      dateUploaded: '2025-12-02',
      size: '8.7 MB',
      status: 'processed',
    },
    {
      id: 'ds_004',
      name: 'user_behavior.csv',
      rawFile: 'user_behavior_raw.csv',
      preparedFile: null,
      rows: 7500,
      columns: 15,
      dateUploaded: '2025-12-01',
      size: '1.8 MB',
      status: 'pending',
    },
  ];

  const sampleData = [
    { id: 1, age: 25, income: 50000, score: 0.79, region: 'North', churn: 0 },
    { id: 2, age: 33, income: 75000, score: 0.85, region: 'South', churn: 0 },
    { id: 3, age: 34, income: 60000, score: 0.72, region: 'East', churn: 1 },
    { id: 4, age: 45, income: 61500, score: 0.91, region: 'East', churn: 0 },
    { id: 5, age: 28, income: 52000, score: 0.68, region: 'West', churn: 1 },
  ];

  const selected = datasets.find(d => d.id === selectedDataset);

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-gray-900 mb-2">Datasets</h1>
            <p className="text-gray-500">Manage your training and test datasets</p>
          </div>
          <button className="flex items-center gap-2 px-6 py-3 bg-[#2563EB] text-white rounded-lg hover:bg-[#1d4ed8] transition-colors shadow-sm">
            <FileText className="w-4 h-4" />
            Upload Dataset
          </button>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {/* Dataset List */}
        <div className="col-span-2 bg-white rounded-xl shadow-sm border border-gray-200">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-gray-900">All Datasets</h3>
          </div>
          
          <div className="divide-y divide-gray-200">
            {datasets.map((dataset) => (
              <div 
                key={dataset.id}
                onClick={() => setSelectedDataset(dataset.id)}
                className={`p-6 cursor-pointer transition-colors ${
                  selectedDataset === dataset.id ? 'bg-blue-50' : 'hover:bg-gray-50'
                }`}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-start gap-3">
                    <div className="w-10 h-10 bg-teal-500 rounded-lg flex items-center justify-center flex-shrink-0">
                      <FileText className="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <div className="text-gray-900 mb-1">{dataset.name}</div>
                      <div className="text-sm text-gray-500 font-mono">{dataset.id}</div>
                    </div>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs ${
                    dataset.status === 'processed' 
                      ? 'bg-green-100 text-green-700' 
                      : 'bg-yellow-100 text-yellow-700'
                  }`}>
                    {dataset.status}
                  </span>
                </div>

                <div className="grid grid-cols-4 gap-4 text-sm">
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Rows</div>
                    <div className="text-gray-900">{dataset.rows.toLocaleString()}</div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Columns</div>
                    <div className="text-gray-900">{dataset.columns}</div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Size</div>
                    <div className="text-gray-900">{dataset.size}</div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Uploaded</div>
                    <div className="text-gray-900">{dataset.dateUploaded}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Dataset Details */}
        <div className="space-y-6">
          {selected ? (
            <>
              <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                <h3 className="text-gray-900 mb-4">Dataset Details</h3>
                
                <div className="space-y-3">
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Dataset ID</div>
                    <div className="text-sm text-gray-900 font-mono bg-gray-50 px-3 py-2 rounded">{selected.id}</div>
                  </div>
                  
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Raw File</div>
                    <div className="text-sm text-gray-900 break-all">{selected.rawFile}</div>
                  </div>
                  
                  {selected.preparedFile && (
                    <div>
                      <div className="text-xs text-gray-500 mb-1">Prepared File</div>
                      <div className="text-sm text-gray-900 break-all">{selected.preparedFile}</div>
                    </div>
                  )}
                  
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <div className="text-xs text-gray-500 mb-1">Rows</div>
                      <div className="text-sm text-gray-900">{selected.rows.toLocaleString()}</div>
                    </div>
                    <div>
                      <div className="text-xs text-gray-500 mb-1">Columns</div>
                      <div className="text-sm text-gray-900">{selected.columns}</div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                <h4 className="text-sm text-gray-900 mb-3">Storage Links</h4>
                <div className="space-y-2">
                  <a href="#" className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors group">
                    <div className="flex items-center gap-2">
                      <Database className="w-4 h-4 text-gray-400" />
                      <span className="text-sm text-gray-700">PostgreSQL Table</span>
                    </div>
                    <ExternalLink className="w-4 h-4 text-gray-400 group-hover:text-[#2563EB]" />
                  </a>
                  
                  <a href="#" className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors group">
                    <div className="flex items-center gap-2">
                      <FileText className="w-4 h-4 text-gray-400" />
                      <span className="text-sm text-gray-700">MinIO File</span>
                    </div>
                    <ExternalLink className="w-4 h-4 text-gray-400 group-hover:text-[#2563EB]" />
                  </a>
                </div>
              </div>

              <div className="space-y-2">
                <button className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-[#2563EB] text-white rounded-lg hover:bg-[#1d4ed8] transition-colors text-sm">
                  <Download className="w-4 h-4" />
                  Download
                </button>
                <button className="w-full px-4 py-2.5 bg-white text-gray-700 rounded-lg hover:bg-gray-50 transition-colors border border-gray-200 text-sm">
                  View Metadata
                </button>
              </div>
            </>
          ) : (
            <div className="bg-gray-50 rounded-xl p-8 text-center border border-gray-200">
              <Database className="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-500 text-sm">Select a dataset to view details</p>
            </div>
          )}
        </div>
      </div>

      {/* Sample Preview */}
      {selected && (
        <div className="mt-6 bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <h3 className="text-gray-900 mb-4">Sample Preview - {selected.name}</h3>
          <div className="overflow-x-auto border border-gray-200 rounded-lg">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs text-gray-600">ID</th>
                  <th className="px-4 py-3 text-left text-xs text-gray-600">Age</th>
                  <th className="px-4 py-3 text-left text-xs text-gray-600">Income</th>
                  <th className="px-4 py-3 text-left text-xs text-gray-600">Score</th>
                  <th className="px-4 py-3 text-left text-xs text-gray-600">Region</th>
                  <th className="px-4 py-3 text-left text-xs text-gray-600">Churn</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {sampleData.map((row) => (
                  <tr key={row.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3 text-sm text-gray-900">{row.id}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">{row.age}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">{row.income.toLocaleString()}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">{row.score}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">{row.region}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">{row.churn}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="text-xs text-gray-500 mt-3">Showing 5 of {selected.rows.toLocaleString()} rows</p>
        </div>
      )}
    </div>
  );
}
