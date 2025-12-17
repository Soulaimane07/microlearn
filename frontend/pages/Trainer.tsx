import React, { useState } from 'react';
import { Zap, Play, ChevronDown } from 'lucide-react';
import { StatusBadge } from '../components/StatusBadge';

export function Trainer() {
  const [isTraining, setIsTraining] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleTrain = () => {
    setIsTraining(true);
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsTraining(false);
          return 100;
        }
        return prev + 10;
      });
    }, 500);
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
        {/* Configuration */}
        <div className="col-span-2 space-y-6">
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Training Configuration</h3>
            
            <div className="space-y-4">
              {/* Model Selection */}
              <div>
                <label className="block text-sm text-gray-700 mb-2">Select Model</label>
                <div className="relative">
                  <select className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 appearance-none cursor-pointer hover:border-[#2563EB] transition-colors">
                    <option>mdl_504 - RandomForest (Winner)</option>
                    <option>mdl_503 - XGBoost</option>
                    <option>mdl_502 - Logistic Regression</option>
                  </select>
                  <ChevronDown className="w-4 h-4 text-gray-400 absolute right-3 top-3.5 pointer-events-none" />
                </div>
              </div>

              {/* Training Strategy */}
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
              <div>
                <label className="block text-sm text-gray-700 mb-2">n_estimators</label>
                <input 
                  type="number" 
                  defaultValue={100}
                  className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 hover:border-[#2563EB] transition-colors"
                />
              </div>
              
              <div>
                <label className="block text-sm text-gray-700 mb-2">max_depth</label>
                <input 
                  type="number" 
                  defaultValue={10}
                  className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 hover:border-[#2563EB] transition-colors"
                />
              </div>
              
              <div>
                <label className="block text-sm text-gray-700 mb-2">learning_rate</label>
                <input 
                  type="number" 
                  step="0.01"
                  defaultValue={0.1}
                  className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 hover:border-[#2563EB] transition-colors"
                />
              </div>
              
              <div>
                <label className="block text-sm text-gray-700 mb-2">min_samples_split</label>
                <input 
                  type="number" 
                  defaultValue={2}
                  className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 hover:border-[#2563EB] transition-colors"
                />
              </div>
              
              <div>
                <label className="block text-sm text-gray-700 mb-2">min_samples_leaf</label>
                <input 
                  type="number" 
                  defaultValue={1}
                  className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 hover:border-[#2563EB] transition-colors"
                />
              </div>
              
              <div>
                <label className="block text-sm text-gray-700 mb-2">random_state</label>
                <input 
                  type="number" 
                  defaultValue={42}
                  className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-900 hover:border-[#2563EB] transition-colors"
                />
              </div>
            </div>
          </div>

          {/* Training Progress */}
          {isTraining && (
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-gray-900">Training Progress</h3>
                <StatusBadge status="in-progress" label="Training" />
              </div>
              
              <div className="mb-4">
                <div className="flex justify-between text-sm text-gray-600 mb-2">
                  <span>Epoch {Math.floor(progress / 10)} / 10</span>
                  <span>{progress}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div 
                    className="bg-[#2563EB] h-3 rounded-full transition-all duration-500"
                    style={{ width: `${progress}%` }}
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div className="bg-gray-50 rounded-lg p-3">
                  <div className="text-xs text-gray-500 mb-1">Current Loss</div>
                  <div className="text-sm text-gray-900">0.{100 - progress}34</div>
                </div>
                <div className="bg-gray-50 rounded-lg p-3">
                  <div className="text-xs text-gray-500 mb-1">Validation Acc</div>
                  <div className="text-sm text-gray-900">{92 + (progress / 25)}%</div>
                </div>
                <div className="bg-gray-50 rounded-lg p-3">
                  <div className="text-xs text-gray-500 mb-1">Time Remaining</div>
                  <div className="text-sm text-gray-900">{Math.floor((100 - progress) / 10)}m {((100 - progress) % 10) * 6}s</div>
                </div>
              </div>
            </div>
          )}

          {/* Training Logs */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-gray-900 mb-4">Training Logs</h3>
            <div className="bg-gray-900 rounded-lg p-4 font-mono text-xs text-green-400 h-64 overflow-y-auto">
              <div>[INFO] Initializing RandomForest model...</div>
              <div>[INFO] Loading training data from ds_004</div>
              <div>[INFO] Training set: 8,000 samples</div>
              <div>[INFO] Validation set: 2,000 samples</div>
              <div>[INFO] Starting training with 100 estimators...</div>
              {isTraining && (
                <>
                  <div>[INFO] Epoch 1/10 - Loss: 0.234, Val Acc: 0.89</div>
                  <div>[INFO] Epoch 2/10 - Loss: 0.189, Val Acc: 0.91</div>
                  <div>[INFO] Epoch 3/10 - Loss: 0.156, Val Acc: 0.92</div>
                  {progress > 40 && <div>[INFO] Epoch 4/10 - Loss: 0.132, Val Acc: 0.93</div>}
                  {progress > 60 && <div>[INFO] Epoch 5/10 - Loss: 0.118, Val Acc: 0.94</div>}
                  {progress > 80 && <div>[SUCCESS] Training complete!</div>}
                </>
              )}
            </div>
          </div>
        </div>

        {/* Right Sidebar */}
        <div className="space-y-6">
          {/* Train Button */}
          <button 
            onClick={handleTrain}
            disabled={isTraining}
            className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-[#2563EB] text-white rounded-lg hover:bg-[#1d4ed8] transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Play className="w-4 h-4" />
            {isTraining ? 'Training...' : 'Start Training'}
          </button>

          {/* Export Summary */}
          {progress === 100 && (
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <h3 className="text-gray-900 mb-4">Training Complete</h3>
              
              <div className="space-y-3">
                <div>
                  <div className="text-xs text-gray-500 mb-1">Model ID</div>
                  <div className="text-sm text-gray-900 font-mono bg-gray-50 px-3 py-2 rounded">mdl_505</div>
                </div>
                
                <div>
                  <div className="text-xs text-gray-500 mb-1">Final Accuracy</div>
                  <div className="text-green-600">94.7%</div>
                </div>
                
                <div>
                  <div className="text-xs text-gray-500 mb-1">Training Time</div>
                  <div className="text-sm text-gray-900">5m 23s</div>
                </div>
                
                <div>
                  <div className="text-xs text-gray-500 mb-1">Model Size</div>
                  <div className="text-sm text-gray-900">24.3 MB</div>
                </div>
                
                <div>
                  <div className="text-xs text-gray-500 mb-1">Saved to</div>
                  <a href="#" className="text-xs text-[#2563EB] hover:underline break-all">
                    minio://models/mdl_505.pkl
                  </a>
                </div>
                
                <button className="w-full mt-4 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm">
                  Export Model
                </button>
              </div>
            </div>
          )}

          {/* Info */}
          <div className="bg-purple-50 rounded-xl p-6 border border-purple-200">
            <h4 className="text-sm text-gray-900 mb-2">Training Tips</h4>
            <ul className="space-y-2 text-xs text-gray-600">
              <li>• Use Auto mode for optimal hyperparameters</li>
              <li>• Monitor validation accuracy to avoid overfitting</li>
              <li>• Larger n_estimators = better accuracy</li>
              <li>• Set random_state for reproducibility</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
