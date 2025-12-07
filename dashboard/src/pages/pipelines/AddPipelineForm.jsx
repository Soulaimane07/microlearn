import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { addPipeline } from "../../redux/slices/pipelinesSlice";

export default function AddPipelineForm({ onClose }) {
  const dispatch = useDispatch();
  const [name, setName] = useState("");
  const [dataset, setDataset] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name || !dataset) return alert("Please fill all fields");

    const newPipeline = {
      id: Date.now(), 
      name,
      status: "Queued",
      dataset,
      stepsCompleted: "0/3",
      createdBy: "You",
      startTime: new Date().toISOString().slice(0, 16).replace("T", " "),
      duration: "00:00",
      metrics: { accuracy: null, f1: null, auc: null },
      steps: [
        { name: "DataPreparer", status: "Queued", duration: null, logs: [] },
        { name: "ModelSelector", status: "Queued", duration: null, logs: [] },
        { name: "HyperOpt", status: "Queued", duration: null, logs: [] },
        { name: "Trainer", status: "Queued", duration: null, logs: [] },
        { name: "Evaluator", status: "Queued", duration: null, logs: [] },
        { name: "Deployer", status: "Queued", duration: null, logs: [] },
      ],
    };

    dispatch(addPipeline(newPipeline));
    onClose();
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700">Pipeline Name</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-1 focus:ring-yellow-500"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">Dataset</label>
        <input
          type="text"
          value={dataset}
          onChange={(e) => setDataset(e.target.value)}
          className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-1 focus:ring-yellow-500"
        />
      </div>
      <div className="flex justify-end gap-2">
        <button
          type="button"
          onClick={onClose}
          className="px-4 py-2 rounded border border-gray-300 hover:bg-gray-100"
        >
          Cancel
        </button>
        <button
          type="submit"
          className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700"
        >
          Add Pipeline
        </button>
      </div>
    </form>
  );
}
