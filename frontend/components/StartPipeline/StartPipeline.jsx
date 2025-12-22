import React, { useState } from "react";
import { OrchestratorUrl } from "../variables";
import { useNavigate } from "react-router-dom";

function StartPipeline({ setOpenRunPipelineModal }) {

    const navigate = useNavigate();

  const initialSteps = [
    "DataPreparer",
    "ModelSelector",
    "Trainer",
    "Evaluator",
    "HyperOpt",
    "Deployer",
  ];

  const [pipelineName, setPipelineName] = useState("");
  const [status, setStatus] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!pipelineName) {
      setStatus("Please enter a pipeline name.");
      return;
    }

    try {
      const response = await fetch(`${OrchestratorUrl}/pipeline/execute`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: pipelineName,
          steps: initialSteps, // always all steps
        }),
      });

        if (response.ok) {
            const data = await response.json(); // read the response body
            setStatus(`✅ Pipeline started successfully!`);
            navigate(`/pipeline/${data.pipelineId}`);
        } else {
            const data = await response.json();
            setStatus(`❌ Error: ${data.message || "Failed to start pipeline."}`);
        }

    } catch (error) {
      setStatus(`❌ Error: ${error.message}`);
    }
  };

  return (
    <div className="fixed top-0 z-50 left-0 w-full h-full flex items-center justify-center bg-gray-900/50 backdrop-blur-xs">
      <div className="p-6 w-full max-w-xl bg-white shadow-lg rounded">
        <h2 className="text-xl font-bold mb-4 text-center">Start a New Pipeline</h2>
        
        
        {status && (
          <p className="mt-4 mb-2 text-sm text-center">
            {status}
          </p>
        )}
        
        <form onSubmit={handleSubmit}>
          <div className="mb-6">
            <label className="block mb-1 font-medium">Pipeline Name:</label>
            <input
              type="text"
              value={pipelineName}
              onChange={(e) => setPipelineName(e.target.value)}
              className="w-full border px-2 py-1 rounded focus:outline-none focus:ring focus:border-blue-300"
              placeholder="Enter pipeline name"
            />
          </div>

          <div className="mb-6">
            <label className="block mb-2 font-medium">Pipeline Steps:</label>
            <div className="flex justify-between items-center">
              {initialSteps.map((step, index) => (
                <div key={step} className="flex-1 relative">
                  {/* Connector line */}
                  {index < initialSteps.length - 1 && (
                    <div className="absolute top-3 left-1/2 w-full h-0.5 bg-gray-300 z-0"></div>
                  )}

                  {/* Step node */}
                  <div
                    className="relative z-10 mx-auto w-6 h-6 rounded-full flex items-center justify-center bg-blue-500 text-white"
                  >
                    {index + 1}
                  </div>
                  <p className="text-center mt-2 text-sm">{step}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="flex space-x-4 mt-10">
            <button
              type="submit"
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
            >
              Start Pipeline
            </button>
            <button
              type="button"
              onClick={() => setOpenRunPipelineModal(false)}
              className="bg-gray-300 text-gray-700 px-4 py-2 rounded hover:bg-gray-400 transition"
            >
              Cancel
            </button>
          </div>
        </form>

      </div>
    </div>
  );
}

export default StartPipeline;
