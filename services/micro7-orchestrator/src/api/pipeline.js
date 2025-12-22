const { startPipeline, onStepCompleted } = require("../core/orchestrator");
const { getPipeline } = require("../storage/redisStore");

async function routes(app) {

  // Start a new pipeline
  app.post("/pipeline/execute", async (req, reply) => {
    const { name, steps } = req.body;

    if (!name || !Array.isArray(steps)) {
      return reply.code(400).send({ error: "Invalid pipeline" });
    }

    const id = await startPipeline(name, steps);
    return { pipelineId: id };
  });

  // Check pipeline status
  app.get("/pipeline/status/:id", async (req) => {
    return await getPipeline(req.params.id);
  });

  // Endpoint for microservices to update a step
  app.post("/pipeline/step/update", async (req, reply) => {
    const { pipelineId, stepName, status } = req.body;

    if (!pipelineId || !stepName || !status) {
      return reply.code(400).send({ error: "Missing required fields" });
    }

    try {
      await onStepCompleted({ pipelineId, step: stepName, status });
      return { message: "Step updated successfully" };
    } catch (err) {
      console.error(err);
      return reply.code(500).send({ error: "Failed to update step" });
    }
  });
}

module.exports = routes;
