import React, { useState } from "react";

function PipelineLogs({ pipeline }) {
  // State to track which steps are open
  const [openSteps, setOpenSteps] = useState(
    pipeline.steps ? pipeline.steps.map(() => true) : []
  );

  const toggleStep = (idx) => {
    const newState = [...openSteps];
    newState[idx] = !newState[idx];
    setOpenSteps(newState);
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="font-semibold mb-4 text-lg">Logs</h3>
      <div className="space-y-3">
        {pipeline.steps && pipeline.steps.length > 0 ? (
          pipeline.steps.map((step, idx) => (
            <div key={idx} className="border border-gray-200 rounded">
              {/* Step header */}
              <div
                onClick={() => toggleStep(idx)}
                className="bg-gray-100 px-4 py-2 flex justify-between items-center cursor-pointer"
              >
                <span className="font-semibold">{step.name}</span>
                <span
                  className={`px-2 py-0.5 rounded-full text-white text-xs ${
                    step.status === "Success"
                      ? "bg-green-500"
                      : step.status === "Failed"
                      ? "bg-red-500"
                      : step.status === "Running"
                      ? "bg-blue-500"
                      : "bg-yellow-400"
                  }`}
                >
                  {step.status}
                </span>
              </div>

              {/* Step logs */}
              {openSteps[idx] && (
                <div className="bg-gray-50 p-4 max-h-48 overflow-y-auto text-xs">
                  {step.logs && step.logs.length > 0 ? (
                    step.logs.map((log, i) => (
                      <div key={i} className="mb-1">
                        <span className="text-gray-800 font-mono">{log}</span>
                      </div>
                    ))
                  ) : (
                    <p className="text-gray-500">No logs available</p>
                  )}
                </div>
              )}
            </div>
          ))
        ) : (
          <p className="text-gray-500">No logs available</p>
        )}
      </div>
    </div>
  );
}

export default PipelineLogs;
