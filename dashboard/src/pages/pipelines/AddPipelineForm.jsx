import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { addPipeline } from "../../redux/slices/pipelinesSlice";

export default function AddPipelineForm({ onClose }) {
  const dispatch = useDispatch();
  const [name, setName] = useState("");
  const [datasetId, setDatasetId] = useState("");

  const user = useSelector((state) => state.auth.user);
  const datasets = useSelector((state) => state.datasets.list);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name || !datasetId) return alert("Please fill all fields");

    const selectedDataset = datasets.find(d => d.id.toString() === datasetId);
    if (!selectedDataset) return alert("Invalid dataset selected");

    const newPipeline = {
      id: Date.now(),
      name,
      status: "Queued",
      datasetId: selectedDataset.id,
      dataset: selectedDataset.name,
      stepsCompleted: "0/6",
      createdBy: user?.name,
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
        <label className="block mb-1 text-sm font-medium text-gray-700">Pipeline Name</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-1 focus:ring-yellow-500"
        />
      </div>
      <div>
        <label className="block mb-1 text-sm font-medium text-gray-700">Dataset</label>
        <select
          value={datasetId}
          onChange={(e) => setDatasetId(e.target.value)}
          className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-1 focus:ring-yellow-500"
        >
          <option value="">Select a dataset</option>
          {datasets.map(d => (
            <option key={d.id} value={d.id}>
              {d.name} ({d.type}, {d.size})
            </option>
          ))}
        </select>
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
          className="px-4 py-2 rounded bg-yellow-600 text-white hover:bg-yellow-700"
        >
          Add Pipeline
        </button>
      </div>
    </form>
  );
}
