const { v4: uuid } = require("uuid");
const { savePipeline, getPipeline } = require("../storage/redisStore");
const { publishStep } = require("../messaging/publisher");

async function startPipeline(name, steps) {
  const pipeline = {
    id: uuid(),
    name,
    status: "RUNNING",
    currentStep: 0,
    steps: steps.map(s => ({ name: s, status: "PENDING" })),
    createdAt: new Date().toISOString(),
    updatedAt: null
  };

  await savePipeline(pipeline);
  await executeCurrentStep(pipeline);

  return pipeline.id;
}

async function executeCurrentStep(pipeline) {
  const step = pipeline.steps[pipeline.currentStep];
  step.status = "RUNNING";
  await savePipeline(pipeline);

  await publishStep(step.name, {
    pipelineId: pipeline.id,
    step: step.name
  });
}

async function onStepCompleted(event) {
  const pipeline = await getPipeline(event.pipelineId);
  if (!pipeline) return;

  const step = pipeline.steps[pipeline.currentStep];

  if (event.status === "FAILED") {
    step.status = "FAILED";
    pipeline.status = "FAILED";
  } else {
    step.status = "SUCCESS";
    pipeline.currentStep++;

    if (pipeline.currentStep >= pipeline.steps.length) {
      pipeline.status = "COMPLETED";
    } else {
      await executeCurrentStep(pipeline);
    }
  }

  await savePipeline(pipeline);
}

module.exports = { startPipeline, onStepCompleted };
