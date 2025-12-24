import React, { useEffect, useState } from "react";
import axios from "axios";
import { Zap, Play, ChevronDown } from "lucide-react";
import { useDispatch, useSelector } from "react-redux";
import { StatusBadge } from "../components/StatusBadge";
import { storetrainer } from "../store/slices/pipelineSlice";

export default function Trainer() {
  const dispatch = useDispatch();
  const { datapreparer, modelselection } = useSelector((state) => state.pipeline);

  const [isTraining, setIsTraining] = useState(false);
  const [progress, setProgress] = useState(0);
  const [jobId, setJobId] = useState(null);
  const [trainingData, setTrainingData] = useState(null);
  const [selectedModelId, setSelectedModelId] = useState(
    modelselection?.candidates?.[0]?.model_id || ""
  );
  const [hyperparams, setHyperparams] = useState({});

  // Load default hyperparameters when model changes
  useEffect(() => {
    if (!modelselection) return;

    const model = modelselection.candidates.find((m) => m.model_id === selectedModelId);
    if (model) setHyperparams(model.default_params || {});
  }, [selectedModelId, modelselection]);

  // Handle hyperparameter changes
  const handleHyperparamChange = (e) => {
    const { name, value } = e.target;
    setHyperparams((prev) => ({ ...prev, [name]: Number(value) }));
  };

  // Start training
  const handleTrain = async () => {
    if (!datapreparer || !modelselection) {
      alert("Pipeline data missing");
      return;
    }

    setIsTraining(true);
    setProgress(0);

    const payload = {
      model_id: selectedModelId,
      data_id: datapreparer.minio_object,
      task_type: modelselection.dataset_analysis.task_type,
      epochs: 100,
      batch_size: 32,
      learning_rate: hyperparams.learning_rate || 0.001,
      hyperparameters: hyperparams,
      target_column: datapreparer.target_column,
      use_gpu: true,
      num_workers: 4,
      experiment_name: `pipeline_${Date.now()}`,
      run_name: selectedModelId,
      tags: { pipeline_id: datapreparer.pipeline_id },
      early_stopping: true,
      patience: 10,
    };

    try {
      const response = await axios.post("http://localhost:8002/train", payload);
      dispatch(storetrainer(response.data));
      setJobId(response.data.job_id);

      // Poll training status
      const interval = setInterval(async () => {
        try {
          const res = await axios.get(`http://localhost:8002/train/${response.data.job_id}`);
          setTrainingData(res.data);
          setProgress(res.data.progress_percentage || 0);
          dispatch(storetrainer(res.data));

          if (res.data.status === "completed") {
            clearInterval(interval);
            setIsTraining(false);
            alert("Training completed successfully!");
          }

          if (res.data.status === "failed") {
            clearInterval(interval);
            setIsTraining(false);
            alert(`Training failed: ${res.data.error_message || "Unknown error"}`);
          }
        } catch (err) {
          console.error(err);
          clearInterval(interval);
          setIsTraining(false);
        }
      }, 2000);
    } catch (err) {
      console.error("Training error:", err);
      setIsTraining(false);
      alert(`Failed to start training: ${err.message}`);
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
          <h1 className="text-gray-900">Trainer Microservice</h1>
        </div>
        <p className="text-gray-500">Train selected model using prepared pipeline data</p>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {/* Left */}
        <div className="col-span-2 space-y-6">
          {/* Configuration */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Training Configuration</h3>
            <label className="block text-sm text-gray-700 mb-2">Select Model</label>
            <div className="relative">
              <select
                className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg appearance-none"
                value={selectedModelId}
                onChange={(e) => setSelectedModelId(e.target.value)}
              >
                {modelselection?.candidates?.map((model) => (
                  <option key={model.model_id} value={model.model_id}>
                    {model.model_name} ({model.category})
                  </option>
                ))}
              </select>
              <ChevronDown className="w-4 h-4 absolute right-3 top-3.5 text-gray-400" />
            </div>
          </div>

          {/* Hyperparameters */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Hyperparameters</h3>
            <div className="grid grid-cols-2 gap-4">
              {Object.entries(hyperparams).map(([key, value]) => (
                <div key={key}>
                  <label className="block text-sm text-gray-700 mb-1">{key}</label>
                  <input
                    type="number"
                    name={key}
                    value={value}
                    step="any"
                    onChange={handleHyperparamChange}
                    className="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg"
                  />
                </div>
              ))}
            </div>
          </div>

          {/* Progress */}
          {trainingData && (
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <div className="flex justify-between mb-4">
                <h3 className="text-gray-900">Training Progress</h3>
                <StatusBadge
                  status={
                    trainingData.status === "completed"
                      ? "completed"
                      : trainingData.status === "failed"
                      ? "failed"
                      : "in-progress"
                  }
                  label={trainingData.status}
                />
              </div>

              <div>
                <div className="flex justify-between text-sm text-gray-600 mb-2">
                  <span>
                    Epoch {trainingData.current_epoch || 0} / {trainingData.total_epochs || 0}
                  </span>
                  <span>{progress.toFixed(1)}%</span>
                </div>
                <div className="w-full bg-gray-200 h-3 rounded-full">
                  <div
                    className={`h-3 rounded-full transition-all ${
                      trainingData.status === "failed"
                        ? "bg-red-500"
                        : "bg-[#2563EB]"
                    }`}
                    style={{ width: `${progress}%` }}
                  />
                </div>
              </div>

              {trainingData.status === "failed" && trainingData.error_message && (
                <p className="text-red-600 mt-2">{trainingData.error_message}</p>
              )}
            </div>
          )}
        </div>

        {/* Right */}
        <div>
          <button
            onClick={handleTrain}
            disabled={isTraining}
            className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-[#2563EB] text-white rounded-lg hover:bg-[#1d4ed8] disabled:opacity-50"
          >
            <Play className="w-4 h-4" />
            {isTraining ? "Training..." : "Start Training"}
          </button>
        </div>
      </div>
    </div>
  );
}
