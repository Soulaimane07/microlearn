import React, { useState } from 'react';
import { Upload, Play, FileText, Database, ChevronDown, CheckCircle2 } from 'lucide-react';
import { StatusBadge } from '../components/StatusBadge';

export function DataPreparer() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [showPreview, setShowPreview] = useState(false);

  const handleRun = () => {
    setIsProcessing(true);
    setTimeout(() => {
      setIsProcessing(false);
      setShowPreview(true);
    }, 3000);
  };

  const rawData = [
    { id: 1, age: '25', income: '50000', score: '', region: 'North' },
    { id: 2, age: '', income: '75000', score: '0.85', region: 'South' },
    { id: 3, age: '34', income: '60000', score: '0.72', region: '' },
    { id: 4, age: '45', income: '', score: '0.91', region: 'East' },
  ];

  const cleanedData = [
    { id: 1, age: 25, income: 50000, score: 0.79, region: 'North', region_encoded: [1,0,0,0] },
    { id: 2, age: 33, income: 75000, score: 0.85, region: 'South', region_encoded: [0,1,0,0] },
    { id: 3, age: 34, income: 60000, score: 0.72, region: 'East', region_encoded: [0,0,1,0] },
    { id: 4, age: 45, income: 61500, score: 0.91, region: 'East', region_encoded: [0,0,1,0] },
  ];

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 bg-[#2563EB] rounded-lg flex items-center justify-center">
            <Database className="w-5 h-5 text-white" />
          </div>
          <h1 className="text-gray-900">DataPreparer Microservice</h1>
        </div>
        <p className="text-gray-500">Upload, clean, and transform your datasets for machine learning</p>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {/* Left Column - Upload & Config */}
        <div className="col-span-2 space-y-6">
          {/* Upload Section */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Upload Dataset</h3>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-[#2563EB] transition-colors cursor-pointer bg-gray-50">
              <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-900 mb-1">Drop CSV file here or click to browse</p>
              <p className="text-sm text-gray-500">Supports CSV files up to 100MB</p>
            </div>
          </div>

          {/* Configuration Panel */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Configuration</h3>
            
            <div className="space-y-4">
              {/* Pipeline Config */}
              <div>
                <label className="block text-sm text-gray-700 mb-2">Pipeline Configuration</label>
                <div className="relative">
                  <select className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 appearance-none cursor-pointer hover:border-[#2563EB] transition-colors">
                    <option>pipeline_default.yaml</option>
                    <option>pipeline_advanced.yaml</option>
                    <option>pipeline_minimal.yaml</option>
                  </select>
                  <ChevronDown className="w-4 h-4 text-gray-400 absolute right-3 top-3.5 pointer-events-none" />
                </div>
              </div>

              {/* Imputation */}
              <div>
                <label className="block text-sm text-gray-700 mb-2">Missing Value Imputation</label>
                <div className="grid grid-cols-2 gap-3">
                  <label className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 border border-gray-200">
                    <input type="radio" name="imputation" defaultChecked className="text-[#2563EB]" />
                    <span className="text-sm text-gray-700">Mean</span>
                  </label>
                  <label className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 border border-gray-200">
                    <input type="radio" name="imputation" className="text-[#2563EB]" />
                    <span className="text-sm text-gray-700">Median</span>
                  </label>
                  <label className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 border border-gray-200">
                    <input type="radio" name="imputation" className="text-[#2563EB]" />
                    <span className="text-sm text-gray-700">Mode</span>
                  </label>
                  <label className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 border border-gray-200">
                    <input type="radio" name="imputation" className="text-[#2563EB]" />
                    <span className="text-sm text-gray-700">Drop</span>
                  </label>
                </div>
              </div>

              {/* Scaling */}
              <div>
                <label className="block text-sm text-gray-700 mb-2">Feature Scaling</label>
                <div className="grid grid-cols-3 gap-3">
                  <label className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 border border-gray-200">
                    <input type="radio" name="scaling" defaultChecked className="text-[#2563EB]" />
                    <span className="text-sm text-gray-700">StandardScaler</span>
                  </label>
                  <label className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 border border-gray-200">
                    <input type="radio" name="scaling" className="text-[#2563EB]" />
                    <span className="text-sm text-gray-700">MinMaxScaler</span>
                  </label>
                  <label className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 border border-gray-200">
                    <input type="radio" name="scaling" className="text-[#2563EB]" />
                    <span className="text-sm text-gray-700">None</span>
                  </label>
                </div>
              </div>

              {/* Encoding */}
              <div>
                <label className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 border border-gray-200">
                  <input type="checkbox" defaultChecked className="text-[#2563EB] rounded" />
                  <span className="text-sm text-gray-700">Apply OneHot Encoding to categorical features</span>
                </label>
              </div>
            </div>
          </div>

          {/* Preview Tables */}
          {showPreview && (
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <h3 className="text-gray-900 mb-4">Data Preview</h3>
              
              <div className="mb-6">
                <div className="text-sm text-gray-700 mb-2">Raw Data</div>
                <div className="overflow-x-auto border border-gray-200 rounded-lg">
                  <table className="w-full">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-4 py-2 text-left text-xs text-gray-600">ID</th>
                        <th className="px-4 py-2 text-left text-xs text-gray-600">Age</th>
                        <th className="px-4 py-2 text-left text-xs text-gray-600">Income</th>
                        <th className="px-4 py-2 text-left text-xs text-gray-600">Score</th>
                        <th className="px-4 py-2 text-left text-xs text-gray-600">Region</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {rawData.map((row) => (
                        <tr key={row.id} className="hover:bg-gray-50">
                          <td className="px-4 py-2 text-sm text-gray-900">{row.id}</td>
                          <td className="px-4 py-2 text-sm text-gray-500">{row.age || <span className="text-red-500">NULL</span>}</td>
                          <td className="px-4 py-2 text-sm text-gray-500">{row.income || <span className="text-red-500">NULL</span>}</td>
                          <td className="px-4 py-2 text-sm text-gray-500">{row.score || <span className="text-red-500">NULL</span>}</td>
                          <td className="px-4 py-2 text-sm text-gray-500">{row.region || <span className="text-red-500">NULL</span>}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              <div>
                <div className="text-sm text-gray-700 mb-2">Cleaned Data</div>
                <div className="overflow-x-auto border border-gray-200 rounded-lg">
                  <table className="w-full">
                    <thead className="bg-green-50">
                      <tr>
                        <th className="px-4 py-2 text-left text-xs text-gray-600">ID</th>
                        <th className="px-4 py-2 text-left text-xs text-gray-600">Age</th>
                        <th className="px-4 py-2 text-left text-xs text-gray-600">Income</th>
                        <th className="px-4 py-2 text-left text-xs text-gray-600">Score</th>
                        <th className="px-4 py-2 text-left text-xs text-gray-600">Region</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {cleanedData.map((row) => (
                        <tr key={row.id} className="hover:bg-gray-50">
                          <td className="px-4 py-2 text-sm text-gray-900">{row.id}</td>
                          <td className="px-4 py-2 text-sm text-green-600">{row.age}</td>
                          <td className="px-4 py-2 text-sm text-green-600">{row.income}</td>
                          <td className="px-4 py-2 text-sm text-green-600">{row.score}</td>
                          <td className="px-4 py-2 text-sm text-green-600">{row.region}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Right Column - Output & Actions */}
        <div className="space-y-6">
          {/* Run Button */}
          <button 
            onClick={handleRun}
            disabled={isProcessing}
            className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-[#2563EB] text-white rounded-lg hover:bg-[#1d4ed8] transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Play className="w-4 h-4" />
            {isProcessing ? 'Processing...' : 'Run Data Preprocessing'}
          </button>

          {/* Progress */}
          {isProcessing && (
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <div className="flex items-center gap-2 mb-3">
                <StatusBadge status="in-progress" label="Processing" />
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
                <div className="bg-[#2563EB] h-2 rounded-full animate-pulse" style={{ width: '65%' }}></div>
              </div>
              <div className="text-sm text-gray-500">Step 2 of 3: Applying transformations...</div>
            </div>
          )}

          {/* Output Summary */}
          {showPreview && (
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <div className="flex items-center gap-2 mb-4">
                <CheckCircle2 className="w-5 h-5 text-green-600" />
                <h3 className="text-gray-900">Output Summary</h3>
              </div>
              
              <div className="space-y-4">
                <div>
                  <div className="text-xs text-gray-500 mb-1">Dataset ID</div>
                  <div className="text-sm text-gray-900 font-mono bg-gray-50 px-3 py-2 rounded">ds_004</div>
                </div>
                
                <div>
                  <div className="text-xs text-gray-500 mb-1">Table Name</div>
                  <div className="text-sm text-gray-900 font-mono bg-gray-50 px-3 py-2 rounded">customer_data_cleaned</div>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Rows</div>
                    <div className="text-sm text-gray-900">10,000</div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Columns</div>
                    <div className="text-sm text-gray-900">27</div>
                  </div>
                </div>
                
                <div>
                  <div className="text-xs text-gray-500 mb-1">MinIO File</div>
                  <a href="#" className="text-sm text-[#2563EB] hover:underline break-all">
                    minio://datasets/ds_004.parquet
                  </a>
                </div>
              </div>
            </div>
          )}

          {/* Logs Panel */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Processing Logs</h3>
            <div className="bg-gray-900 rounded-lg p-4 font-mono text-xs text-green-400 h-64 overflow-y-auto">
              <div>[INFO] Starting data preprocessing pipeline...</div>
              <div>[INFO] Loading dataset: customer_data.csv</div>
              <div>[INFO] Detected 10,000 rows, 23 columns</div>
              <div>[INFO] Found 147 missing values across 4 columns</div>
              <div>[INFO] Applying mean imputation...</div>
              <div>[INFO] Encoding categorical features...</div>
              <div>[INFO] Applying StandardScaler to numeric features...</div>
              <div>[SUCCESS] Data preprocessing complete!</div>
              <div>[INFO] Saved to PostgreSQL table: customer_data_cleaned</div>
              <div>[INFO] Uploaded to MinIO: datasets/ds_004.parquet</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
