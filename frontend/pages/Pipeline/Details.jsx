import React, { useEffect } from "react";
import { useParams } from "react-router-dom";
import { motion } from "framer-motion";
import { useDispatch, useSelector } from "react-redux";
import { fetchPipeline } from "../../store/slices/pipelineSlice";
import DataPreparer from "../DataPreparer";
import ModelSelector from "../ModelSelector";
import Trainer from "../Trainer";
import Evaluator from "../Evaluator";
import HyperOpt from "../HyperOpt";
import Deployer from "../Deployer";

function Details() {
  const { pipelineId } = useParams();
  const dispatch = useDispatch();
  const { pipeline, status, error } = useSelector((state) => state.pipeline);

  useEffect(() => {
    dispatch(fetchPipeline(pipelineId));

    const interval = setInterval(() => {
      dispatch(fetchPipeline(pipelineId));
    }, 10000); // Poll every 10s

    return () => clearInterval(interval);
  }, [dispatch, pipelineId]);

  if (!pipeline) return null;

  const renderStepComponent = (step) => {
    switch (step.name) {
      case "DataPreparer": return <DataPreparer pipeline_id={pipelineId} />;
      case "ModelSelector": return <ModelSelector />;
      case "Trainer": return <Trainer />;
      case "Evaluator": return <Evaluator />;
      case "HyperOpt": return <HyperOpt />;
      case "Deployer": return <Deployer />;
      default: return null;
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-6 bg-white shadow-xl rounded-xl mt-10">
      <div className="mb-10 text-center">
        <h2 className="text-3xl font-bold mb-2">{pipeline.name}</h2>
        <p className="text-lg mb-6">
          Status:{" "}
          <span className={`font-semibold ${
            pipeline.status === "RUNNING" ? "text-blue-500" :
            pipeline.status === "SUCCESS" ? "text-green-500" :
            "text-gray-500"
          }`}>
            {pipeline.status}
          </span>
        </p>

        {/* Pipeline timeline */}
        <div className="flex justify-between items-center relative mb-12">
          {pipeline.steps.map((step, index) => (
            <div key={step.name} className="flex-1 relative text-center">
              {index < pipeline.steps.length && (
                <div
                  className={`absolute top-3 mt-1.5 left-1/2 w-full h-1 z-0 transform -translate-x-1/2 ${
                    step.status === "SUCCESS" ? "bg-green-500" : step.status === "RUNNING" ? "bg-blue-500" : "bg-gray-300"
                  }`}
                ></div>
              )}
              <motion.div
                animate={{
                  scale: step.status === "RUNNING" ? [1, 1.3, 1] : 1,
                }}
                transition={{
                  duration: 1.2,
                  repeat: step.status === "RUNNING" ? Infinity : 0,
                }}
                className={`relative z-10 mx-auto w-10 h-10 rounded-full flex items-center justify-center
                  ${step.status === "SUCCESS" ? "bg-green-500 text-white" :
                    step.status === "RUNNING" ? "bg-blue-500 text-white" :
                    "bg-gray-300 text-gray-700"}
                `}
              >
                {index + 1}
              </motion.div>
              <p className="mt-2 text-sm font-medium">{step.name}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Step components */}
      <div className="space-y-8">
        {pipeline.steps.map(
          (step) =>
            (step.status === "RUNNING") && (
              <motion.div
                key={step.name}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="p-4 bg-gray-50 rounded-lg shadow"
              >
                {renderStepComponent(step)}
              </motion.div>
            )
        )}
      </div>
    </div>
  );
}

export default Details;
