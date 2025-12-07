import React from "react";
import { useParams } from "react-router-dom";
import Sidebar from "../../components/sidebar/Sidebar";
import Topbar from "../../components/topbar/Topbar";
import Footer from "../../components/footer/Footer";
import { pipelinesDataa, getStatusColor } from "../../components/Variables";


export default function PipelineDetailsPage() {
  const { id } = useParams();
  const pipeline = pipelinesDataa.find((p) => p.id.toString() === id);

  if (!pipeline)
    return (
      <div className="flex items-center justify-center h-screen">
        <p className="text-gray-500 text-lg">Pipeline not found</p>
      </div>
    );

  return (
    <div className="flex min-h-screen bg-gray-50 text-gray-900">
      <Sidebar />

      <div className="flex-1 flex flex-col">
        <Topbar title={`Pipeline #${pipeline.id}`} />

        <main className="flex-1 p-8 space-y-6">
          {/* Pipeline Info Card */}
          <div className="bg-white rounded-lg shadow p-6 space-y-4">
            <div className="flex flex-col md:flex-row md:items-center space-x-6">
              <h2 className="text-2xl font-semibold">{pipeline.name}</h2>
              <span
                className={`px-3 py-1 rounded-full text-white text-sm ${getStatusColor(
                  pipeline.status
                )}`}
              >
                {pipeline.status}
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <p>
                <span className="font-semibold">Dataset:</span> {pipeline.dataset}
              </p>
              <p>
                <span className="font-semibold">Created By:</span> {pipeline.createdBy}
              </p>
              <p>
                <span className="font-semibold">Start Time:</span> {pipeline.startTime}
              </p>
              <p>
                <span className="font-semibold">Steps Completed:</span> {pipeline.stepsCompleted}
              </p>
              <p>
                <span className="font-semibold">Duration:</span> {pipeline.duration}
              </p>
            </div>
          </div>

          {/* Steps Timeline */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="font-semibold mb-3">Steps Timeline</h3>
            <div className="flex gap-4 overflow-x-auto">
              {pipeline.steps && pipeline.steps.length > 0 ? (
                pipeline.steps.map((step, idx) => (
                  <div key={idx} className="flex flex-col items-center">
                    <div
                      className={`px-4 py-2 rounded-md font-medium flex items-center justify-center text-sm text-white ${getStatusColor(
                        step.status
                      )}`}
                    >
                      {step.name}
                    </div>
                    <span className="text-xs mt-1">{step.status}</span>
                    {step.duration && <span className="text-xs mt-0.5 text-gray-600">{step.duration}</span>}
                  </div>
                ))
              ) : (
                <p className="text-gray-500">No steps available</p>
              )}
            </div>
          </div>

          {/* Metrics Section */}
          {pipeline.metrics && (
            <div className="bg-white rounded-lg shadow p-6 grid grid-cols-1 md:grid-cols-3 gap-4">
              <h3 className="col-span-full font-semibold mb-2">Metrics</h3>
              <p>
                <span className="font-semibold">Accuracy:</span> {pipeline.metrics.accuracy ?? "N/A"}
              </p>
              <p>
                <span className="font-semibold">F1 Score:</span> {pipeline.metrics.f1 ?? "N/A"}
              </p>
              <p>
                <span className="font-semibold">AUC:</span> {pipeline.metrics.auc ?? "N/A"}
              </p>
            </div>
          )}

          {/* Logs Section */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="font-semibold mb-2">Logs</h3>
            <div className="bg-gray-100 p-4 rounded h-64 overflow-y-auto text-xs">
              {pipeline.steps && pipeline.steps.length > 0 ? (
                pipeline.steps.map((step, idx) => (
                  <div key={idx} className="mb-2">
                    <p className="font-semibold text-sm">{step.name}:</p>
                    <p className="text-gray-700 text-xs">{step.logs || "No logs available"}</p>
                  </div>
                ))
              ) : (
                <p className="text-gray-500">No logs available</p>
              )}
            </div>
          </div>
        </main>

        <Footer />
      </div>
    </div>
  );
}
