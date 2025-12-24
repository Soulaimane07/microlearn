import React, { useState } from 'react';
import axios from 'axios';
import { Zap, Play, ChevronDown } from 'lucide-react';
import { StatusBadge } from '../components/StatusBadge';

export default function Trainer() {
  const [isTraining, setIsTraining] = useState(false);
  const [progress, setProgress] = useState(0);
  const [jobId, setJobId] = useState(null);
  const [trainingData, setTrainingData] = useState(null);

  // Hyperparameters state
  const [hyperparams, setHyperparams] = useState({
    n_estimators: 100,
    max_depth: 10,
    learning_rate: 0.001,
    min_samples_split: 2,
    min_samples_leaf: 1,
    random_state: 42
  });

  const handleHyperparamChange = (e) => {
    const { name, value } = e.target;
    setHyperparams((prev) => ({ ...prev, [name]: value }));
  };

  const handleTrain = async () => {
    setIsTraining(true);
    setProgress(0);

    try {
      // Start training with full required request body
      const response = await axios.post('http://localhost:8002/train', {
        model_id: 'mdl_504',
        data_id: 'ds_004',
        task_type: 'classification',
        epochs: 100,
        batch_size: 32,
        learning_rate: parseFloat(hyperparams.learning_rate),
        hyperparameters: hyperparams,
        target_column: 'target',      // replace with actual target
        use_gpu: true,
        num_workers: 4,
        experiment_name: 'my_experiment',
        run_name: 'run_001',
        tags: {},
        early_stopping: true,
        patience: 10
      });

      const { job_id } = response.data;
      setJobId(job_id);

      // Poll progress every 2 seconds
      const interval = setInterval(async () => {
        try {
          const progressRes = await axios.get(`http://localhost:8002/train/${job_id}`);
          const data = progressRes.data;
          setTrainingData(data);
          setProgress(data.progress_percentage || 0);

          if (data.status === 'completed') {
            clearInterval(interval);
            setIsTraining(false);
          }
          if (data.status === 'failed') {
            clearInterval(interval);
            setIsTraining(false);
            alert('Training failed!');
          }
        } catch (err) {
          console.error('Error fetching progress:', err);
        }
      }, 2000);
    } catch (err) {
      console.error('Training submission failed:', err);
      setIsTraining(false);
      alert('Failed to start training. Check console.');
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
        <p className="text-gray-500">Train your selected model with custom hyperparameters</p>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {/* Configuration & Hyperparameters */}
        <div className="col-span-2 space-y-6">
          {/* Configuration */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Training Configuration</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-700 mb-2">Select Model</label>
                <div className="relative">
                  <select className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 appearance-none cursor-pointer hover:border-[#2563EB] transition-colors">
                    <option value="mdl_504">mdl_504 - RandomForest (Winner)</option>
                    <option value="mdl_503">mdl_503 - XGBoost</option>
                    <option value="mdl_502">mdl_502 - Logistic Regression</option>
                  </select>
                  <ChevronDown className="w-4 h-4 text-gray-400 absolute right-3 top-3.5 pointer-events-none" />
                </div>
              </div>

              <div>
                <label className="block text-sm text-gray-700 mb-2">Training Strategy</label>
                <div className="grid grid-cols-2 gap-3">
                  <label className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 border border-gray-200">
                    <input type="radio" name="strategy" defaultChecked className="text-[#2563EB]" />
                    <span className="text-sm text-gray-700">Auto</span>
                  </label>
                  <label className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 border border-gray-200">
                    <input type="radio" name="strategy" className="text-[#2563EB]" />
                    <span className="text-sm text-gray-700">Manual</span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          {/* Hyperparameters */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Hyperparameters</h3>
            <div className="grid grid-cols-2 gap-4">
              {Object.entries(hyperparams).map(([key, value]) => (
                <div key={key}>
                  <label className="block text-sm text-gray-700 mb-2">{key}</label>
                  <input
                    type="number"
                    step={key === 'learning_rate' ? 0.001 : 1}
                    name={key}
                    value={value}
                    onChange={handleHyperparamChange}
                    className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 hover:border-[#2563EB] transition-colors"
                  />
                </div>
              ))}
            </div>
          </div>

          {/* Training Progress */}
          {isTraining && trainingData && (
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-gray-900">Training Progress</h3>
                <StatusBadge status="in-progress" label="Training" />
              </div>

              <div className="mb-4">
                <div className="flex justify-between text-sm text-gray-600 mb-2">
                  <span>Epoch {trainingData.current_epoch || 0} / {trainingData.total_epochs || 100}</span>
                  <span>{progress.toFixed(1)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div className="bg-[#2563EB] h-3 rounded-full transition-all duration-500" style={{ width: `${progress}%` }} />
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          <button
            onClick={handleTrain}
            disabled={isTraining}
            className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-[#2563EB] text-white rounded-lg hover:bg-[#1d4ed8] transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Play className="w-4 h-4" />
            {isTraining ? 'Training...' : 'Start Training'}
          </button>
        </div>
      </div>
    </div>
  );
}
