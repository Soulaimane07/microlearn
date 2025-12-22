import React, { useState } from "react";
import axios from "axios";
import { Upload, Play, Database, ChevronDown } from "lucide-react";

export default function DataPreparer() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const [rawData, setRawData] = useState([]);
  const [cleanedData, setCleanedData] = useState([]);
  const [logs, setLogs] = useState([]);
  const [file, setFile] = useState(null);
  const [metadata, setMetadata] = useState(null);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleRun = async () => {
    if (!file) return alert("Please select a CSV file first!");

    setIsProcessing(true);
    setShowPreview(false);
    setLogs(["[INFO] Starting data preprocessing..."]);
    setMetadata(null);
    setRawData([]);
    setCleanedData([]);

    try {
      // --- Step 1: Detect ---
      const detectForm = new FormData();
      detectForm.append("file", file);
      detectForm.append("store_to_minio", true);

      setLogs((prev) => [...prev, "[INFO] Uploading and detecting dataset..."]);
      const detectRes = await axios.post("http://localhost:8000/detect", detectForm, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setMetadata(detectRes.data);
      setLogs((prev) => [
        ...prev,
        `[INFO] Detection complete.`,
        `[INFO] CSV stored in MinIO: ${detectRes.data.minio_object}`,
        `[INFO] Pipeline YAML generated: ${detectRes.data.pipeline_yml}`
      ]);

      // Optional: Set rawData if backend returns first rows
      if (detectRes.data.raw_preview) setRawData(detectRes.data.raw_preview);

      // --- Step 2: Prepare ---
      const prepareForm = new FormData();
      prepareForm.append("minio_object", detectRes.data.minio_object);
      prepareForm.append("pipeline_yml", detectRes.data.pipeline_yml);
      prepareForm.append("target_column", ""); // optional

      setLogs((prev) => [...prev, "[INFO] Preparing dataset..."]);
      const prepareRes = await axios.post("http://localhost:8000/prepare", prepareForm, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setCleanedData(prepareRes.data.cleaned_data || []);
      setLogs((prev) => [...prev, "[SUCCESS] Data preprocessing complete!"]);
      setShowPreview(true);
    } catch (err) {
      console.error(err);
      setLogs((prev) => [...prev, `[ERROR] ${err.message}`]);
    } finally {
      setIsProcessing(false);
    }
  };

  const downloadCSV = (data, filename = "cleaned_data.csv") => {
    if (!data || data.length === 0) return;
    const csvContent = [
      Object.keys(data[0]).join(","),
      ...data.map((row) => Object.values(row).join(",")),
    ].join("\n");
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
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
        {/* Left Column: Upload & Metadata */}
        <div className="col-span-2 space-y-6">
          {/* Upload Section */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 relative">
            <h3 className="text-gray-900 mb-4">Upload Dataset</h3>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-[#2563EB] cursor-pointer bg-gray-50 relative">
              <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <input
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />
              <p className="text-gray-900 mb-1">Drop CSV file here or click to browse</p>
              <p className="text-sm text-gray-500">Supports CSV files up to 100MB</p>
            </div>
            {file && <p className="mt-2 text-sm text-gray-600">Selected file: {file.name}</p>}
          </div>

          {/* Metadata */}
          {metadata && (
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 space-y-4">
              <h3 className="text-gray-900 mb-2">Detected Metadata</h3>
              <div className="text-sm text-gray-700 space-y-1">
                <p><strong>ID Columns:</strong> {metadata.id_columns.join(", ")}</p>
                <p><strong>Date Columns:</strong> {metadata.date_columns.join(", ")}</p>
                <p><strong>Numeric Columns:</strong> {metadata.numeric_columns.join(", ")}</p>
                <p><strong>Categorical Columns:</strong> {metadata.categorical_columns.join(", ")}</p>
                <p><strong>MinIO Path:</strong> {metadata.minio_object}</p>
                <p><strong>Pipeline YAML:</strong> {metadata.pipeline_yml}</p>
              </div>
            </div>
          )}

          {/* Raw Data Preview */}
          {rawData.length > 0 && (
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 space-y-4">
              <h3 className="text-gray-900 mb-2">Raw Data Preview (first 10 rows)</h3>
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
                    {rawData.slice(0, 10).map((row, i) => (
                      <tr key={i} className="hover:bg-gray-50">
                        {Object.values(row).map((val, j) => (
                          <td key={j} className="px-4 py-2 text-sm text-gray-900">{val}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Cleaned Data Preview */}
          {showPreview && cleanedData.length > 0 && (
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 space-y-4">
              <h3 className="text-gray-900 mb-4">Cleaned Data Preview</h3>
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
              <button
                onClick={() => downloadCSV(cleanedData)}
                className="mt-4 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
              >
                Download Cleaned CSV
              </button>
            </div>
          )}
        </div>

        {/* Right Column: Actions & Logs */}
        <div className="space-y-6">
          <button
            onClick={handleRun}
            disabled={isProcessing}
            className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-[#2563EB] text-white rounded-lg hover:bg-[#1d4ed8] transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Play className="w-4 h-4" />
            {isProcessing ? "Processing..." : "Run Data Preprocessing"}
          </button>

          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Processing Logs</h3>
            <div className="bg-gray-900 rounded-lg p-4 font-mono text-xs h-64 overflow-y-auto">
              {logs.map((log, i) => {
                let color = "text-green-400";
                if (log.startsWith("[ERROR]")) color = "text-red-500";
                else if (log.startsWith("[INFO]")) color = "text-blue-400";
                return <div key={i} className={color}>{log}</div>;
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
