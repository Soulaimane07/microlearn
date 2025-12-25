import React, { useEffect, useState } from "react";
import axios from "axios";
import { Zap, Play } from "lucide-react";
import { useDispatch, useSelector } from "react-redux";
import { StatusBadge } from "../components/StatusBadge";
import { storetrainer } from "../store/slices/pipelineSlice";


const mapTrainerStatus = (status?: string) => {
  switch (status) {
    case "completed":
      return "success";
    case "failed":
      return "failed";
    case "running":
      return "in-progress";
    case "pending":
    default:
      return "pending";
  }
};

export default function Trainer() {
  const dispatch = useDispatch();
  const { datapreparer, modelselection, pipeline } = useSelector(
    (state) => state.pipeline
  );

  const [isTraining, setIsTraining] = useState(false);
  const [trainingData, setTrainingData] = useState(null);

  const [selectedModelId, setSelectedModelId] = useState(
    modelselection?.candidates?.[0]?.model_id || ""
  );

  const [selectedTarget, setSelectedTarget] = useState(
    datapreparer?.target_column || ""
  );

  const [hyperparams, setHyperparams] = useState({});

  /* Load default hyperparameters */
  useEffect(() => {
    if (!modelselection) return;
    const model = modelselection.candidates.find(
      (m) => m.model_id === selectedModelId
    );
    if (model) setHyperparams(model.default_params || {});
  }, [selectedModelId, modelselection]);

  /* Hyperparameter update */
  const handleHyperparamChange = (e) => {
    const { name, value } = e.target;
    setHyperparams((prev) => ({
      ...prev,
      [name]: Number(value),
    }));
  };

  /* Start training */
  const handleTrain = async () => {
    if (!datapreparer || !modelselection || !selectedTarget) {
      alert("Missing pipeline data or target column");
      return;
    }

    setIsTraining(true);
    setTrainingData(null);

    const payload = {
      pipeline_id: pipeline?.id,
      model_id: selectedModelId,
      data_id: datapreparer.minio_object,
      task_type: modelselection.dataset_analysis.task_type,
      target_column: selectedTarget,
      hyperparameters: hyperparams,
    };

    try {
      const res = await axios.post("http://localhost:8008/train", payload);
      dispatch(storetrainer(res.data));

      const interval = setInterval(async () => {
        try {
          const statusRes = await axios.get(
            `http://localhost:8008/train/${res.data.job_id}`
          );

          setTrainingData(statusRes.data);
          dispatch(storetrainer(statusRes.data));

          if (
            statusRes.data.status === "completed" ||
            statusRes.data.status === "failed"
          ) {
            clearInterval(interval);
            setIsTraining(false);
          }
        } catch (err) {
          console.error(err);
          clearInterval(interval);
          setIsTraining(false);
        }
      }, 2000);
    } catch (err) {
      console.error(err);
      setIsTraining(false);
      alert("Failed to start training");
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 bg-[#2563EB] rounded-lg flex items-center justify-center">
            <Zap className="w-5 h-5 text-white" />
          </div>
          <h1 className="text-gray-900">Trainer Service</h1>
        </div>
        <p className="text-gray-500">
          Train a selected ML model using prepared data
        </p>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {/* Left */}
        <div className="col-span-2 space-y-6">
          {/* Model selection */}
          <div className="bg-white rounded-xl p-6 shadow-sm border">
            <h3 className="mb-4">Model Selection</h3>
            <select
              className="w-full px-4 py-2 bg-gray-50 border rounded-lg"
              value={selectedModelId}
              onChange={(e) => setSelectedModelId(e.target.value)}
            >
              {modelselection?.candidates?.map((m) => (
                <option key={m.model_id} value={m.model_id}>
                  {m.model_name} ({m.category})
                </option>
              ))}
            </select>
          </div>

          {/* Target column */}
          <div className="bg-white rounded-xl p-6 shadow-sm border">
            <h3 className="mb-4">Target Column</h3>
            <select
              className="w-full px-4 py-2 bg-gray-50 border rounded-lg"
              value={selectedTarget}
              onChange={(e) => setSelectedTarget(e.target.value)}
            >
              <option value="">-- Select target column --</option>
              {modelselection?.dataset_analysis?.columns?.map((col) => (
                <option key={col} value={col}>
                  {col}
                </option>
              ))}
            </select>
          </div>

          {/* Hyperparameters */}
          <div className="bg-white rounded-xl p-6 shadow-sm border">
            <h3 className="mb-4">Hyperparameters</h3>
            <div className="grid grid-cols-2 gap-4">
              {Object.entries(hyperparams).map(([k, v]) => (
                <div key={k}>
                  <label className="text-sm">{k}</label>
                  <input
                    type="number"
                    name={k}
                    value={v}
                    onChange={handleHyperparamChange}
                    className="w-full px-3 py-2 border rounded-lg"
                  />
                </div>
              ))}
            </div>
          </div>

          {/* Status */}
          {trainingData && (
            <div className="bg-white rounded-xl p-6 shadow-sm border">
              <div className="flex justify-between mb-3">
                <h3>Training Status</h3>
                <StatusBadge
                  status={mapTrainerStatus(trainingData.status)}
                  label={trainingData.status}
                />
              </div>

              {trainingData.training_metrics && (
                <pre className="bg-gray-50 p-3 rounded text-sm">
                  {JSON.stringify(trainingData.training_metrics, null, 2)}
                </pre>
              )}

              {trainingData.artifacts?.model_path && (
                <p className="text-sm mt-2 text-green-600">
                  Model stored at: {trainingData.artifacts.model_path}
                </p>
              )}

              {trainingData.error && (
                <p className="text-red-600 mt-2">{trainingData.error}</p>
              )}
            </div>
          )}
        </div>

        {/* Right */}
        <div>
          <button
            onClick={handleTrain}
            disabled={isTraining || !selectedTarget}
            className="w-full flex justify-center gap-2 px-6 py-3 bg-[#2563EB] text-white rounded-lg disabled:opacity-50"
          >
            <Play className="w-4 h-4" />
            {isTraining ? "Training..." : "Start Training"}
          </button>
        </div>
      </div>
    </div>
  );
}
