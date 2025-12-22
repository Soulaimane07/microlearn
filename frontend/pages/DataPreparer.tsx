import React, { useState } from "react";
import axios from "axios";
import { Upload, Play, Database, ChevronDown, CheckCircle2 } from "lucide-react";
import { StatusBadge } from "../components/StatusBadge";

export default function DataPreparer() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const [rawData, setRawData] = useState([]);
  const [cleanedData, setCleanedData] = useState([]);
  const [logs, setLogs] = useState([]);
  const [file, setFile] = useState(null);
  const [pipelineConfig, setPipelineConfig] = useState("pipeline_default.yaml");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleRun = async () => {
    if (!file) return alert("Please select a CSV file first!");

    setIsProcessing(true);
    setShowPreview(false);
    setLogs(["[INFO] Starting data preprocessing..."]);

    try {
      // Step 1: Detect metadata
      const formData = new FormData();
      formData.append("file", file);
      formData.append("store_to_minio", true);

      setLogs((prev) => [...prev, "[INFO] Uploading and detecting dataset..."]);
      const detectRes = await axios.post("http://localhost:8000/detect", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setRawData(detectRes.data.raw_data || []); // Use actual backend data if returned
      setLogs((prev) => [...prev, "[INFO] Detection complete"]);

      // Step 2: Prepare dataset
      const prepareData = new FormData();
      prepareData.append("file", file);
      prepareData.append("pipeline_yml", `pipelines/${pipelineConfig}`);
      prepareData.append("target_column", ""); // Optional

      setLogs((prev) => [...prev, "[INFO] Preparing dataset..."]);
      const prepareRes = await axios.post("http://localhost:8000/prepare", prepareData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setCleanedData(prepareRes.data.cleaned_data || []); // Backend cleaned data
      setLogs((prev) => [...prev, "[SUCCESS] Data preprocessing complete!"]);
      setShowPreview(true);
    } catch (err) {
      console.error(err);
      setLogs((prev) => [...prev, `[ERROR] ${err.message}`]);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">
      {/* Header */}
      <div className="flex items-center gap-3 mb-2">
        <div className="w-10 h-10 bg-[#2563EB] rounded-lg flex items-center justify-center">
          <Database className="w-5 h-5 text-white" />
        </div>
        <h1 className="text-gray-900 text-xl font-bold">DataPreparer Microservice</h1>
      </div>
      <p className="text-gray-500 mb-6">Upload, clean, and transform your datasets for ML</p>

      <div className="grid grid-cols-3 gap-6">
        {/* Left Column: Upload & Configuration */}
        <div className="col-span-2 space-y-6">
          {/* Upload Section */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Upload Dataset</h3>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-[#2563EB] cursor-pointer bg-gray-50">
              <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <input type="file" accept=".csv" onChange={handleFileChange} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
              <p className="text-gray-900 mb-1">Drop CSV file here or click to browse</p>
              <p className="text-sm text-gray-500">Supports CSV files up to 100MB</p>
            </div>
          </div>

          {/* Configuration Panel */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Configuration</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-700 mb-2">Pipeline Configuration</label>
                <div className="relative">
                  <select
                    className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 appearance-none cursor-pointer hover:border-[#2563EB]"
                    value={pipelineConfig}
                    onChange={(e) => setPipelineConfig(e.target.value)}
                  >
                    <option>pipeline_default.yaml</option>
                    <option>pipeline_advanced.yaml</option>
                    <option>pipeline_minimal.yaml</option>
                  </select>
                  <ChevronDown className="w-4 h-4 text-gray-400 absolute right-3 top-3.5 pointer-events-none" />
                </div>
              </div>
            </div>
          </div>

          {/* Preview Tables */}
          {showPreview && (
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 space-y-6">
              <h3 className="text-gray-900 mb-4">Data Preview</h3>

              {/* Raw Data */}
              {rawData.length > 0 && (
                <div>
                  <div className="text-sm text-gray-700 mb-2">Raw Data</div>
                  <div className="overflow-x-auto border border-gray-200 rounded-lg">
                    <table className="w-full">
                      <thead className="bg-gray-50">
                        <tr>
                          {Object.keys(rawData[0]).map((col) => (
                            <th key={col} className="px-4 py-2 text-left text-xs text-gray-600">{col}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-200">
                        {rawData.map((row, i) => (
                          <tr key={i} className="hover:bg-gray-50">
                            {Object.values(row).map((val, j) => (
                              <td key={j} className={`px-4 py-2 text-sm ${val ? "text-gray-900" : "text-red-500"}`}>
                                {val || "NULL"}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* Cleaned Data */}
              {cleanedData.length > 0 && (
                <div>
                  <div className="text-sm text-gray-700 mb-2">Cleaned Data</div>
                  <div className="overflow-x-auto border border-gray-200 rounded-lg">
                    <table className="w-full">
                      <thead className="bg-green-50">
                        <tr>
                          {Object.keys(cleanedData[0]).map((col) => (
                            <th key={col} className="px-4 py-2 text-left text-xs text-gray-600">{col}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-200">
                        {cleanedData.map((row, i) => (
                          <tr key={i} className="hover:bg-gray-50">
                            {Object.values(row).map((val, j) => (
                              <td key={j} className="px-4 py-2 text-sm text-green-600">{val}</td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Right Column: Actions & Logs */}
        <div className="space-y-6">
          {/* Run Button */}
          <button
            onClick={handleRun}
            disabled={isProcessing}
            className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-[#2563EB] text-white rounded-lg hover:bg-[#1d4ed8] transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Play className="w-4 h-4" />
            {isProcessing ? "Processing..." : "Run Data Preprocessing"}
          </button>

          {/* Logs Panel */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Processing Logs</h3>
            <div className="bg-gray-900 rounded-lg p-4 font-mono text-xs text-green-400 h-64 overflow-y-auto">
              {logs.map((log, i) => (
                <div key={i}>{log}</div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
