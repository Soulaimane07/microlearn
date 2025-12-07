import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { useSelector } from "react-redux";
import Sidebar from "../../components/sidebar/Sidebar";
import Topbar from "../../components/topbar/Topbar";
import Footer from "../../components/footer/Footer";
import { getStatusColor } from "../../components/Variables";
import Papa from "papaparse"; // CSV parsing library

export default function DatasetDetailsPage() {
  const { id } = useParams();
  const datasets = useSelector((state) => state.datasets.list);
  const pipelines = useSelector((state) => state.pipelines.list);

  const dataset = datasets.find((d) => d.id.toString() === id);

  const [previewData, setPreviewData] = useState([]);
  const [previewError, setPreviewError] = useState("");

  if (!dataset)
    return (
      <div className="flex items-center justify-center h-screen">
        <p className="text-gray-500 text-lg">Dataset not found</p>
      </div>
    );

  // Get pipelines using this dataset
  const relatedPipelines = pipelines.filter((p) => p.datasetId === dataset.id);

  // Preview parsing
  useEffect(() => {
    setPreviewError("");
    if (!dataset.fileContent) return;

    try {
      if (dataset.type.toLowerCase() === "csv") {
        const parsed = Papa.parse(dataset.fileContent, { header: true });
        setPreviewData(parsed.data.slice(0, 5)); // show first 5 rows
      } else if (dataset.type.toLowerCase() === "json") {
        const jsonData = JSON.parse(dataset.fileContent);
        setPreviewData(jsonData.slice(0, 5)); // show first 5 items
      } else {
        setPreviewError("Preview not available for this file type.");
      }
    } catch (err) {
      setPreviewError("Error parsing file content.");
    }
  }, [dataset]);

  return (
    <div className="flex min-h-screen bg-gray-50 text-gray-900">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Topbar title={`Dataset: ${dataset.name}`} />
        <main className="flex-1 p-8 space-y-6">
          {/* Dataset Info */}
          <div className="bg-white rounded-lg shadow p-6 space-y-4">
            <h2 className="text-2xl font-semibold">{dataset.name}</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm mt-2">
              <p>
                <span className="font-semibold">Type:</span> {dataset.type}
              </p>
              <p>
                <span className="font-semibold">Size:</span> {dataset.size}
              </p>
              <p>
                <span className="font-semibold">Created By:</span> {dataset.createdBy}
              </p>
              <p>
                <span className="font-semibold">Created At:</span> {dataset.createdAt}
              </p>
              <p>
                <span className="font-semibold">Number of Pipelines:</span> {relatedPipelines.length}
              </p>
            </div>
          </div>

          {/* File Preview */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-4">Dataset Preview</h3>
            {previewError && <p className="text-red-500">{previewError}</p>}
            {!previewError && previewData.length > 0 && (
              <div className="overflow-x-auto">
                <table className="min-w-full table-auto border-collapse">
                  <thead>
                    <tr className="bg-gray-100 text-gray-700">
                      {Object.keys(previewData[0]).map((key) => (
                        <th key={key} className="px-4 py-2 text-left">
                          {key}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {previewData.map((row, index) => (
                      <tr key={index} className="border-b border-gray-200 hover:bg-gray-50 transition-all">
                        {Object.values(row).map((val, i) => (
                          <td key={i} className="px-4 py-2">
                            {val}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
            {!previewError && previewData.length === 0 && <p className="text-gray-500">No preview available.</p>}
          </div>

          {/* Related Pipelines */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-4">Pipelines using this dataset</h3>
            {relatedPipelines.length > 0 ? (
              <table className="min-w-full table-auto border-collapse">
                <thead>
                  <tr className="bg-gray-100 text-gray-700">
                    <th className="px-4 py-2 text-left">ID</th>
                    <th className="px-4 py-2 text-left">Name</th>
                    <th className="px-4 py-2 text-left">Status</th>
                    <th className="px-4 py-2 text-left">Steps Completed</th>
                    <th className="px-4 py-2 text-left">Start Time</th>
                    <th className="px-4 py-2 text-left">Duration</th>
                  </tr>
                </thead>
                <tbody>
                  {relatedPipelines.map((p) => (
                    <tr key={p.id} className="border-b border-gray-200 hover:bg-gray-50 transition-all">
                      <td className="px-4 py-2">
                        <Link to={`/pipelines/${p.id}`} className="hover:underline text-blue-600">
                          #{p.id}
                        </Link>
                      </td>
                      <td className="px-4 py-2">{p.name}</td>
                      <td className={`px-6 items-center justify-center mt-1 py-2 text-center w-fit h-fit flex rounded-full text-white text-xs ${getStatusColor(p.status)}`}>
                        {p.status}
                      </td>
                      <td className="px-4 py-2">{p.stepsCompleted}</td>
                      <td className="px-4 py-2">{p.startTime}</td>
                      <td className="px-4 py-2">{p.duration}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="text-gray-500">No pipelines use this dataset yet.</p>
            )}
          </div>
        </main>
        <Footer />
      </div>
    </div>
  );
}
