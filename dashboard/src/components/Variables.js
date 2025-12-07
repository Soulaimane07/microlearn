// datasetsAndPipelines.js

export const datasets = [
  {
    id: 1,
    name: "Customer Data",
    type: "CSV",
    createdBy: "Admin",
    createdAt: "2025-12-07",
    size: "120MB",
    pipelines: [452], // IDs of pipelines using this dataset
  },
  {
    id: 2,
    name: "Sales Data",
    type: "CSV",
    createdBy: "Alice",
    createdAt: "2025-12-06",
    size: "500MB",
    pipelines: [453],
  },
  {
    id: 3,
    name: "Loan Data",
    type: "CSV",
    createdBy: "Mariam",
    createdAt: "2025-12-07",
    size: "80MB",
    pipelines: [454],
  },
];

export const pipelinesDataa = [
  {
    id: 452,
    name: "Fraud Detection Pipeline",
    status: "Success",
    datasetId: 1,
    stepsCompleted: "6/6",
    createdBy: "Soulaimane",
    startTime: "2025-12-07 09:12",
    endTime: "2025-12-07 09:14",
    duration: "02:45",
    metrics: { accuracy: 0.95, f1: 0.942, auc: 0.97 },
    steps: [
      { name: "DataPreparer", status: "Success", duration: "00:20", logs: ["Data prepared successfully."] },
      { name: "ModelSelector", status: "Success", duration: "00:10", logs: ["XGBoost selected."] },
      { name: "HyperOpt", status: "Success", duration: "00:30", logs: ["Hyperparameters optimized."] },
      { name: "Trainer", status: "Success", duration: "01:10", logs: ["Model trained successfully."] },
      { name: "Evaluator", status: "Success", duration: "00:20", logs: ["Metrics computed."] },
      { name: "Deployer", status: "Success", duration: "00:15", logs: ["Model deployed to production."] },
    ],
  },
  {
    id: 453,
    name: "Credit Default Pipeline",
    status: "Running",
    datasetId: 2,
    stepsCompleted: "3/6",
    createdBy: "Ali",
    startTime: "2025-12-07 10:05",
    endTime: null,
    duration: "01:30",
    metrics: { accuracy: null, f1: null, auc: null },
    steps: [
      { name: "DataPreparer", status: "Success", duration: "00:25", logs: ["Data prepared."] },
      { name: "ModelSelector", status: "Success", duration: "00:15", logs: ["RandomForest selected."] },
      { name: "HyperOpt", status: "Running", duration: "00:50", logs: ["HyperOpt in progress..."] },
      { name: "Trainer", status: "Queued", duration: null, logs: [] },
      { name: "Evaluator", status: "Queued", duration: null, logs: [] },
      { name: "Deployer", status: "Queued", duration: null, logs: [] },
    ],
  },
  {
    id: 454,
    name: "Loan Prediction Pipeline",
    status: "Queued",
    datasetId: 3,
    stepsCompleted: "0/5",
    createdBy: "Mariam",
    startTime: "2025-12-07 11:00",
    endTime: null,
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
  },
];

// Utility function to get dataset by pipeline ID
export const getDatasetByPipeline = (pipelineId) => {
  const pipeline = pipelinesDataa.find(p => p.id === pipelineId);
  if (!pipeline) return null;
  return datasets.find(d => d.id === pipeline.datasetId);
};



export const getStatusColor = (status) => {
    switch (status) {
      case "Success":
        return "bg-green-500";
      case "Failed":
        return "bg-red-500";
      case "Running":
        return "bg-blue-500";
      case "Queued":
        return "bg-yellow-400";
      default:
        return "bg-gray-400";
    }
};

export const steps = [
    { name: "DataPreparer", status: "Success" },
    { name: "ModelSelector", status: "Success" },
    { name: "HyperOpt", status: "Success" },
    { name: "Trainer", status: "Success" },
    { name: "Evaluator", status: "Success" },
    { name: "Deployer", status: "Success" },
];


